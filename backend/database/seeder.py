import asyncio
import logging
from datetime import datetime, timedelta
from typing import List
import random
from .database import get_database
from .models import Product, ProductCategory, SupplierPlatform
from ..scoring.engine import ScoringEngine

logger = logging.getLogger(__name__)

class DatabaseSeeder:
    def __init__(self):
        self.scoring_engine = ScoringEngine()
        
    async def seed_products(self, count: int = 100):
        """Seed the database with sample products"""
        try:
            db = await get_database()
            collection = db.get_collection("products")
            
            # Check if products already exist
            existing_count = await collection.count_documents({})
            if existing_count > 0:
                logger.info(f"Database already contains {existing_count} products. Skipping seeding.")
                return
            
            logger.info(f"Seeding database with {count} products...")
            
            products = self._generate_sample_products(count)
            
            # Insert products in batches
            batch_size = 50
            for i in range(0, len(products), batch_size):
                batch = products[i:i + batch_size]
                await collection.insert_many([product.dict() for product in batch])
                logger.info(f"Inserted batch {i//batch_size + 1}")
            
            logger.info(f"Successfully seeded {len(products)} products")
            
        except Exception as e:
            logger.error(f"Failed to seed products: {e}")
            raise

    def _generate_sample_products(self, count: int) -> List[Product]:
        """Generate sample product data"""
        products = []
        
        # Sample product templates
        product_templates = [
            {
                "title": "Smart LED Strip Lights",
                "description": "WiFi-enabled LED strip lights with app control and voice assistant compatibility",
                "category": ProductCategory.GADGETS,
                "tags": ["smart home", "led", "wifi", "voice control"],
                "base_price": 29.99,
                "compare_price": 59.99
            },
            {
                "title": "Portable Car Vacuum Cleaner",
                "description": "Cordless car vacuum with HEPA filter and LED light for thorough cleaning",
                "category": ProductCategory.AUTOMOTIVE,
                "tags": ["car", "vacuum", "portable", "cleaning"],
                "base_price": 39.99,
                "compare_price": 79.99
            },
            {
                "title": "Wireless Bluetooth Earbuds",
                "description": "True wireless earbuds with noise cancellation and 24-hour battery life",
                "category": ProductCategory.GADGETS,
                "tags": ["bluetooth", "earbuds", "wireless", "audio"],
                "base_price": 49.99,
                "compare_price": 99.99
            },
            {
                "title": "Smart Water Bottle with Temperature Display",
                "description": "Hydration tracking water bottle with temperature sensor and app connectivity",
                "category": ProductCategory.FITNESS,
                "tags": ["fitness", "hydration", "smart", "health"],
                "base_price": 34.99,
                "compare_price": 69.99
            },
            {
                "title": "LED Flame Speaker",
                "description": "Portable Bluetooth speaker with realistic LED flame effect and 360° sound",
                "category": ProductCategory.GADGETS,
                "tags": ["speaker", "bluetooth", "led", "flame"],
                "base_price": 24.99,
                "compare_price": 49.99
            },
            {
                "title": "Pet Grooming Kit",
                "description": "Complete pet grooming kit with clippers, scissors, and grooming tools",
                "category": ProductCategory.PETS,
                "tags": ["pet", "grooming", "clippers", "tools"],
                "base_price": 44.99,
                "compare_price": 89.99
            },
            {
                "title": "Smart Plant Pot",
                "description": "Self-watering plant pot with soil moisture sensor and app notifications",
                "category": ProductCategory.GARDEN,
                "tags": ["garden", "smart", "plant", "watering"],
                "base_price": 39.99,
                "compare_price": 79.99
            },
            {
                "title": "Portable Massage Gun",
                "description": "Deep tissue massage gun with multiple speed settings and attachments",
                "category": ProductCategory.FITNESS,
                "tags": ["fitness", "massage", "recovery", "therapy"],
                "base_price": 54.99,
                "compare_price": 109.99
            },
            {
                "title": "Smart Mirror with LED Lights",
                "description": "Vanity mirror with adjustable LED lighting and magnification",
                "category": ProductCategory.BEAUTY,
                "tags": ["beauty", "mirror", "led", "vanity"],
                "base_price": 29.99,
                "compare_price": 59.99
            },
            {
                "title": "Kids Educational Tablet",
                "description": "Child-safe tablet with educational apps and parental controls",
                "category": ProductCategory.KIDS,
                "tags": ["kids", "tablet", "educational", "parental control"],
                "base_price": 79.99,
                "compare_price": 159.99
            }
        ]
        
        for i in range(count):
            # Select random template
            template = random.choice(product_templates)
            
            # Generate variations
            product = self._create_product_variation(template, i)
            products.append(product)
        
        return products

    def _create_product_variation(self, template: dict, index: int) -> Product:
        """Create a product variation from template"""
        # Add some randomness to prices
        price_variation = random.uniform(0.8, 1.2)
        base_price = template["base_price"] * price_variation
        compare_price = template["compare_price"] * price_variation
        
        # Generate supplier data
        supplier_links = {}
        supplier_prices = {}
        
        if random.random() > 0.3:  # 70% chance to have AliExpress
            supplier_links[SupplierPlatform.ALIEXPRESS] = f"https://aliexpress.com/item/{random.randint(100000, 999999)}"
            supplier_prices[SupplierPlatform.ALIEXPRESS] = base_price * random.uniform(0.3, 0.6)
        
        if random.random() > 0.5:  # 50% chance to have Temu
            supplier_links[SupplierPlatform.TEMU] = f"https://temu.com/item/{random.randint(100000, 999999)}"
            supplier_prices[SupplierPlatform.TEMU] = base_price * random.uniform(0.4, 0.7)
        
        # Generate social media data
        facebook_ads = self._generate_facebook_ads(template["title"])
        tiktok_mentions = self._generate_tiktok_mentions(template["title"])
        
        # Generate trend data
        trend_data = self._generate_trend_data(template["title"])
        
        # Create product
        product = Product(
            id=f"product_{index + 1}",
            title=template["title"],
            description=template["description"],
            price=round(base_price, 2),
            compare_price=round(compare_price, 2),
            currency="USD",
            score=0,  # Will be calculated by scoring engine
            category=template["category"],
            tags=template["tags"],
            source_store=f"store-{random.randint(1, 10)}.com",
            source_url=f"https://store-{random.randint(1, 10)}.com/products/{index + 1}",
            supplier_links=supplier_links,
            supplier_prices=supplier_prices,
            facebook_ads=facebook_ads,
            tiktok_mentions=tiktok_mentions,
            trend_data=trend_data,
            created_at=datetime.utcnow() - timedelta(days=random.randint(1, 30)),
            updated_at=datetime.utcnow()
        )
        
        # Calculate score
        product.score = self.scoring_engine.calculate_score(product)
        
        return product

    def _generate_facebook_ads(self, product_title: str) -> List[dict]:
        """Generate sample Facebook ads data"""
        ads = []
        num_ads = random.randint(0, 3)
        
        for i in range(num_ads):
            ad_texts = [
                f"🔥 {product_title} is AMAZING! You won't believe this!",
                f"🚀 Limited time offer on {product_title}!",
                f"💯 {product_title} - The best purchase I've ever made!",
                f"⚡ Don't miss out on {product_title}!",
                f"🎉 {product_title} - Game changer!",
            ]
            
            ad = {
                "id": f"ad_{random.randint(1000, 9999)}",
                "ad_text": random.choice(ad_texts),
                "engagement_rate": round(random.uniform(0.02, 0.08), 4),
                "reach": random.randint(5000, 50000),
                "impressions": random.randint(8000, 80000),
                "clicks": random.randint(200, 2000),
                "spend": round(random.uniform(100, 1000), 2),
                "created_at": datetime.utcnow() - timedelta(days=random.randint(1, 14))
            }
            ads.append(ad)
        
        return ads

    def _generate_tiktok_mentions(self, product_title: str) -> List[dict]:
        """Generate sample TikTok mentions data"""
        mentions = []
        num_mentions = random.randint(0, 5)
        
        for i in range(num_mentions):
            descriptions = [
                f"This {product_title} is so cool! 🔥",
                f"Just got my {product_title}! Love it! 💕",
                f"{product_title} review - must have! ⭐",
                f"Best purchase ever - {product_title}! 🎉",
                f"Can't live without my {product_title}! 💯",
            ]
            
            mention = {
                "id": f"video_{random.randint(10000, 99999)}",
                "video_url": f"https://tiktok.com/@user{random.randint(1, 1000)}/video/{random.randint(100000, 999999)}",
                "description": random.choice(descriptions),
                "views": random.randint(10000, 100000),
                "likes": random.randint(500, 5000),
                "shares": random.randint(100, 1000),
                "comments": random.randint(50, 500),
                "hashtags": ["#dropshipping", "#product", "#review"],
                "created_at": datetime.utcnow() - timedelta(days=random.randint(1, 7))
            }
            mentions.append(mention)
        
        return mentions

    def _generate_trend_data(self, product_title: str) -> dict:
        """Generate sample trend data"""
        return {
            "keyword": product_title.lower(),
            "trend_score": random.randint(30, 90),
            "interest_over_time": [
                {"date": "2024-01-01", "value": random.randint(20, 80)},
                {"date": "2024-01-02", "value": random.randint(20, 80)},
                {"date": "2024-01-03", "value": random.randint(20, 80)},
            ],
            "related_queries": [
                f"best {product_title.lower()}",
                f"{product_title.lower()} review",
                f"buy {product_title.lower()}"
            ],
            "geographic_interest": {
                "US": random.randint(50, 100),
                "CA": random.randint(20, 80),
                "UK": random.randint(20, 80),
                "AU": random.randint(20, 80)
            }
        }

async def seed_database():
    """Main function to seed the database"""
    seeder = DatabaseSeeder()
    await seeder.seed_products(100)

if __name__ == "__main__":
    asyncio.run(seed_database()) 