import mimetypes
import os

from constants import (
    ALLOWED_ATTACHMENT_EXTENSIONS,
    ALLOWED_ATTACHMENT_MIME_TYPES,
    MAX_ATTACHMENTS_PER_MESSAGE,
    MAX_ATTACHMENT_SIZE_BYTES,
)
from werkzeug.utils import secure_filename


def _parse_optional_int(value, field_name):
    if value in (None, ""):
        return True, None

    if isinstance(value, int):
        return True, value

    if isinstance(value, str) and value.isdigit():
        return True, int(value)

    return False, f"{field_name}_must_be_integer"


def _normalized_content(value):
    if value is None:
        return ""

    if not isinstance(value, str):
        return None

    return value.strip()


def validate_create_message_payload(message_payload, *, has_attachments=False):
    if not isinstance(message_payload, dict):
        return False, "invalid_json"

    content = message_payload.get("content")
    reply_to_message_id = message_payload.get("reply_to_id")
    agentId = message_payload.get("agentId")

    content = _normalized_content(content)
    if content is None:
        return False, "content_must_be_string"

    if not content and not has_attachments:
        return False, "content_required"

    if len(content) > 4000:
        return False, "content_too_long"

    ok, reply_to_message_id = _parse_optional_int(
        reply_to_message_id,
        "reply_to_id",
    )
    if not ok:
        return False, reply_to_message_id

    return True, {
        "content": content,
        "reply_to_id": reply_to_message_id,
        "agentId": agentId,
    }


def _attachment_size(file_storage):
    stream = file_storage.stream
    stream.seek(0, os.SEEK_END)
    size = stream.tell()
    stream.seek(0)
    return size


def _attachment_mime_type(file_storage, filename):
    guessed_type, _ = mimetypes.guess_type(filename)
    if file_storage.mimetype and file_storage.mimetype != "application/octet-stream":
        return file_storage.mimetype
    return guessed_type or "application/octet-stream"


def validate_attachment_files(files):
    if len(files) > MAX_ATTACHMENTS_PER_MESSAGE:
        return False, "too_many_attachments"

    validated_files = []
    for file_storage in files:
        if not file_storage or not file_storage.filename:
            continue

        filename = secure_filename(file_storage.filename)
        if not filename:
            return False, "invalid_attachment_name"

        extension = os.path.splitext(filename)[1].lower()
        mime_type = _attachment_mime_type(file_storage, filename)
        if (
            extension not in ALLOWED_ATTACHMENT_EXTENSIONS
            or mime_type not in ALLOWED_ATTACHMENT_MIME_TYPES
        ):
            return False, "unsupported_attachment_type"

        size = _attachment_size(file_storage)
        if size <= 0:
            return False, "empty_attachment"

        if size > MAX_ATTACHMENT_SIZE_BYTES:
            return False, "attachment_too_large"

        validated_files.append(
            {
                "file": file_storage,
                "file_name": filename,
                "type": mime_type,
                "size": size,
                "extension": extension,
            }
        )

    return True, validated_files
