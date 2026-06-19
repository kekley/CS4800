from flask_extensions import db

ROLE_OWNER = 0
ROLE_ADMIN = 1
ROLE_MEMBER = 2


class ServerMember(db.Model):
    __tablename__ = "server_members"

    server_id = db.Column(
        db.Integer,
        db.ForeignKey("servers.id"),
        primary_key=True,
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        primary_key=True,
    )
    role = db.Column(db.Integer)

    server = db.relationship("Server", back_populates="members")
    user = db.relationship("User", back_populates="memberships")
