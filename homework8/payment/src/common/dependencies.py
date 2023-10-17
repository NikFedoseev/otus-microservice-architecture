from fastapi import HTTPException, Header

def get_idempotency_key(
    x_idempotency_key: str | None = Header(None),
):
    if not x_idempotency_key:
        raise HTTPException(400, 'idempotency key required')
    return x_idempotency_key