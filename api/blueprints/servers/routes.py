from datetime import timedelta

from sqlalchemy import select

from auth import require_auth
from flask import Blueprint, g, jsonify, request
from flask_extensions import db

from models.channel import Channel
from models.invite import Invite
from models.server import Server
from models.user import User
from models.agent import Agent
from models.agent_member import AgentMember
from models.server_member import ROLE_ADMIN, ROLE_MEMBER, ROLE_OWNER, ServerMember

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

    icon_url = (
        payload["iconUrl"].strip()
        if "iconUrl" in payload and isinstance(payload["iconUrl"], str)
        else None
    )
    if icon_url and len(icon_url) > 255:
        return jsonify({"message": "Icon URL must be less than 255 characters"}), 400

    public = payload.get("public") if "public" in payload else False
    if public is not None and (not isinstance(payload["public"], bool)):
        return jsonify({"message": "Public must be a boolean value."}), 400

    new_server = Server(
        name=name,
        description=description,
        icon_url=icon_url,
        owner=owner.id,
        public=public,
    )
    db.session.add(new_server)
    if icon_url and len(icon_url) > 255:
        return jsonify({"message": "Icon URL must be less than 255 characters"}), 400
    db.session.flush()  # Flush to get the server ID for the ServerMember entry
    db.session.add(
        ServerMember(server_id=new_server.id, user_id=owner.id, role=ROLE_OWNER)
    )
    db.session.add(new_server)
    if icon_url and len(icon_url) > 255:
        return jsonify({"message": "Icon URL must be less than 255 characters"}), 400
    db.session.flush()  # Flush to get the server ID for the ServerMember entry
    db.session.refresh(owner)
    db.session.add(
        ServerMember(server_id=new_server.id, user_id=owner.id, role=ROLE_OWNER)
    )
    db.session.commit()
    return jsonify(new_server.to_dict()), 201


@servers_blueprint.route("/<int:server_id>/channels", methods=["POST"])
@require_auth
def create_new_channel(server_id: int):
    payload = request.get_json()
    name = (
        payload.get("name").strip()
        if "name" in payload and isinstance(payload["name"], str)
        else None
    )
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
    new_channel = Channel(name=name, server_id=server_id, position=channel_count)
    db.session.add(new_channel)
    db.session.commit()
    return (
        jsonify(
            {
                "id": new_channel.id,
                "name": new_channel.name,
                "position": new_channel.position,
            }
        ),
        201,
    )


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


@servers_blueprint.route("/<int:server_id>/invite", methods=["POST"])
@require_auth
def create_invite(server_id: int):
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
                    "message": "You do not have permission to create invites for this server"
                }
            ),
            403,
        )

    invite_code = server.generate_invite_code()
    db.session.add(
        Invite(
            code=invite_code,
            server_id=server_id,
        )
    )
    db.session.commit()

    return jsonify({"invite_code": invite_code}), 201


@servers_blueprint.route("/join/<string:invite_code>", methods=["GET"])
@require_auth
def accept_invite(invite_code: str):
    invite = Invite.query.filter_by(code=invite_code).first()
    if not invite:
        return jsonify({"message": "Invalid invite code"}), 404

    server = Server.query.get(invite.server_id)
    if not server:
        return jsonify({"message": "Server not found"}), 404

    existing_membership = ServerMember.query.filter_by(
        server_id=server.id, user_id=g.user.id
    ).first()
    if existing_membership:
        return jsonify({"message": "You are already a member of this server"}), 400

    new_membership = ServerMember(
        server_id=server.id, user_id=g.user.id, role=ROLE_MEMBER
    )
    db.session.add(new_membership)
    db.session.commit()

    return jsonify({"message": f"You have joined the server: '{server.name}'"}), 200


@servers_blueprint.route("/<int:server_id>/members", methods=["GET"])
@require_auth
def list_server_members(server_id: int):
    server = Server.query.get(server_id)
    if not server:
        return jsonify({"message": "Server not found"}), 404

    membership = ServerMember.query.filter_by(
        server_id=server_id, user_id=g.user.id
    ).first()
    if not membership:
        return jsonify({"message": "You are not a member of this server"}), 403

    rows = db.session.execute(
        select(
            User.id, User.username, User.displayName, User.avatar_url, ServerMember.role
        )
        .join(ServerMember, ServerMember.user_id == User.id)
        .where(ServerMember.server_id == server_id)
        .order_by(User.username.asc())
    ).all()

    result = [
        {
            "id": row.id,
            "username": row.username,
            "displayName": row.displayName,
            "avatar_url": row.avatar_url,
            "role": row.role,
        }
        for row in rows
    ]

    return jsonify(result), 200


@servers_blueprint.route("/<int:server_id>/agents", methods=["GET"])
@require_auth
def list_server_agents(server_id: int):
    server = Server.query.get(server_id)
    if not server:
        return jsonify({"message": "Server not found"}), 404

    membership = ServerMember.query.filter_by(
        server_id=server_id, user_id=g.user.id
    ).first()
    if not membership:
        return jsonify({"message": "You are not a member of this server"}), 403

    rows = (
        db.session.execute(
            select(Agent)
            .join(AgentMember, AgentMember.agent_id == Agent.id)
            .where(AgentMember.server_id == server_id)
            .order_by(Agent.name.asc())
        )
        .scalars()
        .all()
    )

    result = [row.to_dict() for row in rows]

    return jsonify(result), 200
