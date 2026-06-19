from flask_extensions import db
from sqlalchemy.dialects.mysql import LONGTEXT


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
    extraction_status = db.Column(
        db.String(32),
        nullable=False,
        default="pending",
        server_default="pending",
    )
    extracted_text = db.Column(
        db.Text().with_variant(LONGTEXT(), "mysql"),
        nullable=True,
    )
    extraction_error = db.Column(db.Text, nullable=True)
    extracted_at = db.Column(db.TIMESTAMP, nullable=True)

    message = db.relationship("Message", back_populates="attachments")
