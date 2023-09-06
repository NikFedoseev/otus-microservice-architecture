from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa

from src.profile.schemas import CreateProfileSchema, ProfileSchema, UpdateProfileSchema
from src.profile.models import ProfileModel


async def create_profile(
    db_session: AsyncSession,
    profile_in: CreateProfileSchema
):
    profile = ProfileModel(**profile_in.model_dump())
    db_session.add(profile)

    await db_session.commit()

    return ProfileSchema.model_validate(profile)


async def update_profile(
    db_session: AsyncSession,
    profile_id: int,
    profile_in: UpdateProfileSchema
):
    stmt = (
        sa.update(ProfileModel)
        .where(ProfileModel.id == profile_id)
        .values(**profile_in.model_dump(exclude_none=True))
        .returning(ProfileModel)
    )

    res = await db_session.scalar(stmt)

    return ProfileSchema.model_validate(res)


async def find_profile_by_id(
    id: int,
    db_session: AsyncSession
):
    res = await db_session.scalar(
        sa.select(ProfileModel).where(ProfileModel.id == id)
    )

    if not res:
        return None
    
    return ProfileSchema.model_validate(res)