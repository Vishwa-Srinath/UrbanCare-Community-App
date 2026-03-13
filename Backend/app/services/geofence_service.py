from sqlalchemy.orm import Session
from sqlalchemy import text
import json

from app.core.redis_client import redis_client


def get_nearby_complaints(db: Session, lat: float, lng: float):

    cache_key = f"geo:{round(lat,3)}:{round(lng,3)}"

    cached = redis_client.get(cache_key)

    if cached:
        return json.loads(cached)

    query = text("""
        SELECT *
        FROM (
            SELECT
                c.complaint_id,
                c.issue_type,
                c.status,
                l.latitude,
                l.longitude,
                l.address,
                (
                    6371000 * acos(
                        cos(radians(:lat)) *
                        cos(radians(l.latitude)) *
                        cos(radians(l.longitude) - radians(:lng)) +
                        sin(radians(:lat)) *
                        sin(radians(l.latitude))
                    )
                ) AS distance
            FROM complaints c
            JOIN locations l
            ON c.location_id = l.location_id
        ) AS subquery
        WHERE distance < 5000
        ORDER BY distance
        LIMIT 50
    """)

    result = db.execute(query, {"lat": lat, "lng": lng})

    complaints = []

    for row in result:
        data = dict(row._mapping)
        complaints.append(data)

    # Cache result for 5 minutes
    redis_client.setex(cache_key, 300, json.dumps(complaints, default=str))

    return complaints