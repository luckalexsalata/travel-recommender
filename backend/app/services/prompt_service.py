from typing import List, Optional

class PromptService:
    """Service for generating AI prompts"""
    
    @staticmethod
    def generate_recommendation_prompt(
        user_request: str, 
        num_places: int = 3,
        exclude_places: Optional[List[str]] = None
    ) -> str:
        """
        Generate prompt for travel recommendations
        """
        prompt = f"""
        Generate EXACTLY {num_places} travel recommendations based on this request: \"{user_request}\"
        You MUST return exactly {num_places} places, no more, no less.
        """
        if exclude_places:
            prompt += f"\nExclude these places: {', '.join(exclude_places)}"
        prompt += f"""
        \nReturn ONLY a JSON array with EXACTLY {num_places} objects. Each object must have:
        - "name": place name
        - "description": brief description
        - "coords": {{"lat": number, "lng": number}}
        
        Ensure coordinates are realistic. Return ONLY the JSON array, no additional text.
        Answer in the same language as the user's request.
        """
        return prompt.strip()
    
    @staticmethod
    def get_system_prompt() -> str:
        """Get system prompt for OpenAI"""
        return (
            "You are a travel expert. Always respond with valid JSON arrays only. "
            "Always answer in the same language as the user's request."
        )
    
    @staticmethod
    def generate_refinement_prompt(
        original_request: str,
        excluded_places: List[str],
        num_places: int = 3
    ) -> str:
        """
        Generate prompt for refining recommendations
        """
        return f"""
        Refine travel recommendations based on the original request: \"{original_request}\"
        The user has excluded these places: {', '.join(excluded_places)}
        Generate EXACTLY {num_places} new recommendations that are different from the excluded ones.
        You MUST return exactly {num_places} places, no more, no less.
        
        Return ONLY a JSON array with EXACTLY {num_places} objects. Each object must have:
        - "name": place name
        - "description": brief description
        - "coords": {{"lat": number, "lng": number}}
        
        Ensure coordinates are realistic. Return ONLY the JSON array, no additional text.
        Answer in the same language as the user's request.
        """.strip() 