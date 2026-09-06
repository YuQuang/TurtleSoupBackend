from flask import Flask
from turtlesoup.routes.route import turtlesoup_api, register_turtlesoup_routes
from turtlesoup.logging import get_logger
from turtlesoup.pgsql import create_connection_pool
from turtlesoup.dependencies import create_dependencies


logger = get_logger(__name__)


def create_app() -> Flask:
    logger.info("Creating TurtleSoup application")
    app = Flask(__name__)

    connection_pool = create_connection_pool()
    dependencies = create_dependencies(connection_pool)

    register_turtlesoup_routes(
        message_controller=dependencies["message_controller"],
        story_controller=dependencies["story_controller"]
    )

    app.register_blueprint(turtlesoup_api)

    logger.info("TurtleSoup application created")

    return app