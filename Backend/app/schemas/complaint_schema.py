# Pydantic BaseModel is used to create data validation schemas
from pydantic import BaseModel

# Optional allows fields to be None or missing
from typing import Optional, List

# UUID type used for identifiers
from uuid import UUID


# Schema for location data sent by frontend
class LocationCreate(BaseModel):

    # Latitude coordinate
    latitude: float

    # Longitude coordinate
    longitude: float

    # Optional street address
    address: Optional[str] = None

    # Optional city name
    city: Optional[str] = None

    # Optional district name
    district: Optional[str] = None


# Schema used when creating a complaint
class ComplaintCreate(BaseModel):

    # Type of issue (road_damage, garbage, etc.)
    issue_type: str

    # Short title of the complaint
    title: str

    # Detailed description of the problem
    description: str

    # Optional priority level
    priority: Optional[str] = "medium"

    # Nested location object
    location: LocationCreate

    # Optional list of image URLs from Firebase
    image_urls: Optional[List[str]] = []


# Schema used for API responses
class ComplaintResponse(BaseModel):

    # Complaint unique identifier
    complaint_id: UUID

    # Citizen who reported the complaint
    citizen_id: UUID

    # Location reference
    location_id: UUID

    # Issue type
    issue_type: str

    # Complaint description
    description: str

    # Current complaint status
    status: str


    # Allows Pydantic to convert SQLAlchemy models to JSON
    class Config:
        from_attributes = True