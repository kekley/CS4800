from api.flask_extensions import db
from sqlalchemy.sql import func


class MessageAttachment(db.Model):
    __tablename__ = "message_attachments"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message_id = db.Column(
        db.Integer,
        db.ForeignKey("messages.id"),
        nullable=False,
    )
    file_key = db.Column(db.String(255), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    size = db.Column(db.Integer, nullable=False)

    message = db.relationship("Message", back_populates="attachments")
