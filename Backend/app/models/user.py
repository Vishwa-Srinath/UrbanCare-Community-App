# Import column types from SQLAlchemy
from sqlalchemy import Column, String, Boolean, DateTime

# Import PostgreSQL specific UUID type
# This allows the database to store UUIDs efficiently
from sqlalchemy.dialects.postgresql import UUID

# func provides SQL functions like NOW()
from sqlalchemy.sql import func

# Python library used to generate UUIDs
import uuid

# Base class for all database models
from app.database import Base


# This class represents the "users" table in PostgreSQL
class User(Base):

    # Table name in the database
    __tablename__ = "users"

    # Primary key column
    # UUID(as_uuid=True) means PostgreSQL UUID type
    # default=uuid.uuid4 automatically generates a UUID when a new user is created
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Name of the user
    # max length = 100 characters
    name = Column(String(100), nullable=False)

    # Email address
    # unique=True means no two users can have the same email
    email = Column(String(255), unique=True, nullable=False)

    # Password is stored as a hash (not the real password)
    password_hash = Column(String(255), nullable=False)

    # User role
    # examples: citizen, authority, admin
    role = Column(String(20), nullable=False)

    # Whether the account is active or disabled
    is_active = Column(Boolean, default=True)

    # Time the account was created
    # server_default=func.now() automatically stores the current timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Time the account was last updated
    updated_at = Column(DateTime(timezone=True), server_default=func.now())