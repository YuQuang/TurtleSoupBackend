from __future__ import annotations

from typing import Any, LiteralString, cast
from turtlesoup.entity.user_integration import UserIntegration

from uuid import UUID

from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool
from turtlesoup.logging import get_logger


logger = get_logger(__name__)
_UNSET = object()


class UserIntegrationRepository:
	def __init__(self, pool: ConnectionPool) -> None:
		self._pool = pool

	def create(
		self,
		user_integration: UserIntegration,
	) -> UserIntegration:
		logger.debug("Creating user integration: provider_user_id=%s", user_integration.provider_user_id)
		query = """
			INSERT INTO user_integrations (
				user_id, provider, provider_user_id, avater,
				access_token, refresh_token, token_expires_at
			)
			VALUES (%s, %s, %s, %s, %s, %s, %s)
			RETURNING id, user_id, provider, provider_user_id, avater,
					  access_token, refresh_token, token_expires_at,
					  created_at, updated_at
		"""
		with self._pool.connection() as connection:
			with connection.cursor(row_factory=dict_row) as cursor:
				cursor.execute(
					query,
					(
						user_integration.user_id,
						user_integration.provider,
						user_integration.provider_user_id,
						user_integration.avater,
						user_integration.access_token,
						user_integration.refresh_token,
						user_integration.token_expires_at,
					),
				)
				row = cursor.fetchone()
				if row is None:
					raise RuntimeError("Creating user integration returned no row")
				return self._to_user_integration(row)

	def get_by_provider_id(self, provider_id: str) -> UserIntegration | None:
		logger.debug("Fetching user integration: provider_id=%s", provider_id)
		query = """
			SELECT id, user_id, provider, provider_user_id, avater,
				   access_token, refresh_token, token_expires_at,
				   created_at, updated_at
			FROM user_integrations
			WHERE provider_user_id = %s
		"""
		with self._pool.connection() as connection:
			with connection.cursor(row_factory=dict_row) as cursor:
				cursor.execute(query, (provider_id,))
				row = cursor.fetchone()
				return self._to_user_integration(row) if row else None

	def get_by_user_id(self, user_id: UUID) -> UserIntegration | None:
		logger.debug("Fetching user integration: user_id=%s", user_id)
		query = """
			SELECT id, user_id, provider, provider_user_id, avater,
				   access_token, refresh_token, token_expires_at,
				   created_at, updated_at
			FROM user_integrations
			WHERE user_id = %s
		"""
		with self._pool.connection() as connection:
			with connection.cursor(row_factory=dict_row) as cursor:
				cursor.execute(query, (user_id,))
				row = cursor.fetchone()
				return self._to_user_integration(row) if row else None

	def update(self, user_integration: UserIntegration) -> UserIntegration | None:
		logger.debug("Updating user integration: id=%s", user_integration.id)
		query = """
			UPDATE user_integrations
			SET user_id = %s,
				provider = %s,
				provider_user_id = %s,
				avater = %s,
				access_token = %s,
				refresh_token = %s,
				token_expires_at = %s,
				updated_at = CURRENT_TIMESTAMP
			WHERE id = %s
			RETURNING id, user_id, provider, provider_user_id, avater,
					  access_token, refresh_token, token_expires_at,
					  created_at, updated_at
		"""
		with self._pool.connection() as connection:
			with connection.cursor(row_factory=dict_row) as cursor:
				cursor.execute(
					query,
					(
						user_integration.user_id,
						user_integration.provider,
						user_integration.provider_user_id,
						user_integration.avater,
						user_integration.access_token,
						user_integration.refresh_token,
						user_integration.token_expires_at,
						user_integration.id,
					),
				)
				row = cursor.fetchone()
				return self._to_user_integration(row) if row else None

	def partial_update(
		self,
		provider_user_id: str,
		*,
		user_id: UUID | object = _UNSET,
		provider: str | object = _UNSET,
		avater: str | None | object = _UNSET,
		access_token: str | None | object = _UNSET,
		refresh_token: str | None | object = _UNSET,
		token_expires_at: object = _UNSET,
	) -> UserIntegration | None:
		updates = (
			("user_id", user_id),
			("provider", provider),
			("avater", avater),
			("access_token", access_token),
			("refresh_token", refresh_token),
			("token_expires_at", token_expires_at),
		)
		fields = [(field, value) for field, value in updates if value is not _UNSET]
		if not fields:
			raise ValueError("partial_update requires at least one field")

		logger.debug("Partially updating user integration: provider_user_id=%s", provider_user_id)
		set_clause = ", ".join(f"{field} = %s" for field, _ in fields)
		query = cast(LiteralString, f"""
			UPDATE user_integrations
			SET {set_clause}, updated_at = CURRENT_TIMESTAMP
			WHERE provider_user_id = %s
			RETURNING id, user_id, provider, provider_user_id, avater,
					  access_token, refresh_token, token_expires_at,
					  created_at, updated_at
		""")
		with self._pool.connection() as connection:
			with connection.cursor(row_factory=dict_row) as cursor:
				cursor.execute(query, [value for _, value in fields] + [provider_user_id])
				row = cursor.fetchone()
				return self._to_user_integration(row) if row else None

	@staticmethod
	def _to_user_integration(row: dict[str, Any]) -> UserIntegration:
		return UserIntegration(
			id=row["id"],
			user_id=row["user_id"],
			provider=row["provider"],
			provider_user_id=row["provider_user_id"],
			avater=row["avater"],
			access_token=row["access_token"],
			refresh_token=row["refresh_token"],
			token_expires_at=row["token_expires_at"],
			created_at=row["created_at"],
			updated_at=row["updated_at"],
		)
