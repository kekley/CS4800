from api.flask_extensions import db
from sqlalchemy.sql import func


class UserSession(db.Model):
    __tablename__ = "user_sessions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
    )
    hash = db.Column(db.String(255), nullable=False, unique=True)
    created_at = db.Column(
        db.TIMESTAMP,
        server_default=func.current_timestamp(),
        nullable=False,
    )

    user = db.relationship("User", back_populates="sessions")
