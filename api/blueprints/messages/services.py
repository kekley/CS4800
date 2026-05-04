import os
from uuid import uuid4

from constants import UPLOAD_ROOT
from blueprints.messages.extraction import extract_attachment_text
from flask import abort
from flask_extensions import db
from models.channel import Channel
from models.message import Message
from models.server_member import ServerMember
from models.agent_member import AgentMember
from models.message_attachment import MessageAttachment
from sqlalchemy import select


def create_message(
    *,
    channel_id: int,
    author_id: int,
    agent_id: int,
    content: str,
    reply_to_id: int | None = None,
    attachments: list[dict] | None = None,
):
    attachments = attachments or []
    channel = db.session.get(Channel, channel_id)
    if not channel:
        abort(404, description="channel_not_found")

    if (not author_id) and (not agent_id):
        abort(400, description="needs_author")

    if author_id is not None:
        membership = db.session.execute(
            select(ServerMember).where(
                ServerMember.server_id == channel.server_id,
                ServerMember.user_id == author_id,
            )
        ).scalar_one_or_none()

        if not membership:
            abort(403, description="not_a_server_member")
    elif agent_id is not None:
        membership = db.session.execute(
            select(AgentMember).where(
                AgentMember.server_id == channel.server_id,
                AgentMember.agent_id == agent_id,
            )
        ).scalar_one_or_none()

        if not membership:
            abort(403, description="not_a_server_member")

    if reply_to_id is not None:
        reply_target = db.session.get(Message, reply_to_id)
        if not reply_target or reply_target.channel_id != channel_id:
            abort(400, description="invalid_reply_target")

    message = Message(
        channel_id=channel_id,
        author_id=author_id,
        agent_id=agent_id,
        content=content or None,
        reply_to_id=reply_to_id,
    )

    saved_paths = []
    try:
        db.session.add(message)
        db.session.flush()

        for attachment in attachments:
            storage_name = f"{uuid4().hex}{attachment['extension']}"
            file_key = os.path.join(str(channel_id), storage_name)
            storage_path = os.path.join(UPLOAD_ROOT, file_key)
            os.makedirs(os.path.dirname(storage_path), exist_ok=True)

            attachment["file"].save(storage_path)
            saved_paths.append(storage_path)
            extraction = extract_attachment_text(
                storage_path,
                attachment["type"],
                attachment["file_name"],
            )

            db.session.add(
                MessageAttachment(
                    message_id=message.id,
                    file_key=file_key,
                    file_name=attachment["file_name"],
                    type=attachment["type"],
                    size=attachment["size"],
                    extraction_status=extraction["status"],
                    extracted_text=extraction["text"],
                    extraction_error=extraction["error"],
                    extracted_at=extraction["extracted_at"],
                )
            )

        db.session.commit()
        db.session.refresh(message)
    except Exception:
        db.session.rollback()
        for saved_path in saved_paths:
            try:
                os.remove(saved_path)
            except OSError:
                pass
        raise

    return message
