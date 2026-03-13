from pydantic import BaseModel
from uuid import UUID


class NearbyComplaint(BaseModel):

    complaint_id: UUID
    issue_type: str
    status: str
    latitude: float
    longitude: float
    address: str | None