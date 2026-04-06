from flask_extensions import db
from sqlalchemy.sql import func
import string
import random


from models.invite import Invite


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
    public = db.Column(db.Boolean, nullable=False)
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

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "icon_url": self.icon_url,
            "description": self.description,
            "owner": self.owner,
            "public": self.public,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def generate_invite_code(self):
        characters = string.ascii_letters + string.digits
        while True:
            code = "".join(random.choice(characters) for _ in range(16))
            if not db.session.query(db.exists().where(Invite.code == code)).scalar():
                return code
