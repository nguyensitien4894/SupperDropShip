from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum

class ProductCategory(str, Enum):
    GADGETS = "gadgets"
    HOME = "home"
    FASHION = "fashion"
    BEAUTY = "beauty"
    FITNESS = "fitness"
    PETS = "pets"
    KIDS = "kids"
    AUTOMOTIVE = "automotive"
    GARDEN = "garden"
    SPORTS = "sports"

class SupplierPlatform(str, Enum):
    ALIEXPRESS = "aliexpress"
    TEMU = "temu"
    SHOP1688 = "1688"

class Product(BaseModel):
    id: str = Field(..., description="Unique product identifier")
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., description="Current selling price")
    compare_price: Optional[float] = Field(None, description="Original/compare price")
    currency: str = Field(default="USD", description="Price currency")
    
    # Scoring and analysis
    score: float = Field(default=0.0, description="Winning score (0-100)")
    category: ProductCategory = Field(..., description="Product category")
    tags: List[str] = Field(default=[], description="Product tags")
    
    # Source information
    source_store: Optional[str] = Field(None, description="Original store URL")
    source_url: Optional[str] = Field(None, description="Original product URL")
    image_url: Optional[str] = Field(None, description="Product image URL")
    
    # Supplier links
    supplier_links: Dict[SupplierPlatform, str] = Field(default={}, description="Supplier platform links")
    supplier_prices: Dict[SupplierPlatform, float] = Field(default={}, description="Supplier prices")
    
    # Social media data
    facebook_ads: List[Dict[str, Any]] = Field(default=[], description="Related Facebook ads")
    tiktok_mentions: List[Dict[str, Any]] = Field(default=[], description="TikTok mentions")
    
    # Trend data
    trend_data: Optional[Dict[str, Any]] = Field(None, description="Google Trends data")
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class FacebookAd(BaseModel):
    id: str
    ad_text: str
    engagement_rate: float
    reach: int
    impressions: int
    clicks: int
    spend: Optional[float]
    created_at: datetime
    platform: str = "facebook"

class TikTokVideo(BaseModel):
    id: str
    video_url: str
    description: str
    views: int
    likes: int
    shares: int
    comments: int
    created_at: datetime
    hashtags: List[str] = []

class TrendData(BaseModel):
    keyword: str
    trend_score: int = Field(..., ge=0, le=100)
    interest_over_time: List[Dict[str, Any]] = []
    related_queries: List[str] = []
    geographic_interest: Dict[str, int] = {}

class CrawlRequest(BaseModel):
    keywords: List[str] = Field(..., description="Keywords to search for")
    category: Optional[ProductCategory] = Field(None, description="Product category filter")
    min_score: Optional[float] = Field(None, ge=0, le=100, description="Minimum score filter")
    max_price: Optional[float] = Field(None, description="Maximum price filter")
    limit: int = Field(default=50, ge=1, le=1000, description="Maximum results to return")

class AIRewriteRequest(BaseModel):
    text: str = Field(..., description="Text to rewrite")
    purpose: str = Field(..., description="Purpose: title, description, ad_copy")
    tone: str = Field(default="professional", description="Tone: professional, casual, persuasive")
    max_length: Optional[int] = Field(None, description="Maximum character length")

class ProductResponse(BaseModel):
    success: bool
    data: Optional[Product] = None
    message: Optional[str] = None

class ProductsResponse(BaseModel):
    success: bool
    data: List[Product] = []
    total: int = 0
    page: int = 1
    limit: int = 50
    message: Optional[str] = None 