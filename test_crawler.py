import asyncio
import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.crawlers.general_crawler import GeneralCrawler

async def test_new_crawlers():
    async with GeneralCrawler() as crawler:
        print("Testing Etsy crawler...")
        etsy_products = await crawler.crawl_etsy(5)
        print(f"Etsy products: {len(etsy_products)}")
        for product in etsy_products[:2]:
            print(f"  - {product.get('title', 'N/A')} from {product.get('source_store', 'N/A')}")
        
        print("\nTesting Alibaba crawler...")
        alibaba_products = await crawler.crawl_alibaba(5)
        print(f"Alibaba products: {len(alibaba_products)}")
        for product in alibaba_products[:2]:
            print(f"  - {product.get('title', 'N/A')} from {product.get('source_store', 'N/A')}")
        
        print("\nTesting Taobao crawler...")
        taobao_products = await crawler.crawl_taobao(5)
        print(f"Taobao products: {len(taobao_products)}")
        for product in taobao_products[:2]:
            print(f"  - {product.get('title', 'N/A')} from {product.get('source_store', 'N/A')}")

if __name__ == "__main__":
    asyncio.run(test_new_crawlers()) 