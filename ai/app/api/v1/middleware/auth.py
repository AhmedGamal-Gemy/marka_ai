import os
from fastapi import Request, HTTPException
from jose import jwt, JWTError

JWT_SECRET = os.environ["JWT_SECRET"]
SERVICE_KEY = os.environ["AI_SERVICE_KEY"]


async def verify_request(request: Request) -> dict:
    """Validate service key and JWT on every request.

    Args:
        request: Incoming FastAPI request.

    Returns:
        JWT payload dict containing sub (user_id), email, plan.

    Raises:
        HTTPException: 403 if service key is missing or wrong.
        HTTPException: 401 if JWT is missing, expired, or invalid.
    """
    # Step 1 — service key proves caller is Express, not a rogue client
    if request.headers.get("X-Service-Key") != SERVICE_KEY:
        raise HTTPException(status_code=403, detail="Invalid service key")

    # Step 2 — validate JWT independently (zero trust)
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")

    try:
        payload = jwt.decode(auth.split(" ")[1], JWT_SECRET, algorithms=["HS256"])
        return payload  # { sub: user_id, email, plan }
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")