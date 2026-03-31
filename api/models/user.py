from flask_extensions import db
from sqlalchemy.sql import func


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    auth0_subject = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=True, unique=False)
    username = db.Column(db.String(255), nullable=True, unique=True)
    displayName = db.Column(db.String(255), nullable=True, unique=True)
    avatar_url = db.Column(db.String(512), nullable=True)
    updated_at = db.Column(
        db.TIMESTAMP,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        nullable=False,
    )
    created_at = db.Column(
        db.TIMESTAMP,
        server_default=func.current_timestamp(),
        nullable=False,
    )

    owned_servers = db.relationship(
        "Server",
        back_populates="owner_user",
        cascade="all, delete-orphan",
        foreign_keys="Server.owner",
    )
    memberships = db.relationship(
        "ServerMember",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    messages = db.relationship(
        "Message",
        back_populates="author",
        cascade="all, delete-orphan",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "auth0_subject": self.auth0_subject,
            "email": self.email,
            "username": self.username,
            "displayName": self.displayName,
            "avatar_url": self.avatar_url,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
