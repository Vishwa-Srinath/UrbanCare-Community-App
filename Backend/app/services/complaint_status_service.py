# Import SQLAlchemy session
from sqlalchemy.orm import Session

# Import Complaint model
from app.models.complaint import Complaint


# Function to get the status of a complaint
def get_status(db: Session, complaint_id):

    # Query the complaints table to find the complaint with the given ID
    complaint = db.query(Complaint).filter(
        Complaint.complaint_id == complaint_id
    ).first()

    # If no complaint is found, return None
    if not complaint:
        return None

    # Return only the complaint status
    return complaint.status