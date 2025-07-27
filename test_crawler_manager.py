import asyncio
import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.crawlers.crawler_manager import CrawlerManager

async def test_crawler_manager():
    async with CrawlerManager() as manager:
        print("Testing crawler manager...")
        
        # Test the general platforms crawler directly
        print("\nTesting _crawl_general_platforms_optimized...")
        general_products = await manager._crawl_general_platforms_optimized(5)
        print(f"General platforms products: {len(general_products)}")
        
        # Group by store
        stores = {}
        for product in general_products:
            store = product.get('source_store', 'unknown')
            if store not in stores:
                stores[store] = []
            stores[store].append(product)
        
        print("\nProducts by store from general platforms:")
        for store, products in stores.items():
            print(f"  {store}: {len(products)} products")
            for product in products[:1]:  # Show first product from each store
                print(f"    - {product.get('title', 'N/A')}")
        
        # Test the full crawl
        print("\nTesting full crawl...")
        all_products = await manager.crawl_all_sources_parallel(5)
        print(f"Total products from full crawl: {len(all_products)}")
        
        # Group by store
        stores = {}
        for product in all_products:
            store = product.get('source_store', 'unknown')
            if store not in stores:
                stores[store] = []
            stores[store].append(product)
        
        print("\nProducts by store from full crawl:")
        for store, products in stores.items():
            print(f"  {store}: {len(products)} products")

if __name__ == "__main__":
    asyncio.run(test_crawler_manager()) 