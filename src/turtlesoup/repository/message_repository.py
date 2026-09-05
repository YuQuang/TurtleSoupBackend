from __future__ import annotations

from turtlesoup.entity.message import Message

from typing import Any
from uuid import UUID

from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool
from turtlesoup.logging import get_logger


logger = get_logger(__name__)


class MessageRepository:
	def __init__(self, pool: ConnectionPool) -> None:
		self._pool = pool

	def create(
		self,
		message: Message,
	) -> Message | None:
		logger.debug("Creating message: content=%s", message.content)
		query = """
			INSERT INTO messages (conversation_id, user_id, content, response, error)
			VALUES (%s, %s, %s, %s, %s)
			RETURNING id, conversation_id, user_id, content, response, error, created_at
		"""
		with self._pool.connection() as connection:
			with connection.cursor(row_factory=dict_row) as cursor:
				cursor.execute(
					query,
					(message.conversation_id, message.user_id, message.content, message.response, message.error),
				)
				return self._to_message(cursor.fetchone()) # type: ignore

	def get_by_conversation_id(self, conversation_id: UUID) -> list[Message]:
		logger.debug("Fetching messages for conversation: id=%s", conversation_id)
		query = """
			SELECT id, conversation_id, user_id, content, response, error, created_at
			FROM messages
			WHERE conversation_id = %s
		"""
		with self._pool.connection() as connection:
			with connection.cursor(row_factory=dict_row) as cursor:
				cursor.execute(query, (conversation_id,))
				rows = cursor.fetchall()
				return [self._to_message(row) for row in rows] # type: ignore

	@staticmethod
	def _to_message(row: dict[str, Any]) -> Message | None:
		if row is None: return None
		return Message(
			id=row["id"],
			conversation_id=row["conversation_id"],
			user_id=row["user_id"],
			content=row["content"],
			response=row.get("response", None),
			error=row.get("error", None),
			created_at=row["created_at"],
		)
