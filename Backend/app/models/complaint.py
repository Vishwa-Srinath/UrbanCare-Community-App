from sqlalchemy import Column, String, Text, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from app.database import Base


# This class represents the "complaints" table
class Complaint(Base):
    __tablename__ = "complaints"

    # Primary key for complaint table
    complaint_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Foreign key to users table
    # This tells us which user created the complaint
    citizen_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)

    # Foreign key to locations table
    # This tells us where the complaint happened
    location_id = Column(UUID(as_uuid=True), ForeignKey("locations.location_id"), nullable=False)

    # Type of issue
    # Example: road_damage, garbage, water_leak
    issue_type = Column(String(50), nullable=False)

    # Short title for the complaint
    title = Column(String(150), nullable=False)

    # Full description of the issue
    description = Column(Text, nullable=False)

    # Current complaint status
    # Example: pending, in_progress, resolved
    status = Column(String(30), default="pending")

    # Priority level
    # Example: low, medium, high
    priority = Column(String(20), default="medium")

    # Automatically stores the time when complaint is created
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Automatically stores the latest update time
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())