# Import database session type
from sqlalchemy.orm import Session

# Import models (database tables)
from app.models.location import Location
from app.models.complaint import Complaint
from app.models.complaint_image import ComplaintImage


# ComplaintService contains all logic related to complaints
class ComplaintService:

    # constructor receives the database session
    def __init__(self, db: Session):
        self.db = db


    # Create a new complaint
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

        # Add location object to database session
        self.db.add(location)

        # Flush sends the insert query to DB but does not commit yet
        # This allows us to access the generated location_id
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

        # Add complaint to database session
        self.db.add(complaint)

        # Flush so complaint_id becomes available
        self.db.flush()


        # -----------------------------
        # STEP 3 — Save images
        # -----------------------------
        for url in data.image_urls:

            image = ComplaintImage(
                complaint_id=complaint.complaint_id,
                image_url=url
            )

            # Add each image row
            self.db.add(image)


        # -----------------------------
        # STEP 4 — Commit transaction
        # -----------------------------
        # Commit writes everything permanently to database
        self.db.commit()

        # Refresh loads updated data from DB
        self.db.refresh(complaint)

        return complaint


    # Get all complaints
    def get_all_complaints(self):
        return self.db.query(Complaint).all()


    # Get a complaint by ID
    def get_complaint_by_id(self, complaint_id):

        return (
            self.db.query(Complaint)
            .filter(Complaint.complaint_id == complaint_id)
            .first()
        )