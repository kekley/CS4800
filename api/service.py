import models

from blueprints.messages.routes import messages_blueprint
from blueprints.users.routes import users_blueprint
from blueprints.servers.routes import servers_blueprint
from blueprints.channels.routes import channels_blueprint
from blueprints.agents.routes import agents_blueprint

from constants import MAX_MESSAGE_UPLOAD_SIZE_BYTES, TEST_DB_URI
from flask import Flask, jsonify
from flask_cors import CORS
from flask_extensions import db
from pusher import Pusher
from werkzeug.exceptions import RequestEntityTooLarge

app = Flask(__name__)
CORS(
    app,
    origins=[
        "http://localhost:5173",
    ],
    supports_credentials=True,
)

app.config["SQLALCHEMY_DATABASE_URI"] = TEST_DB_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

app.register_blueprint(messages_blueprint, url_prefix="/messages")

app.register_blueprint(users_blueprint, url_prefix="/users")

app.register_blueprint(servers_blueprint, url_prefix="/servers")

app.register_blueprint(channels_blueprint, url_prefix="/channels")

app.register_blueprint(agents_blueprint, url_prefix="/agents")


@app.errorhandler(RequestEntityTooLarge)
def handle_upload_too_large(_exc):
    return jsonify({"error": "upload_too_large"}), 413


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
