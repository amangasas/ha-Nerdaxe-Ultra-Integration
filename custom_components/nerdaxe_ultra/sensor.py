from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, ATTR_TEMP, ATTR_POWER, ATTR_CURRENT, ATTR_CURRENT_A, ATTR_HASH_RATE, ATTR_HASH_RATE_1M, ATTR_HASH_RATE_10M, ATTR_HASH_RATE_1H, ATTR_HASH_RATE_1D, ATTR_CORE_VOLTAGE, ATTR_FAN_SPEED, ATTR_SHARES_ACCEPTED, ATTR_SHARES_REJECTED


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities([
        NerdaxeSensor(coordinator, "Temperature", ATTR_TEMP, "°C"),
        NerdaxeSensor(coordinator, "Power", ATTR_POWER, "W"),
        NerdaxeSensor(coordinator, "Hashrate", ATTR_HASH_RATE, "GH/s"),
        NerdaxeSensor(coordinator, "Hashrate 1m", ATTR_HASH_RATE_1M, "GH/s"),
        NerdaxeSensor(coordinator, "Hashrate 10m", ATTR_HASH_RATE_10M, "GH/s"),
        NerdaxeSensor(coordinator, "Hashrate 1h", ATTR_HASH_RATE_1H, "GH/s"),
        NerdaxeSensor(coordinator, "Hashrate 1d", ATTR_HASH_RATE_1D, "GH/s"),
        NerdaxeSensor(coordinator, "Fan Speed", ATTR_FAN_SPEED, "%"),
        NerdaxeSensor(coordinator, "Current", ATTR_CURRENT_A, "A"),
        NerdaxeSensor(coordinator, "Core Voltage", ATTR_CORE_VOLTAGE, "mV"),
        NerdaxeSensor(coordinator, "Shares Accepted", ATTR_SHARES_ACCEPTED, "shares"),
        NerdaxeSensor(coordinator, "Shares Rejected", ATTR_SHARES_REJECTED, "shares"),
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
