from sqlalchemy import Column, Text, ForeignKey, DateTime, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from app.database import Base


class Complaint(Base):
    __tablename__ = "complaints"

    complaint_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    citizen_id = Column(UUID(as_uuid=True), ForeignKey("citizens.user_id"))

    assigned_authority_id = Column(UUID(as_uuid=True), ForeignKey("authorities.authority_id"), nullable=True)

    location_id = Column(UUID(as_uuid=True), ForeignKey("locations.location_id"))

    issue_type = Column(Text, nullable=False)

    description = Column(Text, nullable=False)

    status = Column(Text, default="created")

    primary_image_url = Column(Text)

    estimated_fix_at = Column(DateTime(timezone=True))
    fixed_at = Column(DateTime(timezone=True))

    community_verified = Column(Boolean, default=False)

    confirm_yes_count = Column(Integer, default=0)
    confirm_no_count = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )