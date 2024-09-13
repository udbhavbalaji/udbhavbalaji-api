from flask import Flask
from flask_cors import CORS
from api.songsavvy.v1 import songsavvy_v1_blueprint, db


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    CORS(app)

    db.init_app(app)

    app.register_blueprint(songsavvy_v1_blueprint, url_prefix="/api/songsavvy/v1")

    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
