import bcrypt
import sqlalchemy as sa
from typing import Optional
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from authlib.jose import jwt

from src.user.schemas import CreateUserSchema, UserSchema, RegisterUserSchema, LoginUserSchema
from src.user.exceptions import InvalidCredentials, UserNotFound, UserAlreadyRegistered
from src.user.models import UserModel
from src.user.constants import private_key
from src.clients.profile.client import ProfileClient
from src.clients.profile.schemas import CreateProfileSchema, ProfileSchema


async def find_user_by_email(
    email: str,
    db_session: AsyncSession
):
    res = await db_session.scalar(
        sa.select(UserModel).where(UserModel.email == email)
    )

    if not res:
        return None
    
    return UserSchema.model_validate(res)


async def find_user_by_id(
    id: int,
    db_session: AsyncSession
):
    res = await db_session.scalar(
        sa.select(UserModel).where(UserModel.id == id)
    )

    if not res:
        return None
    
    return UserSchema.model_validate(res)


def verify_password(password: str, hashed_password: str):
    if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
        return True
    return False


async def create_user(
    user_in: CreateUserSchema,
    db_session: AsyncSession,
):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(user_in.password.encode('utf-8'), salt)

    user = UserModel(
        **user_in.model_dump(exclude={'password'}),
        password=hashed_password.decode()
    )

    db_session.add(user)
    await db_session.commit()

    return UserSchema.model_validate(user)


async def register_user(
    user_in: RegisterUserSchema,
    db_session: AsyncSession,
    profile_client: ProfileClient
):
    existed_user = await find_user_by_email(
        email=user_in.email,
        db_session=db_session
    )

    if existed_user:
        raise UserAlreadyRegistered

    profile_data = CreateProfileSchema(**user_in.model_dump())

    profile = await profile_client.create_profile(
        payload=profile_data.model_dump(mode='json')
    )
    profile = ProfileSchema(**profile)

    user_data = CreateUserSchema(
        **user_in.model_dump(),
        profile_id=profile.id
    )

    created_user = await create_user(
        user_in=user_data,
        db_session=db_session
    )

    return created_user


async def login_user(
    user_in: LoginUserSchema,
    db_session: AsyncSession,
):
    user = await find_user_by_email(
        db_session=db_session, 
        email=user_in.email
    )

    if not user:
        raise InvalidCredentials

    password_verified = verify_password(
        password=user_in.password, 
        hashed_password=user.password
    )

    if not password_verified:
        raise InvalidCredentials
    
    return UserSchema.model_validate(user)


def create_session_token(user: UserSchema):
    jwt_header = {
        'alg': 'RS256',
        'kid': private_key.thumbprint()
    }

    jwt_data = {
        "profile_id": user.profile_id,
        "user_id": user.id,
        "exp": datetime.utcnow() + timedelta(days=365),
        'iss': 'http://ms-auth-api-service'
    }

    return jwt.encode(jwt_header, jwt_data, private_key).decode('utf-8')