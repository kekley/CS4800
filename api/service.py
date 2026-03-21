from flask import Flask, jsonify
from flask_cors import CORS
from pusher import Pusher

from api.constants import TEST_DB_URI
from api.flask_extensions import db
from api.blueprints.messages.routes import messages_blueprint
from api.blueprints.users.routes import users_blueprint

app = Flask(__name__)
CORS(
    app,
    origins=[
        "https://cloudcontain.net",
        "http://localhost:5173",
    ],
    supports_credentials=True,
)

app.config["SQLALCHEMY_DATABASE_URI"] = TEST_DB_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

app.register_blueprint(messages_blueprint, url_prefix="/api")

app.register_blueprint(users_blueprint, url_prefix="/api")


@app.route("/", methods=["GET"])
def get_user_info():
    return jsonify({"message": "Hello, World!"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
