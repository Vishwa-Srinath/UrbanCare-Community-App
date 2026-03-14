# APIRouter is used to group related API endpoints together
# Depends is used for dependency injection, like database connection
# HTTPException is used to return errors like 404 Not Found
from fastapi import APIRouter, Depends, HTTPException

# Session type for database access
from sqlalchemy.orm import Session

# get_db gives us a database session
from app.database import get_db

# Import schemas for request and response validation
from app.schemas.complaint_schema import ComplaintCreate, ComplaintResponse

# Import the service layer
from app.services.complaint_service import ComplaintService

# List is used for returning multiple complaints
from typing import List

from uuid import UUID

# Create a router object
# prefix="/complaints" means all routes start with /complaints
# tags=["Complaints"] groups these endpoints in Swagger docs
router = APIRouter(prefix="/complaints", tags=["Complaints"])


# ----------------------------------------
# POST /complaints
# Create a new complaint
# ----------------------------------------
@router.post("/", response_model=ComplaintResponse)
def create_complaint(data: ComplaintCreate, db: Session = Depends(get_db)):

    # Create service object and pass database session into it
    service = ComplaintService(db)

    # Call service method to create complaint
    complaint = service.create_complaint(data)

    # Return the saved complaint
    return complaint


# ----------------------------------------
# GET /complaints
# Get all complaints
# ----------------------------------------
@router.get("/", response_model=List[ComplaintResponse])
def get_all_complaints(db: Session = Depends(get_db)):

    # Create service object
    service = ComplaintService(db)

    # Return all complaints from database
    return service.get_all_complaints()


# ----------------------------------------
# GET /complaints/{complaint_id}
# Get one complaint by ID
# ----------------------------------------
@router.get("/{complaint_id}", response_model=ComplaintResponse)

def get_complaint(complaint_id: UUID, db: Session = Depends(get_db)):

    # Create service object
    service = ComplaintService(db)

    # Ask service to find complaint by ID
    complaint = service.get_complaint_by_id(complaint_id)

    # If complaint does not exist, return 404 error
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")

    # Return complaint if found
    return complaint

from app.services.complaint_verification_service import ComplaintVerificationService


@router.post("/{complaint_id}/verify")
def verify_complaint(
    complaint_id: str,
    citizen_id: str,
    is_fixed: bool,
    db: Session = Depends(get_db)
):

    service = ComplaintVerificationService(db)

    return service.verify_complaint(
        complaint_id,
        citizen_id,
        is_fixed
    )