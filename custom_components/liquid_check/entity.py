from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import LiquidCheckCoordinator


class LiquidCheckEntity(CoordinatorEntity[LiquidCheckCoordinator]):
    _attr_has_entity_name = True

    def __init__(self, coordinator: LiquidCheckCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._entry = entry

    def _get_legacy_serial(self) -> str:
        data = self.coordinator.data or {}
        device = data.get("device", {}) if isinstance(data, dict) else {}
        host = self._entry.data[CONF_HOST]
        # Old integration used uuid + host as both the device identifier basis
        # and the entity unique_id prefix. Preserve that exact shape.
        return f"{device.get('uuid') or device.get('serial') or host}{host}"

    @property
    def device_info(self) -> DeviceInfo:
        data = self.coordinator.data or {}
        device = data.get("device", {}) if isinstance(data, dict) else {}
        host = self._entry.options.get(CONF_HOST, self._entry.data[CONF_HOST])

        return DeviceInfo(
            identifiers={(DOMAIN, self._get_legacy_serial())},
            name=device.get("name") or self._entry.title,
            manufacturer="SI-Elektronik GmbH",
            model="Liquid-Check",
            sw_version=device.get("firmware"),
            configuration_url=f"http://{host}",
        )
