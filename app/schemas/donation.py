from datetime import datetime as dt
from typing import Optional

from pydantic import BaseModel, Extra, PositiveInt


class DonationBase(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str] = None

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    pass


class DonationUser(DonationBase):

    id: int
    create_date: dt

    class Config:
        orm_mode = True


class DonationDB(DonationUser):

    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[dt]
