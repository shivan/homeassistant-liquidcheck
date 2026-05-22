from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import PERCENTAGE, Platform

DOMAIN = "liquid_check"
PLATFORMS = [Platform.SENSOR]

DEFAULT_SCAN_INTERVAL = 30
CONF_SCAN_INTERVAL = "scan_interval"

SERVICE_START_MEASURE = "start_measure"

@dataclass(frozen=True)
class LiquidCheckSensorDef:
    key: str
    name: str
    path: tuple[str, ...]
    native_unit_of_measurement: str | None = None
    device_class: SensorDeviceClass | str | None = None
    state_class: SensorStateClass | str | None = None
    icon: str | None = None

SENSORS: tuple[LiquidCheckSensorDef, ...] = (
    LiquidCheckSensorDef(
        key="measure_percent",
        name="Füllstand",
        path=("measure", "percent"),
        native_unit_of_measurement=PERCENTAGE,
        device_class=None,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:gauge",
    ),
    LiquidCheckSensorDef(
        key="content_liters",
        name="Inhalt",
        path=("measure", "content"),
        native_unit_of_measurement="L",
        device_class=SensorDeviceClass.VOLUME,
        state_class=None,
        icon="mdi:water",
    ),
    LiquidCheckSensorDef(
        key="level",
        name="Pegelstand",
        path=("measure", "level"),
        native_unit_of_measurement="m",
        device_class=SensorDeviceClass.DISTANCE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:waves",
    ),
    LiquidCheckSensorDef(
        key="age",
        name="Messwertalter",
        path=("measure", "age"),
        native_unit_of_measurement="s",
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:timer-outline",
    ),
    LiquidCheckSensorDef(
        key="error",
        name="Fehler",
        path=("system", "error"),
        icon="mdi:alert-circle-outline",
    ),
    LiquidCheckSensorDef(
        key="firmware",
        name="Firmware",
        path=("device", "firmware"),
        icon="mdi:chip",
    ),
)
