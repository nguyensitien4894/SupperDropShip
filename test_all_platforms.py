import asyncio
import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.crawlers.general_crawler import GeneralCrawler

async def test_all_platforms():
    async with GeneralCrawler() as crawler:
        print("Testing crawl_all_platforms...")
        all_products = await crawler.crawl_all_platforms(3)
        print(f"Total products: {len(all_products)}")
        
        # Group by store
        stores = {}
        for product in all_products:
            store = product.get('source_store', 'unknown')
            if store not in stores:
                stores[store] = []
            stores[store].append(product)
        
        print("\nProducts by store:")
        for store, products in stores.items():
            print(f"  {store}: {len(products)} products")
            for product in products[:1]:  # Show first product from each store
                print(f"    - {product.get('title', 'N/A')}")

if __name__ == "__main__":
    asyncio.run(test_all_platforms()) 