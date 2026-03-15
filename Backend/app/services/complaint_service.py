# Import SQLAlchemy database session type
from sqlalchemy.orm import Session

# Import models used in complaint creation
from app.models.location import Location
from app.models.complaint import Complaint
from app.models.complaint_image import ComplaintImage


# Service class that contains complaint-related business logic
class ComplaintService:

    # Constructor receives the database session
    def __init__(self, db: Session):
        self.db = db


    # Method to create a new complaint
    # data = validated complaint data from Pydantic schema
    # citizen_id = ID of the currently logged-in citizen
    def create_complaint(self, data, citizen_id):

        # -----------------------------
        # STEP 1 — Save location first
        # -----------------------------
        # Create a Location object using nested location data from request
        location = Location(
            latitude=data.location.latitude,
            longitude=data.location.longitude,
            address=data.location.address,
            city=data.location.city,
            district=data.location.district
        )

        # Add location to database session
        self.db.add(location)

        # Flush sends the INSERT to the database without committing yet
        # This allows location.location_id to be generated and available now
        self.db.flush()


        # -----------------------------
        # STEP 2 — Save complaint
        # -----------------------------
        # Create the complaint object
        complaint = Complaint(
            citizen_id=citizen_id,                 # logged-in citizen
            location_id=location.location_id,      # link to saved location
            issue_type=data.issue_type,            # type of issue
            title=data.title,                      # short title
            description=data.description,          # detailed description
            status="created",                      # initial complaint status
            priority=data.priority                 # priority from request
        )

        # Add complaint to database session
        self.db.add(complaint)

        # Flush again so complaint.complaint_id becomes available
        self.db.flush()


        # -----------------------------
        # STEP 3 — Save complaint images
        # -----------------------------
        # Only run if image URLs were provided
        if data.image_urls:
            for url in data.image_urls:
                image = ComplaintImage(
                    complaint_id=complaint.complaint_id,  # link image to complaint
                    image_url=url                         # URL stored in Firebase/cloud
                )
                self.db.add(image)


        # -----------------------------
        # STEP 4 — Commit everything
        # -----------------------------
        # Commit permanently saves all inserts:
        # location + complaint + images
        self.db.commit()

        # Refresh the complaint object from database
        self.db.refresh(complaint)

        # Return the saved complaint
        return complaint


    # Get all complaints from database
    def get_all_complaints(self):
        return self.db.query(Complaint).all()


    # Get one complaint by its ID
    def get_complaint_by_id(self, complaint_id):
        return (
            self.db.query(Complaint)
            .filter(Complaint.complaint_id == complaint_id)
            .first()
        )