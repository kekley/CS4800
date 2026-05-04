from flask_extensions import db
from sqlalchemy.sql import func


class Agent(db.Model):
    __tablename__ = "agents"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
    )
    name = db.Column(db.Text, nullable=True)
    model = db.Column(db.Text, nullable=True)
    personality = db.Column(db.Text, nullable=True)
    status = db.Column(db.Integer, nullable=True)
    typingIn = db.Column(db.Integer, nullable=True)
    created_at = db.Column(
        db.TIMESTAMP,
        server_default=func.current_timestamp(),
        nullable=False,
    )

    owner = db.relationship("User", back_populates="agents")
    memberships = db.relationship(
        "AgentMember",
        back_populates="agent",
        cascade="all, delete-orphan",
        lazy="dynamic",
    )
    messages = db.relationship(
        "Message",
        back_populates="agent",
        cascade="all, delete-orphan",
    )

    def to_dict(self):
        data = {
            "id": self.id,
            "user_id": self.userId,
            "name": self.name,
            "model": self.model,
            "personality": self.personality,
            "status": self.status,
            "typingIn": self.typingIn,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

        return data
