from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="dev",
    )

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    return app
