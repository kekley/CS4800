import argparse
import os
import ollama
import requests
import sys
import pysher
import json
import queue

from dotenv import load_dotenv
load_dotenv()

AUTH0_TOKEN_URL = os.getenv("AUTH0_TOKEN_URL")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://ollama:11434")

PUSHER_APP_KEY = os.getenv("PUSHER_APP_KEY")

API_URL = os.getenv("API_URL")

token_response = requests.post(AUTH0_TOKEN_URL,
    json={
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "audience": "api.smalltalk.kekley.live",
        "grant_type": "client_credentials"
    },
    headers={
        "Content-Type": "application/json"
    }
)

token_response = token_response.json()
access_token = token_response["access_token"]

def get(endpoint):
	res = requests.get(API_URL + endpoint, headers={
		"Authorization": f"Bearer {access_token}"
	})
	return res

def post(endpoint, body=None):
	res = requests.post(API_URL + endpoint, headers={
		"Content-Type": "application/json",
		"Authorization": f"Bearer {access_token}"	
	}, json=body)
	return res

def put(endpoint, body=None):
	res = requests.put(API_URL + endpoint, headers={
		"Content-Type": "application/json",
		"Authorization": f"Bearer {access_token}"
	}, json=body)
	return res

parser = argparse.ArgumentParser()
parser.add_argument("--agentId", required=True)
parser.add_argument("--model", default="llama3.2", required=True)
args = parser.parse_args()

client = ollama.Client(host=OLLAMA_HOST)

channelIds = []
message_queue = queue.Queue()

def pusher_message_callback(data):
	deserialized = json.loads(data)
	message_queue.put(deserialized)

def pusher_add_server(data):
	deserialized = json.loads(data)
	if deserialized["agentId"] == args.agentId:
		for channelId in deserialized["channels"]:
			channel = pusher.subscribe(f"chat-channel-{channelId}")
			channel.bind("new-message", pusher_message_callback)

register_response = post(f"agents/register/{args.agentId}")
if register_response.status_code != 204:
	print("ERROR: Failed to register agent.")
	sys.exit(1)

channels_response = get(f"agents/{args.agentId}/channels")
if channels_response.status_code != 200:
	print("ERROR: Failed to fetch agent channels.")
	sys.exit(1)

channels_response = channels_response.json()
channelIds = channels_response["channels"]

pusher = pysher.Pusher(PUSHER_APP_KEY, cluster="us3")

def pusher_connection_handler(data):
	for channelId in channelIds:
		channel = pusher.subscribe(f"chat-channel-{channelId}")
		channel.bind("new-message", pusher_message_callback)

	status_channel = pusher.subscribe("agent-control")
	status_channel.bind("membership-added", pusher_add_server)
	print("Registered Pusher channel connections.")

pusher.connection.bind("pusher:connection_established", pusher_connection_handler)
pusher.connect()

while True:
	message = message_queue.get()
	
	print(f"Received message ID {message['id']}")

	if message["author"]["type"] == "AGENT":
		continue

	channelId = message['channel_id'] 

	post(f"agents/{args.agentId}/startreply/{channelId}")
	
	agent_response = client.chat(
		model=args.model,
		messages=[{"role": "user", "content": message["content"]}]
	)

	res = post(f"/channels/{channelId}/messages", {
		"agentId": args.agentId,
		"content": agent_response["message"]["content"]
	})

	if res.status_code != 201:
		print("ERROR: Failed to respond to message", message, res)
		continue

	print(f"Agent ID {args.agentId} responded to message {message['id']}.")

