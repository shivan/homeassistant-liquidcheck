from __future__ import annotations

import asyncio
from typing import Any

from aiohttp import ClientError, ClientSession

START_MEASURE_PAYLOAD: dict[str, Any] = {
    "header": {
        "namespace": "Device.Control",
        "name": "StartMeasure",
        "messageId": "1",
        "payloadVersion": "1",
    },
    "payload": None,
}

class LiquidCheckApiError(Exception):
    """Liquid-Check communication error."""

class LiquidCheckApi:
    def __init__(self, session: ClientSession, host: str) -> None:
        host = host.strip().removeprefix("http://").removeprefix("https://").rstrip("/")
        self.host = host
        self._session = session

    @property
    def base_url(self) -> str:
        return f"http://{self.host}"

    async def async_get_infos(self) -> dict[str, Any]:
        try:
            async with asyncio.timeout(10):
                response = await self._session.get(f"{self.base_url}/infos.json")
                response.raise_for_status()
                data = await response.json(content_type=None)
        except (TimeoutError, ClientError, ValueError) as err:
            raise LiquidCheckApiError(str(err)) from err

        if not isinstance(data, dict):
            raise LiquidCheckApiError("Liquid-Check Antwort ist kein JSON-Objekt")

        payload = data.get("payload", data)
        if not isinstance(payload, dict):
            raise LiquidCheckApiError("Liquid-Check Antwort enthält kein gültiges payload")
        return payload

    async def async_start_measure(self) -> None:
        try:
            async with asyncio.timeout(10):
                response = await self._session.post(
                    f"{self.base_url}/command",
                    json=START_MEASURE_PAYLOAD,
                    headers={"Content-Type": "application/json; charset=utf-8"},
                )
                response.raise_for_status()
        except (TimeoutError, ClientError) as err:
            raise LiquidCheckApiError(str(err)) from err
