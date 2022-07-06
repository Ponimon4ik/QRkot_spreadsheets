from typing import Optional, List

from sqlalchemy import select, true
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):

    @staticmethod
    async def get_project_by_name(
            project_name: str,
            session: AsyncSession,
    ) -> Optional[CharityProject]:
        project = await session.execute(
            select(CharityProject).where(
                CharityProject.name == project_name
            )
        )
        return project.scalars().first()

    @staticmethod
    async def get_projects_by_completion_rate(
            session: AsyncSession,
    ) -> List[CharityProject]:
        closed_projects = await session.execute(
            select(
                [CharityProject.name,
                 CharityProject.create_date,
                 CharityProject.close_date,
                 CharityProject.description
                 ]
            ).where(
                CharityProject.fully_invested == true()
            )
        )
        return closed_projects.all()


charity_project_crud = CRUDCharityProject(CharityProject)
