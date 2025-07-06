import os
import json
import asyncio
from typing import List, Optional, Tuple
from openai import AsyncOpenAI
from openai import RateLimitError, APITimeoutError, APIError
from app.schemas import Place, Coordinates
from app.core.config import settings
from app.services.prompt_service import PromptService
from app.core.exceptions import OpenAIError

class OpenAIService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model
        self.prompt_service = PromptService()

    async def generate_recommendations(
        self, 
        user_request: str, 
        num_places: int = 3,
        max_retries: int = 2
    ) -> Tuple[List[Place], List[str]]:
        """
        Generate travel recommendations and extract exclusions based on user request
        Returns: (places, exclusions)
        """
        for attempt in range(max_retries + 1):
            try:
                # Generate prompt using PromptService
                prompt = self.prompt_service.generate_recommendation_prompt(
                    user_request, num_places
                )
                
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": self.prompt_service.get_system_prompt()},
                        {"role": "user", "content": prompt}
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.7,
                    max_tokens=2000
                )
                
                # Parse the response
                content = response.choices[0].message.content
                response_data = json.loads(content)

                # Extract places and exclusions
                places_data = response_data.get("places", [])
                exclusions = response_data.get("exclusions", [])

                # Ensure places_data is a list
                if not isinstance(places_data, list):
                    raise ValueError(f"Expected places array, got {type(places_data)}")

                # Convert to Place objects
                places = []
                for place_data in places_data:
                    if not isinstance(place_data, dict):
                        continue
                    coords = Coordinates(
                        lat=place_data.get("coords", {}).get("lat", 0.0),
                        lng=place_data.get("coords", {}).get("lng", 0.0)
                    )
                    place = Place(
                        name=place_data.get("name", "Unknown"),
                        description=place_data.get("description", ""),
                        coords=coords
                    )
                    places.append(place)
                
                # Validate that we got the expected number of places
                if len(places) != num_places:
                    print(f"Warning: Expected {num_places} places, but got {len(places)}")
                    # If we got fewer places than expected, try to generate more
                    if len(places) < num_places:
                        print(f"Attempting to generate {num_places - len(places)} more places...")
                        return await self.generate_recommendations(user_request, num_places)
                
                return places, exclusions
                
            except (RateLimitError, APITimeoutError) as e:
                if attempt < max_retries:
                    wait_time = (2 ** attempt) * 1  # Exponential backoff: 1s, 2s, 4s
                    print(f"OpenAI error (attempt {attempt + 1}/{max_retries + 1}): {str(e)}. Retrying in {wait_time}s...")
                    await asyncio.sleep(wait_time)
                    continue
                else:
                    raise OpenAIError(f"OpenAI API error after {max_retries + 1} attempts: {str(e)}")
            except APIError as e:
                if attempt < max_retries:
                    wait_time = (2 ** attempt) * 1
                    print(f"OpenAI API error (attempt {attempt + 1}/{max_retries + 1}): {str(e)}. Retrying in {wait_time}s...")
                    await asyncio.sleep(wait_time)
                    continue
                else:
                    raise OpenAIError(f"OpenAI API error after {max_retries + 1} attempts: {str(e)}")
            except Exception as e:
                raise OpenAIError(f"Error generating recommendations: {str(e)}")

# Create global instance
openai_service = OpenAIService() 