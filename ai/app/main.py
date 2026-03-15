from fastapi import FastAPI, Depends
from app.api.v1.middleware.auth import verify_request

app = FastAPI(title="Marka AI Backend")


@app.get("/health")
def health():
    """Health check — no auth required."""
    return {"status": "ok", "layer": "fastapi"}


@app.get("/ai/hello")
async def hello(user: dict = Depends(verify_request)):
    """Wired hello world — confirms full auth chain is working.

    Args:
        user: JWT payload injected by verify_request dependency.

    Returns:
        Greeting from the AI layer with confirmed user identity.
    """
    return {
        "success": True,
        "data": {
            "message": f"Hello from FastAPI — user {user['sub']} verified",
            "user_id": user["sub"],
            "email": user["email"],
            "chain": "React → Express (JWT ✓) → FastAPI (service key ✓ + JWT ✓)",
        },
    }