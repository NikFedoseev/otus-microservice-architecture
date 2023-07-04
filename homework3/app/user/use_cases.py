import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.user.schemas import (
    UserSchema, CreateUserSchema, UpdateUserSchema
)
from app.user.models import UserModel
from app.user.exceptions import UserNotFound


async def find_user_by_id(
    db_session: AsyncSession, 
    id: int
) -> Optional[UserSchema]:
    res = await db_session.scalar(
        sa.select(UserModel).where(UserModel.id == id)
    )

    if not res:
        return None

    return UserSchema.from_orm(res)


async def get_user_by_id(
    db_session: AsyncSession,
    user_id: int
):
    user = await find_user_by_id(
        db_session=db_session,
        id=user_id
    )

    if not user:
        raise UserNotFound

    return user


async def create_user(
    db_session: AsyncSession, 
    user_in: CreateUserSchema
) -> UserSchema:
    user = UserModel(**user_in.dict())

    db_session.add(user)
    await db_session.commit()

    return UserSchema.from_orm(user)


async def update_user(
    db_session: AsyncSession, 
    user_id: int, 
    user_in: UpdateUserSchema
) -> Optional[UserSchema]:
    existed_user = await find_user_by_id(
        db_session=db_session,
        id=user_id
    )

    if not existed_user:
        raise UserNotFound
    
    stmt = (
        sa.update(UserModel)
        .values(user_in.dict(exclude_unset=True))
        .where(UserModel.id == user_id)
        .returning(UserModel)
    )

    updated_user = await db_session.scalar(stmt)
    await db_session.commit()

    return UserSchema.from_orm(updated_user)


async def delete_user(
    db_session: AsyncSession, 
    user_id: int
):
    existed_user = await find_user_by_id(
        db_session=db_session,
        id=user_id
    )

    if not existed_user:
        raise UserNotFound
    
    stmt = sa.delete(UserModel).where(UserModel.id == user_id)

    await db_session.execute(stmt)
    await db_session.commit()
