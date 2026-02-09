from pydantic import BaseModel
from typing import Optional, Any

class JSONAPIResource(BaseModel):
    type: str
    id : str
    attributes : Optional[dict]
    relationships : Optional[dict]

class JSONAPIResponse(BaseModel):
    links : Optional[dict[str, Any]] = None
    data: Optional[list] = None
