import httpx

class HTTPClient(httpx.AsyncClient):
    def __init__(self, url: str, token: str, *args, **kwargs) -> None:
        self.token = token
        self.event_hooks = {
            'request': [self._accept_json_request, self._x_service_token]
        }
        super().__init__(
            base_url=url,
            *args,
            **kwargs
        )

    def _accept_json_request(self, request: httpx.Request):
        request.headers['Accept'] = 'application/json'
        request.headers['Content-Type'] = 'application/json'

    def _x_service_token(self, request: httpx.Request):
        request.headers['X-Service-Token'] = self.token
        