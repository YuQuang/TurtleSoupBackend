from uuid import UUID
from flask import jsonify, request

from turtlesoup.logging import get_logger
from turtlesoup.services.message_service import MessageService


logger = get_logger(__name__)


class MessageController:

    def __init__(self, service: MessageService):
        self.service = service

    def post_message(self):
        """
        Create a new message.

        Validates the request body using CreateMessageDTO before passing
        the data to the message service.

        Request Body:
            content: Content of the message.
            conversation_id: ID of the conversation to which the message belongs.

        Returns:
            201: Message created successfully.
            400: Request body validation failed.
        """
        payload = request.get_json(silent=True) or {}

        user_id = payload.get("user_id")
        message = payload.get("message")
        conversation_id = payload.get("conversation_id")

        result = self.service.create_message(
            UUID(user_id) if user_id else None,
            message,
            UUID(conversation_id) if conversation_id else None
        )

        return jsonify(
            message=result,
            status="created"
        ), 201