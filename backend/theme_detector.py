class ThemeDetector:
    
    THEMES = {
        'technology': {'primary': '#3b82f6', 'secondary': '#1e40af', 'accent': '#60a5fa', 'name': 'Tech Blue', 'icon': '💻'},
        'business': {'primary': '#10b981', 'secondary': '#047857', 'accent': '#34d399', 'name': 'Business Green', 'icon': '📊'},
        'creative': {'primary': '#f59e0b', 'secondary': '#d97706', 'accent': '#fbbf24', 'name': 'Creative Orange', 'icon': '🎨'},
        'academic': {'primary': '#8b5cf6', 'secondary': '#6d28d9', 'accent': '#a78bfa', 'name': 'Academic Purple', 'icon': '📚'},
        'healthcare': {'primary': '#06b6d4', 'secondary': '#0891b2', 'accent': '#22d3ee', 'name': 'Healthcare Teal', 'icon': '🏥'},
        'nature': {'primary': '#10b981', 'secondary': '#059669', 'accent': '#6ee7b7', 'name': 'Nature Green', 'icon': '🌿'},
        'default': {'primary': '#667eea', 'secondary': '#764ba2', 'accent': '#ffd700', 'name': 'Default Theme', 'icon': '✨'}
    }
    
    @staticmethod
    def detect(content):
        content_lower = content.lower()
        
        keywords = {
            'technology': ['tech', 'ai', 'software', 'code', 'programming', 'digital', 'computer', 'python', 'java', 'javascript', 'blockchain', 'cybersecurity'],
            'business': ['business', 'marketing', 'sales', 'startup', 'company', 'corporate', 'finance', 'management', 'strategy'],
            'creative': ['design', 'art', 'creative', 'style', 'visual', 'aesthetic', 'drawing', 'painting', 'graphic'],
            'academic': ['study', 'learn', 'education', 'school', 'university', 'college', 'research', 'science', 'history', 'math'],
            'healthcare': ['health', 'medical', 'doctor', 'patient', 'hospital', 'wellness', 'fitness', 'diet', 'nutrition'],
            'nature': ['nature', 'environment', 'earth', 'climate', 'green', 'sustainable', 'planet', 'forest', 'ocean']
        }
        
        for theme, words in keywords.items():
            if any(word in content_lower for word in words):
                return ThemeDetector.THEMES[theme]
        
        return ThemeDetector.THEMES['default']