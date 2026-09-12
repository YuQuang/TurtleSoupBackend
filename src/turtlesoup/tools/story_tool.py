from click import UUID
from langchain.tools import tool
from turtlesoup.services.story_service import StoryService


def create_story_tools(story_service: StoryService):

    @tool
    def get_story(
        story_id: str | None = None,
        title: str | None = None,
    ):
        """
        Search for stories.

        Use this tool when the user wants to find or retrieve stories.
        You can search by story ID or title.
        If no search criteria are provided, return published stories.
        """
        return story_service.get_story(
            story_id=UUID(story_id) if story_id else None,
            title=title,
        )

    @tool
    def get_story_titles():
        """
        Retrieve all story titles & story ID.

        Returns:
            A list of all story titles & story ID.
        """
        return story_service.get_title_and_story_id()

    return [get_story, get_story_titles]