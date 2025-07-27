import asyncio
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging
from .models import Product, ProductCategory, SupplierPlatform

logger = logging.getLogger(__name__)

class MemoryStorage:
    def __init__(self):
        self.products = {}
        self.counter = 1
        self._load_sample_data()

    def _load_sample_data(self):
        """Load sample product data"""
        sample_products = [
            {
                "id": "product_1",
                "title": "LED Flame Speaker",
                "description": "Portable Bluetooth speaker with realistic LED flame effect",
                "price": 29.99,
                "compare_price": 59.99,
                "currency": "USD",
                "score": 82.5,
                "category": "gadgets",
                "tags": ["gadgets", "home", "gift", "bluetooth"],
                "source_store": "example-store.com",
                "source_url": "https://example-store.com/products/led-flame-speaker",
                "supplier_links": {
                    "aliexpress": "https://aliexpress.com/item/123456",
                    "temu": "https://temu.com/item/789012"
                },
                "supplier_prices": {
                    "aliexpress": 12.50,
                    "temu": 15.00
                },
                "facebook_ads": [
                    {
                        "id": "ad_1",
                        "ad_text": "🔥 This LED Flame Speaker is AMAZING!",
                        "engagement_rate": 0.045,
                        "reach": 10000,
                        "impressions": 15000,
                        "clicks": 450,
                        "spend": 500.00
                    }
                ],
                "tiktok_mentions": [
                    {
                        "id": "video_1",
                        "video_url": "https://tiktok.com/@user/video/123",
                        "description": "This speaker is so cool! 🔥",
                        "views": 50000,
                        "likes": 2500,
                        "shares": 300,
                        "comments": 150
                    }
                ],
                "trend_data": {
                    "keyword": "LED flame speaker",
                    "trend_score": 75
                },
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "id": "product_2",
                "title": "Smart Water Bottle",
                "description": "Hydration tracking water bottle with app connectivity",
                "price": 49.99,
                "compare_price": 79.99,
                "currency": "USD",
                "score": 78.2,
                "category": "fitness",
                "tags": ["fitness", "health", "smart", "hydration"],
                "source_store": "fitness-store.com",
                "source_url": "https://fitness-store.com/products/smart-water-bottle",
                "supplier_links": {
                    "aliexpress": "https://aliexpress.com/item/654321"
                },
                "supplier_prices": {
                    "aliexpress": 25.00
                },
                "facebook_ads": [
                    {
                        "id": "ad_2",
                        "ad_text": "Stay hydrated with this smart water bottle! 💧",
                        "engagement_rate": 0.032,
                        "reach": 8000,
                        "impressions": 12000,
                        "clicks": 256,
                        "spend": 300.00
                    }
                ],
                "tiktok_mentions": [
                    {
                        "id": "video_2",
                        "video_url": "https://tiktok.com/@user/video/456",
                        "description": "My new smart water bottle! 💧",
                        "views": 30000,
                        "likes": 1800,
                        "shares": 200,
                        "comments": 120
                    }
                ],
                "trend_data": {
                    "keyword": "smart water bottle",
                    "trend_score": 65
                },
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "id": "product_3",
                "title": "Portable Car Vacuum Cleaner",
                "description": "Cordless car vacuum with HEPA filter and LED light",
                "price": 39.99,
                "compare_price": 79.99,
                "currency": "USD",
                "score": 85.1,
                "category": "automotive",
                "tags": ["car", "vacuum", "portable", "cleaning"],
                "source_store": "auto-store.com",
                "source_url": "https://auto-store.com/products/car-vacuum",
                "supplier_links": {
                    "aliexpress": "https://aliexpress.com/item/789123"
                },
                "supplier_prices": {
                    "aliexpress": 18.00
                },
                "facebook_ads": [
                    {
                        "id": "ad_3",
                        "ad_text": "Keep your car spotless with this amazing vacuum! 🚗",
                        "engagement_rate": 0.052,
                        "reach": 12000,
                        "impressions": 18000,
                        "clicks": 624,
                        "spend": 450.00
                    }
                ],
                "tiktok_mentions": [
                    {
                        "id": "video_3",
                        "video_url": "https://tiktok.com/@user/video/789",
                        "description": "Best car vacuum ever! 🚗✨",
                        "views": 75000,
                        "likes": 3800,
                        "shares": 450,
                        "comments": 280
                    }
                ],
                "trend_data": {
                    "keyword": "car vacuum cleaner",
                    "trend_score": 82
                },
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
        ]

        for product_data in sample_products:
            self.products[product_data["id"]] = product_data

    async def get_products(
        self,
        skip: int = 0,
        limit: int = 50,
        category: Optional[str] = None,
        min_score: Optional[float] = None,
        max_price: Optional[float] = None,
        search_term: Optional[str] = None,
        tags: Optional[List[str]] = None,
        store: Optional[str] = None,
        sort_by: str = "score",
        sort_order: int = -1
    ) -> List[Product]:
        """Get products with filtering and pagination"""
        try:
            # Filter products
            filtered_products = list(self.products.values())
            
            if category and category != "all":
                filtered_products = [p for p in filtered_products if p.get('category') == category]
                
            if min_score is not None:
                filtered_products = [p for p in filtered_products if p.get('score', 0) >= min_score]
                
            if max_price is not None:
                filtered_products = [p for p in filtered_products if p.get('price', 0) <= max_price]
                
            if search_term:
                search_lower = search_term.lower()
                filtered_products = [
                    p for p in filtered_products 
                    if search_lower in p.get('title', '').lower() or 
                       search_lower in p.get('description', '').lower()
                ]
                
            if tags:
                filtered_products = [
                    p for p in filtered_products 
                    if any(tag in p.get('tags', []) for tag in tags)
                ]
                
            if store and store != "all":
                filtered_products = [
                    p for p in filtered_products 
                    if p.get('source_store') == store
                ]
            
            # Sort products
            if sort_by == "score":
                filtered_products.sort(key=lambda x: x.get('score', 0), reverse=(sort_order == -1))
            elif sort_by == "price":
                filtered_products.sort(key=lambda x: x.get('price', 0), reverse=(sort_order == -1))
            elif sort_by == "price_high":
                filtered_products.sort(key=lambda x: x.get('price', 0), reverse=True)
            elif sort_by == "trend":
                filtered_products.sort(key=lambda x: x.get('trend_data', {}).get('trend_score', 0), reverse=(sort_order == -1))
            elif sort_by == "newest":
                filtered_products.sort(key=lambda x: x.get('created_at', datetime.min), reverse=(sort_order == -1))
            elif sort_by == "name":
                filtered_products.sort(key=lambda x: x.get('title', ''), reverse=(sort_order == -1))
            
            # Pagination
            paginated_products = filtered_products[skip:skip + limit]
            
            # Convert to Product objects
            products = []
            for product_data in paginated_products:
                try:
                    product = Product(**product_data)
                    products.append(product)
                except Exception as e:
                    logger.error(f"Error creating product object: {e}")
                    continue
            
            logger.info(f"Retrieved {len(products)} products from memory storage")
            return products
            
        except Exception as e:
            logger.error(f"Failed to get products: {e}")
            return []

    async def get_product(self, product_id: str) -> Optional[Product]:
        """Get a product by ID"""
        try:
            product_data = self.products.get(product_id)
            if product_data:
                return Product(**product_data)
            return None
        except Exception as e:
            logger.error(f"Failed to get product {product_id}: {e}")
            return None

    async def get_products_count(self, filter_query: Optional[Dict] = None) -> int:
        """Get total count of products"""
        try:
            return len(self.products)
        except Exception as e:
            logger.error(f"Failed to get products count: {e}")
            return 0

    async def get_categories(self) -> List[str]:
        """Get all unique categories"""
        try:
            categories = set()
            for product in self.products.values():
                if 'category' in product:
                    categories.add(product['category'])
            return sorted(list(categories))
        except Exception as e:
            logger.error(f"Failed to get categories: {e}")
            return []

    async def get_tags(self) -> List[str]:
        """Get all unique tags"""
        try:
            tags = set()
            for product in self.products.values():
                if 'tags' in product:
                    tags.update(product['tags'])
            return sorted(list(tags))
        except Exception as e:
            logger.error(f"Failed to get tags: {e}")
            return []

    async def get_stats(self) -> Dict[str, Any]:
        """Get product statistics"""
        try:
            products = list(self.products.values())
            
            total_products = len(products)
            high_score_count = len([p for p in products if p.get('score', 0) >= 80])
            
            if products:
                avg_score = sum(p.get('score', 0) for p in products) / len(products)
                avg_price = sum(p.get('price', 0) for p in products) / len(products)
            else:
                avg_score = 0
                avg_price = 0
            
            total_facebook_ads = sum(len(p.get('facebook_ads', [])) for p in products)
            total_tiktok_mentions = sum(len(p.get('tiktok_mentions', [])) for p in products)
            
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

# Global memory storage instance
memory_storage = MemoryStorage() 