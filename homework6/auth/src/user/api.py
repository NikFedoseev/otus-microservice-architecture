from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis, RedisError
from uuid import uuid4


from src.database.core import get_db_session
from src.database.redis import get_redis_pool
from src.clients.profile.client import ProfileClient
from src.user import use_cases as user_use_cases
from src.user.schemas import RegisterUserSchema, LoginUserSchema, UserOutSchema
from src.user.exceptions import UserAlreadyRegistered, InvalidCredentials
from src.user.dependencies import get_session_id

router = APIRouter()

@router.post('/register', response_model=UserOutSchema)
async def register(
    user_in: RegisterUserSchema,
    db_session: AsyncSession = Depends(get_db_session),
    profile_client: ProfileClient = Depends(ProfileClient)
):
    try:
        user = await user_use_cases.register_user(
            user_in=user_in,
            db_session=db_session,
            profile_client=profile_client
        )
    except UserAlreadyRegistered:
        raise HTTPException(
            status_code=400, 
            detail="User already registered",
        )

    return user



@router.post('/login', response_model=UserOutSchema)
async def login(
    response: Response,
    user_in: LoginUserSchema,
    db_session: AsyncSession = Depends(get_db_session),
    redis_pool: Redis = Depends(get_redis_pool),
    session_id: str | None = Depends(get_session_id), 
):
    try:
        user = await user_use_cases.login_user(db_session=db_session, user_in=user_in)
    except InvalidCredentials:
        raise HTTPException(
            status_code=403, 
            detail="Invalid credentials",
        )
    
    session_id = session_id or str(uuid4())
    session_token = user_use_cases.create_session_token(user)

    try:
        await redis_pool.hset('session_id', session_id, session_token) # type: ignore
    except RedisError:
        raise HTTPException(
            status_code=500,
            detail='Something went wrong'
        )
    
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True
    )

    return user


@router.get('/logout')
async def logout(
    response: Response,
    redis_pool: Redis = Depends(get_redis_pool),
    session_id = Depends(get_session_id), 
):
    if not session_id:
        raise HTTPException(
            status_code=400,
            detail='Could not logout, session_cookie required'
        )

    try:
        await redis_pool.hdel("session_id", session_id) # type: ignore
    except RedisError:
        raise HTTPException(
            status_code=500,
            detail='Something went wrong'
        )
    
    response.delete_cookie(
        key="session_id",
    )