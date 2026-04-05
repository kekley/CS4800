from auth import require_auth
from flask import Blueprint, g, jsonify, request
from flask_extensions import db

from sqlalchemy import select, func

from models.message import Message
from models.agent import Agent
from models.user import User
from models.server import Server

users_blueprint = Blueprint("users", __name__)


@users_blueprint.route("/self", methods=["GET"])
@require_auth
def get_self():
    return jsonify(g.user.to_dict()), 200


@users_blueprint.route("/self", methods=["POST"])
@require_auth
def update_self():
    data = request.get_json() or {}
    username = data.get("username") if "username" in data else None
    displayName = data.get("displayName") if "displayName" in data else None

    if (not username or not username.strip()) and (
        not displayName or not displayName.strip()
    ):
        return jsonify({"message": "Username or Display Name is required"}), 400

    if username:
        existing_user = User.query.filter_by(username=username.strip()).first()
        if existing_user and existing_user.id != g.user.id:
            return jsonify({"message": "User with this username already exists."}), 409
        g.user.username = username.strip()

    if displayName:
        g.user.displayName = displayName.strip()

    db.session.commit()

    return jsonify(g.user.to_dict()), 204


@users_blueprint.route("/self/stats", methods=["GET"])
@require_auth
def get_self_stats():
    message_count = db.session.execute(
        select(func.count(Message.id)).where(Message.author_id == g.user.id)
    ).scalar()

    agent_count = db.session.execute(
        select(func.count(Agent.id)).where(Agent.userId == g.user.id)
    ).scalar()

    server_count = db.session.execute(
        select(func.count(Server.id)).where(Server.owner == g.user.id)
    ).scalar()

    return (
        jsonify(
            {"messages": message_count, "agents": agent_count, "servers": server_count}
        ),
        200,
    )
