from pydantic import BaseModel
from typing import Optional

class StateSchema(BaseModel):
    filters: Optional[dict] = None
    products: Optional[list] = None
    result: Optional[str] = None
