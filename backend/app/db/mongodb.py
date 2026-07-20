"""MongoDB database connection and lifecycle management."""
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.core.config import settings

_db_client: AsyncIOMotorClient | None = None
_db: AsyncIOMotorDatabase | None = None


async def connect_db():
    """Connect to MongoDB on startup."""
    global _db_client, _db
    _db_client = AsyncIOMotorClient(settings.mongodb_url)
    _db = _db_client[settings.mongodb_db]
    # Verify connection
    await _db.command("ping")
    print("Connected to MongoDB")


async def disconnect_db():
    """Disconnect from MongoDB on shutdown."""
    global _db_client
    if _db_client:
        _db_client.close()
        print("Disconnected from MongoDB")


def get_database() -> AsyncIOMotorDatabase:
    """Get MongoDB database instance."""
    if _db is None:
        raise RuntimeError("Database not initialized. Call connect_db() first.")
    return _db
