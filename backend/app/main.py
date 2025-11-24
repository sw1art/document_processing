from fastapi import FastAPI

from backend.app.api.v1.routers import auth

app = FastAPI(title="Document Processing Service")

app.include_router(auth.router, prefix="/auth", tags=["auth"])
# app.include_router(files.router, prefix="/files", tags=["files"])


@app.get("/health", tags=["health"])
async def health():
    return {"status": "ok"}
