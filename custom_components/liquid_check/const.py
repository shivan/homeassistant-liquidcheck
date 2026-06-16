from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import PERCENTAGE, Platform
from homeassistant.helpers.entity import EntityCategory

DOMAIN = "liquid_check"
PLATFORMS = [Platform.SENSOR, Platform.BUTTON]

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
    entity_category: EntityCategory | None = None
    suggested_display_precision: int | None = None
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
        state_class=SensorStateClass.TOTAL,
        suggested_display_precision=0,
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
        name="Letzte Messung",
        path=("measure", "age"),
        native_unit_of_measurement="s",
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=0,
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
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:chip",
    ),
    LiquidCheckSensorDef(
        key="hardware",
        name="Hardware",
        path=("device", "hardware"),
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:memory",
    ),
    LiquidCheckSensorDef(
        key="tank_max_level",
        name="Tankhöhe",
        path=("measure", "tank", "maxLevel"),
        native_unit_of_measurement="m",
        device_class=SensorDeviceClass.DISTANCE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:arrow-expand-vertical",
    ),
    LiquidCheckSensorDef(
        key="system_uptime",
        name="Uptime",
        path=("system", "uptime"),
        native_unit_of_measurement="s",
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        suggested_display_precision=0,
        icon="mdi:timer-sand",
    ),
    LiquidCheckSensorDef(
        key="pump_total_runs",
        name="Pumpenstarts",
        path=("system", "pump", "totalRuns"),
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC,
        suggested_display_precision=0,
        icon="mdi:counter",
    ),
    LiquidCheckSensorDef(
        key="pump_total_runtime",
        name="Pumpenlaufzeit gesamt",
        path=("system", "pump", "totalRuntime"),
        native_unit_of_measurement="s",
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC,
        suggested_display_precision=0,
        icon="mdi:pump",
    ),
    LiquidCheckSensorDef(
        key="wifi_rssi",
        name="WLAN Signal",
        path=("wifi", "accessPoint", "rssi"),
        native_unit_of_measurement="dBm",
        device_class=SensorDeviceClass.SIGNAL_STRENGTH,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:wifi",
    ),
    LiquidCheckSensorDef(
        key="wifi_ssid",
        name="WLAN SSID",
        path=("wifi", "accessPoint", "ssid"),
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:wifi-settings",
    ),
)
