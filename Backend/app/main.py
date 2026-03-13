# Import FastAPI framework
from fastapi import FastAPI

from app.routes import auth_routes
from app.routes import geofence_routes
# Import route files
from app.routes import auth_routes
from app.routes import complaint_routes

# Import models so SQLAlchemy knows about them
# These imports help register the tables in the ORM
from app.models.user import User
from app.models.location import Location
from app.models.complaint import Complaint
from app.models.complaint_image import ComplaintImage


# Create the FastAPI application
app = FastAPI(
    title="UrbanCare Backend",
    description="Backend API for complaint reporting system",
    version="1.0.0"
)


# Include authentication routes
# Example:
# /login
# /register
app.include_router(auth_routes.router)


# Include complaint routes
# Example:
# POST /complaints
# GET /complaints
# GET /complaints/{complaint_id}
app.include_router(complaint_routes.router)

app.include_router(geofence_routes.router)
# Simple test route
# This helps check whether the backend is running properly
@app.get("/")
def root():
    return {"message": "UrbanCare backend is running"}
