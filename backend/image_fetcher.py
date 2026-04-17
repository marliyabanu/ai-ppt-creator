import requests
import random

class ImageFetcher:
    
    @staticmethod
    def get_image_url(keyword):
        """Fetch relevant image URL for slide"""
        
        # Free image API (Unsplash Source - no API key needed)
        # Returns high-quality relevant images
        
        # Clean keyword for URL
        clean_keyword = keyword.replace(' ', ',').lower()
        
        # Unsplash Source URL (free, no API key)
        unsplash_url = f"https://source.unsplash.com/featured/800x450?{clean_keyword}"
        
        # Alternative: Picsum with keyword mapping
        image_map = {
            'ai': 1, 'artificial intelligence': 2, 'robot': 3,
            'python': 4, 'coding': 5, 'programming': 6,
            'business': 20, 'strategy': 21, 'meeting': 22,
            'healthcare': 30, 'doctor': 31, 'medical': 32,
            'education': 40, 'learning': 41, 'students': 42,
            'technology': 50, 'tech': 51, 'digital': 52,
            'environment': 60, 'nature': 61, 'climate': 62,
            'space': 70, 'solar': 71, 'planet': 72,
            'default': 100
        }
        
        # Find matching image ID
        img_id = image_map.get('default')
        for key, img in image_map.items():
            if key in clean_keyword:
                img_id = img
                break
        
        picsum_url = f"https://picsum.photos/id/{img_id}/800/450"
        
        # Return Unsplash URL (more relevant images)
        return unsplash_url