from __future__ import annotations

import asyncio

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import LiquidCheckCoordinator
from .entity import LiquidCheckEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: LiquidCheckCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([LiquidCheckStartMeasureButton(coordinator, entry)])


class LiquidCheckStartMeasureButton(
    LiquidCheckEntity,
    ButtonEntity,
):
    _refresh_delay_seconds = 10
    _attr_has_entity_name = True
    _attr_entity_registry_enabled_default = True
    _attr_translation_key = "start_measure"
    _attr_icon = "mdi:play-circle-outline"

    def __init__(self, coordinator: LiquidCheckCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{self._get_legacy_serial()}_start_measure"
        self._attr_suggested_object_id = "start_measure"

    async def async_press(self) -> None:
        await self.coordinator.api.async_start_measure()
        await asyncio.sleep(self._refresh_delay_seconds)
        await self.coordinator.async_request_refresh()
