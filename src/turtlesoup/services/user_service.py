from turtlesoup.entity.user import User
from turtlesoup.repository.user_integration_repository import UserIntegrationRepository
from turtlesoup.repository.user_repository import UserRepository
from turtlesoup.logging import get_logger


logger = get_logger(__name__)


class UserService:

    def __init__(
        self,
        user_repository: UserRepository,
        user_integration_repository: UserIntegrationRepository
    ) -> None:
        self.user_repository = user_repository
        self.user_integration_repository = user_integration_repository

    def check_user_email_exist(
        self,
        email: str,
    ) -> bool:
        user = self.user_repository.get_by_user_email(
            email
        )
        if user == None: return False
        else: return True


    def get_user_by_provider_id(
        self,
        provider_id: str
    ) -> User | None:
        user = self.user_integration_repository.get_by_provider_id(provider_id)
        if user == None: return None
        return self.user_repository.get_by_user_id(user.user_id)
        


    def create_user(
        self,
        user_name: str,
        email: str,
        user_password: str | None
    ) -> User:
        user = self.user_repository.create_user(User(
            None,
            user_name,
            user_password,
            email,
            None,
            None
        ))
        return user