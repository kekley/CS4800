from flask_extensions import db


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
