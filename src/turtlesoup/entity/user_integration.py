from dataclasses import dataclass
from uuid import UUID
import datetime

@dataclass(frozen=True, slots=True)
class UserIntegration:
	id: UUID | None
	user_id: UUID
	provider: str
	provider_user_id: str
	avater: str
	access_token: str
	refresh_token: str
	token_expires_at: datetime.datetime | None
	created_at: datetime.datetime | None
	updated_at: datetime.datetime | None