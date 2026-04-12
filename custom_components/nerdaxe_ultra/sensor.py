from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities([
        NerdaxeSensor(coordinator, "Temperature", "temp", "°C"),
        NerdaxeSensor(coordinator, "Power", "power", "W"),
        NerdaxeSensor(coordinator, "Hashrate", "hashRate", "GH/s"),
        NerdaxeSensor(coordinator, "Fan", "fanspeed", "%"),
    ])


class NerdaxeSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, name, key, unit):
        super().__init__(coordinator)
        self._attr_name = f"NerdAxe {name}"
        self._key = key
        self._unit = unit

    @property
    def state(self):
        return self.coordinator.data.get(self._key)

    @property
    def unit_of_measurement(self):
        return self._unit