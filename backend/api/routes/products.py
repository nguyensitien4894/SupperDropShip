from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from datetime import datetime
import logging

from backend.database.models import Product, ProductResponse, ProductsResponse, CrawlRequest
from backend.scoring.engine import ScoringEngine

logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize scoring engine
scoring_engine = ScoringEngine()

# Mock database for demo purposes
mock_products = [
    {
        "id": "product_1",
        "title": "LED Flame Speaker",
        "description": "Portable Bluetooth speaker with realistic LED flame effect",
        "price": 29.99,
        "compare_price": 59.99,
        "currency": "USD",
        "score": 82.5,
        "category": "gadgets",
        "tags": ["gadgets", "home", "gift", "bluetooth"],
        "source_store": "example-store.com",
        "source_url": "https://example-store.com/products/led-flame-speaker",
        "supplier_links": {
            "aliexpress": "https://aliexpress.com/item/123456",
            "temu": "https://temu.com/item/789012"
        },
        "supplier_prices": {
            "aliexpress": 12.50,
            "temu": 15.00
        },
        "facebook_ads": [
            {
                "id": "ad_1",
                "ad_text": "🔥 This LED Flame Speaker is AMAZING!",
                "engagement_rate": 0.045,
                "reach": 10000,
                "impressions": 15000,
                "clicks": 450,
                "spend": 500.00
            }
        ],
        "tiktok_mentions": [
            {
                "id": "video_1",
                "video_url": "https://tiktok.com/@user/video/123",
                "description": "This speaker is so cool! 🔥",
                "views": 50000,
                "likes": 2500,
                "shares": 300,
                "comments": 150
            }
        ],
        "trend_data": {
            "keyword": "LED flame speaker",
            "trend_score": 75
        },
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": "product_2",
        "title": "Smart Water Bottle",
        "description": "Hydration tracking water bottle with app connectivity",
        "price": 49.99,
        "compare_price": 79.99,
        "currency": "USD",
        "score": 78.2,
        "category": "fitness",
        "tags": ["fitness", "health", "smart", "hydration"],
        "source_store": "fitness-store.com",
        "source_url": "https://fitness-store.com/products/smart-water-bottle",
        "supplier_links": {
            "aliexpress": "https://aliexpress.com/item/654321"
        },
        "supplier_prices": {
            "aliexpress": 25.00
        },
        "facebook_ads": [
            {
                "id": "ad_2",
                "ad_text": "Stay hydrated with this smart water bottle! 💧",
                "engagement_rate": 0.032,
                "reach": 8000,
                "impressions": 12000,
                "clicks": 256,
                "spend": 300.00
            }
        ],
        "tiktok_mentions": [
            {
                "id": "video_2",
                "video_url": "https://tiktok.com/@user/video/456",
                "description": "My new smart water bottle! 💧",
                "views": 30000,
                "likes": 1800,
                "shares": 200,
                "comments": 120
            }
        ],
        "trend_data": {
            "keyword": "smart water bottle",
            "trend_score": 65
        },
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
]

@router.get("/", response_model=ProductsResponse)
async def get_products(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(50, ge=1, le=100, description="Items per page"),
    category: Optional[str] = Query(None, description="Filter by category"),
    min_score: Optional[float] = Query(None, ge=0, le=100, description="Minimum score"),
    max_price: Optional[float] = Query(None, description="Maximum price"),
    search: Optional[str] = Query(None, description="Search in title and description")
):
    """Get all products with optional filtering"""
    try:
        # Apply filters
        filtered_products = mock_products.copy()
        
        if category:
            filtered_products = [p for p in filtered_products if p.get('category') == category]
        
        if min_score is not None:
            filtered_products = [p for p in filtered_products if p.get('score', 0) >= min_score]
        
        if max_price is not None:
            filtered_products = [p for p in filtered_products if p.get('price', 0) <= max_price]
        
        if search:
            search_lower = search.lower()
            filtered_products = [
                p for p in filtered_products 
                if search_lower in p.get('title', '').lower() or 
                   search_lower in p.get('description', '').lower()
            ]
        
        # Pagination
        total = len(filtered_products)
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        paginated_products = filtered_products[start_idx:end_idx]
        
        return ProductsResponse(
            success=True,
            data=paginated_products,
            total=total,
            page=page,
            limit=limit
        )
        
    except Exception as e:
        logger.error(f"Error getting products: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: str):
    """Get a specific product by ID"""
    try:
        product = next((p for p in mock_products if p['id'] == product_id), None)
        
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return ProductResponse(success=True, data=product)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting product {product_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{product_id}/similar", response_model=ProductsResponse)
async def get_similar_products(
    product_id: str,
    limit: int = Query(10, ge=1, le=50, description="Number of similar products")
):
    """Get similar products based on category and tags"""
    try:
        # Find the target product
        target_product = next((p for p in mock_products if p['id'] == product_id), None)
        
        if not target_product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Find similar products (same category or similar tags)
        target_category = target_product.get('category')
        target_tags = set(target_product.get('tags', []))
        
        similar_products = []
        for product in mock_products:
            if product['id'] == product_id:
                continue  # Skip the target product
            
            # Calculate similarity score
            category_match = product.get('category') == target_category
            tag_overlap = len(set(product.get('tags', [])) & target_tags)
            
            if category_match or tag_overlap > 0:
                similar_products.append(product)
        
        # Sort by similarity (category match + tag overlap)
        similar_products.sort(
            key=lambda p: (
                p.get('category') == target_category,
                len(set(p.get('tags', [])) & target_tags)
            ),
            reverse=True
        )
        
        return ProductsResponse(
            success=True,
            data=similar_products[:limit],
            total=len(similar_products),
            page=1,
            limit=limit
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting similar products for {product_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{product_id}/score-breakdown")
async def get_score_breakdown(product_id: str):
    """Get detailed score breakdown for a product"""
    try:
        product = next((p for p in mock_products if p['id'] == product_id), None)
        
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Get score breakdown using scoring engine
        breakdown = scoring_engine.get_score_breakdown(product)
        
        return {
            "success": True,
            "product_id": product_id,
            "data": breakdown
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting score breakdown for {product_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/crawl", response_model=ProductsResponse)
async def crawl_products(request: CrawlRequest):
    """Crawl for new products based on keywords"""
    try:
        # This would integrate with the actual crawlers
        # For now, return mock data
        logger.info(f"Crawling for products with keywords: {request.keywords}")
        
        # Simulate crawling delay
        import asyncio
        await asyncio.sleep(1)
        
        # Return mock products that match the keywords
        matching_products = []
        for product in mock_products:
            if any(keyword.lower() in product['title'].lower() for keyword in request.keywords):
                matching_products.append(product)
        
        return ProductsResponse(
            success=True,
            data=matching_products[:request.limit],
            total=len(matching_products),
            page=1,
            limit=request.limit,
            message=f"Found {len(matching_products)} products matching keywords"
        )
        
    except Exception as e:
        logger.error(f"Error crawling products: {e}")
        raise HTTPException(status_code=500, detail="Internal server error") 