from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import LiquidCheckApi, LiquidCheckApiError
from .const import CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL, DOMAIN, PLATFORMS, SERVICE_START_MEASURE
from .coordinator import LiquidCheckCoordinator

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    session = async_get_clientsession(hass)
    api = LiquidCheckApi(session, entry.data[CONF_HOST])
    coordinator = LiquidCheckCoordinator(hass, api, entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL))
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    async def async_start_measure(call: ServiceCall) -> None:
        entry_id = call.data.get("entry_id")
        coordinators = hass.data.get(DOMAIN, {})
        targets = [coordinators[entry_id]] if entry_id else list(coordinators.values())
        for target in targets:
            try:
                await target.api.async_start_measure()
                await target.async_request_refresh()
            except LiquidCheckApiError as err:
                raise HomeAssistantError(str(err)) from err

    if not hass.services.has_service(DOMAIN, SERVICE_START_MEASURE):
        hass.services.async_register(DOMAIN, SERVICE_START_MEASURE, async_start_measure)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data.get(DOMAIN, {}).pop(entry.entry_id, None)
        if not hass.data.get(DOMAIN):
            hass.services.async_remove(DOMAIN, SERVICE_START_MEASURE)
    return unload_ok
