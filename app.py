from flask import Flask, url_for

app = Flask(__name__)


@app.route("/")
def hello():
    print(url_for("static", filename="index.html"))
    return "<h1>Hello, World!</h1>"
