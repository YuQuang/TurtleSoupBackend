from __future__ import annotations

from turtlesoup.entity.story import Story

from typing import Any
from uuid import UUID

from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool
from turtlesoup.logging import get_logger


logger = get_logger(__name__)


class StoryRepository:
	def __init__(self, pool: ConnectionPool) -> None:
		self._pool = pool

	def create(
		self,
		story: Story,
	) -> Story | None:
		logger.debug("Creating story: title=%s", story.title)
		query = """
			INSERT INTO stories (title, mystery, solution, hint, is_published)
			VALUES (%s, %s, %s, %s, %s)
			RETURNING id, title, mystery, solution, hint, is_published,
					  created_at, updated_at
		"""
		with self._pool.connection() as connection:
			with connection.cursor(row_factory=dict_row) as cursor:
				cursor.execute(
					query,
					(story.title, story.mystery, story.solution, story.hint, story.is_published),
				)
				return self._to_story(cursor.fetchone()) # type: ignore

	def get_by_id(self, story_id: UUID) -> list[Story]:
		logger.debug("Fetching story: id=%s", story_id)
		query = """
			SELECT id, title, mystery, solution, hint, is_published,
				   created_at, updated_at
			FROM stories
			WHERE id = %s
		"""
		with self._pool.connection() as connection:
			with connection.cursor(row_factory=dict_row) as cursor:
				cursor.execute(query, (story_id,))
				row = cursor.fetchone()
				return [self._to_story(row)] # type: ignore

	def get_by_title(self, title: str) -> list[Story]:
		logger.debug("Fetching story: title=%s", title)
		query = """
			SELECT id, title, mystery, solution, hint, is_published,
				   created_at, updated_at
			FROM stories
			WHERE title LIKE %s
		"""
		with self._pool.connection() as connection:
			with connection.cursor(row_factory=dict_row) as cursor:
				cursor.execute(query, (f"%{title}%",))
				rows = cursor.fetchall()
				return [self._to_story(row) for row in rows] # type: ignore

	def get_stories(self, *, limit: int = 20, offset: int = 0) -> list[Story]:
		if limit < 1 or limit > 100:
			logger.warning("Invalid story list limit: %s", limit)
			raise ValueError("limit must be between 1 and 100")
		if offset < 0:
			logger.warning("Invalid story list offset: %s", offset)
			raise ValueError("offset must be non-negative")

		query = """
			SELECT id, title, mystery, solution, hint, is_published,
				   created_at, updated_at
			FROM stories
			ORDER BY created_at DESC
			LIMIT %s OFFSET %s
		"""
		with self._pool.connection() as connection:
			with connection.cursor(row_factory=dict_row) as cursor:
				cursor.execute(query, (limit, offset))
				return [self._to_story(row) for row in cursor.fetchall()] # type: ignore

	def get_title_and_story_id(self) -> list[dict[str,str]]:
		logger.debug("Fetching all story titles")
		query = """
			SELECT title, id
			FROM stories
		"""
		with self._pool.connection() as connection:
			with connection.cursor(row_factory=dict_row) as cursor:
				cursor.execute(query)
				rows = cursor.fetchall()
				return [row for row in rows]

	def update(
		self,
		story_id: UUID,
		*,
		story: Story,
	) -> Story | None:
		logger.debug("Updating story: id=%s", story_id)
		query = """
			UPDATE stories
			SET title = %s,
				mystery = %s,
				solution = %s,
				hint = %s,
				is_published = %s,
				updated_at = NOW()
			WHERE id = %s
			RETURNING id, title, mystery, solution, hint, is_published,
					  created_at, updated_at
		"""
		with self._pool.connection() as connection:
			with connection.cursor(row_factory=dict_row) as cursor:
				cursor.execute(
					query,
					(story.title, story.mystery, story.solution, story.hint, story.is_published, story_id),
				)
				row = cursor.fetchone()
				return self._to_story(row) if row else None

	def delete(self, story_id: UUID) -> bool:
		logger.debug("Deleting story: id=%s", story_id)
		with self._pool.connection() as connection:
			with connection.cursor() as cursor:
				cursor.execute("DELETE FROM stories WHERE id = %s", (story_id,))
				return cursor.rowcount == 1

	@staticmethod
	def _to_story(row: dict[str, Any]) -> Story | None:
		if row is None: return None
		return Story(
			id=row["id"],
			title=row["title"],
			mystery=row["mystery"],
			solution=row["solution"],
			hint=row["hint"],
			is_published=row["is_published"],
			created_at=row["created_at"],
			updated_at=row["updated_at"],
		)
