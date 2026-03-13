from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.services.geofence_service import get_nearby_complaints
from app.schemas.geofence_schema import NearbyComplaint

router = APIRouter(
    prefix="/geofence",
    tags=["Geofence"]
)


@router.get("/nearby", response_model=List[NearbyComplaint])
def nearby_damage(lat: float, lng: float, db: Session = Depends(get_db)):

    complaints = get_nearby_complaints(db, lat, lng)

    return complaints