import hashlib
import pickle
import time
import logging
from pathlib import Path
from typing import Any, Optional, Dict
import json

logger = logging.getLogger(__name__)

class CrawlerCache:
    def __init__(self, cache_dir: str = "cache", cache_duration: int = 3600):
        """
        Initialize cache manager
        
        Args:
            cache_dir: Directory to store cache files
            cache_duration: Cache duration in seconds (default: 1 hour)
        """
        self.cache_dir = Path(cache_dir)
        self.cache_duration = cache_duration
        self.cache_dir.mkdir(exist_ok=True)
        
        # Create subdirectories for different cache types
        (self.cache_dir / "html").mkdir(exist_ok=True)
        (self.cache_dir / "json").mkdir(exist_ok=True)
        (self.cache_dir / "products").mkdir(exist_ok=True)
    
    def get_cache_key(self, url: str, cache_type: str = "html") -> str:
        """Generate cache key from URL"""
        # Create a hash of the URL
        url_hash = hashlib.md5(url.encode()).hexdigest()
        return f"{cache_type}_{url_hash}"
    
    def get_cache_path(self, cache_key: str, cache_type: str = "html") -> Path:
        """Get cache file path"""
        return self.cache_dir / cache_type / f"{cache_key}.pkl"
    
    def get(self, url: str, cache_type: str = "html") -> Optional[Any]:
        """
        Get cached data
        
        Args:
            url: The URL that was cached
            cache_type: Type of cache (html, json, products)
            
        Returns:
            Cached data or None if not found/expired
        """
        try:
            cache_key = self.get_cache_key(url, cache_type)
            cache_path = self.get_cache_path(cache_key, cache_type)
            
            if not cache_path.exists():
                return None
            
            # Check if cache is expired
            if time.time() - cache_path.stat().st_mtime > self.cache_duration:
                logger.debug(f"Cache expired for {url}")
                cache_path.unlink()  # Delete expired cache
                return None
            
            # Load cached data
            with open(cache_path, 'rb') as f:
                cached_data = pickle.load(f)
            
            logger.debug(f"Cache hit for {url}")
            return cached_data
            
        except Exception as e:
            logger.warning(f"Error reading cache for {url}: {e}")
            return None
    
    def set(self, url: str, data: Any, cache_type: str = "html") -> bool:
        """
        Set cached data
        
        Args:
            url: The URL to cache
            data: Data to cache
            cache_type: Type of cache (html, json, products)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            cache_key = self.get_cache_key(url, cache_type)
            cache_path = self.get_cache_path(cache_key, cache_type)
            
            # Save data to cache
            with open(cache_path, 'wb') as f:
                pickle.dump(data, f)
            
            logger.debug(f"Cached data for {url}")
            return True
            
        except Exception as e:
            logger.warning(f"Error writing cache for {url}: {e}")
            return False
    
    def clear(self, cache_type: Optional[str] = None) -> int:
        """
        Clear cache
        
        Args:
            cache_type: Specific cache type to clear, or None for all
            
        Returns:
            Number of files deleted
        """
        deleted_count = 0
        
        try:
            if cache_type:
                cache_type_dir = self.cache_dir / cache_type
                if cache_type_dir.exists():
                    for cache_file in cache_type_dir.glob("*.pkl"):
                        cache_file.unlink()
                        deleted_count += 1
            else:
                # Clear all cache types
                for cache_type_dir in self.cache_dir.iterdir():
                    if cache_type_dir.is_dir():
                        for cache_file in cache_type_dir.glob("*.pkl"):
                            cache_file.unlink()
                            deleted_count += 1
            
            logger.info(f"Cleared {deleted_count} cache files")
            return deleted_count
            
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")
            return 0
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        stats = {
            "total_files": 0,
            "total_size_mb": 0,
            "cache_types": {}
        }
        
        try:
            for cache_type_dir in self.cache_dir.iterdir():
                if cache_type_dir.is_dir():
                    cache_type = cache_type_dir.name
                    files = list(cache_type_dir.glob("*.pkl"))
                    total_size = sum(f.stat().st_size for f in files)
                    
                    stats["cache_types"][cache_type] = {
                        "files": len(files),
                        "size_mb": round(total_size / (1024 * 1024), 2)
                    }
                    stats["total_files"] += len(files)
                    stats["total_size_mb"] += total_size / (1024 * 1024)
            
            stats["total_size_mb"] = round(stats["total_size_mb"], 2)
            
        except Exception as e:
            logger.error(f"Error getting cache stats: {e}")
        
        return stats
    
    def cleanup_expired(self) -> int:
        """Clean up expired cache files"""
        deleted_count = 0
        
        try:
            for cache_type_dir in self.cache_dir.iterdir():
                if cache_type_dir.is_dir():
                    for cache_file in cache_type_dir.glob("*.pkl"):
                        if time.time() - cache_file.stat().st_mtime > self.cache_duration:
                            cache_file.unlink()
                            deleted_count += 1
            
            if deleted_count > 0:
                logger.info(f"Cleaned up {deleted_count} expired cache files")
            
        except Exception as e:
            logger.error(f"Error cleaning up expired cache: {e}")
        
        return deleted_count

# Global cache instance
crawler_cache = CrawlerCache() 