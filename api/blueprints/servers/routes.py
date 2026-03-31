from sqlalchemy import select

from auth import require_auth
from flask import Blueprint, g, jsonify, request
from flask_extensions import db

from models.server import Server
from models.server_member import ServerMember

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