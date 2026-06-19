from flask_extensions import db

ROLE_OWNER = 0
ROLE_ADMIN = 1
ROLE_MEMBER = 2


class AgentMember(db.Model):
    __tablename__ = "agent_members"

    server_id = db.Column(
        db.Integer,
        db.ForeignKey("servers.id"),
        primary_key=True,
    )
    agent_id = db.Column(
        db.Integer,
        db.ForeignKey("agents.id"),
        primary_key=True,
    )

    server = db.relationship("Server", back_populates="agent_members")
    agent = db.relationship("Agent", back_populates="memberships")
