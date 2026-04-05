from http.client import HTTPException

from sqlalchemy import select

from auth import require_auth
from flask import Blueprint, g, jsonify, request
from flask_extensions import db

from models import Channel
from models.message import Message
from blueprints.messages.services import create_message
from blueprints.messages.validation import validate_create_message_payload
from models.user import User

channels_blueprint = Blueprint("channels", __name__)


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
    if g.user.memberships.filter_by(server_id=channel.server_id).first() is None:
        return jsonify({"error": "You are not a member of this server"}), 403
    if validated["reply_to_id"]:
        parent_message = Message.query.get(validated["reply_to_id"])
        if not parent_message or parent_message.channel_id != channel_id:
            return jsonify({"error": "Invalid reply_to_id"}), 400

    try:
        message = create_message(
            channel_id=channel_id,
            author_id=g.user.id,
            content=validated["content"],
            reply_to_id=validated["reply_to_id"],
        )
    except HTTPException as exc:
        return jsonify({"error": exc.description}), exc.code

    result = message.to_dict()

    return jsonify(result), 201


@channels_blueprint.route("/<int:channel_id>/messages", methods=["GET"])
@require_auth
def get_messages(channel_id: int):
    from models.channel import Channel

    channel = Channel.query.get(channel_id)
    if not channel:
        return jsonify({"error": "Channel not found"}), 404
    if g.user.memberships.filter_by(server_id=channel.server_id).first() is None:
        return jsonify({"error": "You are not a member of this server"}), 403

    messages = db.session.execute(
        select(Message, User.id, User.username, User.displayName, User.avatar_url)
        .join(User, User.id == Message.author_id)
        .where(Message.channel_id == channel_id)
        .order_by(Message.created_at.asc())
    ).all()

    result = [
        {
            "id": message.Message.id,
            "content": message.Message.content,
            "created_at": message.Message.created_at.isoformat(),
            "author": {
                "id": message.id,
                "username": message.username,
                "displayName": message.displayName,
                "avatar_url": message.avatar_url,
            },
            "reply_to_id": message.Message.reply_to_id,
        }
        for message in messages
    ]

    return jsonify(result), 200
