from flask import abort
from flask_extensions import db
from models.channel import Channel
from models.message import Message
from models.server_member import ServerMember
from models.agent_member import AgentMember
from sqlalchemy import select


def create_message(
    *,
    channel_id: int,
    author_id: int,
    agent_id: int,
    content: str,
    reply_to_id: int | None = None,
):
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
        content=content,
        reply_to_id=reply_to_id,
    )

    db.session.add(message)
    db.session.commit()
    db.session.refresh(message)

    return message
