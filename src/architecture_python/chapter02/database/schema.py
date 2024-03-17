from pydantic import BaseModel
from datetime import date
from typing import List, Optional

class BatchBase(BaseModel):
    ref: str
    sku: str
    qty: int
    eta: Optional[date]