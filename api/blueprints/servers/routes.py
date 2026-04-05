from sqlalchemy import select

from auth import require_auth
from flask import Blueprint, g, jsonify, request
from flask_extensions import db

from models.channel import Channel
from models.server import Server
from models.server_member import ROLE_ADMIN, ROLE_OWNER, ServerMember

servers_blueprint = Blueprint("servers", __name__)


@servers_blueprint.route("/self/list", methods=["GET"])
@require_auth
def list_membership_servers():
    rows = db.session.execute(
        select(Server, ServerMember.role)
        .join(ServerMember, ServerMember.server_id == Server.id)
        .where(ServerMember.user_id == g.user.id)
        .order_by(Server.name.asc())
    ).all()

    result = [
        {
            "id": server.id,
            "name": server.name,
            "icon_url": server.icon_url,
            "description": server.description,
            "owner": server.owner,
            "role": role,
        }
        for server, role in rows
    ]

    return jsonify(result), 200


@servers_blueprint.route("/create", methods=["POST"])
@require_auth
def create_new_server():
    payload = request.get_json()
    owner = g.user
    name = (
        payload["name"].strip()
        if "name" in payload and isinstance(payload["name"], str)
        else None
    )
    if not name:
        return jsonify({"message": "Name is required"}), 400
    if len(name) > 255:
        return jsonify({"message": "Name must be less than 255 characters"}), 400
    
    description = (
        payload.get("description").strip()
        if "description" in payload and isinstance(payload["description"], str)
        else None
    )
    if description and len(description) > 255:
        return jsonify({"message": "Description must be less than 255 characters"}), 400
    icon_url = payload.get("iconUrl").strip() if "iconUrl" in payload else None
    if icon_url and len(icon_url) > 255:
        return jsonify({"message": "Icon URL must be less than 255 characters"}), 400
    
    new_server = Server(name=name, description=description, icon_url=icon_url, owner=owner.id)
    db.session.add(new_server)
   if icon_url and len(icon_url) > 255:
        return jsonify({"message": "Icon URL must be less than 255 characters"}), 400
    db.session.flush()  # Flush to get the server ID for the ServerMember entry
    db.session.refresh(owner)
    db.session.add(
        ServerMember(server_id=new_server.id, user_id=owner.id, role="0")
    )
    db.session.commit()
    return jsonify(new_server.to_dict()), 201


@servers_blueprint.route("/<int:server_id>/channels", methods=["POST"])
@require_auth
def create_new_channel(server_id: int):
    payload = request.get_json()
    name = payload.get("name").strip() if "name" in payload else None
    if not name:
        return jsonify({"message": "Name is required"}), 400
    if len(name) > 255:
        return jsonify({"message": "Name must be less than 255 characters"}), 400
    server = Server.query.get(server_id)
    if not server:
        return jsonify({"message": "Server not found"}), 404
    membership = ServerMember.query.filter_by(
        server_id=server_id, user_id=g.user.id
    ).first()
    if not membership:
        return jsonify({"message": "You are not a member of this server"}), 403

    if membership.role not in [ROLE_OWNER, ROLE_ADMIN]:
        return (
            jsonify(
                {
                    "message": "You do not have permission to create channels in this server"
                }
            ),
            403,
        )

    channel_count = Channel.query.filter_by(server_id=server_id).count()
    db.session.add(Channel(name=name, server_id=server_id, position=channel_count))
    db.session.commit()
    return jsonify({"message": "Channel created successfully"}), 201


@servers_blueprint.route("/<int:server_id>/channels", methods=["GET"])
@require_auth
def get_channel_list(server_id: int):
    server = Server.query.get(server_id)
    if not server:
        return jsonify({"message": "Server not found"}), 404
    membership = ServerMember.query.filter_by(
        server_id=server_id, user_id=g.user.id
    ).first()
    if not membership:
        return jsonify({"message": "You are not a member of this server"}), 403

    channels = (
        Channel.query.filter_by(server_id=server_id)
        .order_by(Channel.position.asc())
        .all()
    )
    result = [
        {
            "id": channel.id,
            "name": channel.name,
            "position": channel.position,
        }
        for channel in channels
    ]

    return jsonify(result), 200
