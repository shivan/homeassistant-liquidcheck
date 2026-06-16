from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, SENSORS, LiquidCheckSensorDef
from .coordinator import LiquidCheckCoordinator
from .entity import LiquidCheckEntity

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

class LiquidCheckSensor(LiquidCheckEntity, SensorEntity):

    def __init__(
        self,
        coordinator: LiquidCheckCoordinator,
        entry: ConfigEntry,
        sensor_def: LiquidCheckSensorDef,
    ) -> None:
        super().__init__(coordinator, entry)
        self._sensor_def = sensor_def

        # No custom EntityDescription object. This avoids the HA 2026
        # entity_description compatibility problem from the old integration.
        self._attr_translation_key = sensor_def.key
        self._attr_unique_id = f"{self._get_legacy_serial()}_{sensor_def.key}"
        self._attr_suggested_object_id = sensor_def.key
        self._attr_native_unit_of_measurement = sensor_def.native_unit_of_measurement
        self._attr_device_class = sensor_def.device_class
        self._attr_state_class = sensor_def.state_class
        self._attr_entity_category = sensor_def.entity_category
        self._attr_suggested_display_precision = sensor_def.suggested_display_precision
        self._attr_icon = sensor_def.icon

    @property
    def native_value(self) -> Any:
        value = _get_path(self.coordinator.data or {}, self._sensor_def.path)
        if self._sensor_def.key == "system_uptime" and isinstance(value, (int, float)):
            return round(float(value) / 86400.0, 1)
        if self._sensor_def.key == "pump_total_runtime" and isinstance(value, (int, float)):
            return round(float(value) / 3600.0, 1)
        if self._sensor_def.key in {
            "content_liters",
            "age",
            "pump_total_runs",
        } and isinstance(value, (int, float)):
            return int(round(value))
        return value

