from typing import List, Optional, Dict, Any
from app.schemas import TravelRequestCreate, TravelRequestUpdate, Place
from app.services.openai_service import openai_service
from app.services.database_service import DatabaseService
from app.core.exceptions import OpenAIError, DatabaseError

class RecommendationService:
    def __init__(self, database_service: DatabaseService):
        self.db_service = database_service
    
    async def create_recommendations(self, request_data: TravelRequestCreate) -> Dict[str, Any]:
        """Create new travel recommendations"""
        try:
            # Generate recommendations using OpenAI
            places = await openai_service.generate_recommendations(
                user_request=request_data.text,
                num_places=request_data.num_places,
                exclude_places=request_data.exclude
            )
            
            # Save to database
            db_request = await self.db_service.create_travel_request(
                request_data, 
                [place.dict() for place in places]
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
    
    async def update_recommendations(self, request_id: int, update_data: TravelRequestUpdate) -> Dict[str, Any]:
        """Update recommendations by excluding places"""
        try:
            # Get original request
            original_request = await self.db_service.get_travel_request_by_id(request_id)
            if not original_request:
                raise ValueError("Request not found")
            
            # Generate new recommendations using refinement
            places = await openai_service.refine_recommendations(
                original_request.text,
                update_data.exclude,
                original_request.num_places
            )
            
            # Update database
            updated_request = await self.db_service.update_travel_request(
                request_id, 
                update_data.exclude, 
                [place.dict() for place in places]
            )
            
            return {
                "id": updated_request.id,
                "text": updated_request.text,
                "exclude": updated_request.exclude,
                "num_places": updated_request.num_places,
                "response_json": places,
                "created_at": updated_request.created_at
            }
            
        except ValueError as e:
            raise e
        except Exception as e:
            raise OpenAIError(f"Failed to update recommendations: {str(e)}")
    
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