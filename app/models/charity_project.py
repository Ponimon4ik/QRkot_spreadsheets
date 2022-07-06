from sqlalchemy import Column, String, Text

from app.models.base import CharityBase


class CharityProject(CharityBase):

    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return (
            f'name: {self.name[:10]}, '
            f'description: {self.description[:10]}, '
        ) + super().__repr__()
