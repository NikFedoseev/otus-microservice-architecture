from typing import Optional, List
from fastapi.routing import APIRoute
from starlette.requests import Request
from starlette.routing import Match, Mount, Route

def get_route_name(request: Request) -> Optional[str]:
    scope = request.scope
    routes: List[Route] = request.app.routes

    for route in routes:
        if not isinstance(route, APIRoute):
            continue
        match, _ = route.matches(scope)
        if match == Match.FULL:
            return route.path
    
    return None