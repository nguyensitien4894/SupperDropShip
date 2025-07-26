from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import logging

from backend.database.models import AIRewriteRequest
from backend.ai.writer import AIWriter

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
        
        # For demo purposes, we'll use a mock response if no API keys are configured
        if not hasattr(ai_writer, '_has_api_keys') or not ai_writer._has_api_keys():
            mock_titles = [
                f"🔥 {request.text} - LIMITED TIME OFFER!",
                f"AMAZING {request.text.upper()} - MUST SEE!",
                f"Best {request.text} - 50% OFF Today Only!"
            ]
            return {
                "success": True,
                "original": request.text,
                "titles": mock_titles,
                "tone": request.tone,
                "message": "Mock titles generated (no API keys configured)"
            }
        
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
        
        # For demo purposes, we'll use a mock response if no API keys are configured
        if not hasattr(ai_writer, '_has_api_keys') or not ai_writer._has_api_keys():
            mock_ads = [
                {
                    "primary_text": f"🔥 {product_title} is going VIRAL! Don't miss out!",
                    "headline": f"Amazing {product_title} - 50% OFF!",
                    "description": "Limited time offer! Get yours today!"
                },
                {
                    "primary_text": f"Everyone is talking about this {product_title}!",
                    "headline": f"Trending {product_title} - Must Have!",
                    "description": "Join thousands of happy customers!"
                },
                {
                    "primary_text": f"Transform your life with this {product_title}!",
                    "headline": f"Revolutionary {product_title} - Game Changer!",
                    "description": "See why everyone loves it!"
                }
            ]
            return {
                "success": True,
                "product_title": product_title,
                "ads": mock_ads,
                "message": "Mock ad copy generated (no API keys configured)"
            }
        
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
        
        # For demo purposes, we'll use a mock response if no API keys are configured
        if not hasattr(ai_writer, '_has_api_keys') or not ai_writer._has_api_keys():
            mock_description = f"""
🔥 {product_title.upper()} - THE ULTIMATE GAME CHANGER! 🔥

Are you ready to experience something AMAZING? This {product_title} is taking the world by storm and for good reason!

✨ WHY EVERYONE LOVES IT:
• Revolutionary design that stands out
• Premium quality materials
• Incredible value for money
• Perfect for {category} enthusiasts

💥 LIMITED TIME OFFER - Don't wait!
Thousands of satisfied customers can't be wrong. Join the revolution today!

🚀 ORDER NOW and transform your life with this incredible {product_title}!
            """.strip()
            
            return {
                "success": True,
                "product_title": product_title,
                "description": mock_description,
                "message": "Mock description generated (no API keys configured)"
            }
        
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
        
        # For demo purposes, we'll use a mock response if no API keys are configured
        if not hasattr(ai_writer, '_has_api_keys') or not ai_writer._has_api_keys():
            mock_analysis = f"""
🎯 WINNING ANALYSIS: {product_data.get('title', 'Product')}

✅ KEY STRENGTHS:
• Strong social media presence with {len(product_data.get('facebook_ads', []))} Facebook ads
• Viral potential with {len(product_data.get('tiktok_mentions', []))} TikTok mentions
• Good profit margin potential
• Trending keyword with {product_data.get('trend_data', {}).get('trend_score', 0)}/100 trend score

⚠️ POTENTIAL CHALLENGES:
• Market competition level
• Seasonal demand considerations

📈 RECOMMENDED STRATEGY:
• Focus on TikTok marketing
• Use Facebook ads for retargeting
• Optimize pricing strategy
• Target {product_data.get('category', 'general')} audience

💰 PRICE OPTIMIZATION:
• Current price: ${product_data.get('price', 0)}
• Consider A/B testing different price points
• Monitor competitor pricing

🎯 TARGET AUDIENCE:
• Primary: {product_data.get('category', 'general')} enthusiasts
• Secondary: Social media savvy consumers
• Age: 18-45 demographic
            """.strip()
            
            return {
                "success": True,
                "product_title": product_data.get('title', 'Product'),
                "analysis": mock_analysis,
                "message": "Mock analysis generated (no API keys configured)"
            }
        
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