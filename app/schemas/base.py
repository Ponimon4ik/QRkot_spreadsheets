from datetime import datetime as dt
from typing import Optional

from pydantic import BaseModel, Field


class CharityBase(BaseModel):

    id: int
    invested_amount: int = Field(0, ge=0)
    fully_invested: bool = Field(False)
    create_date: dt
    close_date: Optional[dt]
