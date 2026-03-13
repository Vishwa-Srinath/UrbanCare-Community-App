from sqlalchemy import Column, String, Date, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.database import Base


class Citizen(Base):
    __tablename__ = "citizens"

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id"),
        primary_key=True
    )

    phone_number = Column(String(15))

    address = Column(String)

    date_of_birth = Column(Date)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    updated_at = Column(DateTime(timezone=True), server_default=func.now())