from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import logging
from ..dependencies import get_current_user
from ...database.memory_storage import memory_storage
from ...database.models import Product

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/overview")
async def get_store_overview():
    """Get store overview and statistics"""
    try:
        products = list(memory_storage.products.values())
        
        # Store statistics
        total_products = len(products)
        total_value = sum(p.get('price', 0) for p in products)
        avg_price = total_value / total_products if total_products > 0 else 0
        
        # Store performance metrics
        total_facebook_ads = sum(len(p.get('facebook_ads', [])) for p in products)
        total_tiktok_mentions = sum(len(p.get('tiktok_mentions', [])) for p in products)
        
        # Calculate total reach and engagement
        total_reach = 0
        total_engagement = 0
        total_spend = 0
        
        for product in products:
            for ad in product.get('facebook_ads', []):
                total_reach += ad.get('reach', 0)
                total_engagement += ad.get('engagement_rate', 0) * ad.get('reach', 0)
                total_spend += ad.get('spend', 0)
        
        avg_engagement_rate = total_engagement / total_reach if total_reach > 0 else 0
        
        # Store categories
        categories = {}
        for product in products:
            category = product.get('category', 'unknown')
            categories[category] = categories.get(category, 0) + 1
        
        # Store sources
        sources = {}
        for product in products:
            source = product.get('source_store', 'unknown')
            sources[source] = sources.get(source, 0) + 1
        
        return {
            "success": True,
            "data": {
                "store_info": {
                    "name": "Dropship Intelligence Store",
                    "description": "Premium dropshipping product store with AI-powered insights",
                    "established": "2024",
                    "total_products": total_products,
                    "total_value": round(total_value, 2),
                    "average_price": round(avg_price, 2)
                },
                "performance": {
                    "total_facebook_ads": total_facebook_ads,
                    "total_tiktok_mentions": total_tiktok_mentions,
                    "total_reach": total_reach,
                    "total_spend": round(total_spend, 2),
                    "average_engagement_rate": round(avg_engagement_rate, 4)
                },
                "categories": categories,
                "sources": sources,
                "last_updated": datetime.utcnow().isoformat()
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting store overview: {e}")
        raise HTTPException(status_code=500, detail="Failed to get store overview")

@router.get("/products")
async def get_store_products(
    category: Optional[str] = Query(None, description="Filter by category"),
    source: Optional[str] = Query(None, description="Filter by source store"),
    min_score: Optional[float] = Query(None, description="Minimum score"),
    max_price: Optional[float] = Query(None, description="Maximum price"),
    sort_by: str = Query("score", description="Sort by field"),
    sort_order: int = Query(-1, description="Sort order (-1 for descending, 1 for ascending)"),
    page: int = Query(1, description="Page number"),
    limit: int = Query(20, description="Items per page")
):
    """Get store products with filtering and pagination"""
    try:
        products = list(memory_storage.products.values())
        
        # Apply filters
        if category:
            products = [p for p in products if p.get('category') == category]
        
        if source:
            products = [p for p in products if p.get('source_store') == source]
        
        if min_score is not None:
            products = [p for p in products if p.get('score', 0) >= min_score]
        
        if max_price is not None:
            products = [p for p in products if p.get('price', 0) <= max_price]
        
        # Sort products
        reverse = sort_order == -1
        if sort_by == "score":
            products.sort(key=lambda x: x.get('score', 0), reverse=reverse)
        elif sort_by == "price":
            products.sort(key=lambda x: x.get('price', 0), reverse=reverse)
        elif sort_by == "title":
            products.sort(key=lambda x: x.get('title', ''), reverse=reverse)
        elif sort_by == "created_at":
            products.sort(key=lambda x: x.get('created_at', datetime.min), reverse=reverse)
        
        # Pagination
        total = len(products)
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        paginated_products = products[start_idx:end_idx]
        
        return {
            "success": True,
            "data": {
                "products": paginated_products,
                "pagination": {
                    "page": page,
                    "limit": limit,
                    "total": total,
                    "pages": (total + limit - 1) // limit
                }
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting store products: {e}")
        raise HTTPException(status_code=500, detail="Failed to get store products")

@router.get("/categories")
async def get_store_categories():
    """Get all store categories with statistics"""
    try:
        products = list(memory_storage.products.values())
        
        categories = {}
        for product in products:
            category = product.get('category', 'unknown')
            if category not in categories:
                categories[category] = {
                    'count': 0,
                    'total_value': 0,
                    'avg_price': 0,
                    'avg_score': 0,
                    'total_engagement': 0
                }
            
            categories[category]['count'] += 1
            categories[category]['total_value'] += product.get('price', 0)
            categories[category]['avg_score'] += product.get('score', 0)
            
            # Calculate engagement for this product
            product_engagement = 0
            for ad in product.get('facebook_ads', []):
                product_engagement += ad.get('engagement_rate', 0) * ad.get('reach', 0)
            categories[category]['total_engagement'] += product_engagement
        
        # Calculate averages
        for category in categories:
            count = categories[category]['count']
            if count > 0:
                categories[category]['avg_price'] = round(categories[category]['total_value'] / count, 2)
                categories[category]['avg_score'] = round(categories[category]['avg_score'] / count, 2)
                categories[category]['total_value'] = round(categories[category]['total_value'], 2)
        
        return {
            "success": True,
            "data": {
                "categories": categories,
                "total_categories": len(categories)
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting store categories: {e}")
        raise HTTPException(status_code=500, detail="Failed to get store categories")

@router.get("/sources")
async def get_store_sources():
    """Get all store sources with statistics"""
    try:
        products = list(memory_storage.products.values())
        
        sources = {}
        for product in products:
            source = product.get('source_store', 'unknown')
            if source not in sources:
                sources[source] = {
                    'count': 0,
                    'total_value': 0,
                    'avg_price': 0,
                    'avg_score': 0,
                    'categories': set()
                }
            
            sources[source]['count'] += 1
            sources[source]['total_value'] += product.get('price', 0)
            sources[source]['avg_score'] += product.get('score', 0)
            sources[source]['categories'].add(product.get('category', 'unknown'))
        
        # Calculate averages and convert sets to lists
        for source in sources:
            count = sources[source]['count']
            if count > 0:
                sources[source]['avg_price'] = round(sources[source]['total_value'] / count, 2)
                sources[source]['avg_score'] = round(sources[source]['avg_score'] / count, 2)
                sources[source]['total_value'] = round(sources[source]['total_value'], 2)
                sources[source]['categories'] = list(sources[source]['categories'])
        
        return {
            "success": True,
            "data": {
                "sources": sources,
                "total_sources": len(sources)
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting store sources: {e}")
        raise HTTPException(status_code=500, detail="Failed to get store sources")

@router.get("/performance")
async def get_store_performance():
    """Get store performance metrics"""
    try:
        products = list(memory_storage.products.values())
        
        # Performance metrics
        performance = {
            'total_products': len(products),
            'high_score_products': len([p for p in products if p.get('score', 0) >= 80]),
            'medium_score_products': len([p for p in products if 60 <= p.get('score', 0) < 80]),
            'low_score_products': len([p for p in products if p.get('score', 0) < 60]),
            'total_facebook_ads': 0,
            'total_tiktok_mentions': 0,
            'total_reach': 0,
            'total_spend': 0,
            'avg_engagement_rate': 0
        }
        
        # Calculate social media metrics
        total_engagement = 0
        for product in products:
            performance['total_facebook_ads'] += len(product.get('facebook_ads', []))
            performance['total_tiktok_mentions'] += len(product.get('tiktok_mentions', []))
            
            for ad in product.get('facebook_ads', []):
                performance['total_reach'] += ad.get('reach', 0)
                performance['total_spend'] += ad.get('spend', 0)
                total_engagement += ad.get('engagement_rate', 0) * ad.get('reach', 0)
        
        if performance['total_reach'] > 0:
            performance['avg_engagement_rate'] = round(total_engagement / performance['total_reach'], 4)
        
        performance['total_spend'] = round(performance['total_spend'], 2)
        
        return {
            "success": True,
            "data": performance
        }
        
    except Exception as e:
        logger.error(f"Error getting store performance: {e}")
        raise HTTPException(status_code=500, detail="Failed to get store performance") 