from motor.motor_asyncio import AsyncIOMotorClient
from config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MongoDB:
    def __init__(self):
        self.client = None

    async def connect(self):
        self.client = AsyncIOMotorClient(settings.MONGO_URI)
        logger.info(" Connected to database cluster.")

    async def close(self):
        self.client.close()
        logger.info("Disconnected from database cluster.")


db_client = MongoDB()


async def get_mdb():
    return db_client.client
