import openai
import google.generativeai as genai
from typing import Dict, List, Optional
import os
from dotenv import load_dotenv

load_dotenv()

class AIWriter:
    """
    AI-powered content writer for dropshipping products.
    Uses OpenAI and Google Gemini APIs to rewrite titles, descriptions, and ad copy.
    """
    
    def __init__(self):
        # Initialize OpenAI
        openai.api_key = os.getenv("OPENAI_API_KEY")
        
        # Initialize Google Gemini
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.gemini_model = genai.GenerativeModel('gemini-pro')
    
    async def rewrite_title(self, original_title: str, category: str, tone: str = "professional") -> Dict[str, str]:
        """Rewrite product title for better virality and SEO"""
        try:
            prompt = f"""
            Rewrite this dropshipping product title to be more viral and engaging:
            
            Original: {original_title}
            Category: {category}
            Tone: {tone}
            
            Requirements:
            - Keep it under 60 characters
            - Include power words that drive action
            - Make it benefit-focused
            - Add urgency or scarcity if appropriate
            - Optimize for social media sharing
            
            Provide 3 different versions.
            """
            
            # Try OpenAI first
            if openai.api_key:
                response = await self._call_openai(prompt)
                return {"success": True, "titles": response.split('\n')[:3]}
            
            # Fallback to Gemini
            elif os.getenv("GEMINI_API_KEY"):
                response = await self._call_gemini(prompt)
                return {"success": True, "titles": response.split('\n')[:3]}
            
            else:
                return {"success": False, "error": "No AI API keys configured"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def write_ad_copy(self, product_title: str, category: str, price: float, 
                           target_audience: str = "general") -> Dict[str, str]:
        """Generate engaging Facebook ad copy"""
        try:
            prompt = f"""
            Create compelling Facebook ad copy for this dropshipping product:
            
            Product: {product_title}
            Category: {category}
            Price: ${price}
            Target Audience: {target_audience}
            
            Requirements:
            - Create 3 different ad variations
            - Include emotional triggers
            - Add social proof elements
            - Include clear call-to-action
            - Keep under 125 characters for primary text
            - Add 2-3 hashtags
            - Make it feel urgent and exclusive
            
            Format each ad as: "Primary Text | Headline | Description"
            """
            
            if openai.api_key:
                response = await self._call_openai(prompt)
                return {"success": True, "ads": self._parse_ad_response(response)}
            
            elif os.getenv("GEMINI_API_KEY"):
                response = await self._call_gemini(prompt)
                return {"success": True, "ads": self._parse_ad_response(response)}
            
            else:
                return {"success": False, "error": "No AI API keys configured"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def write_description(self, product_title: str, category: str, 
                              features: List[str] = None) -> Dict[str, str]:
        """Generate product description optimized for conversion"""
        try:
            features_text = "\n".join([f"- {feature}" for feature in (features or [])])
            
            prompt = f"""
            Write a compelling product description for this dropshipping item:
            
            Product: {product_title}
            Category: {category}
            Features: {features_text}
            
            Requirements:
            - Start with a hook
            - Include benefits, not just features
            - Add social proof
            - Include urgency/scarcity
            - End with strong call-to-action
            - Keep it scannable with bullet points
            - Optimize for mobile reading
            - Include relevant keywords naturally
            
            Make it 150-300 words.
            """
            
            if openai.api_key:
                response = await self._call_openai(prompt)
                return {"success": True, "description": response.strip()}
            
            elif os.getenv("GEMINI_API_KEY"):
                response = await self._call_gemini(prompt)
                return {"success": True, "description": response.strip()}
            
            else:
                return {"success": False, "error": "No AI API keys configured"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def explain_why_winning(self, product_data: Dict) -> Dict[str, str]:
        """Explain why a product is likely to be a winning dropshipping product"""
        try:
            score = product_data.get('score', 0)
            category = product_data.get('category', 'unknown')
            price = product_data.get('price', 0)
            
            prompt = f"""
            Analyze this dropshipping product and explain why it's likely to be a winner:
            
            Score: {score}/100
            Category: {category}
            Price: ${price}
            Facebook Ads: {len(product_data.get('facebook_ads', []))} ads found
            TikTok Mentions: {len(product_data.get('tiktok_mentions', []))} videos
            Trend Score: {product_data.get('trend_data', {}).get('trend_score', 0)}/100
            
            Provide:
            1. Key strengths (2-3 points)
            2. Potential challenges (1-2 points)
            3. Recommended marketing strategy
            4. Suggested price optimization
            5. Target audience recommendations
            
            Keep it concise and actionable.
            """
            
            if openai.api_key:
                response = await self._call_openai(prompt)
                return {"success": True, "analysis": response.strip()}
            
            elif os.getenv("GEMINI_API_KEY"):
                response = await self._call_gemini(prompt)
                return {"success": True, "analysis": response.strip()}
            
            else:
                return {"success": False, "error": "No AI API keys configured"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API"""
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert dropshipping copywriter specializing in viral product marketing."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].message.content
    
    async def _call_gemini(self, prompt: str) -> str:
        """Call Google Gemini API"""
        response = await self.gemini_model.generate_content_async(prompt)
        return response.text
    
    def _parse_ad_response(self, response: str) -> List[Dict[str, str]]:
        """Parse AI response into structured ad copy"""
        ads = []
        lines = response.split('\n')
        
        current_ad = {}
        for line in lines:
            line = line.strip()
            if '|' in line:
                parts = line.split('|')
                if len(parts) >= 3:
                    ads.append({
                        'primary_text': parts[0].strip(),
                        'headline': parts[1].strip(),
                        'description': parts[2].strip()
                    })
        
        return ads[:3]  # Return max 3 ads 