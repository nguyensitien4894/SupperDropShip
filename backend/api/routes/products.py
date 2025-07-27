from fastapi import APIRouter, HTTPException, Query, Depends, BackgroundTasks
from typing import List, Optional
from datetime import datetime
import logging
import asyncio
from ..dependencies import get_current_user
from ...database.memory_storage import memory_storage
from ...database.models import Product, ProductsResponse, ProductResponse, CrawlRequest
from ...scoring.engine import ScoringEngine
from ...crawlers.crawler_manager import crawler_manager
from ...crawlers.cache_manager import crawler_cache

logger = logging.getLogger(__name__)
router = APIRouter()

# Global variable to track background crawl status
background_crawl_task = None

@router.get("/", response_model=ProductsResponse)
async def get_products(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(50, ge=1, le=100, description="Items per page"),
    category: Optional[str] = Query(None, description="Filter by category"),
    min_score: Optional[float] = Query(None, ge=0, le=100, description="Minimum score"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price"),
    search: Optional[str] = Query(None, description="Search term"),
    tags: Optional[str] = Query(None, description="Comma-separated tags"),
    sort_by: str = Query("score", description="Sort field"),
    sort_order: int = Query(-1, description="Sort order (-1 for desc, 1 for asc)")
):
    """Get products with filtering and pagination"""
    try:
        # Parse tags
        tag_list = None
        if tags:
            tag_list = [tag.strip() for tag in tags.split(",") if tag.strip()]
        
        # Calculate skip
        skip = (page - 1) * limit
        
        # Get products from memory storage
        products = await memory_storage.get_products(
            skip=skip,
            limit=limit,
            category=category,
            min_score=min_score,
            max_price=max_price,
            search_term=search,
            tags=tag_list,
            sort_by=sort_by,
            sort_order=sort_order
        )
        
        # Get total count for pagination
        filter_query = {}
        if category and category != "all":
            filter_query["category"] = category
        if min_score is not None:
            filter_query["score"] = {"$gte": min_score}
        if max_price is not None:
            if "score" in filter_query:
                filter_query["score"]["$lte"] = max_price
            else:
                filter_query["price"] = {"$lte": max_price}
        if tag_list:
            filter_query["tags"] = {"$in": tag_list}
        
        total = await memory_storage.get_products_count(filter_query)
        
        return ProductsResponse(
            success=True,
            data=products,
            total=total,
            page=page,
            limit=limit
        )
        
    except Exception as e:
        logger.error(f"Failed to get products: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve products")

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: str):
    """Get a specific product by ID"""
    try:
        product = await memory_storage.get_product(product_id)
        
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return ProductResponse(success=True, data=product)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get product {product_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve product")

@router.post("/", response_model=ProductResponse)
async def create_product(product: Product):
    """Create a new product"""
    try:
        # Calculate score if not provided
        if product.score == 0:
            scoring_engine = ScoringEngine()
            product.score = scoring_engine.calculate_score(product)
        
        # Add to memory storage
        await memory_storage.add_product(product)
        
        return ProductResponse(success=True, data=product)
        
    except Exception as e:
        logger.error(f"Failed to create product: {e}")
        raise HTTPException(status_code=500, detail="Failed to create product")

@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(product_id: str, product_update: dict):
    """Update an existing product"""
    try:
        updated_product = await memory_storage.update_product(product_id, product_update)
        
        if not updated_product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return ProductResponse(success=True, data=updated_product)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update product {product_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to update product")

@router.delete("/{product_id}")
async def delete_product(product_id: str):
    """Delete a product"""
    try:
        success = await memory_storage.delete_product(product_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return {"success": True, "message": "Product deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete product {product_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete product")

@router.get("/categories/list")
async def get_categories():
    """Get list of all product categories"""
    try:
        categories = await memory_storage.get_categories()
        return {"success": True, "data": categories}
        
    except Exception as e:
        logger.error(f"Failed to get categories: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve categories")

@router.get("/tags/list")
async def get_tags():
    """Get list of all product tags"""
    try:
        tags = await memory_storage.get_tags()
        return {"success": True, "data": tags}
        
    except Exception as e:
        logger.error(f"Failed to get tags: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve tags")

@router.get("/stats/overview")
async def get_stats():
    """Get product statistics overview"""
    try:
        stats = await memory_storage.get_stats()
        return {"success": True, "data": stats}
        
    except Exception as e:
        logger.error(f"Failed to get stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve stats")

@router.post("/bulk/import")
async def bulk_import_products(products: List[Product]):
    """Bulk import products"""
    try:
        created_products = []
        
        for product in products:
            try:
                # Calculate score if not provided
                if product.score == 0:
                    scoring_engine = ScoringEngine()
                    product.score = scoring_engine.calculate_score(product)
                
                await memory_storage.add_product(product)
                created_products.append(product)
                
            except Exception as e:
                logger.error(f"Error importing product {product.title}: {e}")
                continue
        
        return {
            "success": True,
            "message": f"Successfully imported {len(created_products)} products",
            "data": created_products
        }
        
    except Exception as e:
        logger.error(f"Failed to bulk import products: {e}")
        raise HTTPException(status_code=500, detail="Failed to import products")

@router.post("/search/advanced")
async def advanced_search(request: CrawlRequest):
    """Advanced product search with multiple criteria"""
    try:
        # Build filter query based on request
        filter_query = {}
        
        if request.category:
            filter_query["category"] = request.category
            
        if request.min_score is not None:
            filter_query["score"] = {"$gte": request.min_score}
            
        if request.max_price is not None:
            if "score" in filter_query:
                filter_query["score"]["$lte"] = request.max_price
            else:
                filter_query["price"] = {"$lte": request.max_price}
        
        # Get products
        products = await memory_storage.get_products(
            limit=request.limit,
            category=request.category.value if request.category else None,
            min_score=request.min_score,
            max_price=request.max_price,
            sort_by="score",
            sort_order=-1
        )
        
        # Filter by keywords if provided
        if request.keywords:
            filtered_products = []
            for product in products:
                product_text = f"{product.title} {product.description} {' '.join(product.tags)}".lower()
                if any(keyword.lower() in product_text for keyword in request.keywords):
                    filtered_products.append(product)
            products = filtered_products
        
        return ProductsResponse(
            success=True,
            data=products,
            total=len(products),
            page=1,
            limit=len(products)
        )
        
    except Exception as e:
        logger.error(f"Failed to perform advanced search: {e}")
        raise HTTPException(status_code=500, detail="Failed to perform search")

@router.post("/crawl/start")
async def start_product_crawl(max_products_per_source: int = 30):
    """Start crawling products from various sources (blocking)"""
    try:
        logger.info(f"Starting optimized product crawl with {max_products_per_source} products per source")
        
        # Run the crawler
        async with crawler_manager:
            products = await crawler_manager.run_full_crawl(max_products_per_source)
        
        return {
            "success": True, 
            "message": f"Successfully crawled {len(products)} products from multiple sources",
            "data": {
                "total_products": len(products),
                "products_added": len(products)
            }
        }
        
    except Exception as e:
        logger.error(f"Error during product crawl: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to crawl products: {str(e)}")

@router.post("/crawl/background")
async def start_background_crawl(max_products_per_source: int = 30):
    """Start crawling products in background (non-blocking)"""
    global background_crawl_task
    
    if background_crawl_task and not background_crawl_task.done():
        raise HTTPException(status_code=409, detail="Background crawl already in progress")
    
    async def run_background_crawl():
        global background_crawl_task
        try:
            async with crawler_manager:
                await crawler_manager.run_full_crawl(max_products_per_source)
            logger.info("Background crawl completed successfully")
        except Exception as e:
            logger.error(f"Background crawl failed: {e}")
        finally:
            background_crawl_task = None
    
    background_crawl_task = asyncio.create_task(run_background_crawl())
    
    return {
        "success": True,
        "message": "Background crawl started successfully",
        "data": {
            "status": "started",
            "max_products_per_source": max_products_per_source
        }
    }

@router.get("/crawl/progress")
async def get_crawl_progress():
    """Get current crawl progress"""
    try:
        progress = crawler_manager.get_crawl_progress()
        return {
            "success": True,
            "data": progress
        }
        
    except Exception as e:
        logger.error(f"Error getting crawl progress: {e}")
        raise HTTPException(status_code=500, detail="Failed to get crawl progress")

@router.get("/crawl/status")
async def get_crawl_status():
    """Get current crawl status and product count"""
    try:
        total_products = len(memory_storage.products)
        
        # Check if background crawl is running
        background_status = "idle"
        if background_crawl_task and not background_crawl_task.done():
            background_status = "running"
        elif background_crawl_task and background_crawl_task.done():
            background_status = "completed"
        
        return {
            "success": True,
            "data": {
                "total_products": total_products,
                "last_updated": datetime.utcnow().isoformat(),
                "status": "ready",
                "background_crawl_status": background_status
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting crawl status: {e}")
        raise HTTPException(status_code=500, detail="Failed to get crawl status")

@router.get("/cache/stats")
async def get_cache_stats():
    """Get cache statistics"""
    try:
        stats = crawler_cache.get_cache_stats()
        return {
            "success": True,
            "data": stats
        }
        
    except Exception as e:
        logger.error(f"Error getting cache stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to get cache stats")

@router.delete("/cache/clear")
async def clear_cache(cache_type: Optional[str] = None):
    """Clear cache"""
    try:
        deleted_count = crawler_cache.clear(cache_type)
        return {
            "success": True,
            "message": f"Cleared {deleted_count} cache files",
            "data": {
                "deleted_count": deleted_count,
                "cache_type": cache_type or "all"
            }
        }
        
    except Exception as e:
        logger.error(f"Error clearing cache: {e}")
        raise HTTPException(status_code=500, detail="Failed to clear cache")

@router.post("/cache/cleanup")
async def cleanup_expired_cache():
    """Clean up expired cache files"""
    try:
        deleted_count = crawler_cache.cleanup_expired()
        return {
            "success": True,
            "message": f"Cleaned up {deleted_count} expired cache files",
            "data": {
                "deleted_count": deleted_count
            }
        }
        
    except Exception as e:
        logger.error(f"Error cleaning up expired cache: {e}")
        raise HTTPException(status_code=500, detail="Failed to cleanup expired cache") 