"""Minimal read-only discovery API."""
import os

from fastapi import FastAPI, HTTPException

from .moonraker import MoonrakerClient

from .vision_api import router as vision_router

app = FastAPI(title="PrintTune AI", version="0.1.0")
app.include_router(vision_router)


@app.get("/api/health")
async def health():
    return {"status": "ok", "mode": "read-only"}


@app.get("/api/capabilities")
async def capabilities():
    url = os.getenv("MOONRAKER_URL")
    if not url:
        raise HTTPException(status_code=503, detail="Set MOONRAKER_URL")
    try:
        return await MoonrakerClient(url, os.getenv("MOONRAKER_API_KEY")).discover()
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Moonraker discovery failed: {type(exc).__name__}") from exc
