from turtlesoup.api.message_controller import MessageController
from turtlesoup.api.story_controller import StoryController
from flask import Blueprint

turtlesoup_api = Blueprint("turtlesoup_api", __name__)

def register_turtlesoup_routes(
        message_controller: MessageController,
        story_controller: StoryController
    ):

    turtlesoup_api.add_url_rule(
        "/api/messages",
        view_func=message_controller.post_message,
        methods=["POST"]
    )
    
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
