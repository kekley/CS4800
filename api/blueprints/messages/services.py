from flask import abort
from sqlalchemy import select

from api.flask_extensions import db
from api.models.channel import Channel
from api.models.message import Message
from api.models.server_member import ServerMember


def create_message(
    *,
    channel_id: int,
    author_id: int,
    content: str,
    reply_to_id: int | None = None,
):
    channel = db.session.get(Channel, channel_id)
    if not channel:
        abort(404, description="channel_not_found")

    membership = db.session.execute(
        select(ServerMember).where(
            ServerMember.server_id == channel.server_id,
            ServerMember.user_id == author_id,
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
        content=content,
        reply_to_id=reply_to_id,
    )

    db.session.add(message)
    db.session.commit()
    db.session.refresh(message)

    return message
