from datetime import datetime as dt

from app.core.db import Base
from sqlalchemy import DATETIME, Boolean, Column, Integer


class CharityBase(Base):

    __abstract__ = True

    full_amount = Column(Integer, nullable=False, )
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DATETIME, default=dt.now)
    close_date = Column(DATETIME)

    def __repr__(self):
        return (
            f'full_amount: {self.full_amount}, '
            f'invested_amount: {self.invested_amount}, '
            f'create_date: {self.create_date}'
        )
