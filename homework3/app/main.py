from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app.api import api_router

app = FastAPI()

app.include_router(api_router)

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder({
            'code': exc.status_code,
            'message': exc.detail,
        })
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    messages = [
        pydantic_error["msg"]
        for pydantic_error in exc.errors()
    ]
   
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({
            'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
            'message': '; '.join(messages),
        })
    )