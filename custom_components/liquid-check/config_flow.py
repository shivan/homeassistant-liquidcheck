from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import LiquidCheckApi, LiquidCheckApiError
from .const import CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL, DOMAIN

class LiquidCheckConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        errors: dict[str, str] = {}
        if user_input is not None:
            host = user_input[CONF_HOST].strip().removeprefix("http://").removeprefix("https://").rstrip("/")
            api = LiquidCheckApi(async_get_clientsession(self.hass), host)
            try:
                data = await api.async_get_infos()
            except LiquidCheckApiError:
                errors["base"] = "cannot_connect"
            else:
                device = data.get("device", {}) if isinstance(data, dict) else {}
                unique = str(device.get("uuid") or device.get("serial") or host)
                await self.async_set_unique_id(unique)
                self._abort_if_unique_id_configured(updates={CONF_HOST: host})
                return self.async_create_entry(
                    title=device.get("name") or f"Liquid-Check {host}",
                    data={
                        CONF_HOST: host,
                        CONF_SCAN_INTERVAL: user_input.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
                    },
                )

        schema = vol.Schema(
            {
                vol.Required(CONF_HOST, default="liquid-check.local"): str,
                vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): vol.All(vol.Coerce(int), vol.Range(min=10, max=3600)),
            }
        )
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)
