from __future__ import annotations

import asyncio
from datetime import timedelta
from typing import Any
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import LiquidCheckApi, LiquidCheckApiError
from .const import DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)

class LiquidCheckCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    def __init__(
        self,
        hass: HomeAssistant,
        api: LiquidCheckApi,
        scan_interval: int = DEFAULT_SCAN_INTERVAL,
    ) -> None:
        super().__init__(
            hass,
            logger=_LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=max(10, int(scan_interval))),
        )
        self.api = api

    async def _async_update_data(self) -> dict[str, Any]:
        try:
            data = await self.api.async_get_infos()
        except LiquidCheckApiError as err:
            # Some devices occasionally return a transient invalid/empty payload.
            # Retry once shortly after the first failure to reduce noisy logs.
            await asyncio.sleep(1)
            try:
                data = await self.api.async_get_infos()
            except LiquidCheckApiError as retry_err:
                raise UpdateFailed(str(retry_err)) from retry_err

        return data
