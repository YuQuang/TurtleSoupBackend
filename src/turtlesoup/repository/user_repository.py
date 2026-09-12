from __future__ import annotations
from uuid import UUID

from turtlesoup.entity.user import User

from typing import Any

from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool
from turtlesoup.logging import get_logger


logger = get_logger(__name__)


class UserRepository:
	def __init__(self, pool: ConnectionPool) -> None:
		self._pool = pool

	def create_user(self, user: User) -> User:
		logger.debug("Creating user: email=%s", user.email)
		query = """
			INSERT INTO users (user_name, user_password, email)
			VALUES (%s, %s, %s)
			RETURNING user_id, user_name, user_password, email,
					  created_at, last_login
		"""
		with self._pool.connection() as connection:
			with connection.cursor(row_factory=dict_row) as cursor:
				cursor.execute(query, (user.user_name, user.user_password, user.email))
				row = cursor.fetchone()
				if row is None:
					raise RuntimeError("Creating user returned no row")
				return self._to_user(row)

	def get_by_user_email(self, email: str) -> User | None:
		logger.debug("Fetching user: email=%s", email)
		query = """
			SELECT user_id, user_name, user_password, email,
				   created_at, last_login
			FROM users
			WHERE email = %s
		"""
		with self._pool.connection() as connection:
			with connection.cursor(row_factory=dict_row) as cursor:
				cursor.execute(query, (email,))
				row = cursor.fetchone()
				return self._to_user(row) if row else None

	def get_by_user_id(self, user_id: UUID) -> User | None:
		logger.debug("Fetching user: user_id=%s", user_id)
		query = """
			SELECT user_id, user_name, user_password, email,
				   created_at, last_login
			FROM users
			WHERE user_id = %s
		"""
		with self._pool.connection() as connection:
			with connection.cursor(row_factory=dict_row) as cursor:
				cursor.execute(query, (user_id,))
				row = cursor.fetchone()
				return self._to_user(row) if row else None

	@staticmethod
	def _to_user(row: dict[str, Any]) -> User:
		return User(
			user_id=row["user_id"],
			user_name=row["user_name"],
			user_password=row["user_password"],
			email=row["email"],
			created_at=row["created_at"],
			last_login=row["last_login"],
		)
