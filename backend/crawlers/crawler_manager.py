import asyncio
import logging
from typing import List, Dict, Any
from datetime import datetime
import random

from .shopify_crawler import ShopifyCrawler
from .general_crawler import GeneralCrawler
from database.memory_storage import memory_storage
from ..database.models import Product

logger = logging.getLogger(__name__)

class CrawlerManager:
    def __init__(self):
        self.shopify_crawler = None
        self.general_crawler = None
        
    async def __aenter__(self):
        self.shopify_crawler = ShopifyCrawler()
        self.general_crawler = GeneralCrawler()
        await self.shopify_crawler.__aenter__()
        await self.general_crawler.__aenter__()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.shopify_crawler:
            await self.shopify_crawler.__aexit__(exc_type, exc_val, exc_tb)
        if self.general_crawler:
            await self.general_crawler.__aexit__(exc_type, exc_val, exc_tb)

    async def crawl_all_sources(self, max_products_per_source: int = 30) -> List[Dict[str, Any]]:
        """Crawl all available sources and return combined products"""
        all_products = []
        
        logger.info("Starting comprehensive REAL product crawl from all sources...")
        
        # 1. Crawl general platforms (AliExpress, Temu, Amazon) - REAL PRODUCTS
        try:
            logger.info("Crawling real e-commerce platforms for actual products...")
            general_products = await self.general_crawler.crawl_all_platforms(max_products_per_source)
            all_products.extend(general_products)
            logger.info(f"Added {len(general_products)} REAL products from e-commerce platforms")
        except Exception as e:
            logger.error(f"Error crawling general platforms: {e}")
        
        # 2. Crawl Shopify stores (if we have specific store URLs)
        try:
            logger.info("Crawling Shopify stores for real products...")
            # Use real Shopify store URLs
            store_urls = [
                'https://www.oberlo.com/blog/shopify-stores',
                'https://www.shopify.com/partners/shopify-stores'
            ]
            shopify_products = await self.shopify_crawler.crawl_multiple_stores(store_urls, max_products_per_source)
            all_products.extend(shopify_products)
            logger.info(f"Added {len(shopify_products)} products from Shopify stores")
        except Exception as e:
            logger.error(f"Error crawling Shopify stores: {e}")
        
        # 3. Generate minimal mock products only if we don't have enough real products
        if len(all_products) < 10:
            try:
                logger.info(f"Only {len(all_products)} real products found. Generating minimal mock products for variety...")
                mock_products = self._generate_mock_products(min(5, max_products_per_source - len(all_products)))
                all_products.extend(mock_products)
                logger.info(f"Added {len(mock_products)} mock products as backup")
            except Exception as e:
                logger.error(f"Error generating mock products: {e}")
        else:
            logger.info(f"Sufficient real products found ({len(all_products)}). Skipping mock generation.")
        
        logger.info(f"Total products crawled: {len(all_products)} (Real: {len([p for p in all_products if not p['id'].startswith('mock_')])}, Mock: {len([p for p in all_products if p['id'].startswith('mock_')])})")
        return all_products

    def _generate_mock_products(self, count: int) -> List[Dict[str, Any]]:
        """Generate additional mock products for variety"""
        products = []
        
        product_templates = [
            {
                'title': 'Smart LED Strip Lights',
                'description': 'WiFi-enabled LED strip lights with app control and voice assistant compatibility',
                'category': 'gadgets',
                'tags': ['smart home', 'led', 'wifi', 'voice control'],
                'base_price': 29.99,
                'compare_price': 59.99
            },
            {
                'title': 'Portable Car Vacuum Cleaner',
                'description': 'Cordless car vacuum with HEPA filter and LED light for thorough cleaning',
                'category': 'automotive',
                'tags': ['car', 'vacuum', 'portable', 'cleaning'],
                'base_price': 39.99,
                'compare_price': 79.99
            },
            {
                'title': 'Wireless Bluetooth Earbuds',
                'description': 'True wireless earbuds with noise cancellation and 24-hour battery life',
                'category': 'gadgets',
                'tags': ['bluetooth', 'earbuds', 'wireless', 'audio'],
                'base_price': 49.99,
                'compare_price': 99.99
            },
            {
                'title': 'Smart Water Bottle with Temperature Display',
                'description': 'Hydration tracking water bottle with temperature sensor and app connectivity',
                'category': 'fitness',
                'tags': ['fitness', 'hydration', 'smart', 'health'],
                'base_price': 34.99,
                'compare_price': 69.99
            },
            {
                'title': 'LED Flame Speaker',
                'description': 'Portable Bluetooth speaker with realistic LED flame effect and 360° sound',
                'category': 'gadgets',
                'tags': ['speaker', 'bluetooth', 'led', 'flame'],
                'base_price': 24.99,
                'compare_price': 49.99
            },
            {
                'title': 'Pet Grooming Kit',
                'description': 'Complete pet grooming kit with clippers, scissors, and grooming tools',
                'category': 'pets',
                'tags': ['pet', 'grooming', 'clippers', 'tools'],
                'base_price': 44.99,
                'compare_price': 89.99
            },
            {
                'title': 'Smart Plant Pot',
                'description': 'Self-watering plant pot with soil moisture sensor and app notifications',
                'category': 'garden',
                'tags': ['garden', 'smart', 'plant', 'watering'],
                'base_price': 39.99,
                'compare_price': 79.99
            },
            {
                'title': 'Portable Massage Gun',
                'description': 'Deep tissue massage gun with multiple speed settings and attachments',
                'category': 'fitness',
                'tags': ['fitness', 'massage', 'recovery', 'therapy'],
                'base_price': 54.99,
                'compare_price': 109.99
            },
            {
                'title': 'Smart Mirror with LED Lights',
                'description': 'Vanity mirror with adjustable LED lighting and magnification',
                'category': 'beauty',
                'tags': ['beauty', 'mirror', 'led', 'vanity'],
                'base_price': 29.99,
                'compare_price': 59.99
            },
            {
                'title': 'Kids Educational Tablet',
                'description': 'Child-safe tablet with educational apps and parental controls',
                'category': 'kids',
                'tags': ['kids', 'tablet', 'educational', 'parental control'],
                'base_price': 79.99,
                'compare_price': 159.99
            }
        ]
        
        for i in range(count):
            template = random.choice(product_templates)
            product = self._create_product_variation(template, i)
            products.append(product)
        
        return products

    def _create_product_variation(self, template: Dict[str, Any], index: int) -> Dict[str, Any]:
        """Create a product variation from template"""
        price_variation = random.uniform(0.8, 1.2)
        base_price = template['base_price'] * price_variation
        compare_price = template['compare_price'] * price_variation
        
        supplier_links = {}
        supplier_prices = {}
        
        if random.random() > 0.3:
            supplier_links['aliexpress'] = f"https://aliexpress.com/item/{random.randint(100000, 999999)}"
            supplier_prices['aliexpress'] = base_price * random.uniform(0.3, 0.6)
        
        if random.random() > 0.5:
            supplier_links['temu'] = f"https://temu.com/item/{random.randint(100000, 999999)}"
            supplier_prices['temu'] = base_price * random.uniform(0.4, 0.7)
        
        facebook_ads = self._generate_facebook_ads(template['title'])
        tiktok_mentions = self._generate_tiktok_mentions(template['title'])
        trend_data = self._generate_trend_data(template['title'])
        
        product = {
            'id': f"mock_{index + 1}",
            'title': template['title'],
            'description': template['description'],
            'price': round(base_price, 2),
            'compare_price': round(compare_price, 2),
            'currency': 'USD',
            'score': self._calculate_score(base_price, template['title']),
            'category': template['category'],
            'tags': template['tags'],
            'source_store': f"mock-store-{random.randint(1, 10)}.com",
            'source_url': f"https://mock-store-{random.randint(1, 10)}.com/products/{index + 1}",
            'supplier_links': supplier_links,
            'supplier_prices': supplier_prices,
            'facebook_ads': facebook_ads,
            'tiktok_mentions': tiktok_mentions,
            'trend_data': trend_data,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        return product

    def _calculate_score(self, price: float, title: str) -> float:
        """Calculate product score"""
        score = 50.0
        
        # Price factor
        if 10 <= price <= 100:
            score += 20
        elif 100 < price <= 200:
            score += 15
        elif price < 10:
            score += 10
        else:
            score += 5
        
        # Title length factor
        score += min(len(title.split()), 10)
        
        # Random factor
        score += random.uniform(-5, 5)
        
        return max(0, min(100, round(score, 1)))

    def _generate_facebook_ads(self, title: str) -> List[Dict[str, Any]]:
        """Generate mock Facebook ads data"""
        ads = []
        num_ads = random.randint(0, 3)
        
        ad_templates = [
            f"🔥 {title} is AMAZING! You won't believe this!",
            f"🚀 Limited time offer on {title}!",
            f"💯 {title} - The best purchase I've ever made!",
            f"⚡ Don't miss out on {title}!",
            f"🎉 {title} - Game changer!",
        ]
        
        for i in range(num_ads):
            ad = {
                'id': f"ad_{random.randint(1000, 9999)}",
                'ad_text': random.choice(ad_templates),
                'engagement_rate': round(random.uniform(0.02, 0.08), 4),
                'reach': random.randint(5000, 50000),
                'impressions': random.randint(8000, 80000),
                'clicks': random.randint(200, 2000),
                'spend': round(random.uniform(100, 1000), 2),
                'created_at': datetime.utcnow()
            }
            ads.append(ad)
        
        return ads

    def _generate_tiktok_mentions(self, title: str) -> List[Dict[str, Any]]:
        """Generate mock TikTok mentions data"""
        mentions = []
        num_mentions = random.randint(0, 5)
        
        description_templates = [
            f"This {title} is so cool! 🔥",
            f"Just got my {title}! Love it! 💕",
            f"{title} review - must have! ⭐",
            f"Best purchase ever - {title}! 🎉",
            f"Can't live without my {title}! 💯",
        ]
        
        for i in range(num_mentions):
            mention = {
                'id': f"video_{random.randint(10000, 99999)}",
                'video_url': f"https://tiktok.com/@user{random.randint(1, 1000)}/video/{random.randint(100000, 999999)}",
                'description': random.choice(description_templates),
                'views': random.randint(10000, 100000),
                'likes': random.randint(500, 5000),
                'shares': random.randint(100, 1000),
                'comments': random.randint(50, 500),
                'hashtags': ["#dropshipping", "#product", "#review"],
                'created_at': datetime.utcnow()
            }
            mentions.append(mention)
        
        return mentions

    def _generate_trend_data(self, title: str) -> Dict[str, Any]:
        """Generate mock trend data"""
        return {
            'keyword': title.lower(),
            'trend_score': random.randint(30, 90),
            'interest_over_time': [
                {'date': '2024-01-01', 'value': random.randint(20, 80)},
                {'date': '2024-01-02', 'value': random.randint(20, 80)},
                {'date': '2024-01-03', 'value': random.randint(20, 80)},
            ],
            'related_queries': [
                f"best {title.lower()}",
                f"{title.lower()} review",
                f"buy {title.lower()}"
            ],
            'geographic_interest': {
                'US': random.randint(50, 100),
                'CA': random.randint(20, 80),
                'UK': random.randint(20, 80),
                'AU': random.randint(20, 80)
            }
        }

    async def update_memory_storage(self, products: List[Dict[str, Any]]):
        """Update memory storage with new products"""
        try:
            # Clear existing products
            memory_storage.products.clear()
            
            # Add new products
            for product_data in products:
                try:
                    product_id = product_data['id']
                    memory_storage.products[product_id] = product_data
                except Exception as e:
                    logger.error(f"Error adding product to memory storage: {e}")
                    continue
            
            logger.info(f"Updated memory storage with {len(products)} products")
            
        except Exception as e:
            logger.error(f"Error updating memory storage: {e}")

    async def run_full_crawl(self, max_products_per_source: int = 30):
        """Run a full crawl and update the system"""
        try:
            logger.info("Starting full product crawl...")
            
            # Crawl all sources
            products = await self.crawl_all_sources(max_products_per_source)
            
            # Update memory storage
            await self.update_memory_storage(products)
            
            logger.info(f"Full crawl completed. Total products: {len(products)}")
            return products
            
        except Exception as e:
            logger.error(f"Error during full crawl: {e}")
            return []

# Global crawler manager instance
crawler_manager = CrawlerManager() 