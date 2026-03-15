# SQLAlchemy session used to interact with database
from sqlalchemy.orm import Session

# Used to raise API errors
from fastapi import HTTPException

# Import database models
from app.models.complaint import Complaint
from app.models.complaint_verification import ComplaintVerification


# Service class that handles complaint verification logic
class ComplaintVerificationService:

    # Constructor receives database session
    def __init__(self, db: Session):
        self.db = db


    # Method to verify a complaint
    # complaint_id = complaint being verified
    # citizen_id = user performing verification
    # is_fixed = True if issue is fixed, False if still broken
    def verify_complaint(self, complaint_id, citizen_id, is_fixed):

        # ---------------------------------
        # STEP 1 — Find the complaint
        # ---------------------------------
        complaint = self.db.query(Complaint).filter(
            Complaint.complaint_id == complaint_id
        ).first()

        # If complaint does not exist return error
        if not complaint:
            raise HTTPException(status_code=404, detail="Complaint not found")


        # ---------------------------------
        # STEP 2 — Prevent duplicate verification
        # ---------------------------------
        existing = self.db.query(ComplaintVerification).filter(
            ComplaintVerification.complaint_id == complaint_id,
            ComplaintVerification.citizen_id == citizen_id
        ).first()

        if existing:
            raise HTTPException(
                status_code=400,
                detail="User already verified this complaint"
            )


        # ---------------------------------
        # STEP 3 — Create verification record
        # ---------------------------------
        verification = ComplaintVerification(
            complaint_id=complaint_id,
            citizen_id=citizen_id,
            is_fixed=is_fixed
        )

        # Add verification row to database
        self.db.add(verification)


        # ---------------------------------
        # STEP 4 — Update complaint counters
        # ---------------------------------
        if is_fixed:
            # Citizen confirmed issue is fixed
            complaint.verification_count += 1
        else:
            # Citizen says issue still exists
            complaint.not_fixed_count += 1


        # ---------------------------------
        # STEP 5 — Close complaint if enough confirmations
        # ---------------------------------
        if complaint.verification_count >= 10:
            complaint.status = "fixed"
            complaint.is_hidden = True


        # ---------------------------------
        # STEP 6 — Reopen complaint if many users say not fixed
        # ---------------------------------
        if complaint.not_fixed_count >= 5:
            complaint.status = "pending"

            # reset counters
            complaint.verification_count = 0
            complaint.not_fixed_count = 0


        # ---------------------------------
        # STEP 7 — Save changes
        # ---------------------------------
        self.db.commit()

        # reload updated complaint from database
        self.db.refresh(complaint)

        return complaint