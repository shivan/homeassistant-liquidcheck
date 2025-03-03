"""Provides the Liquid-Check DataUpdateCoordinator."""
from datetime import timedelta
import logging
import requests
import json

from async_timeout import timeout
from homeassistant.util.dt import utcnow
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class LiquidCheckDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Liquid-Check data."""

    def __init__(self, hass: HomeAssistant, *, config: dict, options: dict):
        """Initialize global liquitd-check data updater."""
        self._host = config[CONF_HOST]
        self._next_update = 0
        update_interval = timedelta(seconds=30)

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=update_interval,
        )

    async def _async_update_data(self) -> dict:
        """Fetch data from LiquidCheck."""

        def _update_data() -> dict:
            """Fetch data from Liquid-Check via sync functions."""
            data = self.data_update()

            return {
                "data": data["payload"]
            }

        try:
            async with timeout(4):
                return await self.hass.async_add_executor_job(_update_data)
        except Exception as error:
            raise UpdateFailed(f"Invalid response from API: {error}") from error

    def data_update(self):
        """Update liquid check data."""
        try:
            response = requests.get(f"http://{self._host}/infos.json")
            data = json.loads(response.text)
            _LOGGER.debug(data)
            return data
        except:
            pass