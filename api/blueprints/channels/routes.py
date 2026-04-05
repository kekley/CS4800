from http.client import HTTPException

from sqlalchemy import select

from models.agent import Agent
from auth import require_auth
from flask import Blueprint, g, jsonify, request
from flask_extensions import db, pusher

from models.channel import Channel
from models.message import Message
from blueprints.messages.services import create_message
from blueprints.messages.validation import validate_create_message_payload
from models.user import User

channels_blueprint = Blueprint("channels", __name__)


def format_message(message_obj, user_obj, channel_id, agent_obj=None):
    res = {
        "id": message_obj.id,
        "channel_id": channel_id,
        "content": message_obj.content,
        "created_at": message_obj.created_at.isoformat(),
        "author": None,
        "reply_to_id": message_obj.reply_to_id,
    }

    if agent_obj is not None:
        res["author"] = {"type": "AGENT", **agent_obj}
    else:
        res["author"] = {
            "type": "USER",
            "id": user_obj.id,
            "username": user_obj.username,
            "displayName": user_obj.displayName,
            "avatar_url": user_obj.avatar_url,
        }

    return res


@channels_blueprint.route("/<int:channel_id>/messages", methods=["POST"])
@require_auth
def post_message(channel_id: int):
    payload = request.get_json(silent=True)

    ok, validated = validate_create_message_payload(payload)
    if not ok:
        return jsonify({"error": validated}), 400

    channel = Channel.query.get(channel_id)
    if not channel:
        return jsonify({"error": "Channel not found"}), 404

    agent = None
    if g.user == "AGENT":
        agent = Agent.query.get(int(validated["agentId"]))
        if not agent:
            return jsonify({"error": "Agent not found"}), 404
        if agent.memberships.filter_by(server_id=channel.server_id).first() is None:
            return jsonify({"error": "Agent is not a member of this server"}), 403
    elif g.user.memberships.filter_by(server_id=channel.server_id).first() is None:
        return jsonify({"error": "You are not a member of this server"}), 403

    if validated["reply_to_id"]:
        parent_message = Message.query.get(validated["reply_to_id"])
        if not parent_message or parent_message.channel_id != channel_id:
            return jsonify({"error": "Invalid reply_to_id"}), 400

    # Push message to DB
    try:
        message = create_message(
            channel_id=channel_id,
            author_id=g.user.id if g.user != "AGENT" else None,
            agent_id=int(validated["agentId"]) if g.user == "AGENT" else None,
            content=validated["content"],
            reply_to_id=validated["reply_to_id"],
        )
    except HTTPException as exc:
        return jsonify({"error": exc.description}), exc.code

    if g.user == "AGENT":
        result = format_message(message, g.user, channel_id, agent_obj=agent.to_dict())
    else:
        result = format_message(message, g.user, channel_id)

    # Push message to Pusher
    pusher.trigger(
        channels=f"chat-channel-{channel_id}", event_name="new-message", data=result
    )

    if g.user == "AGENT":
        agent.status = 1
        agent.typingIn = None
        db.session.commit()

        pusher.trigger(
            channels="agent-control",
            event_name="status-change",
            data={
                "agentId": int(validated["agentId"]),
                "status": 1,
            },
        )

    return jsonify(result), 201


@channels_blueprint.route("/<int:channel_id>/messages", methods=["GET"])
@require_auth
def get_messages(channel_id: int):
    channel = Channel.query.get(channel_id)
    if not channel:
        return jsonify({"error": "Channel not found"}), 404
    if g.user.memberships.filter_by(server_id=channel.server_id).first() is None:
        return jsonify({"error": "You are not a member of this server"}), 403

    messages = db.session.execute(
        select(Message, User, Agent)
        .outerjoin(User, User.id == Message.author_id)
        .outerjoin(Agent, Agent.id == Message.agent_id)
        .where(Message.channel_id == channel_id)
        .order_by(Message.created_at.asc())
    ).all()

    grouped_messages = {}
    for message in messages:
        date_key = message.Message.created_at.date().isoformat()

        if date_key not in grouped_messages:
            grouped_messages[date_key] = []

        grouped_messages[date_key].append(
            format_message(
                message.Message,
                message.User,
                channel_id,
                agent_obj=message.Agent.to_dict() if message.Agent else None,
            )
        )

    sorted_messages = dict(sorted(grouped_messages.items()))

    return jsonify(sorted_messages), 200


@channels_blueprint.route("/<int:channel_id>/messages/recent", methods=["GET"])
@require_auth
def get_recent_message(channel_id: int):
    channel = Channel.query.get(channel_id)
    if not channel:
        return jsonify({"error": "Channel not found"}), 404
    if g.user != "AGENT":
        return jsonify({"error": "This endpoint is for agent access only"}), 403

    messages = db.session.execute(
        select(Message, User, Agent)
        .outerjoin(User, User.id == Message.author_id)
        .outerjoin(Agent, Agent.id == Message.agent_id)
        .where(Message.channel_id == channel_id)
        .order_by(Message.created_at.desc())
        .limit(5)
    ).all()

    res = [
        format_message(
            message.Message,
            message.User,
            channel_id,
            agent_obj=message.Agent.to_dict() if message.Agent else None,
        )
        for message in messages
    ]

    res = sorted(res, key=lambda x: x["created_at"])

    return jsonify(res), 200
