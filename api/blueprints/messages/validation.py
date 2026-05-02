def validate_create_message_payload(message_payload):
    if not isinstance(message_payload, dict):
        return False, "invalid_json"

    content = message_payload.get("content")
    reply_to_message_id = message_payload.get("reply_to_id")
    agentId = message_payload.get("agentId")

    if not isinstance(content, str):
        return False, "content_must_be_string"

    content = content.strip()
    if not content:
        return False, "content_required"

    if len(content) > 4000:
        return False, "content_too_long"

    if reply_to_message_id is not None and not isinstance(reply_to_message_id, int):
        return False, "reply_to_id_must_be_integer"

    return True, {
        "content": content,
        "reply_to_id": reply_to_message_id,
        "agentId": agentId
    }
