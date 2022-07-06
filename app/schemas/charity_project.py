from datetime import datetime as dt
from typing import Optional

from pydantic import (
    BaseModel, Extra, Field, PositiveInt, root_validator
)


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str]
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid
        min_anystr_length = 1

    @root_validator()
    def values_is_not_null(cls, values):
        for value in values:
            if values[value] == '':
                raise ValueError(f'Нельзя назначать пустое {value}')
        return values


class CharityProjectUpdate(CharityProjectBase):
    pass


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., max_length=100)
    description: str
    full_amount: PositiveInt


class CharityProjectDB(CharityProjectBase):

    id: int
    invested_amount: int
    fully_invested: bool
    create_date: dt
    close_date: Optional[dt]

    class Config:
        orm_mode = True
