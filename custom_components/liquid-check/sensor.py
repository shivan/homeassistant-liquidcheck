from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, SENSORS, LiquidCheckSensorDef

# Entity unique_ids and device identifiers must stay compatible with the
# original shivan/homeassistant-liquidcheck integration. Otherwise Home
# Assistant treats the same physical Liquid-Check as a new device after the
# native rewrite and creates duplicate devices/entities.
LEGACY_SENSOR_NAMES: dict[str, str] = {
    "firmware": "Firmware Version",
    "measure_percent": "Füllstand",
    "content_liters": "Inhalt",
    "level": "Pegelstand",
    "age": "Alter",
    "error": "Fehler",
}
from .coordinator import LiquidCheckCoordinator

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: LiquidCheckCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [LiquidCheckSensor(coordinator, entry, sensor_def) for sensor_def in SENSORS]
    )

def _get_path(data: dict[str, Any], path: tuple[str, ...]) -> Any:
    value: Any = data
    for part in path:
        if not isinstance(value, dict):
            return None
        value = value.get(part)
    return value

class LiquidCheckSensor(CoordinatorEntity[LiquidCheckCoordinator], SensorEntity):
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: LiquidCheckCoordinator,
        entry: ConfigEntry,
        sensor_def: LiquidCheckSensorDef,
    ) -> None:
        super().__init__(coordinator)
        self._entry = entry
        self._sensor_def = sensor_def
        host = entry.data[CONF_HOST]

        # No custom EntityDescription object. This avoids the HA 2026
        # entity_description compatibility problem from the old integration.
        self._attr_name = sensor_def.name
        self._legacy_serial = self._get_legacy_serial(host)
        legacy_sensor_name = LEGACY_SENSOR_NAMES.get(sensor_def.key, sensor_def.name)
        self._attr_unique_id = f"{self._legacy_serial} {legacy_sensor_name}"
        self._attr_native_unit_of_measurement = sensor_def.native_unit_of_measurement
        self._attr_device_class = sensor_def.device_class
        self._attr_state_class = sensor_def.state_class
        self._attr_icon = sensor_def.icon

    def _get_legacy_serial(self, host: str) -> str:
        data = self.coordinator.data or {}
        device = data.get("device", {}) if isinstance(data, dict) else {}
        # Old integration used uuid + host as both the device identifier basis
        # and the entity unique_id prefix. Preserve that exact shape.
        return f"{device.get('uuid') or device.get('serial') or host}{host}"

    @property
    def native_value(self) -> Any:
        return _get_path(self.coordinator.data or {}, self._sensor_def.path)

    @property
    def device_info(self) -> DeviceInfo:
        data = self.coordinator.data or {}
        device = data.get("device", {}) if isinstance(data, dict) else {}
        host = self._entry.data[CONF_HOST]
        serial = self._get_legacy_serial(host)

        return DeviceInfo(
            identifiers={(DOMAIN, serial)},
            name=device.get("name") or self._entry.title,
            manufacturer="SI-Elektronik GmbH",
            model="Liquid-Check",
            sw_version=device.get("firmware"),
            configuration_url=f"http://{host}",
        )
