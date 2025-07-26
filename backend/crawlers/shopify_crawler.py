import asyncio
import aiohttp
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
import re
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import random
import time

logger = logging.getLogger(__name__)

class ShopifyCrawler:
    def __init__(self):
        self.session = None
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers=self.headers)
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def crawl_shopify_store(self, store_url: str, max_products: int = 50) -> List[Dict[str, Any]]:
        """Crawl a Shopify store and extract product information"""
        try:
            logger.info(f"Starting to crawl Shopify store: {store_url}")
            
            # Normalize store URL
            if not store_url.startswith('http'):
                store_url = f'https://{store_url}'
            
            # Get products page
            products_url = urljoin(store_url, '/products.json')
            
            async with self.session.get(products_url) as response:
                if response.status != 200:
                    logger.error(f"Failed to fetch products from {store_url}: {response.status}")
                    return []
                
                data = await response.json()
                products_data = data.get('products', [])
                
                logger.info(f"Found {len(products_data)} products in {store_url}")
                
                # Limit products
                products_data = products_data[:max_products]
                
                # Extract product information
                products = []
                for product_data in products_data:
                    try:
                        product = await self._extract_product_info(product_data, store_url)
                        if product:
                            products.append(product)
                            
                        # Add delay to be respectful
                        await asyncio.sleep(0.5)
                        
                    except Exception as e:
                        logger.error(f"Error extracting product {product_data.get('id')}: {e}")
                        continue
                
                logger.info(f"Successfully extracted {len(products)} products from {store_url}")
                return products
                
        except Exception as e:
            logger.error(f"Error crawling Shopify store {store_url}: {e}")
            return []

    async def _extract_product_info(self, product_data: Dict[str, Any], store_url: str) -> Optional[Dict[str, Any]]:
        """Extract detailed product information from Shopify product data"""
        try:
            # Basic product info
            product_id = str(product_data.get('id', ''))
            title = product_data.get('title', '').strip()
            description = product_data.get('body_html', '')
            
            # Clean description
            if description:
                soup = BeautifulSoup(description, 'html.parser')
                description = soup.get_text().strip()
            
            # Price information
            variants = product_data.get('variants', [])
            if not variants:
                return None
                
            # Get price range
            prices = [float(v.get('price', 0)) for v in variants if v.get('price')]
            if not prices:
                return None
                
            price = min(prices)
            compare_price = max(prices) if len(prices) > 1 else price * 1.5
            
            # Images
            images = product_data.get('images', [])
            image_url = images[0].get('src') if images else None
            
            # Tags and categories
            tags = product_data.get('tags', [])
            if isinstance(tags, str):
                tags = [tag.strip() for tag in tags.split(',') if tag.strip()]
            
            # Determine category from tags or product type
            category = self._determine_category(tags, product_data.get('product_type', ''))
            
            # Product URL
            handle = product_data.get('handle', '')
            product_url = urljoin(store_url, f'/products/{handle}')
            
            # Extract store name from URL
            store_name = urlparse(store_url).netloc
            
            # Generate supplier links (mock for now)
            supplier_links = self._generate_supplier_links(title)
            supplier_prices = self._generate_supplier_prices(price)
            
            # Generate social media data (mock for now)
            facebook_ads = self._generate_facebook_ads(title)
            tiktok_mentions = self._generate_tiktok_mentions(title)
            trend_data = self._generate_trend_data(title)
            
            # Calculate score
            score = self._calculate_product_score(price, len(images), len(tags), len(variants))
            
            product = {
                'id': f"shopify_{product_id}",
                'title': title,
                'description': description[:500] + '...' if len(description) > 500 else description,
                'price': round(price, 2),
                'compare_price': round(compare_price, 2),
                'currency': 'USD',
                'score': score,
                'category': category,
                'tags': tags[:10],  # Limit tags
                'source_store': store_name,
                'source_url': product_url,
                'image_url': image_url,
                'supplier_links': supplier_links,
                'supplier_prices': supplier_prices,
                'facebook_ads': facebook_ads,
                'tiktok_mentions': tiktok_mentions,
                'trend_data': trend_data,
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            }
            
            return product
            
        except Exception as e:
            logger.error(f"Error extracting product info: {e}")
            return None

    def _determine_category(self, tags: List[str], product_type: str) -> str:
        """Determine product category from tags and product type"""
        category_keywords = {
            'gadgets': ['gadget', 'tech', 'electronic', 'smart', 'wireless', 'bluetooth', 'led'],
            'fitness': ['fitness', 'workout', 'exercise', 'gym', 'sport', 'athletic', 'health'],
            'home': ['home', 'kitchen', 'bedroom', 'living', 'furniture', 'decor', 'household'],
            'fashion': ['fashion', 'clothing', 'apparel', 'style', 'wear', 'outfit', 'dress'],
            'beauty': ['beauty', 'cosmetic', 'skincare', 'makeup', 'personal care', 'grooming'],
            'pets': ['pet', 'dog', 'cat', 'animal', 'pet care', 'pet accessory'],
            'kids': ['kids', 'children', 'baby', 'toy', 'educational', 'child'],
            'automotive': ['car', 'auto', 'automotive', 'vehicle', 'automobile', 'driving'],
            'garden': ['garden', 'outdoor', 'plant', 'gardening', 'lawn', 'yard'],
            'sports': ['sport', 'outdoor', 'recreation', 'athletic', 'fitness']
        }
        
        # Check tags first
        for tag in tags:
            tag_lower = tag.lower()
            for category, keywords in category_keywords.items():
                if any(keyword in tag_lower for keyword in keywords):
                    return category
        
        # Check product type
        product_type_lower = product_type.lower()
        for category, keywords in category_keywords.items():
            if any(keyword in product_type_lower for keyword in keywords):
                return category
        
        # Default category
        return 'gadgets'

    def _generate_supplier_links(self, title: str) -> Dict[str, str]:
        """Generate mock supplier links"""
        suppliers = {}
        
        # AliExpress
        if random.random() > 0.3:
            suppliers['aliexpress'] = f"https://aliexpress.com/item/{random.randint(100000, 999999)}"
        
        # Temu
        if random.random() > 0.5:
            suppliers['temu'] = f"https://temu.com/item/{random.randint(100000, 999999)}"
        
        # Alibaba
        if random.random() > 0.7:
            suppliers['alibaba'] = f"https://alibaba.com/product/{random.randint(100000, 999999)}"
            
        return suppliers

    def _generate_supplier_prices(self, retail_price: float) -> Dict[str, float]:
        """Generate mock supplier prices"""
        prices = {}
        
        # AliExpress (30-60% of retail)
        if random.random() > 0.3:
            prices['aliexpress'] = round(retail_price * random.uniform(0.3, 0.6), 2)
        
        # Temu (40-70% of retail)
        if random.random() > 0.5:
            prices['temu'] = round(retail_price * random.uniform(0.4, 0.7), 2)
        
        # Alibaba (20-50% of retail)
        if random.random() > 0.7:
            prices['alibaba'] = round(retail_price * random.uniform(0.2, 0.5), 2)
            
        return prices

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

    def _calculate_product_score(self, price: float, image_count: int, tag_count: int, variant_count: int) -> float:
        """Calculate product score based on various factors"""
        score = 50.0  # Base score
        
        # Price factor (lower price = higher score, but not too low)
        if 10 <= price <= 100:
            score += 20
        elif 100 < price <= 200:
            score += 15
        elif price < 10:
            score += 10
        else:
            score += 5
        
        # Image factor
        score += min(image_count * 2, 10)
        
        # Tag factor
        score += min(tag_count, 10)
        
        # Variant factor
        score += min(variant_count * 3, 10)
        
        # Random factor for variety
        score += random.uniform(-5, 5)
        
        return max(0, min(100, round(score, 1)))

    async def crawl_multiple_stores(self, store_urls: List[str], max_products_per_store: int = 20) -> List[Dict[str, Any]]:
        """Crawl multiple Shopify stores"""
        all_products = []
        
        for store_url in store_urls:
            try:
                products = await self.crawl_shopify_store(store_url, max_products_per_store)
                all_products.extend(products)
                
                # Add delay between stores
                await asyncio.sleep(2)
                
            except Exception as e:
                logger.error(f"Error crawling store {store_url}: {e}")
                continue
        
        logger.info(f"Total products crawled: {len(all_products)}")
        return all_products

# Popular Shopify stores to crawl
POPULAR_SHOPIFY_STORES = [
    'https://www.oberlo.com/blog/shopify-stores',
    'https://www.shopify.com/partners/shopify-stores',
    'https://www.etsy.com/shop/trending',
    'https://www.amazon.com/best-sellers',
    'https://www.aliexpress.com/wholesale',
    'https://www.temu.com',
    'https://www.wish.com',
    'https://www.ebay.com/trending',
    'https://www.pinterest.com/trending',
    'https://www.instagram.com/explore/tags/dropshipping'
]

# Example store URLs for testing
EXAMPLE_STORE_URLS = [
    'https://www.oberlo.com/blog/shopify-stores',
    'https://www.shopify.com/partners/shopify-stores',
    'https://www.etsy.com/shop/trending',
    'https://www.amazon.com/best-sellers',
    'https://www.aliexpress.com/wholesale',
    'https://www.temu.com',
    'https://www.wish.com',
    'https://www.ebay.com/trending',
    'https://www.pinterest.com/trending',
    'https://www.instagram.com/explore/tags/dropshipping'
] 