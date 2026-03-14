from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.complaint import Complaint
from app.models.complaint_verification import ComplaintVerification


class ComplaintVerificationService:

    def __init__(self, db: Session):
        self.db = db

    def verify_complaint(self, complaint_id, citizen_id, is_fixed):

        complaint = self.db.query(Complaint).filter(
            Complaint.complaint_id == complaint_id
        ).first()

        if not complaint:
            raise HTTPException(status_code=404, detail="Complaint not found")

        # prevent duplicate verification
        existing = self.db.query(ComplaintVerification).filter(
            ComplaintVerification.complaint_id == complaint_id,
            ComplaintVerification.citizen_id == citizen_id
        ).first()

        if existing:
            raise HTTPException(
                status_code=400,
                detail="User already verified this complaint"
            )

        verification = ComplaintVerification(
            complaint_id=complaint_id,
            citizen_id=citizen_id,
            is_fixed=is_fixed
        )

        self.db.add(verification)

        if is_fixed:
            complaint.verification_count += 1
        else:
            complaint.not_fixed_count += 1

        # hide complaint if enough confirmations
        if complaint.verification_count >= 10:
            complaint.status = "hidden"
            complaint.is_hidden = True

        # reopen complaint
        if complaint.not_fixed_count >= 5:
            complaint.status = "pending"
            complaint.verification_count = 0
            complaint.not_fixed_count = 0

        self.db.commit()

        self.db.refresh(complaint)

        return complaint