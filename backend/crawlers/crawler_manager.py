import asyncio
import logging
from typing import List, Dict, Any
from datetime import datetime
import random
import time

from .shopify_crawler import ShopifyCrawler
from .general_crawler import GeneralCrawler
from ..database.memory_storage import memory_storage
from ..database.models import Product

logger = logging.getLogger(__name__)

class RateLimiter:
    def __init__(self, max_requests_per_second=2):
        self.max_requests = max_requests_per_second
        self.last_request_time = 0
        
    async def wait(self):
        now = time.time()
        time_since_last = now - self.last_request_time
        if time_since_last < 1.0 / self.max_requests:
            await asyncio.sleep(1.0 / self.max_requests - time_since_last)
        self.last_request_time = time.time()

class CrawlProgress:
    def __init__(self):
        self.total_sources = 0
        self.completed_sources = 0
        self.total_products = 0
        self.status = "idle"
        self.start_time = None
        self.end_time = None
    
    def start(self, total_sources):
        self.total_sources = total_sources
        self.completed_sources = 0
        self.total_products = 0
        self.status = "running"
        self.start_time = time.time()
    
    def update(self, source_completed=False, products_found=0):
        if source_completed:
            self.completed_sources += 1
        self.total_products += products_found
    
    def finish(self):
        self.status = "completed"
        self.end_time = time.time()
    
    def get_progress(self):
        if self.total_sources == 0:
            return 0
        return (self.completed_sources / self.total_sources) * 100

