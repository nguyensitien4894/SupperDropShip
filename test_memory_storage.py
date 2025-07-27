import asyncio
import sys
import os
from datetime import datetime

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.database.memory_storage import memory_storage

async def test_memory_storage():
    # Create some test products from different platforms
    test_products = [
        {
            'id': 'etsy_test_1',
            'title': 'Handmade Ceramic Mug',
            'description': 'Beautiful handmade ceramic mug from Etsy',
            'price': 25.0,
            'compare_price': 30.0,
            'currency': 'USD',
            'score': 85.0,
            'category': 'home',
            'tags': ['handmade', 'ceramic', 'mug'],
            'image_url': 'https://picsum.photos/400/400?random=1001',
            'source_url': 'https://www.etsy.com/listing/123456789',
            'source_store': 'etsy.com',
            'supplier_links': ['https://www.etsy.com/listing/123456789'],
            'supplier_prices': [25.0],
            'created_at': datetime.utcnow()
        },
        {
            'id': 'alibaba_test_1',
            'title': 'Wholesale Wireless Earbuds',
            'description': 'Wholesale wireless earbuds from Alibaba',
            'price': 15.0,
            'compare_price': 22.5,
            'currency': 'USD',
            'score': 78.0,
            'category': 'gadgets',
            'tags': ['wireless', 'earbuds', 'wholesale'],
            'image_url': 'https://picsum.photos/400/400?random=1002',
            'source_url': 'https://www.alibaba.com/product-detail/987654321.html',
            'source_store': 'alibaba.com',
            'supplier_links': ['https://www.alibaba.com/product-detail/987654321.html'],
            'supplier_prices': [15.0],
            'created_at': datetime.utcnow()
        },
        {
            'id': 'taobao_test_1',
            'title': '时尚女装连衣裙',
            'description': 'Chinese market fashion dress from Taobao',
            'price': 50.0,
            'compare_price': 65.0,
            'currency': 'CNY',
            'score': 82.0,
            'category': 'fashion',
            'tags': ['fashion', 'dress', 'chinese'],
            'image_url': 'https://picsum.photos/400/400?random=1003',
            'source_url': 'https://item.taobao.com/item.htm?id=111222333',
            'source_store': 'taobao.com',
            'supplier_links': ['https://item.taobao.com/item.htm?id=111222333'],
            'supplier_prices': [50.0],
            'created_at': datetime.utcnow()
        }
    ]
    
    # Add products to memory storage
    for product in test_products:
        memory_storage.products[product['id']] = product
    
    print(f"Added {len(test_products)} test products to memory storage")
    print(f"Total products in storage: {len(memory_storage.products)}")
    
    # Check what stores are available
    stores = set(p.get('source_store', 'N/A') for p in memory_storage.products.values())
    print(f"Available stores: {stores}")

if __name__ == "__main__":
    asyncio.run(test_memory_storage()) 