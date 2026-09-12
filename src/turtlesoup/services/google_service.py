from uuid import UUID

from turtlesoup.entity.user_integration import UserIntegration
from turtlesoup.logging import get_logger
from turtlesoup.repository.user_integration_repository import UserIntegrationRepository


logger = get_logger(__name__)


class GoogleService:

    def __init__(
        self,
        user_integration_repository: UserIntegrationRepository
    ) -> None:
        self.user_integration_repository = user_integration_repository

    def check_user_integration(
        self,
        provider_id: str,
    ) -> bool:
        user_integration = self.user_integration_repository.get_by_provider_id(
            provider_id
        )
        if user_integration == None: return False
        else: return True

    def create_integration(
        self,
        user_id: UUID,
        provider: str,
        provider_user_id: str,
        access_token: str,
        refresh_token: str,
        avater: str
    ) -> None:
        self.user_integration_repository.create(
            UserIntegration(
                None,
                user_id,
                provider,
                provider_user_id,
                avater,
                access_token,
                refresh_token,
                None,
                None,
                None
            )
        )

    def partial_update_integration(
            self,
            provider_user_id: str,
            access_token: str,
            refresh_token: str,
            avater: str
        ) -> None:
            self.user_integration_repository.partial_update(
                provider_user_id=provider_user_id,
                access_token=access_token,
                refresh_token=refresh_token,
                avater=avater
            )
        