from fastapi import HTTPException

class TravelRecommenderException(HTTPException):
    """Base exception for travel recommender application"""
    pass

class OpenAIError(TravelRecommenderException):
    """Exception raised when OpenAI API fails"""
    def __init__(self, detail: str):
        super().__init__(status_code=500, detail=f"OpenAI API error: {detail}")

class DatabaseError(TravelRecommenderException):
    """Exception raised when database operations fail"""
    def __init__(self, detail: str):
        super().__init__(status_code=500, detail=f"Database error: {detail}") 