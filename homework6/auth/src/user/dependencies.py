from fastapi import Cookie, Depends

def get_session_id(
    session_id: str | None = Cookie(None),
):
    return session_id