from api.flask_extensions import db


class Invite(db.Model):
    __tablename__ = "invites"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    server_id = db.Column(
        db.Integer,
        db.ForeignKey("servers.id"),
        nullable=False,
    )
    code = db.Column(db.String(100), nullable=False, unique=True)

    server = db.relationship("Server", back_populates="invites")
