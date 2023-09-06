from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.profile import use_cases as profile_use_cases
from src.profile.schemas import CreateProfileSchema, ProfileSchema
from src.database.core import get_db_session

router = APIRouter()


@router.post('', response_model=ProfileSchema)
async def create_profile(
    profile_in: CreateProfileSchema,
    db_session: AsyncSession = Depends(get_db_session),
):
    profile = await profile_use_cases.create_profile(
        db_session=db_session, 
        profile_in=profile_in
    )

    return profile