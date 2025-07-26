import asyncio
import logging
from typing import List, Dict, Any
from datetime import datetime
import random

from .shopify_crawler import ShopifyCrawler
from .general_crawler import GeneralCrawler
from ..database.memory_storage import memory_storage
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
        
        # 2. Crawl Shopify stores
        try:
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
            
            shopify_products = await self.shopify_crawler.crawl_multiple_stores(store_urls, max_products_per_source)
            all_products.extend(shopify_products)
            logger.info(f"Added {len(shopify_products)} products from Shopify stores")
        except Exception as e:
            logger.error(f"Error crawling Shopify stores: {e}")
        
        logger.info(f"Total products crawled: {len(all_products)}")
        return all_products

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