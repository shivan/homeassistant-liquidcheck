from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers import selector

from .api import LiquidCheckApi, LiquidCheckApiError
from .const import CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL, DOMAIN

class LiquidCheckConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    @staticmethod
    def _sanitize_host(raw_host: str) -> str:
        return raw_host.strip().removeprefix("http://").removeprefix("https://").rstrip("/")

    @classmethod
    async def _async_validate_host(cls, hass, raw_host: str) -> tuple[str, dict[str, Any]]:
        host = cls._sanitize_host(raw_host)

        candidates = [host]
        if "." not in host and ":" not in host and not host.endswith(".local"):
            candidates.append(f"{host}.local")

        last_error: LiquidCheckApiError | None = None
        for candidate in candidates:
            api = LiquidCheckApi(async_get_clientsession(hass), candidate)
            try:
                data = await api.async_get_infos()
                return candidate, data
            except LiquidCheckApiError as err:
                last_error = err

        raise last_error or LiquidCheckApiError("cannot_connect")

    @staticmethod
    def _device_unique_id(device: dict[str, Any], host: str) -> str:
        value = device.get("uuid")
        if isinstance(value, str) and value.strip():
            return value.strip()
        return host

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> "LiquidCheckOptionsFlow":
        return LiquidCheckOptionsFlow(config_entry)

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                host, data = await self._async_validate_host(self.hass, user_input[CONF_HOST])
            except LiquidCheckApiError:
                errors["base"] = "cannot_connect"
            else:
                device = data.get("device", {}) if isinstance(data, dict) else {}
                unique = self._device_unique_id(device, host)
                await self.async_set_unique_id(unique)
                # Don't update host automatically on duplicate add attempts.
                # Host/IP changes are handled explicitly via Options Flow.
                self._abort_if_unique_id_configured()
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
                vol.Optional(
                    CONF_SCAN_INTERVAL,
                    default=DEFAULT_SCAN_INTERVAL,
                ): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=10,
                        max=3600,
                        step=1,
                        mode=selector.NumberSelectorMode.BOX,
                        unit_of_measurement="s",
                    )
                ),
            }
        )
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)


class LiquidCheckOptionsFlow(config_entries.OptionsFlowWithConfigEntry):

    async def async_step_init(self, user_input: dict[str, Any] | None = None):
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                host, _ = await LiquidCheckConfigFlow._async_validate_host(
                    self.hass,
                    user_input[CONF_HOST],
                )
            except LiquidCheckApiError:
                errors["base"] = "cannot_connect"
            else:
                return self.async_create_entry(
                    title="",
                    data={
                        CONF_HOST: host,
                        CONF_SCAN_INTERVAL: int(
                            user_input.get(
                                CONF_SCAN_INTERVAL,
                                DEFAULT_SCAN_INTERVAL,
                            )
                        ),
                    },
                )

        current_host = self.config_entry.options.get(
            CONF_HOST,
            self.config_entry.data.get(CONF_HOST, "liquid-check.local"),
        )

        current_scan_interval = self.config_entry.options.get(
            CONF_SCAN_INTERVAL,
            self.config_entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
        )

        schema = vol.Schema(
            {
                vol.Required(
                    CONF_HOST,
                    default=current_host,
                ): str,
                vol.Required(
                    CONF_SCAN_INTERVAL,
                    default=current_scan_interval,
                ): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=10,
                        max=3600,
                        step=1,
                        mode=selector.NumberSelectorMode.BOX,
                        unit_of_measurement="s",
                    )
                ),
            }
        )

        return self.async_show_form(step_id="init", data_schema=schema, errors=errors)
