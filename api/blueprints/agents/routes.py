from http.client import HTTPException

import pusher
import docker
from sqlalchemy import select

from models.server import Server
from models.channel import Channel
from models.agent import Agent
from models.agent_member import AgentMember
from auth import require_auth
from flask import Blueprint, g, jsonify, request
from flask_extensions import db, pusher

agents_blueprint = Blueprint("agents", __name__)

docker_client = docker.from_env()


@agents_blueprint.route("/create/<int:serverId>", methods=["POST"])
@require_auth
def create_agent(serverId):
    payload = request.get_json()
    owner = g.user

    models = {
        "llama": "llama3.2",
        "mistral": "mistral",
        "gemma": "gemma3"
    }

    name = (
        payload["name"].strip()
        if "name" in payload and isinstance(payload["name"], str)
        else None
    )
    if not name:
        return jsonify({"message": "Name is required"}), 400
    if len(name) > 255:
        return jsonify({"message": "Name must be less than 255 characters"}), 400
    
    model = (
        payload["model"].strip()
        if "model" in payload and isinstance(payload["model"], str)
        else None
    )
    if not model:
        return jsonify({"message": "Model type is required (Llama, Mistral, Gemma)."}), 400
    if model.lower() not in ["llama", "mistral", "gemma"]:
        return jsonify({"message": "Agents only support Llama, Mistral, or Gemma model types."}), 400
    
    new_agent = Agent(
        name=name,
        userId=owner.id,
        model=models[model.lower()],
        personality=payload["personality"].strip() if "personality" in payload else None,
        status=0
    )
    db.session.add(new_agent)
    db.session.flush() 

    db.session.add(
        AgentMember(server_id=serverId, agent_id=new_agent.id)
    )
    db.session.commit()

    docker_client.containers.run(
        image="agent-app:latest",
        name=f"agent-{new_agent.id}-{name}",
        command=["python", "agent.py", "--agentId", str(new_agent.id), "--model", models[model.lower()],],
        environment={
            "OLLAMA_HOST": "http://ollama:11434",
        },
        network="agents_default",
        detach=True,
        remove=True,
    )

    pusher.trigger(
        channels="agent-control",
        event_name="new-agent",
        data={
            "serverId": serverId,
            "agent": new_agent.to_dict()
        }
    )

    return jsonify(new_agent.to_dict()), 201


@agents_blueprint.route("/<int:agentId>", methods=["PUT"])
@require_auth
def update_agent(agentId):
    agent = Agent.query.get(agentId)
    if not agent:
        return jsonify({"error": "Agent not found"}), 404
    
    if agent.userId != g.user.id:
        return jsonify({"error": "You do not own this agent"}), 403
    
    models = {
        "llama": "llama3.2",
        "mistral": "mistral",
        "gemma": "gemma3"
    }

    payload = request.get_json()

    name = (
        payload["name"].strip()
        if "name" in payload and isinstance(payload["name"], str)
        else None
    )
    if name is not None:
        agent.name = name
    
    model = (
        payload["model"].strip()
        if "model" in payload and isinstance(payload["model"], str)
        else None
    )
    if model is not None:
        agent.model = models[model.lower()]

    personality = (
        payload["personality"].strip()
        if "personality" in payload and isinstance(payload["personality"], str)
        else None
    )
    if personality is not None:
        agent.personality = personality

    db.session.commit()

    return jsonify(agent.to_dict()), 200

@agents_blueprint.route("/<int:agentId>/wake", methods=["POST"])
@require_auth
def wake_agent(agentId):
    agent = Agent.query.get(agentId)
    if not agent:
        return jsonify({"error": "Agent not found"}), 404
    
    if agent.status != 3:
        return jsonify({"error": "Agent is alrady awake"}), 400
    
    agent.status = 0
    db.session.commit()

    pusher.trigger(
        channels="agent-control",
        event_name="status-change",
        data={
            "agentId": agentId,
            "status": 0
        }
    )

    docker_client.containers.run(
        image="agent-app",
        name=f"agent-{agent.id}-{agent.name}",
        command=["python", "agent.py", "--agentId", str(agent.id), "--model", agent.model],
        environment={
            "OLLAMA_HOST": "http://ollama:11434",
        },
        network="agents_default",
        detach=False,
        remove=True,
    )

    return "", 204


