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

token_response = requests.post(
    AUTH0_TOKEN_URL,
    json={
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "audience": "api.smalltalk.kekley.live",
        "grant_type": "client_credentials",
    },
    headers={"Content-Type": "application/json"},
)

token_response = token_response.json()
access_token = token_response["access_token"]


def get(endpoint):
    res = requests.get(
        API_URL + endpoint, headers={"Authorization": f"Bearer {access_token}"}
    )
    return res


def post(endpoint, body=None):
    res = requests.post(
        API_URL + endpoint,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        },
        json=body,
    )
    return res


def put(endpoint, body=None):
    res = requests.put(
        API_URL + endpoint,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        },
        json=body,
    )
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
    if deserialized["agentId"] == int(args.agentId):
        for channelId in deserialized["channels"]:
            channel = pusher.subscribe(f"chat-channel-{channelId}")
            channel.bind("new-message", pusher_message_callback)


info_response = get(f"agents/{args.agentId}/info")
if info_response.status_code != 200:
    print("ERROR: Failed to fetch agent information.")
    sys.exit(1)

agent_info = info_response.json()
print(f"Personality: {agent_info['personality']}")

channels_response = get(f"agents/{args.agentId}/channels")
if channels_response.status_code != 200:
    print("ERROR: Failed to fetch agent channels.")
    sys.exit(1)

channels_response = channels_response.json()
channelIds = channels_response["channels"]

pusher = pysher.Pusher(PUSHER_APP_KEY, cluster="us3")

register_response = post(f"agents/register/{args.agentId}")
if register_response.status_code != 204:
    print("ERROR: Failed to register agent.")
    sys.exit(1)


def pusher_connection_handler(data):
    for channelId in channelIds:
        channel = pusher.subscribe(f"chat-channel-{channelId}")
        channel.bind("new-message", pusher_message_callback)

    status_channel = pusher.subscribe("agent-control")
    status_channel.bind("membership-added", pusher_add_server)

    print("Registered Pusher channel connections.")


pusher.connection.bind("pusher:connection_established", pusher_connection_handler)
pusher.connect()

agentReplyMap = {}


def prompt_content_for_message(message):
    content = (message.get("content") or "").strip()
    attachment_sections = []

    for attachment in message.get("attachments") or []:
        file_name = attachment.get("file_name") or "attachment"
        extracted_text = (attachment.get("extracted_text") or "").strip()
        extraction_status = attachment.get("extraction_status")

        if extracted_text:
            if len(extracted_text) > MAX_ATTACHMENT_PROMPT_CHARS:
                extracted_text = (
                    extracted_text[:MAX_ATTACHMENT_PROMPT_CHARS].rstrip()
                    + "\n\n[Attachment text truncated.]"
                )
            attachment_sections.append(f"[{file_name}]\n{extracted_text}")
        elif extraction_status and extraction_status != "unsupported":
            attachment_sections.append(
                f"[{file_name}]\nNo extracted text is available ({extraction_status})."
            )

    if not attachment_sections:
        return content

    message_text = content if content else "(no message text)"
    return f"Message:\n{message_text}\n\n" "Attachments:\n" + "\n\n".join(
        attachment_sections
    )


while True:
    message = message_queue.get()

    print(f"Received message ID {message['id']}")

    if message["author"]["type"] == "AGENT":
        if message["author"]["id"] == int(args.agentId):
            continue

        if message["author"]["id"] not in agentReplyMap:
            agentReplyMap[message["author"]["id"]] = {"received": 0, "reset": 0}

        if agentReplyMap[message["author"]["id"]]["received"] >= 3:
            agentReplyMap[message["author"]["id"]]["reset"] += 1
            continue

        if agentReplyMap[message["author"]["id"]]["reset"] >= 5:
            agentReplyMap[message["author"]["id"]]["received"] = 0
            agentReplyMap[message["author"]["id"]]["reset"] = 0

        agentReplyMap[message["author"]["id"]]["received"] += 1

    channelId = message["channel_id"]

    post(f"agents/{args.agentId}/startreply/{channelId}")

    recentMessages = get(f"channels/{channelId}/messages/recent")
    recentMessages = recentMessages.json()

    current_message = next(
        (
            recent_message
            for recent_message in recentMessages
            if recent_message["id"] == message["id"]
        ),
        message,
    )

    messages = [
        {
            "role": "system",
            "content": f"You are an agent in a virtual messaging system where you will interact with real users and other LLM agents. Do not end your responses with follow up questions. Your personality is as follows: {agent_info['personality']}",
        }
    ]

    for msg in recentMessages:
        if msg["id"] == message["id"]:
            continue

        role = "user"
        if msg["author"]["type"] == "AGENT" and msg["author"]["id"] == args.agentId:
            role = "assistant"

        messages.append({"role": role, "content": prompt_content_for_message(msg)})

    messages.append(
        {"role": "user", "content": prompt_content_for_message(current_message)}
    )

    agent_response = client.chat(model=args.model, messages=messages)

    res = post(
        f"/channels/{channelId}/messages",
        {"agentId": args.agentId, "content": agent_response["message"]["content"]},
    )

    if res.status_code != 201:
        print("ERROR: Failed to respond to message", message, res)
        continue

    print(f"Agent ID {args.agentId} responded to message {message['id']}.")
