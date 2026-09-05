from __future__ import annotations

import os

from dotenv import load_dotenv
from psycopg.conninfo import make_conninfo
from psycopg_pool import ConnectionPool


load_dotenv()


def _connection_info() -> str:
	database_url = os.getenv("DATABASE_URL")
	if database_url:
		return database_url

	required_variables = {
		"host": os.getenv("DB_HOST"),
		"port": os.getenv("DB_PORT", "5432"),
		"dbname": os.getenv("DB_NAME"),
		"user": os.getenv("DB_USER"),
		"password": os.getenv("DB_PASSWORD"),
	}
	missing_variables = [
		name for name, value in required_variables.items()
		if value is None and name != "port"
	]
	if missing_variables:
		missing = ", ".join(f"DB_{name.upper()}" for name in missing_variables)
		raise RuntimeError(
			f"PostgreSQL configuration is missing: {missing}. "
			"Set DATABASE_URL or the DB_* variables in .env."
		)

	return make_conninfo(**required_variables)


def create_connection_pool() -> ConnectionPool:
	return ConnectionPool(
		conninfo=_connection_info(),
		min_size=int(os.getenv("DB_POOL_MIN_SIZE", "1")),
		max_size=int(os.getenv("DB_POOL_MAX_SIZE", "10")),
		open=True,
	)
