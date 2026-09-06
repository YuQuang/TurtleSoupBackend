from dataclasses import dataclass
from uuid import UUID
import datetime

@dataclass(frozen=True, slots=True)
class Message:
	id: UUID | None
	conversation_id: UUID
	user_id: UUID
	content: str
	response: str | None
	error: str | None
	created_at: datetime.datetime | None