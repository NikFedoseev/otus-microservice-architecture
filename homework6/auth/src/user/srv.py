from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis, RedisError
from authlib.jose import jwt

from src.database.core import get_db_session
from src.database.redis import get_redis_pool
from src.user.dependencies import get_session_id
from src.user.constants import public_key
from src.user import use_cases as user_use_cases

router = APIRouter()


@router.get('/.well-known/jwks.json')
async def jwks():
    return {
        'keys': [
            public_key.as_dict(add_kid=True)
        ]
    }


@router.api_route('/verify_auth', methods=["GET", "PUT", "PATCH", "POST", "DELETE"])
async def verify_auth(
    response: Response,
    session_id: str | None = Depends(get_session_id),
    db_session: AsyncSession = Depends(get_db_session),
    resis_pool: Redis = Depends(get_redis_pool),
):
    if not session_id:
        return HTTPException(status_code=401)
    
    try:
        session_token = await resis_pool.hget('session_id', session_id) # type: ignore
    except RedisError:
        return HTTPException(status_code=401)
    
    if not session_token:
        return HTTPException(status_code=401)
    
    claims = jwt.decode(session_token, public_key)
    
    headers = {
        'x-user-id': f"{claims['user_id']}",
        'x-profile-id': f"{claims['profile_id']}",
        'x-auth-token': session_token
    }
    
    return JSONResponse(content={'status': 'ok'}, headers=headers)