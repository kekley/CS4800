from api.flask_extensions import db
from sqlalchemy.sql import func


class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    channel_id = db.Column(
        db.Integer,
        db.ForeignKey("channels.id"),
        nullable=False,
    )
    author_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
    )
    content = db.Column(db.Text, nullable=True)
    reply_to_id = db.Column(
        db.Integer,
        db.ForeignKey("messages.id"),
        nullable=True,
    )
    created_at = db.Column(
        db.TIMESTAMP,
        server_default=func.current_timestamp(),
        nullable=False,
    )
    edited_at = db.Column(db.TIMESTAMP, nullable=True)
    deleted_at = db.Column(db.TIMESTAMP, nullable=True)

    channel = db.relationship("Channel", back_populates="messages")
    author = db.relationship("User", back_populates="messages")

    reply_to = db.relationship(
        "Message",
        remote_side=[id],
        backref=db.backref("replies", lazy=True),
    )

    attachments = db.relationship(
        "MessageAttachment",
        back_populates="message",
        cascade="all, delete-orphan",
    )

    def to_dict(self):
        data = {
            "id": self.id,
            "channel_id": self.channel_id,
            "author_id": self.author_id,
            "content": self.content,
            "reply_to_id": self.reply_to_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "edited_at": self.edited_at.isoformat() if self.edited_at else None,
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None,
        }

        return data
