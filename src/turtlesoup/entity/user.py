from dataclasses import dataclass
from uuid import UUID
import datetime

@dataclass(frozen=True, slots=True)
class User:
	user_id: UUID | None
	user_name: str
	user_password: str | None
	email: str
	created_at: datetime.datetime | None
	last_login: datetime.datetime | None
	