from flask import Blueprint, jsonify, request, g
from werkzeug.exceptions import HTTPException

from api.auth import require_auth
from api.blueprints.messages.validation import validate_create_message_payload
from api.blueprints.messages.services import create_message

messages_blueprint = Blueprint("messages", __name__)


@messages_blueprint.route("/channels/<int:channel_id>/messages", methods=["POST"])
@require_auth
def post_message(channel_id: int):
    payload = request.get_json(silent=True)

    ok, validated = validate_create_message_payload(payload)
    if not ok:
        return jsonify({"error": validated}), 400

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
