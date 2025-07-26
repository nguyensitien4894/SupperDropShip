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
async def get_analytics_overview():
    """Get comprehensive analytics overview"""
    try:
        products = list(memory_storage.products.values())
        
        # Calculate basic metrics
        total_products = len(products)
        total_value = sum(p.get('price', 0) for p in products)
        avg_price = total_value / total_products if total_products > 0 else 0
        
        # Score distribution
        score_ranges = {
            'excellent': len([p for p in products if p.get('score', 0) >= 80]),
            'good': len([p for p in products if 60 <= p.get('score', 0) < 80]),
            'average': len([p for p in products if 40 <= p.get('score', 0) < 60]),
            'poor': len([p for p in products if p.get('score', 0) < 40])
        }
        
        # Category distribution
        categories = {}
        for product in products:
            category = product.get('category', 'unknown')
            categories[category] = categories.get(category, 0) + 1
        
        # Top performing products
        top_products = sorted(products, key=lambda x: x.get('score', 0), reverse=True)[:10]
        
        # Social media metrics
        total_facebook_ads = sum(len(p.get('facebook_ads', [])) for p in products)
        total_tiktok_mentions = sum(len(p.get('tiktok_mentions', [])) for p in products)
        
        # Engagement metrics
        total_engagement = 0
        total_reach = 0
        total_spend = 0
        
        for product in products:
            for ad in product.get('facebook_ads', []):
                total_engagement += ad.get('engagement_rate', 0) * ad.get('reach', 0)
                total_reach += ad.get('reach', 0)
                total_spend += ad.get('spend', 0)
        
        avg_engagement_rate = total_engagement / total_reach if total_reach > 0 else 0
        
        return {
            "success": True,
            "data": {
                "overview": {
                    "total_products": total_products,
                    "total_value": round(total_value, 2),
                    "average_price": round(avg_price, 2),
                    "total_facebook_ads": total_facebook_ads,
                    "total_tiktok_mentions": total_tiktok_mentions,
                    "total_reach": total_reach,
                    "total_spend": round(total_spend, 2),
                    "average_engagement_rate": round(avg_engagement_rate, 4)
                },
                "score_distribution": score_ranges,
                "category_distribution": categories,
                "top_products": [
                    {
                        "id": p.get('id'),
                        "title": p.get('title'),
                        "score": p.get('score'),
                        "price": p.get('price'),
                        "category": p.get('category')
                    } for p in top_products
                ]
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting analytics overview: {e}")
        raise HTTPException(status_code=500, detail="Failed to get analytics overview")

@router.get("/trends")
async def get_trend_analytics():
    """Get trend analytics data"""
    try:
        products = list(memory_storage.products.values())
        
        # Trend analysis by category
        category_trends = {}
        for product in products:
            category = product.get('category', 'unknown')
            if category not in category_trends:
                category_trends[category] = {
                    'count': 0,
                    'avg_score': 0,
                    'avg_price': 0,
                    'total_engagement': 0
                }
            
            category_trends[category]['count'] += 1
            category_trends[category]['avg_score'] += product.get('score', 0)
            category_trends[category]['avg_price'] += product.get('price', 0)
            
            # Calculate engagement for this product
            product_engagement = 0
            for ad in product.get('facebook_ads', []):
                product_engagement += ad.get('engagement_rate', 0) * ad.get('reach', 0)
            category_trends[category]['total_engagement'] += product_engagement
        
        # Calculate averages
        for category in category_trends:
            count = category_trends[category]['count']
            if count > 0:
                category_trends[category]['avg_score'] = round(category_trends[category]['avg_score'] / count, 2)
                category_trends[category]['avg_price'] = round(category_trends[category]['avg_price'] / count, 2)
        
        # Price range analysis
        price_ranges = {
            'budget': len([p for p in products if p.get('price', 0) < 20]),
            'mid_range': len([p for p in products if 20 <= p.get('price', 0) < 50]),
            'premium': len([p for p in products if p.get('price', 0) >= 50])
        }
        
        # Source store analysis
        source_analysis = {}
        for product in products:
            source = product.get('source_store', 'unknown')
            if source not in source_analysis:
                source_analysis[source] = 0
            source_analysis[source] += 1
        
        return {
            "success": True,
            "data": {
                "category_trends": category_trends,
                "price_ranges": price_ranges,
                "source_analysis": source_analysis,
                "trending_keywords": [
                    "bluetooth", "wireless", "portable", "smart", "rechargeable",
                    "waterproof", "led", "usb", "cable", "charger"
                ]
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting trend analytics: {e}")
        raise HTTPException(status_code=500, detail="Failed to get trend analytics")

@router.get("/performance")
async def get_performance_metrics():
    """Get detailed performance metrics"""
    try:
        products = list(memory_storage.products.values())
        
        # Facebook Ads performance
        facebook_metrics = {
            'total_ads': 0,
            'total_reach': 0,
            'total_impressions': 0,
            'total_clicks': 0,
            'total_spend': 0,
            'avg_engagement_rate': 0,
            'avg_ctr': 0,
            'avg_cpc': 0
        }
        
        # TikTok performance
        tiktok_metrics = {
            'total_videos': 0,
            'total_views': 0,
            'total_likes': 0,
            'total_shares': 0,
            'total_comments': 0,
            'avg_engagement_rate': 0
        }
        
        for product in products:
            # Facebook metrics
            for ad in product.get('facebook_ads', []):
                facebook_metrics['total_ads'] += 1
                facebook_metrics['total_reach'] += ad.get('reach', 0)
                facebook_metrics['total_impressions'] += ad.get('impressions', 0)
                facebook_metrics['total_clicks'] += ad.get('clicks', 0)
                facebook_metrics['total_spend'] += ad.get('spend', 0)
            
            # TikTok metrics
            for video in product.get('tiktok_mentions', []):
                tiktok_metrics['total_videos'] += 1
                tiktok_metrics['total_views'] += video.get('views', 0)
                tiktok_metrics['total_likes'] += video.get('likes', 0)
                tiktok_metrics['total_shares'] += video.get('shares', 0)
                tiktok_metrics['total_comments'] += video.get('comments', 0)
        
        # Calculate averages
        if facebook_metrics['total_ads'] > 0:
            facebook_metrics['avg_engagement_rate'] = round(
                sum(ad.get('engagement_rate', 0) for p in products for ad in p.get('facebook_ads', [])) / facebook_metrics['total_ads'], 4
            )
            facebook_metrics['avg_ctr'] = round(facebook_metrics['total_clicks'] / facebook_metrics['total_impressions'], 4)
            facebook_metrics['avg_cpc'] = round(facebook_metrics['total_spend'] / facebook_metrics['total_clicks'], 2) if facebook_metrics['total_clicks'] > 0 else 0
        
        if tiktok_metrics['total_videos'] > 0:
            total_engagement = tiktok_metrics['total_likes'] + tiktok_metrics['total_shares'] + tiktok_metrics['total_comments']
            tiktok_metrics['avg_engagement_rate'] = round(total_engagement / tiktok_metrics['total_views'], 4) if tiktok_metrics['total_views'] > 0 else 0
        
        # Round monetary values
        facebook_metrics['total_spend'] = round(facebook_metrics['total_spend'], 2)
        
        return {
            "success": True,
            "data": {
                "facebook_metrics": facebook_metrics,
                "tiktok_metrics": tiktok_metrics,
                "performance_summary": {
                    "best_performing_platform": "Facebook" if facebook_metrics['avg_engagement_rate'] > tiktok_metrics['avg_engagement_rate'] else "TikTok",
                    "total_social_mentions": facebook_metrics['total_ads'] + tiktok_metrics['total_videos'],
                    "total_social_reach": facebook_metrics['total_reach'] + tiktok_metrics['total_views']
                }
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting performance metrics: {e}")
        raise HTTPException(status_code=500, detail="Failed to get performance metrics")

@router.get("/revenue")
async def get_revenue_analytics():
    """Get revenue and profit analytics"""
    try:
        products = list(memory_storage.products.values())
        
        revenue_data = {
            'total_revenue': 0,
            'total_cost': 0,
            'total_profit': 0,
            'profit_margin': 0,
            'avg_profit_per_product': 0,
            'revenue_by_category': {},
            'profit_by_category': {},
            'top_profitable_products': []
        }
        
        for product in products:
            price = product.get('price', 0)
            compare_price = product.get('compare_price', price)
            
            # Estimate cost (60% of selling price for dropshipping)
            estimated_cost = price * 0.6
            profit = price - estimated_cost
            
            revenue_data['total_revenue'] += price
            revenue_data['total_cost'] += estimated_cost
            revenue_data['total_profit'] += profit
            
            # Category breakdown
            category = product.get('category', 'unknown')
            if category not in revenue_data['revenue_by_category']:
                revenue_data['revenue_by_category'][category] = 0
                revenue_data['profit_by_category'][category] = 0
            
            revenue_data['revenue_by_category'][category] += price
            revenue_data['profit_by_category'][category] += profit
            
            # Track top profitable products
            revenue_data['top_profitable_products'].append({
                'id': product.get('id'),
                'title': product.get('title'),
                'price': price,
                'profit': profit,
                'profit_margin': round((profit / price) * 100, 2) if price > 0 else 0,
                'category': category
            })
        
        # Calculate overall metrics
        if revenue_data['total_revenue'] > 0:
            revenue_data['profit_margin'] = round((revenue_data['total_profit'] / revenue_data['total_revenue']) * 100, 2)
            revenue_data['avg_profit_per_product'] = round(revenue_data['total_profit'] / len(products), 2)
        
        # Sort top profitable products
        revenue_data['top_profitable_products'] = sorted(
            revenue_data['top_profitable_products'], 
            key=lambda x: x['profit'], 
            reverse=True
        )[:10]
        
        # Round monetary values
        revenue_data['total_revenue'] = round(revenue_data['total_revenue'], 2)
        revenue_data['total_cost'] = round(revenue_data['total_cost'], 2)
        revenue_data['total_profit'] = round(revenue_data['total_profit'], 2)
        
        for category in revenue_data['revenue_by_category']:
            revenue_data['revenue_by_category'][category] = round(revenue_data['revenue_by_category'][category], 2)
            revenue_data['profit_by_category'][category] = round(revenue_data['profit_by_category'][category], 2)
        
        return {
            "success": True,
            "data": revenue_data
        }
        
    except Exception as e:
        logger.error(f"Error getting revenue analytics: {e}")
        raise HTTPException(status_code=500, detail="Failed to get revenue analytics") 