# BaseModel is used to create schemas in FastAPI/Pydantic
from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID


# This schema defines the location data the frontend sends
class LocationCreate(BaseModel):
    # latitude is required
    latitude: float

    # longitude is required
    longitude: float

    # address is optional
    address: Optional[str] = None

    # city is optional
    city: Optional[str] = None

    # district is optional
    district: Optional[str] = None


# This schema defines the full complaint data the frontend sends
class ComplaintCreate(BaseModel):
    # user who created the complaint
    citizen_id: UUID

    # type of issue
    # example: road_damage, garbage, water_leak
    issue_type: str

    # short title of complaint
    title: str

    # full description
    description: str

    # optional priority
    # if not sent, default value becomes "medium"
    priority: Optional[str] = "medium"

    # nested location object
    location: LocationCreate

    # optional list of image URLs
    image_urls: Optional[List[str]] = []


# This schema defines the response sent back to frontend
class ComplaintResponse(BaseModel):
    # complaint ID from database
    complaint_id: UUID

    # user ID
    citizen_id: UUID

    # linked location ID
    location_id: UUID

    # complaint details
    issue_type: str
    title: str
    description: str
    status: str
    priority: str

    # very important:
    # this tells Pydantic it can read data directly from SQLAlchemy model objects
    class Config:
        from_attributes = True