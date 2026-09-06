from dataclasses import dataclass
from uuid_utils import UUID
import datetime

@dataclass(frozen=True, slots=True)
class Story:
	id: UUID | None
	title: str
	mystery: str
	solution: str
	hint: str | None
	is_published: bool
	created_at: datetime.datetime | None
	updated_at: datetime.datetime | None