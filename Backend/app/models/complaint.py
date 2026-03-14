from sqlalchemy import Column, String, Text, ForeignKey, DateTime, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from app.database import Base


class Complaint(Base):

    __tablename__ = "complaints"

    complaint_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    citizen_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)

    location_id = Column(UUID(as_uuid=True), ForeignKey("locations.location_id"), nullable=False)

    issue_type = Column(String(50), nullable=False)

    title = Column(String(150), nullable=False)

    description = Column(Text, nullable=False)

    status = Column(String(30), default="pending")

    priority = Column(String(20), default="medium")

    verification_count = Column(Integer, default=0)

    not_fixed_count = Column(Integer, default=0)

    is_hidden = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())