from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class LocationCreate(BaseModel):
    latitude: float
    longitude: float
    address: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None


class ComplaintCreate(BaseModel):

    citizen_id: UUID

    issue_type: str

    description: str

    location: LocationCreate

    primary_image_url: Optional[str] = None


class ComplaintResponse(BaseModel):

    complaint_id: UUID
    citizen_id: UUID
    location_id: UUID

    issue_type: str
    description: str
    status: str

    class Config:
        from_attributes = True