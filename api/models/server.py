from flask_extensions import db
from sqlalchemy.sql import func


class Server(db.Model):
    __tablename__ = "servers"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
    )
    name = db.Column(db.String(255), nullable=False)
    icon_url = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(
        db.TIMESTAMP,
        server_default=func.current_timestamp(),
        nullable=False,
    )

    owner_user = db.relationship(
        "User",
        back_populates="owned_servers",
        foreign_keys=[owner],
    )
    members = db.relationship(
        "ServerMember",
        back_populates="server",
        cascade="all, delete-orphan",
    )
    channels = db.relationship(
        "Channel",
        back_populates="server",
        cascade="all, delete-orphan",
    )
    invites = db.relationship(
        "Invite",
        back_populates="server",
        cascade="all, delete-orphan",
    )
