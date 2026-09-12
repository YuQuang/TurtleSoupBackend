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
        content = payload.get("content")
        conversation_id = payload.get("conversation_id")

        result = self.service.create_message(
            UUID(user_id) if user_id else None,
            content,
            UUID(conversation_id) if conversation_id else None
        )

        return jsonify(
            message=result,
            status="created"
        ), 201

    def get_messages(self):
        """
        Retrieve messages for a specific conversation.

        Args:
            conversation_id: ID of the conversation for which to retrieve messages.

        Returns:
            200: List of messages for the specified conversation.
            404: Conversation not found.
        """
        conversation_id = request.args.get("conversation_id")

        if not conversation_id:
            return jsonify({"error": "conversation_id is required"}), 400
        
        result = self.service.get_messages(
            UUID(conversation_id) if conversation_id else None
        )

        return jsonify(
            message=result,
            status="created"
        ), 201