from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crude
from app.models.donation import Donation
from app.models.user import User
from app.schemas.donation import DonationCreate, DonationDB, DonationUser
from app.services.investing import investing

router = APIRouter()


@router.get(
    '/',
    response_model=List[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session)
) -> List[Donation]:
    donations = await donation_crude.get_multi(session)
    return donations


@router.get(
    '/my',
    response_model=List[DonationUser],
)
async def donations_user(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
) -> List[Donation]:
    donations = await donation_crude.get_by_user(user, session)
    return donations


@router.post(
    '/',
    response_model=DonationUser,
    response_model_exclude_none=True
)
async def create_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
) -> Donation:
    donation = await donation_crude.create(donation, session, user)
    await investing(donation, session)
    await session.commit()
    await session.refresh(donation)
    return donation
