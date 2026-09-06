
from uuid import UUID

from turtlesoup.logging import get_logger
from turtlesoup.entity.message import Message
from turtlesoup.repository.message_repository import MessageRepository


logger = get_logger(__name__)


class MessageService:

    def __init__(
        self,
        agent,
        message_repository: MessageRepository
    ) -> None:
        self.agent = agent
        self.message_repository = message_repository


    def create_message(
        self,
        user_id: UUID | None,
        message: str | None,
        conversation_id: UUID | None
    ) -> str:
        if user_id is None or message is None or conversation_id is None:
            raise ValueError("User ID, message, and conversation_id must be provided.")
        
        result = self.agent.invoke(
            {
                "messages": [
                    {"role": "user", "content": message}
                ]
            },
            config = {
                "configurable": {
                    "thread_id": conversation_id
                }
            }
        )

        response = result["messages"][-1].content

        logger.info("response: %s", response)
        self.message_repository.create(Message(
            id=None,
            user_id=user_id,
            content=message,
            conversation_id=conversation_id,
            response=response[0]["text"] if response else None,
            error=None,
            created_at=None
        ))

        return response

    def get_messages(
            self,
            conversation_id: UUID | None
        ) -> list[Message]:
        if conversation_id is None:
            raise ValueError("conversation_id must be provided.")
        return self.message_repository.get_by_conversation_id(conversation_id)