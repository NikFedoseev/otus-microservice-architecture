import time
from typing import Any, Callable, Sequence, Tuple
from fastapi import FastAPI
from prometheus_client import REGISTRY, CollectorRegistry
from starlette.requests import Request
from starlette.types import Message, Receive, Scope, Send
from app.prometheus.use_cases import get_route_name
from app.prometheus.metrics import Info

class PrometheusMiddleware:
    def __init__(
        self, 
        app: FastAPI,
        *,
        registry: CollectorRegistry = REGISTRY,
        round_latency_decimals: int = 4,
        instrumentations: Sequence[Callable[[Info], None]] = (),
        excluded_handlers: Sequence[str] = ()
    ) -> None:
        print(instrumentations)
        self.app = app
        self.registry = registry
        self.round_latency_decimals = round_latency_decimals
        self.instrumentations = instrumentations
        

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> Any:
        if scope['type'] != 'http':
            return await self.app(scope, receive, send)
        start_time = time.time()
        request = Request(scope)

        handler, is_templated = self._get_handler(request)

        status_code = 500
        headers = []

        print(handler, is_templated)
        
        async def send_wrapper(message: Message):
            if message['type'] == 'http.response.start':
                nonlocal status_code, headers
                status_code = message['status']
                headers = message['headers']
            await send(message)

        try:
            await self.app(scope, receive, send_wrapper)
        except Exception as exc:
            raise exc
        finally:
            if not is_templated:
                return
            
            duration = max(time.time() - start_time, 0)
            duration = round(duration, self.round_latency_decimals)
            info = Info(
                request=request,
                response=None,
                method=request.method,
                handler=handler,
                status=str(status_code),
                duration=duration
            )
            for instrumentation in self.instrumentations:
                instrumentation(info)
    
    def _get_handler(self, request: Request) -> Tuple[str, bool]:
        route_name = get_route_name(request)
        return route_name or request.url.path, True if route_name else False
    