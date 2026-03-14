from sqlalchemy import Column, Boolean, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from app.database import Base


class ComplaintVerification(Base):

    __tablename__ = "complaint_verifications"

    verification_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    complaint_id = Column(UUID(as_uuid=True), ForeignKey("complaints.complaint_id"))

    citizen_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"))

    is_fixed = Column(Boolean, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())