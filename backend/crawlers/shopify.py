import aiohttp
import asyncio
from bs4 import BeautifulSoup
import json
import re
from typing import List, Dict, Any, Optional
from urllib.parse import urljoin, urlparse
import logging

logger = logging.getLogger(__name__)

class ShopifyCrawler:
    """
    Crawler for discovering and extracting products from public Shopify stores.
    """
    
    def __init__(self):
        self.session = None
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers=self.headers)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def discover_stores(self, keywords: List[str], limit: int = 50) -> List[str]:
        """Discover Shopify stores based on keywords"""
        stores = []
        
        # Common Shopify store discovery patterns
        search_terms = []
        for keyword in keywords:
            search_terms.extend([
                f"{keyword} shopify",
                f"{keyword} store",
                f"buy {keyword} online"
            ])
        
        # This is a simplified version - in production you'd use search APIs
        # For now, we'll return some example stores
        example_stores = [
            "https://www.example-store1.com",
            "https://www.example-store2.com",
            "https://www.example-store3.com"
        ]
        
        return example_stores[:limit]
    
    async def crawl_store(self, store_url: str) -> List[Dict[str, Any]]:
        """Crawl a single Shopify store for products"""
        try:
            # Get the main page
            async with self.session.get(store_url) as response:
                if response.status != 200:
                    logger.warning(f"Failed to access {store_url}: {response.status}")
                    return []
                
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
            
            # Extract product links
            product_links = await self._extract_product_links(soup, store_url)
            
            # Crawl each product
            products = []
            for link in product_links[:10]:  # Limit to 10 products per store
                try:
                    product = await self._extract_product(link)
                    if product:
                        products.append(product)
                except Exception as e:
                    logger.error(f"Error extracting product from {link}: {e}")
            
            return products
            
        except Exception as e:
            logger.error(f"Error crawling store {store_url}: {e}")
            return []
    
    async def _extract_product_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Extract product page links from store homepage"""
        links = []
        
        # Look for common Shopify product link patterns
        selectors = [
            'a[href*="/products/"]',
            'a[href*="/collections/"]',
            '.product-item a',
            '.product-card a',
            '[data-product-url]'
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            for element in elements:
                href = element.get('href')
                if href:
                    full_url = urljoin(base_url, href)
                    if '/products/' in full_url:
                        links.append(full_url)
        
        return list(set(links))  # Remove duplicates
    
    async def _extract_product(self, product_url: str) -> Optional[Dict[str, Any]]:
        """Extract product information from a product page"""
        try:
            async with self.session.get(product_url) as response:
                if response.status != 200:
                    return None
                
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
            
            # Extract basic product info
            product = {
                'id': self._generate_product_id(product_url),
                'title': self._extract_title(soup),
                'description': self._extract_description(soup),
                'price': self._extract_price(soup),
                'compare_price': self._extract_compare_price(soup),
                'currency': self._extract_currency(soup),
                'category': self._extract_category(soup),
                'tags': self._extract_tags(soup),
                'source_store': self._extract_store_name(product_url),
                'source_url': product_url,
                'images': self._extract_images(soup),
                'variants': self._extract_variants(soup),
                'created_at': None,  # Will be set by database
                'updated_at': None   # Will be set by database
            }
            
            # Clean up None values
            product = {k: v for k, v in product.items() if v is not None}
            
            return product if product.get('title') else None
            
        except Exception as e:
            logger.error(f"Error extracting product from {product_url}: {e}")
            return None
    
    def _generate_product_id(self, url: str) -> str:
        """Generate a unique product ID from URL"""
        # Extract product handle from URL
        match = re.search(r'/products/([^/?]+)', url)
        if match:
            return f"product_{match.group(1)}"
        return f"product_{hash(url) % 1000000}"
    
    def _extract_title(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract product title"""
        selectors = [
            'h1.product-title',
            'h1[data-product-title]',
            '.product-single__title',
            'h1',
            '[data-product-title]'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text().strip()
        
        return None
    
    def _extract_description(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract product description"""
        selectors = [
            '.product-description',
            '.product-single__description',
            '[data-product-description]',
            '.description',
            '#product-description'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text().strip()
        
        return None
    
    def _extract_price(self, soup: BeautifulSoup) -> Optional[float]:
        """Extract product price"""
        selectors = [
            '.price',
            '.product-price',
            '[data-product-price]',
            '.price__regular',
            '.price-item--regular'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                text = element.get_text().strip()
                # Extract numeric price
                price_match = re.search(r'[\d,]+\.?\d*', text.replace(',', ''))
                if price_match:
                    return float(price_match.group())
        
        return None
    
    def _extract_compare_price(self, soup: BeautifulSoup) -> Optional[float]:
        """Extract compare/regular price"""
        selectors = [
            '.price__compare',
            '.price-item--compare',
            '.compare-price',
            '.was-price'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                text = element.get_text().strip()
                price_match = re.search(r'[\d,]+\.?\d*', text.replace(',', ''))
                if price_match:
                    return float(price_match.group())
        
        return None
    
    def _extract_currency(self, soup: BeautifulSoup) -> str:
        """Extract currency (default to USD)"""
        # Look for currency indicators
        currency_selectors = [
            '[data-currency]',
            '.currency',
            'meta[property="product:price:currency"]'
        ]
        
        for selector in currency_selectors:
            element = soup.select_one(selector)
            if element:
                currency = element.get('content') or element.get('data-currency')
                if currency:
                    return currency.upper()
        
        return "USD"  # Default
    
    def _extract_category(self, soup: BeautifulSoup) -> str:
        """Extract product category"""
        # Look for breadcrumbs or category indicators
        breadcrumb_selectors = [
            '.breadcrumb a',
            '.breadcrumbs a',
            '.nav-breadcrumb a'
        ]
        
        for selector in breadcrumb_selectors:
            elements = soup.select(selector)
            if elements:
                # Get the last breadcrumb item (usually the category)
                category = elements[-1].get_text().strip()
                if category and category.lower() not in ['home', 'shop', 'products']:
                    return category.lower()
        
        return "general"
    
    def _extract_tags(self, soup: BeautifulSoup) -> List[str]:
        """Extract product tags"""
        tags = []
        
        # Look for tag elements
        tag_selectors = [
            '.product-tags a',
            '.tags a',
            '[data-product-tags] a'
        ]
        
        for selector in tag_selectors:
            elements = soup.select(selector)
            for element in elements:
                tag = element.get_text().strip()
                if tag:
                    tags.append(tag.lower())
        
        return list(set(tags))  # Remove duplicates
    
    def _extract_store_name(self, url: str) -> str:
        """Extract store name from URL"""
        parsed = urlparse(url)
        return parsed.netloc
    
    def _extract_images(self, soup: BeautifulSoup) -> List[str]:
        """Extract product images"""
        images = []
        
        # Look for product images
        img_selectors = [
            '.product-image img',
            '.product-single__photo img',
            '[data-product-image] img',
            '.product__media img'
        ]
        
        for selector in img_selectors:
            elements = soup.select(selector)
            for element in elements:
                src = element.get('src') or element.get('data-src')
                if src:
                    images.append(src)
        
        return images[:5]  # Limit to 5 images
    
    def _extract_variants(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Extract product variants"""
        variants = []
        
        # Look for variant options
        variant_selectors = [
            '.product-variant',
            '.variant-option',
            '[data-variant]'
        ]
        
        for selector in variant_selectors:
            elements = soup.select(selector)
            for element in elements:
                variant = {
                    'title': element.get_text().strip(),
                    'value': element.get('data-value'),
                    'price': None  # Would need more complex extraction
                }
                variants.append(variant)
        
        return variants 