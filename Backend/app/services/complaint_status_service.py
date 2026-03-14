from sqlalchemy.orm import Session
from app.models.complaint import Complaint


def get_status(db: Session, complaint_id):

    complaint = db.query(Complaint).filter(
        Complaint.complaint_id == complaint_id
    ).first()

    if not complaint:
        return None

    return complaint.status