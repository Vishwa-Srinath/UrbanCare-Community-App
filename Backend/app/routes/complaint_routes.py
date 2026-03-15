# APIRouter groups complaint-related API endpoints
# Depends is used for dependency injection
# HTTPException is used for errors like 404 Not Found
from fastapi import APIRouter, Depends, HTTPException

# SQLAlchemy session type
from sqlalchemy.orm import Session

# Database session provider
from app.database import get_db

# Request and response schemas
from app.schemas.complaint_schema import ComplaintCreate, ComplaintResponse

# Complaint business logic
from app.services.complaint_service import ComplaintService

# Auth dependency to get currently logged-in user
from app.dependencies.auth_dependency import get_current_user

# Verification business logic
from app.services.complaint_verification_service import ComplaintVerificationService

# Used when returning multiple complaints
from typing import List

# UUID type for complaint IDs
from uuid import UUID


# Create complaint router
# All routes here start with /complaints
router = APIRouter(prefix="/complaints", tags=["Complaints"])


# ----------------------------------------
# POST /complaints
# Create a new complaint
# ----------------------------------------



@router.post("/", response_model=ComplaintResponse)
def create_complaint(
    data: ComplaintCreate,                    # request body validated by schema
    user=Depends(get_current_user),          # logged-in user from auth
    db: Session = Depends(get_db)            # database session
):
    # Create complaint service object
    service = ComplaintService(db)

    # Save complaint using request data and logged-in user's ID
    complaint = service.create_complaint(data, user["user_id"])

    # Return created complaint
    return complaint




# ----------------------------------------
# GET /complaints
# Get all complaints
# ----------------------------------------
@router.get("/", response_model=List[ComplaintResponse])
def get_all_complaints(db: Session = Depends(get_db)):
    # Create complaint service
    service = ComplaintService(db)

    # Return all complaints from database
    return service.get_all_complaints()


# ----------------------------------------
# GET /complaints/{complaint_id}
# Get one complaint by ID
# ----------------------------------------
@router.get("/{complaint_id}", response_model=ComplaintResponse)
def get_complaint(complaint_id: UUID, db: Session = Depends(get_db)):
    # Create complaint service
    service = ComplaintService(db)

    # Find complaint by its ID
    complaint = service.get_complaint_by_id(complaint_id)

    # Return 404 if not found
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")

    # Return complaint if found
    return complaint


# ----------------------------------------
# POST /complaints/{complaint_id}/verify
# Citizen verifies whether issue is fixed
# Example:
# POST /complaints/{id}/verify?is_fixed=true
# ----------------------------------------
@router.post("/{complaint_id}/verify")
def verify_complaint(
    complaint_id: UUID,                       # complaint being verified
    is_fixed: bool,                           # verification result
    user=Depends(get_current_user),          # current logged-in user
    db: Session = Depends(get_db)            # database session
):
    # Create verification service
    service = ComplaintVerificationService(db)

    # Verify complaint using service logic
    return service.verify_complaint(
        complaint_id,
        user["user_id"],
        is_fixed
    )