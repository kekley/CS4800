from auth import require_auth
from flask import Blueprint, g, jsonify, request
from flask_extensions import db

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

    if (not username or not username.strip()) and (not displayName or not displayName.strip()):
        return jsonify({"message": "Username or Display Name is required"}), 400
    
    if username:
        g.user.username = username.strip()
    
    if displayName:
        g.user.displayName = displayName.strip()

    db.session.commit()

    return jsonify(g.user.to_dict()), 204