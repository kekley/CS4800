from http.client import HTTPException

from sqlalchemy import select

from auth import require_auth
from flask import Blueprint, g, jsonify, request
from flask_extensions import db

from models.channel import Channel
from models.message import Message
from blueprints.messages.services import create_message
from blueprints.messages.validation import validate_create_message_payload
from models.user import User

from pusher import Pusher

from constants import (
    PUSHER_APP_ID, 
    PUSHER_KEY, 
    PUSHER_CLUSTER, 
    PUSHER_SECRET
)

channels_blueprint = Blueprint("channels", __name__)

pusher = Pusher(
    app_id=PUSHER_APP_ID,
    key=PUSHER_KEY,
    secret=PUSHER_SECRET,
    cluster=PUSHER_CLUSTER,
    ssl=True
)


def format_message(message_obj, user_obj):
    return {
        "id": message_obj.id,
        "content": message_obj.content,
        "created_at": message_obj.created_at.isoformat(),
        "author": {
            "id": user_obj.id,
            "username": user_obj.username,
            "displayName": user_obj.displayName,
            "avatar_url": user_obj.avatar_url,
        },
        "reply_to_id": message_obj.reply_to_id,
    }


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

    # Push message to DB
    try:
        message = create_message(
            channel_id=channel_id,
            author_id=g.user.id,
            content=validated["content"],
            reply_to_id=validated["reply_to_id"],
        )
    except HTTPException as exc:
        return jsonify({"error": exc.description}), exc.code
    
    result = format_message(message, g.user)

    # Push message to Pusher
    pusher.trigger(
        channels=f"chat-channel-{channel_id}",
        event_name="new-message",
        data=result
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
        select(Message, User)
        .join(User, User.id == Message.author_id)
        .where(Message.channel_id == channel_id)
        .order_by(Message.created_at.asc())
    ).all()

    grouped_messages = {}
    for message in messages:
        date_key = message.Message.created_at.date().isoformat() 

        if date_key not in grouped_messages:
            grouped_messages[date_key] = []
        
        grouped_messages[date_key].append(
            format_message(message.Message, message.User)
        )

    sorted_messages = dict(sorted(grouped_messages.items()))

    return jsonify(sorted_messages), 200
