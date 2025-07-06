from typing import List, Optional, Dict, Any
from app.schemas import TravelRequestCreate, Place
from app.services.openai_service import openai_service
from app.services.database_service import DatabaseService
from app.core.exceptions import OpenAIError, DatabaseError

class RecommendationService:
    def __init__(self, database_service: DatabaseService):
        self.db_service = database_service
    
    async def create_recommendations(self, request_data: TravelRequestCreate) -> Dict[str, Any]:
        """Create new travel recommendations with context from previous requests"""
        try:
            # Get recent requests to build context
            recent_requests = await self.db_service.get_recent_requests(limit=5)
            
            # Build context from recent requests
            context = self._build_context_from_history(recent_requests, request_data)
            
            # Generate recommendations and extract exclusions from text
            places, new_exclusions = await openai_service.generate_recommendations(
                user_request=context,
                num_places=request_data.num_places
            )
            
            # Accumulate exclusions from previous requests
            accumulated_exclusions = self._accumulate_exclusions(recent_requests, new_exclusions)
            
            # Save to database with accumulated exclusions
            db_request = await self.db_service.create_travel_request(
                request_data, 
                [place.dict() for place in places],
                accumulated_exclusions
            )
            
            return {
                "id": db_request.id,
                "text": db_request.text,
                "exclude": db_request.exclude,
                "num_places": db_request.num_places,
                "response_json": places,
                "created_at": db_request.created_at
            }
            
        except Exception as e:
            raise OpenAIError(f"Failed to create recommendations: {str(e)}")
    
    def _build_context_from_history(self, recent_requests: List[Dict], current_request: TravelRequestCreate) -> str:
        """Build context from recent requests"""
        context_parts = []
        
        # Add recent user requests for context
        for i, request in enumerate(recent_requests, 1):
            context_parts.append(f"Message {i}: {request['text']}")
            if request['exclude']:
                context_parts.append(f"Excluded in message {i}: {', '.join(request['exclude'])}")
        
        # Add current request
        context_parts.append(f"Current message: {current_request.text}")
        
        # Add summary instruction
        if len(recent_requests) > 0:
            context_parts.append("IMPORTANT: Maintain the original travel preferences while applying any new exclusions.")
        
        return "\n".join(context_parts)
    
    def _accumulate_exclusions(self, recent_requests: List[Dict], new_exclusions: List[str]) -> List[str]:
        """Accumulate exclusions from previous requests and new ones"""
        accumulated_exclusions = []
        
        # Add exclusions from recent requests
        for request in recent_requests:
            if request['exclude']:
                accumulated_exclusions.extend(request['exclude'])
        
        # Add new exclusions from current request
        accumulated_exclusions.extend(new_exclusions)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_exclusions = []
        for exclusion in accumulated_exclusions:
            if exclusion not in seen:
                seen.add(exclusion)
                unique_exclusions.append(exclusion)
        
        return unique_exclusions
    
    async def get_recommendations(self, request_id: int) -> Optional[Dict[str, Any]]:
        """Get recommendations by ID"""
        try:
            request = await self.db_service.get_travel_request_by_id(request_id)
            if not request:
                return None
            
            places = [Place(**place_data) for place_data in request.response_json]
            
            return {
                "id": request.id,
                "text": request.text,
                "exclude": request.exclude,
                "num_places": request.num_places,
                "response_json": places,
                "created_at": request.created_at
            }
            
        except Exception as e:
            raise DatabaseError(f"Failed to get recommendations: {str(e)}")
    
    async def get_all_recommendations(self, limit: int = 10, offset: int = 0) -> List[Dict[str, Any]]:
        """Get all recommendations with pagination"""
        try:
            requests = await self.db_service.get_all_travel_requests(limit, offset)
            
            result = []
            for request in requests:
                places = [Place(**place_data) for place_data in request.response_json]
                result.append({
                    "id": request.id,
                    "text": request.text,
                    "exclude": request.exclude,
                    "num_places": request.num_places,
                    "response_json": places,
                    "created_at": request.created_at
                })
            
            return result
            
        except Exception as e:
            raise DatabaseError(f"Failed to get all recommendations: {str(e)}")
    
    async def delete_recommendations(self, request_id: int) -> bool:
        """Delete recommendations"""
        try:
            return await self.db_service.delete_travel_request(request_id)
        except Exception as e:
            raise DatabaseError(f"Failed to delete recommendations: {str(e)}")
    
    async def search_recommendations(self, search_term: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search recommendations by text"""
        try:
            requests = await self.db_service.search_requests(search_term, limit)
            
            result = []
            for request in requests:
                places = [Place(**place_data) for place_data in request.response_json]
                result.append({
                    "id": request.id,
                    "text": request.text,
                    "exclude": request.exclude,
                    "num_places": request.num_places,
                    "response_json": places,
                    "created_at": request.created_at
                })
            
            return result
            
        except Exception as e:
            raise DatabaseError(f"Failed to search recommendations: {str(e)}")
    
    async def get_statistics(self) -> Dict[str, Any]:
        """Get service statistics"""
        try:
            return await self.db_service.get_statistics()
        except Exception as e:
            raise DatabaseError(f"Failed to get statistics: {str(e)}") 