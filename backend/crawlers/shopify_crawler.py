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
            
            # Try different Shopify API endpoints
            api_endpoints = [
                '/products.json',
                '/collections/all/products.json',
                '/collections/frontpage/products.json'
            ]
            
            products_data = []
            
            for endpoint in api_endpoints:
                try:
                    products_url = urljoin(store_url, endpoint)
                    logger.info(f"Trying endpoint: {products_url}")
                    
                    async with self.session.get(products_url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                        if response.status == 200:
                            data = await response.json()
                            products_data = data.get('products', [])
                            logger.info(f"Found {len(products_data)} products using endpoint: {endpoint}")
                            break
                        else:
                            logger.warning(f"Endpoint {endpoint} returned status {response.status}")
                            
                except Exception as e:
                    logger.warning(f"Error trying endpoint {endpoint}: {e}")
                    continue
            
            if not products_data:
                logger.warning(f"No products found for store: {store_url}")
                return []
            
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
            
            # Generate supplier links (placeholder for real supplier data)
            supplier_links = {}
            supplier_prices = {}
            
            # Generate social media data (placeholder for real social media data)
            facebook_ads = []
            tiktok_mentions = []
            trend_data = {}
            
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
        """Determine product category based on tags and type"""
        # Check tags first
        for tag in tags:
            tag_lower = tag.lower()
            if any(keyword in tag_lower for keyword in ['gadget', 'tech', 'electronic', 'smart']):
                return 'gadgets'
            elif any(keyword in tag_lower for keyword in ['home', 'kitchen', 'household']):
                return 'home'
            elif any(keyword in tag_lower for keyword in ['fashion', 'clothing', 'wear', 'style']):
                return 'fashion'
            elif any(keyword in tag_lower for keyword in ['beauty', 'skincare', 'makeup', 'cosmetic']):
                return 'beauty'
            elif any(keyword in tag_lower for keyword in ['fitness', 'workout', 'exercise', 'sport']):
                return 'fitness'
            elif any(keyword in tag_lower for keyword in ['pet', 'dog', 'cat', 'animal']):
                return 'pets'
            elif any(keyword in tag_lower for keyword in ['kid', 'child', 'baby', 'toy']):
                return 'kids'
            elif any(keyword in tag_lower for keyword in ['car', 'auto', 'vehicle', 'automotive']):
                return 'automotive'
            elif any(keyword in tag_lower for keyword in ['garden', 'plant', 'outdoor', 'lawn']):
                return 'garden'
            elif any(keyword in tag_lower for keyword in ['sport', 'athletic', 'game']):
                return 'sports'
        
        # Check product type
        type_lower = product_type.lower()
        if any(keyword in type_lower for keyword in ['gadget', 'tech', 'electronic', 'smart']):
            return 'gadgets'
        elif any(keyword in type_lower for keyword in ['home', 'kitchen', 'household']):
            return 'home'
        elif any(keyword in type_lower for keyword in ['fashion', 'clothing', 'wear', 'style']):
            return 'fashion'
        elif any(keyword in type_lower for keyword in ['beauty', 'skincare', 'makeup', 'cosmetic']):
            return 'beauty'
        elif any(keyword in type_lower for keyword in ['fitness', 'workout', 'exercise', 'sport']):
            return 'fitness'
        elif any(keyword in type_lower for keyword in ['pet', 'dog', 'cat', 'animal']):
            return 'pets'
        elif any(keyword in type_lower for keyword in ['kid', 'child', 'baby', 'toy']):
            return 'kids'
        elif any(keyword in type_lower for keyword in ['car', 'auto', 'vehicle', 'automotive']):
            return 'automotive'
        elif any(keyword in type_lower for keyword in ['garden', 'plant', 'outdoor', 'lawn']):
            return 'garden'
        elif any(keyword in type_lower for keyword in ['sport', 'athletic', 'game']):
            return 'sports'
        
        # Default category
        return 'gadgets'

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
                logger.info(f"Crawling Shopify store: {store_url}")
                products = await self.crawl_shopify_store(store_url, max_products_per_store)
                all_products.extend(products)
                
                # Add delay between stores to be respectful
                await asyncio.sleep(2)
                
            except Exception as e:
                logger.error(f"Error crawling store {store_url}: {e}")
                continue
        
        logger.info(f"Total products from Shopify stores: {len(all_products)}")
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