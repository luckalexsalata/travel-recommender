from typing import List, Optional

class PromptService:
    """Service for generating AI prompts"""
    
    @staticmethod
    def generate_recommendation_prompt(
        user_request: str, 
        num_places: int = 3
    ) -> str:
        """
        Generate prompt for travel recommendations with exclusion handling
        """
        prompt = f"""
        Generate EXACTLY {num_places} travel recommendations based on this request: "{user_request}"
        
        IMPORTANT: This request contains conversation history. Pay attention to:
        1. The original user preferences (where they want to go, what they like)
        2. Any places they want to exclude from previous messages
        
        If the user is making a refinement (like "не хочу в..."), maintain the original context 
        and preferences while applying the new exclusions.
        
        Analyze the user's request carefully. If they mention places they don't want to visit 
        (using phrases like "не хочу", "don't want", "no quiero", "je ne veux pas", "не показуй", etc.), 
        extract those places as exclusions.
        
        Return a JSON object with TWO fields:
        1. "places": array with EXACTLY {num_places} objects, each with:
           - "name": place name
           - "description": brief description  
           - "coords": {{"lat": number, "lng": number}}
        2. "exclusions": array of places to exclude (can be empty if no exclusions mentioned)
        
        Ensure coordinates are realistic. Return ONLY the JSON object, no additional text.
        Answer in the same language as the user's request.
        """
        return prompt.strip()
    
    @staticmethod
    def get_system_prompt() -> str:
        """Get system prompt for OpenAI"""
        return (
            "You are a travel expert. Always respond with valid JSON objects only. "
            "Always answer in the same language as the user's request. "
            "Understand and respect user preferences and exclusions mentioned in their request. "
            "When processing refinements, maintain the original context and preferences. "
            "Extract exclusions from user text and return them separately from recommendations."
        ) 