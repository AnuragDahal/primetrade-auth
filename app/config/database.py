from motor.motor_asyncio import AsyncIOMotorClient
from app.config.settings import settings


client = AsyncIOMotorClient(settings.MONGO_URI)

db = client["auth-system"]

user_collection = db["users"]
notes_collection = db["notes"]
