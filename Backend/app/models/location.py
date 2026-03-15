from sqlalchemy import Column, String, Float
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.database import Base


# This class represents the "locations" table in the database
class Location(Base):
    __tablename__ = "locations"

    # Primary key for location table
    # UUID is automatically generated when a new location is created
    location_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Latitude of the location
    latitude = Column(Float, nullable=False)

    # Longitude of the location
    longitude = Column(Float, nullable=False)

    # Optional address text
    address = Column(String(255), nullable=True)

    # Optional city name
    city = Column(String(100), nullable=True)

    # Optional district name
    district = Column(String(100), nullable=True)