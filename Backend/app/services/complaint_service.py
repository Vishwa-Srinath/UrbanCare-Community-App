from sqlalchemy.orm import Session

from app.models.location import Location
from app.models.complaint import Complaint
from app.models.complaint_image import ComplaintImage


class ComplaintService:

    def __init__(self, db: Session):
        self.db = db


    def create_complaint(self, data):

        # -----------------------------
        # STEP 1 — Save location
        # -----------------------------
        location = Location(
            latitude=data.location.latitude,
            longitude=data.location.longitude,
            address=data.location.address,
            city=data.location.city,
            district=data.location.district
        )

        self.db.add(location)
        self.db.flush()


        # -----------------------------
        # STEP 2 — Save complaint
        # -----------------------------
        complaint = Complaint(
            citizen_id=data.citizen_id,
            location_id=location.location_id,
            issue_type=data.issue_type,
            title=data.title,
            description=data.description,
            status="pending",
            priority=data.priority
        )

        self.db.add(complaint)
        self.db.flush()


        # -----------------------------
        # STEP 3 — Save images
        # -----------------------------
        if data.image_urls:
            for url in data.image_urls:
                image = ComplaintImage(
                    complaint_id=complaint.complaint_id,
                    image_url=url
                )
                self.db.add(image)


        # -----------------------------
        # STEP 4 — Commit transaction
        # -----------------------------
        self.db.commit()
        self.db.refresh(complaint)

        return complaint


    def get_all_complaints(self):
        return self.db.query(Complaint).all()


    def get_complaint_by_id(self, complaint_id):
        return (
            self.db.query(Complaint)
            .filter(Complaint.complaint_id == complaint_id)
            .first()
        )