"""Standalone inspection router; no printer write access."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from .vision import ALLOWED_VIEWS, inspect_benchy

router = APIRouter(prefix="/api/vision", tags=["vision"])


@router.post("/inspect")
async def inspect(
    images: list[UploadFile] = File(...),
    views: list[str] = Form(...),
    context_json: str = Form("{}"),
):
    if not 1 <= len(images) <= 5 or len(images) != len(views):
        raise HTTPException(400, "Provide 1–5 images and matching views")
    if len(set(views)) != len(views) or any(v not in ALLOWED_VIEWS for v in views):
        raise HTTPException(400, "Views must be unique and recognized")
    try:
        context = json.loads(context_json)
        if not isinstance(context, dict):
            raise ValueError("Context must be an object")
    except (ValueError, json.JSONDecodeError) as exc:
        raise HTTPException(400, "Invalid context JSON") from exc
    with TemporaryDirectory() as temp:
        paths = {}
        for view, upload in zip(views, images):
            suffix = Path(upload.filename or "").suffix.lower()
            if suffix not in {".png", ".jpg", ".jpeg", ".webp"}:
                raise HTTPException(400, "Unsupported image format")
            data = await upload.read(8 * 1024 * 1024 + 1)
            if len(data) > 8 * 1024 * 1024:
                raise HTTPException(413, "Image exceeds 8 MiB")
            path = Path(temp) / f"{view}{suffix}"
            path.write_bytes(data)
            paths[view] = path
        try:
            return await inspect_benchy(paths, context)
        except (ValueError, RuntimeError) as exc:
            raise HTTPException(422, str(exc)) from exc
        except Exception as exc:
            raise HTTPException(502, "Vision provider failed") from exc
