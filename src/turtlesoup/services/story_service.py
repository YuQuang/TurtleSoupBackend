from uuid import UUID

from turtlesoup.entity.story import Story

from turtlesoup.logging import get_logger
from turtlesoup.repository.story_repository import StoryRepository


logger = get_logger(__name__)


class StoryService:
    def __init__(
            self,
            story_repository: StoryRepository
        ):
        self.story_repository = story_repository

    def get_story(
        self,
        story_id: UUID | None,
        title: str | None
    ) -> list[Story] | None:
        """
        Retrieve stories based on the provided search criteria.

        The search priority is:
        1. Search by story ID if provided.
        2. Search by title if provided.
        3. Return all published stories when no criteria are provided.

        Args:
            story_id: UUID of the story to retrieve.
            title: Title of the story to search for.

        Returns:
            A single Story when searching by ID, a list of stories when
            searching by title or without search criteria, or None when
            no matching story is found.
        """
        logger.info("Fetching story: id=%s, title=%s", story_id, title)

        if story_id: return self.story_repository.get_by_id(story_id)
        if title: return self.story_repository.get_by_title(title)

        return self.story_repository.list_published()

    def create_story(self, title: str, mystery: str, solution: str, hint: str, is_published: bool = False) -> Story | None:
        """
        Create a new unpublished story.

        Args:
            title: Title of the story.
            mystery: Mystery description of the story.
            solution: Solution to the mystery.
            hint: Hint provided to help solve the mystery.
            is_published: Flag indicating whether the story should be published.

        Returns:
            The newly created Story, or None if creation fails.
        """
        logger.info("Creating story: title=%s", title)
        story = Story(
            id=None,
            title=title,
            mystery=mystery,
            solution=solution,
            hint=hint,
            is_published=is_published,
            created_at=None,
            updated_at=None
        )
        return self.story_repository.create(story)