@agents_blueprint.route("/<int:agentId>/sleep", methods=["POST"])
@require_auth
def sleep_agent(agentId):
    agent = Agent.query.get(agentId)
    if not agent:
        return jsonify({"error": "Agent not found"}), 404
    
    if agent.status == 3:
        return jsonify({"error": "Agent is already asleep"}), 400
    
    agent.status = 3
    db.session.commit()
    
    container = docker_client.containers.get(f"agent-{agent.id}-{agent.name}")
    container.stop()

    pusher.trigger(
        channels="agent-control",
        event_name="status-change",
        data={
            "agentId": agentId,
            "status": 3
        }
    )

    return "", 204


@agents_blueprint.route("/register/<int:agentId>", methods=["POST"])
@require_auth
def register_agent(agentId):
    agent = Agent.query.get(agentId)
    if not agent:
        return jsonify({"error": "Agent not found"}), 404
    
    agent.status = 1
    db.session.commit()

    pusher.trigger(
        channels="agent-control",
        event_name="status-change",
        data={
            "agentId": agentId,
            "status": 1
        }
    )

    return "", 204


@agents_blueprint.route("/<int:agentId>/startreply/<int:channelId>", methods=["POST"])
@require_auth
def agent_startreply(agentId, channelId):
    agent = Agent.query.get(agentId)
    if not agent:
        return jsonify({"error": "Agent not found"}), 404
    
    channel = Channel.query.get(channelId)
    if not channel:
        return jsonify({"error": "Channel not found"}), 404
    
    agent.status = 2
    agent.typingIn = int(channelId)
    db.session.commit()

    pusher.trigger(
        channels="agent-control",
        event_name="status-change",
        data={
            "agentId": agentId,
            "status": 2,
            "typingIn": int(channelId)
        }
    )

    return "", 204


@agents_blueprint.route("/<int:agentId>/assoc/<int:serverId>", methods=["PUT"])
@require_auth
def associate_agent_to_server(agentId, serverId):
    agent = Agent.query.get(agentId)
    if not agent:
        return jsonify({"error": "Agent not found"}), 404
    
    db.session.add(
        AgentMember(server_id=serverId, agent_id=agentId)
    )
    db.session.commit()

    channels = db.session.execute(
        select(Channel)
        .join(AgentMember, AgentMember.server_id == Channel.server_id)
        .where(AgentMember.agent_id == agentId)
        .order_by(Channel.position.asc())
    ).scalars().all()
    channel_list = [
        channel.id
        for channel in channels
    ]

    pusher.trigger(
        channels=f"agent-control",
        event_name="membership-added",
        data={
            "agentId": agentId,
            "serverId": serverId,
            "channels": channel_list
        }
    )

    return "", 204


@agents_blueprint.route("/<int:agentId>/channels", methods=["GET"])
@require_auth
def get_agent_channels(agentId):
    agent = Agent.query.get(agentId)
    if not agent:
        return jsonify({"error": "Agent not found"}), 404
    
    channels = db.session.execute(
        select(Channel)
        .join(AgentMember, AgentMember.server_id == Channel.server_id)
        .where(AgentMember.agent_id == agentId)
        .order_by(Channel.position.asc())
    ).scalars().all()
    channel_list = [
        channel.id
        for channel in channels
    ]

    return jsonify({
        "channels": channel_list
    }), 200


@agents_blueprint.route("/list", methods=["GET"])
@require_auth
def list_owned_agents():
    owner = g.user

    agents = db.session.execute(
        select(Agent)
        .where(Agent.userId == owner.id)
    ).scalars().all()

    res = [
        agent.to_dict()
        for agent in agents
    ]

    return jsonify(res), 200


@agents_blueprint.route("/<int:agentId>/info", methods=["GET"])
@require_auth
def get_agent_info(agentId):
    if g.user != "AGENT":
        return jsonify({"error": "This endpoint is for agent access only"}), 403

    agent = Agent.query.get(agentId)
    return jsonify(agent.to_dict()), 200