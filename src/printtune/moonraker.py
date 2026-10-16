"""Read-only Moonraker API adapter."""
from __future__ import annotations

import httpx


class MoonrakerClient:
    def __init__(self, url: str, api_key: str | None = None):
        self.url = url.rstrip("/")
        self.headers = {"X-Api-Key": api_key} if api_key else {}

    async def _get(self, path: str) -> dict:
        async with httpx.AsyncClient(timeout=12.0, headers=self.headers) as client:
            response = await client.get(f"{self.url}{path}")
            response.raise_for_status()
            payload = response.json()
            if "error" in payload:
                raise RuntimeError(str(payload["error"]))
            return payload.get("result", {})

    async def discover(self) -> dict:
        info = await self._get("/printer/info")
        objects = await self._get("/printer/objects/list")
        config = await self._get("/printer/objects/query?configfile")
        status = config.get("status", {}).get("configfile", {})
        settings = status.get("settings", {})
        return {
            "schema_version": "0.1",
            "firmware": "Klipper",
            "state": info.get("state"),
            "klipper_version": info.get("software_version"),
            "available_objects": objects.get("objects", []),
            "configured": {
                "printer": settings.get("printer", {}),
                "extruder": settings.get("extruder", {}),
                "input_shaper": settings.get("input_shaper", {}),
                "bed_mesh": settings.get("bed_mesh", {}),
            },
            "measurement_status": "unverified",
            "note": "Configured limits are not proven print-quality limits.",
        }
