from uuid import UUID

from flask import jsonify, request
from pydantic_core import ValidationError
from turtlesoup.dto.StoryDTO import CreateStoryDTO, UpdateStoryDTO
from turtlesoup.logging import get_logger
from turtlesoup.services.story_service import StoryService


logger = get_logger(__name__)


class StoryController:


    def __init__(self, service: StoryService):
        self.service = service


    def get_stories(self):
        """
        Retrieve stories.

        Supports filtering by story ID or title through query parameters.
        When no filter is provided, all published stories are returned.

        Query Parameters:
            story_id: UUID of the story to retrieve.
            title: Title of the story to search for.

        Returns:
            JSON response containing the matching story or stories.
        """
        story_id = request.args.get("story_id", None)
        title = request.args.get("title", None)

        story = self.service.get_story(
                story_id=UUID(story_id) if story_id else None,
                title=title
            )

        return jsonify({"message": story, "status": "success"}), 200
    

    def get_title_and_story_id(self):
        """
        Retrieve all story titles & story id.

        Returns:
            JSON response containing a list of all story titles & story id.
        """
        titlesAndID = self.service.get_title_and_story_id()
        return jsonify({"message": titlesAndID, "status": "success"}), 200
    

    def update_story(self):
        """
        Update story.

        Validates the request body using UpdateStoryDTO before passing
        the data to the story service.

        Request Body:
            id: story id
            title: Title of the story.
            mystery: Mystery description of the story.
            solution: Solution to the mystery.
            hint: Hint for solving the mystery.

        Returns:
            201: Story created successfully.
            400: Request body validation failed.
        """
        payload = request.get_json(silent=True) or {}
        try:
            dto = UpdateStoryDTO.model_validate(payload)
        except ValidationError as e:
            logger.warning("Story validation failed")
            return jsonify({
                "message": e.errors(),
                "status": "failed",
            }), 400

        self.service.update_story(
            id=dto.id,
            title=dto.title,
            mystery=dto.mystery,
            solution=dto.solution,
            hint=dto.hint,
            is_published=dto.is_published
        )
        logger.info("Story created: title=%s", dto.title)

        return jsonify(
            message=dto.model_dump(),
            status="created"
        ), 201
    

    def post_story(self):
        """
        Create a new story.

        Validates the request body using CreateStoryDTO before passing
        the data to the story service.

        Request Body:
            title: Title of the story.
            mystery: Mystery description of the story.
            solution: Solution to the mystery.
            hint: Hint for solving the mystery.

        Returns:
            201: Story created successfully.
            400: Request body validation failed.
        """
        payload = request.get_json(silent=True) or {}
        try:
            dto = CreateStoryDTO.model_validate(payload)
        except ValidationError as e:
            logger.warning("Story validation failed")
            return jsonify({
                "message": e.errors(),
                "status": "failed",
            }), 400

        self.service.create_story(
            title=dto.title,
            mystery=dto.mystery,
            solution=dto.solution,
            hint=dto.hint,
            is_published=dto.is_published
        )
        logger.info("Story created: title=%s", dto.title)

        return jsonify(
            message=dto.model_dump(),
            status="created"
        ), 201