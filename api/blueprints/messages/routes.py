from auth import require_auth
from blueprints.messages.services import create_message
from blueprints.messages.validation import validate_create_message_payload
from flask import Blueprint, g, jsonify, request
from werkzeug.exceptions import HTTPException

from flask_extensions import db, pusher
from sqlalchemy import select

from models.channel import Channel
from models.server_member import ServerMember
from models.message import Message
from models.user import User
from models.agent import Agent

from blueprints.channels.routes import format_message

messages_blueprint = Blueprint("messages", __name__)


@messages_blueprint.route("/search", methods=["POST"])
@require_auth
def search_messages():
    payload = request.get_json()
    search_query = payload.get("query")

    if not search_query:
        return jsonify({"error": "Please provide a valid search query"}), 400
    
    server_ids = [
        sm.server_id for sm in ServerMember.query.filter_by(user_id=g.user.id).all()
    ]

    channel_ids = [
        c.id for c in Channel.query.filter(Channel.server_id.in_(server_ids)).all()
    ]

    messages = db.session.execute(
        select(Message, User, Agent)
        .outerjoin(User, User.id == Message.author_id)
        .outerjoin(Agent, Agent.id == Message.agent_id)
        .where(
            Message.channel_id.in_(channel_ids),
            Message.content.ilike(f"%{search_query}%")
        )
        .order_by(Message.created_at.desc())
    ).all()

    res = [
        format_message(message.Message, message.User, message.Message.channel_id, agent_obj=message.Agent.to_dict() if message.Agent else None)
        for message in messages
    ]

    return jsonify({
        "count": len(res),
        "results": res
    }), 200