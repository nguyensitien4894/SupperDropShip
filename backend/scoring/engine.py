from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import math

class ScoringEngine:
    """
    Calculates winning scores for dropshipping products based on 5 criteria:
    1. Facebook Ad Engagement (30%)
    2. TikTok Viral Ratio (25%)
    3. Profit Margin (20%)
    4. Google Trends Volume (10%)
    5. Store Saturation Level (15%)
    """
    
    def __init__(self):
        self.weights = {
            'facebook_engagement': 0.30,
            'tiktok_viral_ratio': 0.25,
            'profit_margin': 0.20,
            'google_trends': 0.10,
            'store_saturation': 0.15
        }
    
    def calculate_facebook_engagement_score(self, facebook_ads: List[Dict[str, Any]]) -> float:
        """Calculate Facebook engagement score (0-100)"""
        if not facebook_ads:
            return 0.0
        
        total_engagement = 0
        total_ads = len(facebook_ads)
        
        for ad in facebook_ads:
            # Calculate engagement rate: (likes + comments + shares) / reach
            likes = ad.get('likes', 0)
            comments = ad.get('comments', 0)
            shares = ad.get('shares', 0)
            reach = ad.get('reach', 1)  # Avoid division by zero
            
            engagement_rate = (likes + comments + shares) / reach
            total_engagement += engagement_rate
        
        avg_engagement = total_engagement / total_ads
        
        # Convert to 0-100 scale (typical engagement rates are 0.01-0.05)
        score = min(100, avg_engagement * 2000)  # Scale factor
        return round(score, 2)
    
    def calculate_tiktok_viral_ratio(self, tiktok_mentions: List[Dict[str, Any]]) -> float:
        """Calculate TikTok viral ratio score (0-100)"""
        if not tiktok_mentions:
            return 0.0
        
        total_viral_score = 0
        total_videos = len(tiktok_mentions)
        
        for video in tiktok_mentions:
            views = video.get('views', 0)
            likes = video.get('likes', 0)
            shares = video.get('shares', 0)
            comments = video.get('comments', 0)
            
            # Viral ratio: (likes + shares + comments) / views
            if views > 0:
                viral_ratio = (likes + shares + comments) / views
                # Convert to 0-100 scale
                viral_score = min(100, viral_ratio * 1000)  # Scale factor
                total_viral_score += viral_score
        
        avg_viral_score = total_viral_score / total_videos
        return round(avg_viral_score, 2)
    
    def calculate_profit_margin_score(self, price: float, supplier_prices: Dict[str, float]) -> float:
        """Calculate profit margin score (0-100)"""
        if not supplier_prices:
            return 50.0  # Neutral score if no supplier data
        
        # Find the lowest supplier price
        min_supplier_price = min(supplier_prices.values())
        
        if min_supplier_price <= 0:
            return 50.0
        
        # Calculate profit margin percentage
        profit_margin = ((price - min_supplier_price) / price) * 100
        
        # Score based on profit margin (higher is better, but not too high)
        if profit_margin < 0:
            score = 0
        elif profit_margin < 50:
            score = profit_margin * 2  # Linear scaling up to 50% margin
        else:
            score = 100 - (profit_margin - 50)  # Penalize extremely high margins
        
        return round(max(0, min(100, score)), 2)
    
    def calculate_google_trends_score(self, trend_data: Optional[Dict[str, Any]]) -> float:
        """Calculate Google Trends score (0-100)"""
        if not trend_data:
            return 50.0  # Neutral score if no trend data
        
        trend_score = trend_data.get('trend_score', 50)
        return round(trend_score, 2)
    
    def calculate_store_saturation_score(self, similar_stores: List[str]) -> float:
        """Calculate store saturation score (0-100) - lower saturation is better"""
        if not similar_stores:
            return 100.0  # Perfect score if no competition
        
        # Count stores selling similar products
        store_count = len(similar_stores)
        
        # Score decreases as more stores sell the product
        if store_count <= 5:
            score = 100
        elif store_count <= 20:
            score = 80
        elif store_count <= 50:
            score = 60
        elif store_count <= 100:
            score = 40
        else:
            score = 20
        
        return round(score, 2)
    
    def calculate_winning_score(self, product_data: Dict[str, Any]) -> float:
        """Calculate overall winning score (0-100)"""
        scores = {}
        
        # Calculate individual scores
        scores['facebook_engagement'] = self.calculate_facebook_engagement_score(
            product_data.get('facebook_ads', [])
        )
        
        scores['tiktok_viral_ratio'] = self.calculate_tiktok_viral_ratio(
            product_data.get('tiktok_mentions', [])
        )
        
        scores['profit_margin'] = self.calculate_profit_margin_score(
            product_data.get('price', 0),
            product_data.get('supplier_prices', {})
        )
        
        scores['google_trends'] = self.calculate_google_trends_score(
            product_data.get('trend_data')
        )
        
        scores['store_saturation'] = self.calculate_store_saturation_score(
            product_data.get('similar_stores', [])
        )
        
        # Calculate weighted average
        total_score = 0
        for metric, score in scores.items():
            weight = self.weights[metric]
            total_score += score * weight
        
        return round(total_score, 2)
    
    def get_score_breakdown(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get detailed score breakdown for analysis"""
        scores = {}
        
        scores['facebook_engagement'] = self.calculate_facebook_engagement_score(
            product_data.get('facebook_ads', [])
        )
        
        scores['tiktok_viral_ratio'] = self.calculate_tiktok_viral_ratio(
            product_data.get('tiktok_mentions', [])
        )
        
        scores['profit_margin'] = self.calculate_profit_margin_score(
            product_data.get('price', 0),
            product_data.get('supplier_prices', {})
        )
        
        scores['google_trends'] = self.calculate_google_trends_score(
            product_data.get('trend_data')
        )
        
        scores['store_saturation'] = self.calculate_store_saturation_score(
            product_data.get('similar_stores', [])
        )
        
        total_score = self.calculate_winning_score(product_data)
        
        return {
            'total_score': total_score,
            'breakdown': scores,
            'weights': self.weights,
            'recommendations': self._generate_recommendations(scores)
        }
    
    def _generate_recommendations(self, scores: Dict[str, float]) -> List[str]:
        """Generate improvement recommendations based on scores"""
        recommendations = []
        
        if scores['facebook_engagement'] < 30:
            recommendations.append("Low Facebook engagement - consider improving ad creative")
        
        if scores['tiktok_viral_ratio'] < 25:
            recommendations.append("Low TikTok virality - focus on trending hashtags and content")
        
        if scores['profit_margin'] < 40:
            recommendations.append("Low profit margin - negotiate better supplier prices")
        
        if scores['google_trends'] < 30:
            recommendations.append("Low search interest - consider different keywords")
        
        if scores['store_saturation'] < 40:
            recommendations.append("High market saturation - consider niche differentiation")
        
        return recommendations 