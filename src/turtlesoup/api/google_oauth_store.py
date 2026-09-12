import time
from dataclasses import dataclass

@dataclass
class OAuthSession:
    code_verifier: str
    expires_at: float


oauth_sessions: dict[str, OAuthSession] = {}

OAUTH_SESSION_TTL = 5 * 60  # 5 minutes