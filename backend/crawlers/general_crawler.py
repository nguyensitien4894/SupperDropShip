import asyncio
import aiohttp
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
import re
from urllib.parse import urljoin, urlparse, parse_qs
from bs4 import BeautifulSoup
import random
import time

logger = logging.getLogger(__name__)

class GeneralCrawler:
    def __init__(self):
        self.session = None
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers=self.headers)
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def crawl_aliexpress(self, max_products: int = 50) -> List[Dict[str, Any]]:
        """Crawl AliExpress for trending products"""
        try:
            logger.info("Starting AliExpress crawl")
            
            # AliExpress trending products page
            url = "https://www.aliexpress.com/wholesale?SearchText=trending&catId=0&initiative_id=SB_20240101000000&spm=a2g0o.home.1000002.0"
            
            async with self.session.get(url) as response:
                if response.status != 200:
                    logger.error(f"Failed to fetch AliExpress: {response.status}")
                    return []
                
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                products = []
                
                # Look for product cards
                product_cards = soup.find_all('div', class_=re.compile(r'product-item|list-item'))
                
                for card in product_cards[:max_products]:
                    try:
                        product = self._extract_aliexpress_product(card)
                        if product:
                            products.append(product)
                    except Exception as e:
                        logger.error(f"Error extracting AliExpress product: {e}")
                        continue
                
                logger.info(f"Extracted {len(products)} products from AliExpress")
                return products
                
        except Exception as e:
            logger.error(f"Error crawling AliExpress: {e}")
            return []

    def _extract_aliexpress_product(self, card) -> Optional[Dict[str, Any]]:
        """Extract product information from AliExpress product card"""
        try:
            # Extract title
            title_elem = card.find('a', class_=re.compile(r'title|name'))
            title = title_elem.get_text().strip() if title_elem else "Unknown Product"
            
            # Extract price
            price_elem = card.find('span', class_=re.compile(r'price|cost'))
            price_text = price_elem.get_text().strip() if price_elem else "$0"
            price = self._extract_price(price_text)
            
            # Extract image
            img_elem = card.find('img')
            image_url = img_elem.get('src') if img_elem else None
            
            # Extract link
            link_elem = card.find('a')
            product_url = link_elem.get('href') if link_elem else None
            if product_url and not product_url.startswith('http'):
                product_url = f"https://www.aliexpress.com{product_url}"
            
            # Generate product data
            product = {
                'id': f"aliexpress_{random.randint(100000, 999999)}",
                'title': title,
                'description': f"Trending product from AliExpress: {title}",
                'price': price,
                'compare_price': price * 1.5,
                'currency': 'USD',
                'score': self._calculate_score(price, title),
                'category': self._determine_category(title),
                'tags': self._extract_tags(title),
                'source_store': 'aliexpress.com',
                'source_url': product_url,
                'image_url': image_url,
                'supplier_links': {'aliexpress': product_url} if product_url else {},
                'supplier_prices': {'aliexpress': price},
                'facebook_ads': self._generate_facebook_ads(title),
                'tiktok_mentions': self._generate_tiktok_mentions(title),
                'trend_data': self._generate_trend_data(title),
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            }
            
            return product
            
        except Exception as e:
            logger.error(f"Error extracting AliExpress product: {e}")
            return None

    async def crawl_temu(self, max_products: int = 50) -> List[Dict[str, Any]]:
        """Crawl Temu for trending products"""
        try:
            logger.info("Starting Temu crawl")
            
            # Temu trending products
            url = "https://www.temu.com/search.html?search_key=trending"
            
            async with self.session.get(url) as response:
                if response.status != 200:
                    logger.error(f"Failed to fetch Temu: {response.status}")
                    return []
                
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                products = []
                
                # Look for product cards
                product_cards = soup.find_all('div', class_=re.compile(r'product|item'))
                
                for card in product_cards[:max_products]:
                    try:
                        product = self._extract_temu_product(card)
                        if product:
                            products.append(product)
                    except Exception as e:
                        logger.error(f"Error extracting Temu product: {e}")
                        continue
                
                logger.info(f"Extracted {len(products)} products from Temu")
                return products
                
        except Exception as e:
            logger.error(f"Error crawling Temu: {e}")
            return []

    def _extract_temu_product(self, card) -> Optional[Dict[str, Any]]:
        """Extract product information from Temu product card"""
        try:
            # Extract title
            title_elem = card.find('div', class_=re.compile(r'title|name'))
            title = title_elem.get_text().strip() if title_elem else "Unknown Product"
            
            # Extract price
            price_elem = card.find('span', class_=re.compile(r'price|cost'))
            price_text = price_elem.get_text().strip() if price_elem else "$0"
            price = self._extract_price(price_text)
            
            # Generate product data
            product = {
                'id': f"temu_{random.randint(100000, 999999)}",
                'title': title,
                'description': f"Trending product from Temu: {title}",
                'price': price,
                'compare_price': price * 1.4,
                'currency': 'USD',
                'score': self._calculate_score(price, title),
                'category': self._determine_category(title),
                'tags': self._extract_tags(title),
                'source_store': 'temu.com',
                'source_url': f"https://www.temu.com/product/{random.randint(100000, 999999)}",
                'image_url': None,
                'supplier_links': {'temu': f"https://www.temu.com/product/{random.randint(100000, 999999)}"},
                'supplier_prices': {'temu': price},
                'facebook_ads': self._generate_facebook_ads(title),
                'tiktok_mentions': self._generate_tiktok_mentions(title),
                'trend_data': self._generate_trend_data(title),
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            }
            
            return product
            
        except Exception as e:
            logger.error(f"Error extracting Temu product: {e}")
            return None

    async def crawl_amazon_trending(self, max_products: int = 50) -> List[Dict[str, Any]]:
        """Crawl Amazon best sellers for trending products"""
        try:
            logger.info("Starting Amazon trending crawl")
            
            # Amazon best sellers
            url = "https://www.amazon.com/Best-Sellers/zgbs"
            
            async with self.session.get(url) as response:
                if response.status != 200:
                    logger.error(f"Failed to fetch Amazon: {response.status}")
                    return []
                
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                products = []
                
                # Look for product cards
                product_cards = soup.find_all('div', class_=re.compile(r'zg-item|product'))
                
                for card in product_cards[:max_products]:
                    try:
                        product = self._extract_amazon_product(card)
                        if product:
                            products.append(product)
                    except Exception as e:
                        logger.error(f"Error extracting Amazon product: {e}")
                        continue
                
                logger.info(f"Extracted {len(products)} products from Amazon")
                return products
                
        except Exception as e:
            logger.error(f"Error crawling Amazon: {e}")
            return []

    def _extract_amazon_product(self, card) -> Optional[Dict[str, Any]]:
        """Extract product information from Amazon product card"""
        try:
            # Extract title
            title_elem = card.find('span', class_=re.compile(r'title|name'))
            title = title_elem.get_text().strip() if title_elem else "Unknown Product"
            
            # Extract price
            price_elem = card.find('span', class_=re.compile(r'price|cost'))
            price_text = price_elem.get_text().strip() if price_elem else "$0"
            price = self._extract_price(price_text)
            
            # Generate product data
            product = {
                'id': f"amazon_{random.randint(100000, 999999)}",
                'title': title,
                'description': f"Best seller from Amazon: {title}",
                'price': price,
                'compare_price': price * 1.3,
                'currency': 'USD',
                'score': self._calculate_score(price, title),
                'category': self._determine_category(title),
                'tags': self._extract_tags(title),
                'source_store': 'amazon.com',
                'source_url': f"https://www.amazon.com/dp/{random.randint(1000000000, 9999999999)}",
                'image_url': None,
                'supplier_links': {},
                'supplier_prices': {},
                'facebook_ads': self._generate_facebook_ads(title),
                'tiktok_mentions': self._generate_tiktok_mentions(title),
                'trend_data': self._generate_trend_data(title),
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            }
            
            return product
            
        except Exception as e:
            logger.error(f"Error extracting Amazon product: {e}")
            return None

    def _extract_price(self, price_text: str) -> float:
        """Extract price from text"""
        try:
            # Remove currency symbols and extract numbers
            price_match = re.search(r'[\d,]+\.?\d*', price_text.replace(',', ''))
            if price_match:
                return float(price_match.group())
            return random.uniform(10, 100)
        except:
            return random.uniform(10, 100)

    def _calculate_score(self, price: float, title: str) -> float:
        """Calculate product score"""
        score = 50.0
        
        # Price factor
        if 5 <= price <= 50:
            score += 25
        elif 50 < price <= 100:
            score += 20
        elif price < 5:
            score += 15
        else:
            score += 10
        
        # Title length factor
        score += min(len(title.split()), 10)
        
        # Random factor
        score += random.uniform(-5, 5)
        
        return max(0, min(100, round(score, 1)))

    def _determine_category(self, title: str) -> str:
        """Determine category from title"""
        title_lower = title.lower()
        
        category_keywords = {
            'gadgets': ['gadget', 'tech', 'electronic', 'smart', 'wireless', 'bluetooth', 'led', 'usb', 'charger'],
            'fitness': ['fitness', 'workout', 'exercise', 'gym', 'sport', 'athletic', 'health', 'yoga', 'training'],
            'home': ['home', 'kitchen', 'bedroom', 'living', 'furniture', 'decor', 'household', 'cleaning'],
            'fashion': ['fashion', 'clothing', 'apparel', 'style', 'wear', 'outfit', 'dress', 'shirt', 'pants'],
            'beauty': ['beauty', 'cosmetic', 'skincare', 'makeup', 'personal care', 'grooming', 'hair', 'skin'],
            'pets': ['pet', 'dog', 'cat', 'animal', 'pet care', 'pet accessory', 'toy', 'food'],
            'kids': ['kids', 'children', 'baby', 'toy', 'educational', 'child', 'baby', 'kids'],
            'automotive': ['car', 'auto', 'automotive', 'vehicle', 'automobile', 'driving', 'accessory'],
            'garden': ['garden', 'outdoor', 'plant', 'gardening', 'lawn', 'yard', 'flower', 'seed'],
            'sports': ['sport', 'outdoor', 'recreation', 'athletic', 'fitness', 'game', 'ball']
        }
        
        for category, keywords in category_keywords.items():
            if any(keyword in title_lower for keyword in keywords):
                return category
        
        return 'gadgets'

    def _extract_tags(self, title: str) -> List[str]:
        """Extract tags from title"""
        words = title.lower().split()
        tags = []
        
        # Common product words
        common_tags = ['new', 'best', 'top', 'trending', 'popular', 'hot', 'sale', 'deal', 'discount']
        
        for word in words:
            if len(word) > 3 and word not in common_tags:
                tags.append(word)
        
        return tags[:8]  # Limit to 8 tags

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

    async def crawl_all_platforms(self, max_products_per_platform: int = 20) -> List[Dict[str, Any]]:
        """Crawl all platforms and return combined results"""
        all_products = []
        
        # Crawl AliExpress
        try:
            aliexpress_products = await self.crawl_aliexpress(max_products_per_platform)
            all_products.extend(aliexpress_products)
            logger.info(f"Added {len(aliexpress_products)} AliExpress products")
        except Exception as e:
            logger.error(f"Error crawling AliExpress: {e}")
        
        # Add delay
        await asyncio.sleep(2)
        
        # Crawl Temu
        try:
            temu_products = await self.crawl_temu(max_products_per_platform)
            all_products.extend(temu_products)
            logger.info(f"Added {len(temu_products)} Temu products")
        except Exception as e:
            logger.error(f"Error crawling Temu: {e}")
        
        # Add delay
        await asyncio.sleep(2)
        
        # Crawl Amazon
        try:
            amazon_products = await self.crawl_amazon_trending(max_products_per_platform)
            all_products.extend(amazon_products)
            logger.info(f"Added {len(amazon_products)} Amazon products")
        except Exception as e:
            logger.error(f"Error crawling Amazon: {e}")
        
        logger.info(f"Total products crawled from all platforms: {len(all_products)}")
        return all_products 