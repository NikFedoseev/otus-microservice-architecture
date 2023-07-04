from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.core import get_db_session
from app.user.schemas import (
    UserOutSchema, CreateUserSchema, UpdateUserSchema
)
from app.user.exceptions import UserNotFound
import app.user.use_cases as user_use_cases

user_router = APIRouter()

@user_router.post('')
async def create_user(
    user_in: CreateUserSchema,
    db_session: AsyncSession = Depends(get_db_session),
):
    await user_use_cases.create_user(
        db_session=db_session, 
        user_in=user_in
    )

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content="successful operation"
    )


@user_router.get('/{user_id}', response_model=UserOutSchema)
async def get_user_by_id(
    user_id: int,
    db_session: AsyncSession = Depends(get_db_session),
):
    try:
        user = await user_use_cases.get_user_by_id(
            db_session=db_session,
            user_id=user_id
        )
    except UserNotFound:
        raise HTTPException(
            status_code=404, 
            detail="User with this id not found",
        )
    return user


@user_router.put('/{user_id}')
async def update_user_by_id(
    user_id: int,
    user_in: UpdateUserSchema,
    db_session: AsyncSession = Depends(get_db_session),
):
    try:
        user = await user_use_cases.update_user(
            db_session=db_session,
            user_id=user_id,
            user_in=user_in,
        )
    except UserNotFound:
        raise HTTPException(
            status_code=404, 
            detail="User with this id not found",
        ) 

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content="user updated"
    )


@user_router.delete('/{user_id}')
async def delete_user_by_id(
    user_id: int,
    db_session: AsyncSession = Depends(get_db_session),
):
    try:
        await user_use_cases.delete_user(
            db_session=db_session,
            user_id=user_id
        )
    except UserNotFound:
        raise HTTPException(
            status_code=404, 
            detail="User with this id not found",
        )
    
    return JSONResponse(
        status_code=status.HTTP_204_NO_CONTENT,
        content="user deleted"
    )