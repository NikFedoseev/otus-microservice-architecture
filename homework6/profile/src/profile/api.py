from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.core import get_db_session
from src.profile.schemas import UpdateProfileSchema, ProfileOutSchema 
import src.profile.use_cases as profile_use_cases

router = APIRouter()

@router.patch('/{profile_id}', response_model=ProfileOutSchema)
async def update_profile(
    profile_id: int,
    profile_in: UpdateProfileSchema,
    x_profile_id: str | None = Header(),
    db_session: AsyncSession = Depends(get_db_session)
):
    if not x_profile_id or int(x_profile_id) != profile_id:
        raise HTTPException(status_code=403)
    
    res = await profile_use_cases.update_profile(
        db_session=db_session,
        profile_id=profile_id,
        profile_in=profile_in
    )

    return res


@router.get('/me', response_model=ProfileOutSchema)
async def my_profile(
    x_profile_id: str | None = Header(),
    db_session: AsyncSession = Depends(get_db_session)
):
    if not x_profile_id:
        raise HTTPException(status_code=401, detail="profile_id required")
    
    res = await profile_use_cases.find_profile_by_id(
        id=int(x_profile_id),
        db_session=db_session
    )

    if not res:
        raise HTTPException(status_code=404)

    return res


@router.get('/{profile_id}', response_model=ProfileOutSchema)
async def get_profile_by_id(
    profile_id: int,
    x_profile_id: str | None = Header(),
    db_session: AsyncSession = Depends(get_db_session)
):
    if not x_profile_id or int(x_profile_id) != profile_id:
        raise HTTPException(status_code=403)
    
    res = await profile_use_cases.find_profile_by_id(
        id=int(profile_id),
        db_session=db_session
    )

    if not res:
        raise HTTPException(status_code=404)

    return res