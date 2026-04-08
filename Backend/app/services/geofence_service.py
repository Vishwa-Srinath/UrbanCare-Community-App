# Import text() so we can write raw SQL queries safely
from sqlalchemy import text

# Import Session type for database operations
from sqlalchemy.orm import Session


# Service class for geofence-related operations
class GeofenceService:

    # Constructor receives the database session
    def __init__(self, db: Session):
        self.db = db

    # Method to get complaints near a given point
    def get_nearby_complaints(
        self,
        lat: float,          # user's latitude
        lng: float,          # user's longitude
        radius_m: int = 5000,  # search radius in meters
        limit: int = 50         # maximum number of results
    ):
        # Raw SQL query using PostGIS functions
        query = text("""
            SELECT
                -- Complaint details
                c.complaint_id,
                c.issue_type,
                c.title,
                c.description,
                c.status,
                c.priority,

                -- Location details
                l.latitude,
                l.longitude,
                l.address,
                l.city,
                l.district,

                -- Calculate exact distance from user location to complaint location
                ST_Distance(
                    l.geog,
                    ST_SetSRID(ST_MakePoint(:lng, :lat), 4326)::geography
                ) AS distance_m

            FROM complaints c

            -- Join complaints with locations using location_id
            JOIN locations l
              ON c.location_id = l.location_id

            WHERE
                -- Only show complaints that are not hidden
                c.is_hidden = FALSE

                -- Make sure the spatial column exists
                AND l.geog IS NOT NULL

                -- Only return complaints within the given radius
                AND ST_DWithin(
                    l.geog,
                    ST_SetSRID(ST_MakePoint(:lng, :lat), 4326)::geography,
                    :radius_m
                )

            -- Show nearest complaints first
            ORDER BY distance_m

            -- Limit total rows returned
            LIMIT :limit
        """)

        # Execute the query with actual parameter values
        result = self.db.execute(
            query,
            {
                "lat": lat,
                "lng": lng,
                "radius_m": radius_m,
                "limit": limit
            }
        )

        # Convert each returned row into a normal dictionary
        # row._mapping gives dictionary-like access to columns
        return [dict(row._mapping) for row in result]