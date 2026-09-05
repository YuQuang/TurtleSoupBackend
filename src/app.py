from dotenv import load_dotenv
from turtlesoup import create_app
from turtlesoup.logging import get_logger


logger = get_logger(__name__)

load_dotenv()
logger.info("Starting Turtlesoup application")
app = create_app()

if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )