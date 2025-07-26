from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any, List, Optional
import logging

from ...database.models import AIRewriteRequest
from ...ai.writer import AIWriter
from ...database.memory_storage import memory_storage

logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize AI writer
ai_writer = AIWriter()

@router.post("/rewrite-title")
async def rewrite_title(request: AIRewriteRequest):
    """Rewrite product title for better virality"""
    try:
        if request.purpose != "title":
            raise HTTPException(status_code=400, detail="Purpose must be 'title' for this endpoint")
        
        # Check if API keys are configured
        if not hasattr(ai_writer, '_has_api_keys') or not ai_writer._has_api_keys():
            raise HTTPException(status_code=503, detail="AI service not configured. Please configure API keys.")
        
        # Call AI writer
        result = await ai_writer.rewrite_title(
            original_title=request.text,
            category="general",  # Could be extracted from request
            tone=request.tone
        )
        
        if not result.get("success"):
            raise HTTPException(status_code=500, detail=result.get("error", "AI service error"))
        
        return {
            "success": True,
            "original": request.text,
            "titles": result.get("titles", []),
            "tone": request.tone
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error rewriting title: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/write-ad-copy")
async def write_ad_copy(request: Dict[str, Any]):
    """Generate Facebook ad copy for a product"""
    try:
        product_title = request.get("product_title")
        category = request.get("category", "general")
        price = request.get("price", 0.0)
        target_audience = request.get("target_audience", "general")
        
        if not product_title:
            raise HTTPException(status_code=400, detail="product_title is required")
        
        # Check if API keys are configured
        if not hasattr(ai_writer, '_has_api_keys') or not ai_writer._has_api_keys():
            raise HTTPException(status_code=503, detail="AI service not configured. Please configure API keys.")
        
        # Call AI writer
        result = await ai_writer.write_ad_copy(
            product_title=product_title,
            category=category,
            price=price,
            target_audience=target_audience
        )
        
        if not result.get("success"):
            raise HTTPException(status_code=500, detail=result.get("error", "AI service error"))
        
        return {
            "success": True,
            "product_title": product_title,
            "ads": result.get("ads", [])
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error writing ad copy: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/write-description")
async def write_description(request: Dict[str, Any]):
    """Generate product description optimized for conversion"""
    try:
        product_title = request.get("product_title")
        category = request.get("category", "general")
        features = request.get("features", [])
        
        if not product_title:
            raise HTTPException(status_code=400, detail="product_title is required")
        
        # Check if API keys are configured
        if not hasattr(ai_writer, '_has_api_keys') or not ai_writer._has_api_keys():
            raise HTTPException(status_code=503, detail="AI service not configured. Please configure API keys.")
        
        # Call AI writer
        result = await ai_writer.write_description(
            product_title=product_title,
            category=category,
            features=features
        )
        
        if not result.get("success"):
            raise HTTPException(status_code=500, detail=result.get("error", "AI service error"))
        
        return {
            "success": True,
            "product_title": product_title,
            "description": result.get("description", "")
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error writing description: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/explain-why-winning")
async def explain_why_winning(request: Dict[str, Any]):
    """Explain why a product is likely to be a winning dropshipping product"""
    try:
        product_data = request.get("product_data")
        
        if not product_data:
            raise HTTPException(status_code=400, detail="product_data is required")
        
        # Check if API keys are configured
        if not hasattr(ai_writer, '_has_api_keys') or not ai_writer._has_api_keys():
            raise HTTPException(status_code=503, detail="AI service not configured. Please configure API keys.")
        
        # Call AI writer
        result = await ai_writer.explain_why_winning(product_data)
        
        if not result.get("success"):
            raise HTTPException(status_code=500, detail=result.get("error", "AI service error"))
        
        return {
            "success": True,
            "product_title": product_data.get('title', 'Product'),
            "analysis": result.get("analysis", "")
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error explaining why winning: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/generate-keywords")
async def generate_seo_keywords(request: Dict[str, Any]):
    """Generate SEO keywords for a product"""
    try:
        title = request.get('title', '')
        category = request.get('category', '')
        
        if not title:
            raise HTTPException(status_code=400, detail="Title is required")
        
        # Generate keywords based on title and category
        base_keywords = title.lower().split()
        category_keywords = [category.lower()] if category else []
        
        # Add common dropshipping keywords
        dropshipping_keywords = [
            "best seller", "trending", "hot", "popular", "viral",
            "must have", "essential", "premium", "quality", "affordable"
        ]
        
        # Add platform-specific keywords
        platform_keywords = [
            "amazon", "aliexpress", "temu", "ebay", "shopify",
            "dropshipping", "wholesale", "bulk", "discount"
        ]
        
        all_keywords = base_keywords + category_keywords + dropshipping_keywords + platform_keywords
        
        # Remove duplicates and common words
        common_words = {'the', 'and', 'or', 'for', 'with', 'in', 'on', 'at', 'to', 'of', 'a', 'an'}
        filtered_keywords = [kw for kw in all_keywords if kw not in common_words and len(kw) > 2]
        
        # Get unique keywords
        unique_keywords = list(set(filtered_keywords))[:15]
        
        return {
            "success": True,
            "data": {
                "product_title": title,
                "primary_keywords": unique_keywords[:5],
                "secondary_keywords": unique_keywords[5:10],
                "long_tail_keywords": unique_keywords[10:],
                "keyword_suggestions": [
                    f"best {title.lower()}",
                    f"{title.lower()} review",
                    f"buy {title.lower()}",
                    f"{title.lower()} price",
                    f"where to buy {title.lower()}"
                ]
            }
        }
    except Exception as e:
        logger.error(f"Error generating keywords: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate keywords")

@router.post("/analyze-trends")
async def analyze_product_trends(request: Dict[str, Any]):
    """Analyze product trends and market insights"""
    try:
        keyword = request.get('keyword', '')
        category = request.get('category', '')
        
        if not keyword and not category:
            raise HTTPException(status_code=400, detail="Keyword or category is required")
        
        # Get products for analysis
        products = list(memory_storage.products.values())
        relevant_products = []
        
        if keyword:
            relevant_products = [p for p in products if keyword.lower() in p.get('title', '').lower()]
        elif category:
            relevant_products = [p for p in products if p.get('category') == category]
        
        # Analyze trends
        if relevant_products:
            avg_score = sum(p.get('score', 0) for p in relevant_products) / len(relevant_products)
            avg_price = sum(p.get('price', 0) for p in relevant_products) / len(relevant_products)
            total_engagement = sum(len(p.get('facebook_ads', [])) for p in relevant_products)
        else:
            avg_score = 0
            avg_price = 0
            total_engagement = 0
        
        trend_analysis = {
            "keyword": keyword or category,
            "total_products": len(relevant_products),
            "average_score": round(avg_score, 2),
            "average_price": round(avg_price, 2),
            "total_engagement": total_engagement,
            "trend_status": "Rising" if avg_score > 70 else "Stable" if avg_score > 50 else "Declining",
            "market_insights": [
                f"Average price point: ${avg_price}",
                f"Market demand: {'High' if avg_score > 70 else 'Medium' if avg_score > 50 else 'Low'}",
                f"Competition level: {'High' if len(relevant_products) > 10 else 'Medium' if len(relevant_products) > 5 else 'Low'}"
            ]
        }
        
        return {
            "success": True,
            "data": trend_analysis
        }
    except Exception as e:
        logger.error(f"Error analyzing trends: {e}")
        raise HTTPException(status_code=500, detail="Failed to analyze trends")

@router.get("/ai-insights")
async def get_ai_insights():
    """Get AI-powered insights for the entire store"""
    try:
        products = list(memory_storage.products.values())
        
        if not products:
            return {
                "success": True,
                "data": {
                    "message": "No products available for analysis"
                }
            }
        
        # Calculate insights
        total_products = len(products)
        avg_score = sum(p.get('score', 0) for p in products) / total_products
        avg_price = sum(p.get('price', 0) for p in products) / total_products
        
        # Category performance
        category_performance = {}
        for product in products:
            category = product.get('category', 'unknown')
            if category not in category_performance:
                category_performance[category] = {'count': 0, 'total_score': 0}
            category_performance[category]['count'] += 1
            category_performance[category]['total_score'] += product.get('score', 0)
        
        # Find best performing category
        best_category = max(category_performance.items(), key=lambda x: x[1]['total_score'] / x[1]['count'])[0]
        
        # Price optimization insights
        price_insights = {
            'budget_products': len([p for p in products if p.get('price', 0) < 20]),
            'mid_range_products': len([p for p in products if 20 <= p.get('price', 0) < 50]),
            'premium_products': len([p for p in products if p.get('price', 0) >= 50])
        }
        
        insights = {
            "store_overview": {
                "total_products": total_products,
                "average_score": round(avg_score, 2),
                "average_price": round(avg_price, 2),
                "overall_performance": "Excellent" if avg_score > 80 else "Good" if avg_score > 60 else "Average"
            },
            "recommendations": [
                f"Focus on {best_category} category for best performance",
                f"Optimize pricing strategy around ${avg_price}",
                f"Enhance product descriptions for better SEO",
                "Increase social media presence for better engagement"
            ],
            "category_performance": category_performance,
            "price_optimization": price_insights,
            "ai_suggestions": [
                "Consider adding more products in the $20-50 range",
                "Focus on high-scoring products for marketing campaigns",
                "Use trending keywords in product titles",
                "Implement A/B testing for product descriptions"
            ]
        }
        
        return {
            "success": True,
            "data": insights
        }
    except Exception as e:
        logger.error(f"Error getting AI insights: {e}")
        raise HTTPException(status_code=500, detail="Failed to get AI insights") 