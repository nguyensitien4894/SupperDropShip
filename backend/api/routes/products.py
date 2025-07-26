from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
import logging
from ..dependencies import get_current_user
from ...database.repository import product_repository
from ...database.models import Product, ProductsResponse, ProductResponse, CrawlRequest
from ...scoring.engine import ScoringEngine

logger = logging.getLogger(__name__)
router = APIRouter()

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
        
        # Get products from database
        products = await product_repository.get_products(
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
        
        total = await product_repository.get_products_count(filter_query)
        
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
        product = await product_repository.get_product(product_id)
        
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
        
        created_product = await product_repository.create_product(product)
        
        return ProductResponse(
            success=True,
            data=created_product,
            message="Product created successfully"
        )
        
    except Exception as e:
        logger.error(f"Failed to create product: {e}")
        raise HTTPException(status_code=500, detail="Failed to create product")

@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(product_id: str, product_update: dict):
    """Update a product"""
    try:
        updated_product = await product_repository.update_product(product_id, product_update)
        
        if not updated_product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return ProductResponse(
            success=True,
            data=updated_product,
            message="Product updated successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update product {product_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to update product")

@router.delete("/{product_id}")
async def delete_product(product_id: str):
    """Delete a product"""
    try:
        success = await product_repository.delete_product(product_id)
        
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
    """Get all available categories"""
    try:
        categories = await product_repository.get_categories()
        return {"success": True, "data": categories}
        
    except Exception as e:
        logger.error(f"Failed to get categories: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve categories")

@router.get("/tags/list")
async def get_tags():
    """Get all available tags"""
    try:
        tags = await product_repository.get_tags()
        return {"success": True, "data": tags}
        
    except Exception as e:
        logger.error(f"Failed to get tags: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve tags")

@router.get("/stats/overview")
async def get_stats():
    """Get product statistics"""
    try:
        stats = await product_repository.get_stats()
        return {"success": True, "data": stats}
        
    except Exception as e:
        logger.error(f"Failed to get stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve statistics")

@router.post("/bulk/import")
async def bulk_import_products(products: List[Product]):
    """Bulk import products"""
    try:
        created_products = []
        scoring_engine = ScoringEngine()
        
        for product in products:
            # Calculate score if not provided
            if product.score == 0:
                product.score = scoring_engine.calculate_score(product)
            
            created_product = await product_repository.create_product(product)
            created_products.append(created_product)
        
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
        products = await product_repository.get_products(
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