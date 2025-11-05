from pydantic import BaseModel
from typing import Optional


class TelexIncoming(BaseModel):
    user_id: str
    message: Optional[str] = None
    image_url: Optional[str] = None
    metadata: Optional[dict] = {}


class TelexResponse(BaseModel):
    user_id: str
    response: str
    quick_replies: Optional[list[str]] = None
