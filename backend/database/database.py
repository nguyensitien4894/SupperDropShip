import os
import motor.motor_asyncio
from pymongo import MongoClient
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.client: Optional[MotorClient] = None
        self.db = None
        self.is_connected = False

    async def connect(self):
        """Connect to MongoDB database"""
        try:
            # Get MongoDB connection string from environment
            mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
            database_name = os.getenv("MONGODB_DB", "dropship_intelligence")
            
            # Create async motor client
            self.client = motor.motor_asyncio.AsyncIOMotorClient(mongo_uri)
            self.db = self.client[database_name]
            
            # Test connection
            await self.client.admin.command('ping')
            self.is_connected = True
            
            logger.info(f"Connected to MongoDB database: {database_name}")
            
            # Create indexes for better performance
            await self._create_indexes()
            
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            self.is_connected = False
            raise

    async def disconnect(self):
        """Disconnect from MongoDB database"""
        if self.client:
            self.client.close()
            self.is_connected = False
            logger.info("Disconnected from MongoDB")

    async def _create_indexes(self):
        """Create database indexes for better performance"""
        try:
            # Products collection indexes
            products_collection = self.db.products
            
            # Create indexes
            await products_collection.create_index("score", -1)  # Descending score
            await products_collection.create_index("category", 1)  # Category
            await products_collection.create_index("price", 1)  # Price
            await products_collection.create_index("created_at", -1)  # Created date
            await products_collection.create_index("tags", 1)  # Tags
            await products_collection.create_index("source_store", 1)  # Source store
            
            # Text search index
            await products_collection.create_index([
                ("title", "text"),
                ("description", "text"),
                ("tags", "text")
            ])
            
            # Facebook ads collection indexes
            facebook_ads_collection = self.db.facebook_ads
            await facebook_ads_collection.create_index("product_id", 1)
            await facebook_ads_collection.create_index("created_at", -1)
            
            # TikTok mentions collection indexes
            tiktok_mentions_collection = self.db.tiktok_mentions
            await tiktok_mentions_collection.create_index("product_id", 1)
            await tiktok_mentions_collection.create_index("created_at", -1)
            
            # Trends collection indexes
            trends_collection = self.db.trends
            await trends_collection.create_index("keyword", 1)
            await trends_collection.create_index("created_at", -1)
            
            logger.info("Database indexes created successfully")
            
        except Exception as e:
            logger.error(f"Failed to create indexes: {e}")

    def get_collection(self, collection_name: str):
        """Get a database collection"""
        if not self.is_connected:
            raise Exception("Database not connected")
        return self.db[collection_name]

# Global database instance
db = Database()

async def get_database() -> Database:
    """Get database instance"""
    if not db.is_connected:
        await db.connect()
    return db 