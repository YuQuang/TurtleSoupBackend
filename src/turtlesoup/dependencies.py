from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

from psycopg_pool import ConnectionPool

from turtlesoup.api.message_controller import MessageController
from turtlesoup.api.story_controller import StoryController

from turtlesoup.services.message_service import MessageService
from turtlesoup.services.story_service import StoryService

from turtlesoup.repository.story_repository import StoryRepository
from turtlesoup.repository.message_repository import MessageRepository
from turtlesoup.tools.story_tool import create_story_tools


def create_dependencies(
    connection_pool: ConnectionPool,
):
    story_repository = StoryRepository(connection_pool)
    story_service = StoryService(story_repository)
    story_controller = StoryController(story_service)


    story_tools = create_story_tools(story_service)
    checkpointer = InMemorySaver()
    agent = create_agent(
        model="google_genai:gemini-3.5-flash-lite",
        tools=story_tools,
        system_prompt="""
        你是海龜湯主持人
        請根據使用者給予的指令，去查詢故事資料庫，
        以海龜湯的形式，提供給使用者一個謎題故事。
        在回覆上給予是、否、無關的回答，
        最後使用者猜對時，提供完整的故事解答。
        """,
        checkpointer=checkpointer
    )
    message_repository = MessageRepository(connection_pool)
    message_service = MessageService(agent, message_repository)
    message_controller = MessageController(message_service)

    return {
        "story_controller": story_controller,
        "message_controller": message_controller,
    }