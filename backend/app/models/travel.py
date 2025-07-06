from sqlalchemy import Column, Integer, String, DateTime, JSON, Text
from sqlalchemy.sql import func
from app.core.database import Base

class TravelRequest(Base):
    __tablename__ = "travel_requests"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)  # User's request text
    exclude = Column(JSON, nullable=True)  # List of places to exclude
    num_places = Column(Integer, default=3)  # Number of places to recommend
    response_json = Column(JSON, nullable=False)  # AI response with places
    created_at = Column(DateTime(timezone=True), server_default=func.now()) 