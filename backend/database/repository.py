from typing import List, Optional, Dict, Any
from datetime import datetime
import logging
from bson import ObjectId
from .database import get_database
from .models import Product, FacebookAd, TikTokVideo, TrendData, CrawlRequest

logger = logging.getLogger(__name__)

class ProductRepository:
    def __init__(self):
        self.collection_name = "products"

    async def create_product(self, product: Product) -> Product:
        """Create a new product"""
        try:
            db = await get_database()
            collection = db.get_collection(self.collection_name)
            
            # Convert to dict and add MongoDB _id
            product_dict = product.dict()
            product_dict["_id"] = ObjectId()
            product_dict["id"] = str(product_dict["_id"])
            
            # Set timestamps
            now = datetime.utcnow()
            product_dict["created_at"] = now
            product_dict["updated_at"] = now
            
            await collection.insert_one(product_dict)
            logger.info(f"Created product: {product.title}")
            
            return Product(**product_dict)
            
        except Exception as e:
            logger.error(f"Failed to create product: {e}")
            raise

    async def get_product(self, product_id: str) -> Optional[Product]:
        """Get a product by ID"""
        try:
            db = await get_database()
            collection = db.get_collection(self.collection_name)
            
            # Try to find by ObjectId first, then by string id
            try:
                result = await collection.find_one({"_id": ObjectId(product_id)})
            except:
                result = await collection.find_one({"id": product_id})
            
            if result:
                return Product(**result)
            return None
            
        except Exception as e:
            logger.error(f"Failed to get product {product_id}: {e}")
            return None

    async def get_products(
        self,
        skip: int = 0,
        limit: int = 50,
        category: Optional[str] = None,
        min_score: Optional[float] = None,
        max_price: Optional[float] = None,
        search_term: Optional[str] = None,
        tags: Optional[List[str]] = None,
        sort_by: str = "score",
        sort_order: int = -1
    ) -> List[Product]:
        """Get products with filtering and pagination"""
        try:
            db = await get_database()
            collection = db.get_collection(self.collection_name)
            
            # Build filter query
            filter_query = {}
            
            if category and category != "all":
                filter_query["category"] = category
                
            if min_score is not None:
                filter_query["score"] = {"$gte": min_score}
                
            if max_price is not None:
                if "score" in filter_query:
                    filter_query["score"]["$lte"] = max_price
                else:
                    filter_query["price"] = {"$lte": max_price}
                    
            if search_term:
                filter_query["$text"] = {"$search": search_term}
                
            if tags:
                filter_query["tags"] = {"$in": tags}
            
            # Build sort query
            sort_query = [(sort_by, sort_order)]
            
            # Execute query
            cursor = collection.find(filter_query).sort(sort_query).skip(skip).limit(limit)
            products = []
            
            async for doc in cursor:
                products.append(Product(**doc))
                
            logger.info(f"Retrieved {len(products)} products")
            return products
            
        except Exception as e:
            logger.error(f"Failed to get products: {e}")
            return []

    async def update_product(self, product_id: str, update_data: Dict[str, Any]) -> Optional[Product]:
        """Update a product"""
        try:
            db = await get_database()
            collection = db.get_collection(self.collection_name)
            
            # Add updated timestamp
            update_data["updated_at"] = datetime.utcnow()
            
            # Try to find by ObjectId first, then by string id
            try:
                result = await collection.find_one_and_update(
                    {"_id": ObjectId(product_id)},
                    {"$set": update_data},
                    return_document=True
                )
            except:
                result = await collection.find_one_and_update(
                    {"id": product_id},
                    {"$set": update_data},
                    return_document=True
                )
            
            if result:
                logger.info(f"Updated product: {product_id}")
                return Product(**result)
            return None
            
        except Exception as e:
            logger.error(f"Failed to update product {product_id}: {e}")
            return None

    async def delete_product(self, product_id: str) -> bool:
        """Delete a product"""
        try:
            db = await get_database()
            collection = db.get_collection(self.collection_name)
            
            # Try to find by ObjectId first, then by string id
            try:
                result = await collection.delete_one({"_id": ObjectId(product_id)})
            except:
                result = await collection.delete_one({"id": product_id})
            
            if result.deleted_count > 0:
                logger.info(f"Deleted product: {product_id}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Failed to delete product {product_id}: {e}")
            return False

    async def get_products_count(self, filter_query: Optional[Dict] = None) -> int:
        """Get total count of products"""
        try:
            db = await get_database()
            collection = db.get_collection(self.collection_name)
            
            if filter_query is None:
                filter_query = {}
                
            count = await collection.count_documents(filter_query)
            return count
            
        except Exception as e:
            logger.error(f"Failed to get products count: {e}")
            return 0

    async def get_categories(self) -> List[str]:
        """Get all unique categories"""
        try:
            db = await get_database()
            collection = db.get_collection(self.collection_name)
            
            categories = await collection.distinct("category")
            return sorted(categories)
            
        except Exception as e:
            logger.error(f"Failed to get categories: {e}")
            return []

    async def get_tags(self) -> List[str]:
        """Get all unique tags"""
        try:
            db = await get_database()
            collection = db.get_collection(self.collection_name)
            
            tags = await collection.distinct("tags")
            return sorted(tags)
            
        except Exception as e:
            logger.error(f"Failed to get tags: {e}")
            return []

    async def get_stats(self) -> Dict[str, Any]:
        """Get product statistics"""
        try:
            db = await get_database()
            collection = db.get_collection(self.collection_name)
            
            # Total products
            total_products = await collection.count_documents({})
            
            # High score products (score >= 80)
            high_score_count = await collection.count_documents({"score": {"$gte": 80}})
            
            # Average score
            pipeline = [
                {"$group": {"_id": None, "avg_score": {"$avg": "$score"}}}
            ]
            avg_score_result = await collection.aggregate(pipeline).to_list(1)
            avg_score = avg_score_result[0]["avg_score"] if avg_score_result else 0
            
            # Average price
            pipeline = [
                {"$group": {"_id": None, "avg_price": {"$avg": "$price"}}}
            ]
            avg_price_result = await collection.aggregate(pipeline).to_list(1)
            avg_price = avg_price_result[0]["avg_price"] if avg_price_result else 0
            
            # Total Facebook ads
            facebook_ads_count = await collection.aggregate([
                {"$unwind": "$facebook_ads"},
                {"$count": "total"}
            ]).to_list(1)
            total_facebook_ads = facebook_ads_count[0]["total"] if facebook_ads_count else 0
            
            # Total TikTok mentions
            tiktok_mentions_count = await collection.aggregate([
                {"$unwind": "$tiktok_mentions"},
                {"$count": "total"}
            ]).to_list(1)
            total_tiktok_mentions = tiktok_mentions_count[0]["total"] if tiktok_mentions_count else 0
            
            return {
                "total_products": total_products,
                "high_score_products": high_score_count,
                "average_score": round(avg_score, 1),
                "average_price": round(avg_price, 2),
                "total_facebook_ads": total_facebook_ads,
                "total_tiktok_mentions": total_tiktok_mentions
            }
            
        except Exception as e:
            logger.error(f"Failed to get stats: {e}")
            return {
                "total_products": 0,
                "high_score_products": 0,
                "average_score": 0,
                "average_price": 0,
                "total_facebook_ads": 0,
                "total_tiktok_mentions": 0
            }

# Global repository instance
product_repository = ProductRepository() 