class CrawlerManager:
    def __init__(self):
        self.shopify_crawler = None
        self.general_crawler = None
        self.rate_limiter = RateLimiter(max_requests_per_second=3)
        self.progress = CrawlProgress()
        
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

    async def crawl_all_sources_parallel(self, max_products_per_source: int = 30) -> List[Dict[str, Any]]:
        """Crawl all available sources in parallel and return combined products"""
        logger.info("Starting optimized parallel crawl from all sources...")
        
        # Popular Shopify stores to crawl
        store_urls = [
            "https://www.gymshark.com",
            "https://www.kyliecosmetics.com", 
            "https://www.allbirds.com",
            "https://www.glossier.com",
            "https://www.awaytravel.com",
            "https://www.ring.com",
            "https://www.peloton.com",
            "https://www.warbyparker.com",
            "https://www.casper.com",
            "https://www.bombas.com"
        ]
        
        # Initialize progress tracking
        total_sources = 8  # AliExpress, Temu, Amazon, Shopify, Etsy, Alibaba, Taobao, Wish, eBay
        self.progress.start(total_sources)
        
        # Use sequential approach for debugging
        all_products = []
        
        # Crawl general platforms first
        try:
            logger.info("Starting general platforms crawl...")
            general_products = await self._crawl_general_platforms_optimized(max_products_per_source)
            all_products.extend(general_products)
            logger.info(f"General platforms completed with {len(general_products)} products")
            self.progress.update(source_completed=True, products_found=len(general_products))
        except Exception as e:
            logger.error(f"General platforms failed: {e}")
            self.progress.update(source_completed=True)
        
        # Crawl Shopify stores
        try:
            logger.info("Starting Shopify crawl...")
            shopify_products = await self._crawl_shopify_optimized(store_urls, max_products_per_source)
            all_products.extend(shopify_products)
            logger.info(f"Shopify completed with {len(shopify_products)} products")
            self.progress.update(source_completed=True, products_found=len(shopify_products))
        except Exception as e:
            logger.error(f"Shopify failed: {e}")
            self.progress.update(source_completed=True)
        
        self.progress.finish()
        logger.info(f"Parallel crawl completed: {len(all_products)} total products")
        return all_products

    async def _crawl_aliexpress_optimized(self, max_products: int) -> List[Dict[str, Any]]:
        """Optimized AliExpress crawling with rate limiting"""
        try:
            await self.rate_limiter.wait()
            return await self.general_crawler.crawl_aliexpress(max_products)
        except Exception as e:
            logger.error(f"Error in optimized AliExpress crawl: {e}")
            return []

    async def _crawl_temu_optimized(self, max_products: int) -> List[Dict[str, Any]]:
        """Optimized Temu crawling with rate limiting"""
        try:
            await self.rate_limiter.wait()
            return await self.general_crawler.crawl_temu(max_products)
        except Exception as e:
            logger.error(f"Error in optimized Temu crawl: {e}")
            return []

    async def _crawl_amazon_optimized(self, max_products: int) -> List[Dict[str, Any]]:
        """Optimized Amazon crawling with rate limiting"""
        try:
            await self.rate_limiter.wait()
            return await self.general_crawler.crawl_amazon_trending(max_products)
        except Exception as e:
            logger.error(f"Error in optimized Amazon crawl: {e}")
            return []

    async def _crawl_general_platforms_optimized(self, max_products_per_platform: int) -> List[Dict[str, Any]]:
        """Optimized crawling for all general platforms (AliExpress, Temu, Amazon, Etsy, Alibaba, Taobao, Wish, eBay)"""
        try:
            await self.rate_limiter.wait()
            logger.info("Starting general platforms crawl...")
            products = await self.general_crawler.crawl_all_platforms(max_products_per_platform)
            logger.info(f"General platforms crawl completed: {len(products)} products")
            
            # Log the stores found
            stores = set(p.get('source_store', 'unknown') for p in products)
            logger.info(f"Stores found: {stores}")
            
            return products
        except Exception as e:
            logger.error(f"Error in optimized general platforms crawl: {e}")
            return []

    async def _crawl_shopify_optimized(self, store_urls: List[str], max_products_per_store: int) -> List[Dict[str, Any]]:
        """Optimized Shopify crawling with rate limiting"""
        try:
            await self.rate_limiter.wait()
            return await self.shopify_crawler.crawl_multiple_stores(store_urls, max_products_per_store)
        except Exception as e:
            logger.error(f"Error in optimized Shopify crawl: {e}")
            return []

    async def _crawl_etsy_optimized(self, max_products: int) -> List[Dict[str, Any]]:
        """Optimized Etsy crawling with rate limiting"""
        try:
            await self.rate_limiter.wait()
            return await self.general_crawler.crawl_etsy(max_products)
        except Exception as e:
            logger.error(f"Error in optimized Etsy crawl: {e}")
            return []

    async def _crawl_alibaba_optimized(self, max_products: int) -> List[Dict[str, Any]]:
        """Optimized Alibaba crawling with rate limiting"""
        try:
            await self.rate_limiter.wait()
            return await self.general_crawler.crawl_alibaba(max_products)
        except Exception as e:
            logger.error(f"Error in optimized Alibaba crawl: {e}")
            return []

    async def _crawl_taobao_optimized(self, max_products: int) -> List[Dict[str, Any]]:
        """Optimized Taobao crawling with rate limiting"""
        try:
            await self.rate_limiter.wait()
            return await self.general_crawler.crawl_taobao(max_products)
        except Exception as e:
            logger.error(f"Error in optimized Taobao crawl: {e}")
            return []

    async def _crawl_wish_optimized(self, max_products: int) -> List[Dict[str, Any]]:
        """Optimized Wish crawling with rate limiting"""
        try:
            await self.rate_limiter.wait()
            return await self.general_crawler.crawl_wish(max_products)
        except Exception as e:
            logger.error(f"Error in optimized Wish crawl: {e}")
            return []

    async def _crawl_ebay_optimized(self, max_products: int) -> List[Dict[str, Any]]:
        """Optimized eBay crawling with rate limiting"""
        try:
            await self.rate_limiter.wait()
            return await self.general_crawler.crawl_ebay(max_products)
        except Exception as e:
            logger.error(f"Error in optimized eBay crawl: {e}")
            return []

    async def crawl_all_sources(self, max_products_per_source: int = 30) -> List[Dict[str, Any]]:
        """Legacy method - now uses parallel crawling"""
        return await self.crawl_all_sources_parallel(max_products_per_source)

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
            logger.info("Starting optimized full product crawl...")
            
            # Crawl all sources in parallel
            products = await self.crawl_all_sources_parallel(max_products_per_source)
            
            # Update memory storage
            await self.update_memory_storage(products)
            
            logger.info(f"Full crawl completed: {len(products)} products processed")
            return products
            
        except Exception as e:
            logger.error(f"Error during full crawl: {e}")
            raise

    def get_crawl_progress(self) -> Dict[str, Any]:
        """Get current crawl progress"""
        return {
            "status": self.progress.status,
            "total_sources": self.progress.total_sources,
            "completed_sources": self.progress.completed_sources,
            "total_products": self.progress.total_products,
            "progress_percentage": self.progress.get_progress(),
            "start_time": self.progress.start_time,
            "end_time": self.progress.end_time
        }

# Global crawler manager instance
crawler_manager = CrawlerManager() 