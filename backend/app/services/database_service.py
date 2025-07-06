from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime

from app.models import TravelRequest
from app.schemas import TravelRequestCreate
from app.core.exceptions import DatabaseError

class DatabaseService:
    """Service for database operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_travel_request(
        self, 
        request_data: TravelRequestCreate, 
        response_json: List[Dict[str, Any]],
        exclusions: List[str] = None
    ) -> TravelRequest:
        """Create new travel request"""
        try:
            db_request = TravelRequest(
                text=request_data.text,
                exclude=exclusions or [],
                num_places=request_data.num_places,
                response_json=response_json
            )
            
            self.db.add(db_request)
            await self.db.commit()
            await self.db.refresh(db_request)
            return db_request
            
        except Exception as e:
            await self.db.rollback()
            raise DatabaseError(f"Failed to create travel request: {str(e)}")
    
    async def get_travel_request_by_id(self, request_id: int) -> Optional[TravelRequest]:
        """Get travel request by ID"""
        try:
            result = await self.db.execute(
                select(TravelRequest).where(TravelRequest.id == request_id)
            )
            return result.scalar_one_or_none()
            
        except Exception as e:
            raise DatabaseError(f"Failed to get travel request: {str(e)}")
    
    async def get_recent_requests(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get recent requests for context building"""
        try:
            result = await self.db.execute(
                select(TravelRequest)
                .order_by(TravelRequest.created_at.desc())
                .limit(limit)
            )
            requests = result.scalars().all()
            
            return [
                {
                    "text": request.text,
                    "exclude": request.exclude,
                    "num_places": request.num_places,
                    "created_at": request.created_at
                }
                for request in requests
            ]
            
        except Exception as e:
            raise DatabaseError(f"Failed to get recent requests: {str(e)}")
    
    async def get_all_travel_requests(
        self, 
        limit: int = 10, 
        offset: int = 0
    ) -> List[TravelRequest]:
        """Get all travel requests with pagination"""
        try:
            result = await self.db.execute(
                select(TravelRequest)
                .order_by(TravelRequest.created_at.desc())
                .limit(limit)
                .offset(offset)
            )
            return result.scalars().all()
            
        except Exception as e:
            raise DatabaseError(f"Failed to get travel requests: {str(e)}")
    
    async def delete_travel_request(self, request_id: int) -> bool:
        """Delete travel request"""
        try:
            request = await self.get_travel_request_by_id(request_id)
            if not request:
                return False
            
            await self.db.delete(request)
            await self.db.commit()
            return True
            
        except Exception as e:
            await self.db.rollback()
            raise DatabaseError(f"Failed to delete travel request: {str(e)}")
    
    async def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics"""
        try:
            # Total requests
            total_result = await self.db.execute(
                select(func.count(TravelRequest.id))
            )
            total_requests = total_result.scalar()
            
            # Requests today
            today = datetime.now().date()
            today_result = await self.db.execute(
                select(func.count(TravelRequest.id))
                .where(func.date(TravelRequest.created_at) == today)
            )
            today_requests = today_result.scalar()
            
            # Average places per request
            avg_result = await self.db.execute(
                select(func.avg(TravelRequest.num_places))
            )
            avg_places = avg_result.scalar()
            
            return {
                "total_requests": total_requests,
                "today_requests": today_requests,
                "average_places": round(avg_places, 2) if avg_places else 0
            }
            
        except Exception as e:
            raise DatabaseError(f"Failed to get statistics: {str(e)}")
    
    async def search_requests(self, search_term: str, limit: int = 10) -> List[TravelRequest]:
        """Search travel requests by text"""
        try:
            result = await self.db.execute(
                select(TravelRequest)
                .where(TravelRequest.text.ilike(f"%{search_term}%"))
                .order_by(TravelRequest.created_at.desc())
                .limit(limit)
            )
            return result.scalars().all()
            
        except Exception as e:
            raise DatabaseError(f"Failed to search requests: {str(e)}") 