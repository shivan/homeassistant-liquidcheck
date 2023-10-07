"""Constants for the liquid-check integration."""
from datetime import timedelta

from homeassistant.const import (
    UnitOfVolume,
    UnitOfLength,
    PERCENTAGE,
)

DOMAIN = "liquid-check"

DATA_COORDINATOR = "corrdinator"

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=10)

SENSOR_TYPES = {
    "device": ["Device", None, "", "data", "device/name"],
    "firmware": ["Firmware Version", None, "", "data", "device/firmware"],
    "measure_percent": ["Füllstand", PERCENTAGE, "", "data", "measure/percent"],
    "level": ["Pegelstand", UnitOfLength.METERS, "", "data", "measure/level"],
    "content_liters": ["Inhalt", UnitOfVolume.LITERS, "", "data", "measure/content"],
    "age": ["Alter", None, "", "data", "measure/age"],
    "error": ["Fehler", None, "", "data", "system/error"],
}
