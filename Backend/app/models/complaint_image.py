from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.database import Base


# This class represents the "complaint_images" table
class ComplaintImage(Base):
    __tablename__ = "complaint_images"

    # Primary key for image table
    image_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Foreign key to complaints table
    # This tells us which complaint this image belongs to
    complaint_id = Column(UUID(as_uuid=True), ForeignKey("complaints.complaint_id"), nullable=False)

    # URL of the uploaded image
    # Usually this comes from Firebase or cloud storage
    image_url = Column(String(500), nullable=False)