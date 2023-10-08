"""The liquid-check integration."""

import logging
from homeassistant.const import CONF_MONITORED_CONDITIONS
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import SENSOR_TYPES, DOMAIN, DATA_COORDINATOR
from .coordinator import LiquidCheckDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """Add an Liquid-Check entry."""
    coordinator: LiquidCheckDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id][
        DATA_COORDINATOR
    ]

    entities = []

    for sensor in entry.data[CONF_MONITORED_CONDITIONS]:
        entities.append(LiquidCheckDevice(coordinator, sensor, entry.title))
    async_add_entities(entities)


class LiquidCheckDevice(CoordinatorEntity):
    """Representation of a Liquid-Check device."""

    def __init__(self, coordinator, sensor_type, name):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor = SENSOR_TYPES[sensor_type][0]
        self._name = name
        self.type = sensor_type
        self._data_source = SENSOR_TYPES[sensor_type][3]
        # json path for data
        self._data_path = SENSOR_TYPES[sensor_type][4]
        self.coordinator = coordinator
        self._last_value = None
        self._unit_of_measurement = SENSOR_TYPES[self.type][1]
        self._icon = SENSOR_TYPES[self.type][2]
        self.serial_number = self.coordinator.data[self._data_source]["device"]["uuid"]
        self.model = self.coordinator.data[self._data_source]["device"]["name"]
        _LOGGER.debug(self.coordinator)

    def getDataByPath(self, dataObject, jsonPath):
        keys = jsonPath.split('/')
        value = dataObject
        for key in keys:
            value = value.get(key)
            if value is None:
                return None  # Schlüssel nicht gefunden, gib None zurück
        return value

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self._name} {self._sensor}"

    @property
    def state(self):
        """Return the state of the device."""
        try:
            state = self.getDataByPath(self.coordinator.data[self._data_source], self._data_path)
            
            self._last_value = state
        except Exception as ex:
            _LOGGER.error(ex)
            state = self._last_value

        return state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement this sensor expresses itself in."""
        return self._unit_of_measurement

    @property
    def icon(self):
        """Return icon."""
        return self._icon

    @property
    def unique_id(self):
        """Return unique id based on device serial and variable."""
        return "{} {}".format(self.serial_number, self._sensor)

    @property
    def device_info(self):
        """Return information about the device."""
        return {
            "identifiers": {(DOMAIN, self.serial_number)},
            "name": self._name,
            "manufacturer": "SI-Elektronik GmbH",
            "model": self.model,
        }