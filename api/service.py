from flask import Flask
from flask_cors import CORS
from pusher import Pusher

from auth import require_auth

app = Flask(__name__)
CORS(
    app,
    origins=[
        "https://cloudcontain.net",
        "http://localhost:5173",
    ],
    supports_credentials=True,
)

@app.route("/userinfo", methods=["GET"])
@require_auth
def get_user_info():
    return jsonify({"message": "Hello, World!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)