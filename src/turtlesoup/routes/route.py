from turtlesoup.api.message_controller import MessageController
from turtlesoup.api.story_controller import StoryController
from turtlesoup.api.google_controller import GoogleController
from flask import Blueprint

turtlesoup_api = Blueprint("turtlesoup_api", __name__)

def register_turtlesoup_routes(
        message_controller: MessageController,
        story_controller: StoryController,
        google_controller: GoogleController,
        auth_controller
    ):


    """
        Message Endpoint
    """
    turtlesoup_api.add_url_rule(
        "/api/messages",
        view_func=message_controller.post_message,
        methods=["POST"]
    )
    turtlesoup_api.add_url_rule(
        "/api/messages",
        view_func=message_controller.get_messages,
        methods=["GET"]
    )


    """
        Stories Endpoint
    """
    turtlesoup_api.add_url_rule(
        "/api/stories",
        view_func=story_controller.post_story,
        methods=["POST"]
    )
    turtlesoup_api.add_url_rule(
        "/api/stories",
        view_func=story_controller.get_stories,
        methods=["GET"]
    )
    turtlesoup_api.add_url_rule(
        "/api/stories",
        view_func=story_controller.update_story,
        methods=["PATCH"]
    )


    """
        Google Endpoint
    """
    turtlesoup_api.add_url_rule(
        "/api/integrations/google/connect",
        view_func=google_controller.connect,
        methods=["GET"]
    )
    turtlesoup_api.add_url_rule(
        "/api/integrations/google/callback",
        view_func=google_controller.callback,
        methods=["GET"]
    )


    """
        Auth Endpoint
    """
    turtlesoup_api.add_url_rule(
        "/api/auth/me",
        view_func=auth_controller.me,
        methods=["POST"]
    )
