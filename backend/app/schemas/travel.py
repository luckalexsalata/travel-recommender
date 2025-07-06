from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Coordinates(BaseModel):
    lat: float
    lng: float

class Place(BaseModel):
    name: str
    description: str
    coords: Coordinates

class TravelRequestCreate(BaseModel):
    text: str
    num_places: Optional[int] = 3
    exclude: Optional[List[str]] = None

class TravelRequestUpdate(BaseModel):
    exclude: List[str]

class TravelRequestResponse(BaseModel):
    id: int
    text: str
    exclude: Optional[List[str]]
    num_places: int
    response_json: List[Place]
    created_at: datetime

    class Config:
        from_attributes = True 