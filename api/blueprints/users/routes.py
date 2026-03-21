from flask import Blueprint, jsonify, request, g
from werkzeug.exceptions import HTTPException

from api.auth import require_auth

users_blueprint = Blueprint("users", __name__)


@users_blueprint.route("/me", methods=["GET"])
@require_auth
def me():
    result = g.user.to_dict()
    return jsonify(result), 201
