from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from prometheus_client import make_asgi_app

from app.api import api_router
from app.prometheus.middleware import PrometheusMiddleware
from app.prometheus.metrics import latency, rps

app = FastAPI()

metrics_app = make_asgi_app()
app.mount('/metrics', metrics_app)

app.include_router(api_router)
app.add_middleware(
    PrometheusMiddleware, 
    instrumentations=(
        latency(
            buckets=(0.5, 0.95, 0.99),
        ),
        rps()
    )
)

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