import os
import json

class AIContentGenerator:
    def __init__(self):
        # Try to load OpenAI if available
        self.use_openai = False
        try:
            from dotenv import load_dotenv
            import openai
            load_dotenv()
            self.api_key = os.getenv('OPENAI_API_KEY')
            if self.api_key:
                openai.api_key = self.api_key
                self.use_openai = True
                print("OpenAI API loaded successfully")
            else:
                print("No OpenAI API key found, using mock data")
        except:
            print("OpenAI not available, using mock data")
    
    def generate_outline(self, prompt, num_slides=10):
        """Generate presentation outline"""
        return self._generate_mock_outline(prompt, num_slides)
    
    def _generate_mock_outline(self, prompt, num_slides):
        """Generate mock outline for testing"""
        outline = []
        
        # Title slide
        outline.append({
            "title": f"{prompt}",
            "content": [
                "A Comprehensive Overview",
                "Key Insights & Analysis", 
                "Strategic Recommendations",
                "Executive Summary"
            ]
        })
        
        # Topics based on prompt keywords
        topics = [
            "Introduction & Background",
            "Market Analysis & Trends",
            "Key Challenges & Opportunities",
            "Strategic Framework",
            "Implementation Plan",
            "Timeline & Milestones",
            "Resource Requirements",
            "Risk Assessment",
            "Performance Metrics",
            "Case Studies & Examples",
            "Best Practices",
            "Technology & Tools",
            "Team Structure & Roles",
            "Budget & Resources",
            "ROI Analysis",
            "Next Steps & Action Items",
            "Conclusion & Key Takeaways",
            "Q&A Session",
            "References & Resources",
            "Appendix"
        ]
        
        # Generate content slides
        for i in range(min(num_slides - 1, len(topics))):
            outline.append({
                "title": topics[i],
                "content": [
                    f"Overview of {topics[i].lower()} in context of {prompt}",
                    f"Key considerations for successful implementation",
                    f"Best practices and industry standards",
                    f"Expected outcomes and measurable benefits",
                    f"Recommendations for moving forward"
                ]
            })
        
        # Add more slides if needed
        while len(outline) < num_slides:
            outline.append({
                "title": f"Additional Insights - Part {len(outline)}",
                "content": [
                    "Deep dive into critical aspects",
                    "Supporting data and evidence",
                    "Practical applications",
                    "Future considerations"
                ]
            })
        
        return outline[:num_slides]
    