from typing import Optional
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


NAME_DUPLICATE = 'Проект с таким именем уже существует!'
PROJECT_NOT_FOUND = 'Проект не найден'
LESS_INVESTED = 'Новая сумма не может быть меньше внесенной!'
FORBID_UPDATE_FULLY_INVESTED_PROJECT = 'Закрытый проект нельзя редактировать!'
FORBID_DELETE_INVESTED_PROJECT = (
    'В проект были внесены средства, не подлежит удалению!'
)


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    project = await charity_project_crud.get_project_by_name(
        project_name, session
    )
    if project:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=NAME_DUPLICATE
        )


class ValidateProject:

    @staticmethod
    async def check_project(
            project_id: int,
            session: AsyncSession
    ) -> Optional[CharityProject]:
        project = await charity_project_crud.get(project_id, session)
        if not project:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=PROJECT_NOT_FOUND
            )
        return project

    @staticmethod
    def check_fully_invested_project(
            project: CharityProject
    ) -> None:
        if project.fully_invested:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=FORBID_UPDATE_FULLY_INVESTED_PROJECT
            )

    @staticmethod
    def check_invested_project(
            project: CharityProject
    ) -> None:
        if project.invested_amount > 0:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=FORBID_DELETE_INVESTED_PROJECT
            )

    @staticmethod
    def check_project_new_full_amount(
            project: CharityProject,
            obj_in: CharityProjectUpdate
    ) -> None:
        if project.invested_amount > obj_in.full_amount:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=LESS_INVESTED
            )


validate_project = ValidateProject()
