from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.api.dependencies import get_db
from app.schemas import TravelRequestCreate, TravelRequestUpdate, TravelRequestResponse
from app.services import RecommendationService, DatabaseService
from app.core.exceptions import OpenAIError, DatabaseError

router = APIRouter()

def get_recommendation_service(db: AsyncSession = Depends(get_db)) -> RecommendationService:
    """Dependency to get recommendation service"""
    database_service = DatabaseService(db)
    return RecommendationService(database_service)

@router.post("/generate", response_model=TravelRequestResponse)
async def generate_recommendations(
    request: TravelRequestCreate,
    service: RecommendationService = Depends(get_recommendation_service)
):
    """
    Generate travel recommendations based on user message
    Example: "Хочу в Рим, люблю історію та макарони"
    """
    try:
        result = await service.create_recommendations(request)
        return TravelRequestResponse(**result)
        
    except OpenAIError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.post("/", response_model=TravelRequestResponse)
async def create_recommendations(
    request: TravelRequestCreate,
    service: RecommendationService = Depends(get_recommendation_service)
):
    """
    Create new travel recommendations based on user request
    """
    try:
        result = await service.create_recommendations(request)
        return TravelRequestResponse(**result)
        
    except OpenAIError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.post("/{request_id}/refine", response_model=TravelRequestResponse)
async def refine_recommendations(
    request_id: int,
    update_request: TravelRequestUpdate,
    service: RecommendationService = Depends(get_recommendation_service)
):
    """
    Refine recommendations by excluding specific places
    Example: exclude places like "Колізей" from previous recommendations
    """
    try:
        result = await service.update_recommendations(request_id, update_request)
        return TravelRequestResponse(**result)
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except OpenAIError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.put("/{request_id}", response_model=TravelRequestResponse)
async def update_recommendations(
    request_id: int,
    update_request: TravelRequestUpdate,
    service: RecommendationService = Depends(get_recommendation_service)
):
    """
    Update recommendations by excluding specific places
    """
    try:
        result = await service.update_recommendations(request_id, update_request)
        return TravelRequestResponse(**result)
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except OpenAIError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get("/{request_id}", response_model=TravelRequestResponse)
async def get_recommendations(
    request_id: int,
    service: RecommendationService = Depends(get_recommendation_service)
):
    """
    Get specific travel recommendations by ID
    """
    try:
        result = await service.get_recommendations(request_id)
        
        if not result:
            raise HTTPException(status_code=404, detail="Request not found")
        
        return TravelRequestResponse(**result)
        
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get("/history", response_model=List[TravelRequestResponse])
async def get_history(
    service: RecommendationService = Depends(get_recommendation_service),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """
    Get all travel recommendations history (alias for GET /)
    """
    try:
        recommendations = await service.get_all_recommendations(limit, offset)
        return [TravelRequestResponse(**rec) for rec in recommendations]
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get history: {str(e)}")

@router.get("/", response_model=List[TravelRequestResponse])
async def get_all_recommendations(
    service: RecommendationService = Depends(get_recommendation_service),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """
    Get all travel recommendations with pagination
    """
    try:
        recommendations = await service.get_all_recommendations(limit, offset)
        return [TravelRequestResponse(**rec) for rec in recommendations]
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get recommendations: {str(e)}")

@router.get("/search/", response_model=List[TravelRequestResponse])
async def search_recommendations(
    q: str = Query(..., min_length=1, description="Search term"),
    limit: int = Query(10, ge=1, le=50),
    service: RecommendationService = Depends(get_recommendation_service)
):
    """
    Search travel recommendations by text
    """
    try:
        recommendations = await service.search_recommendations(q, limit)
        return [TravelRequestResponse(**rec) for rec in recommendations]
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to search recommendations: {str(e)}")

@router.get("/statistics/")
async def get_statistics(
    service: RecommendationService = Depends(get_recommendation_service)
):
    """
    Get service statistics
    """
    try:
        return await service.get_statistics()
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get statistics: {str(e)}")

@router.delete("/{request_id}")
async def delete_recommendations(
    request_id: int,
    service: RecommendationService = Depends(get_recommendation_service)
):
    """
    Delete travel recommendations
    """
    try:
        success = await service.delete_recommendations(request_id)
        if not success:
            raise HTTPException(status_code=404, detail="Request not found")
        return {"message": "Recommendations deleted successfully"}
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete recommendations: {str(e)}") 