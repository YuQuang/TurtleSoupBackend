import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from turtlesoup.routes.route import turtlesoup_api, register_turtlesoup_routes
from turtlesoup.logging import get_logger
from turtlesoup.pgsql import create_connection_pool
from turtlesoup.dependencies import create_dependencies


logger = get_logger(__name__)

load_dotenv()

def create_app() -> Flask:
    logger.info("Creating TurtleSoup application")
    app = Flask(__name__)

    app.secret_key = os.getenv("FLASK_SECRET_KEY")
    app.config.update(
        SECRET_KEY=os.environ["FLASK_SECRET_KEY"],
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
    )

    CORS(
        app,
        origins=[
            "http://localhost:5173",
            "https://turtlesoupfrontend.onrender.com",
        ],
        supports_credentials=True,
    )

    connection_pool = create_connection_pool()
    dependencies = create_dependencies(connection_pool)

    register_turtlesoup_routes(
        message_controller=dependencies["message_controller"],
        story_controller=dependencies["story_controller"],
        google_controller=dependencies["google_controller"],
        auth_controller=dependencies["auth_controller"]
    )

    app.register_blueprint(turtlesoup_api)

    logger.info("TurtleSoup application created")

    return app