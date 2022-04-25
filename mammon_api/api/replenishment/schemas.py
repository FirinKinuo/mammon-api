from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Replenishment(BaseModel):
    id: int
    datetime: datetime
    currency: int


class ReplenishmentDate(BaseModel):
    start: Optional[datetime] = datetime.min
    end: Optional[datetime] = datetime.max
