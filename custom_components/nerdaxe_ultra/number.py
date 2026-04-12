from homeassistant.components.number import NumberEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities([
        NerdaxeNumber(coordinator, hass, entry, "Fan Speed", "manualFanSpeed", 0, 100, 1),
        NerdaxeNumber(coordinator, hass, entry, "Frequency", "frequency", 100, 800, 5),
        NerdaxeNumber(coordinator, hass, entry, "Voltage", "coreVoltage", 800, 1500, 10),
    ])


class NerdaxeNumber(CoordinatorEntity, NumberEntity):
    def __init__(self, coordinator, hass, entry, name, key, min_v, max_v, step):
        super().__init__(coordinator)
        self.hass = hass
        self.entry = entry

        self._attr_name = f"NerdAxe {name}"
        self._key = key
        self._min = min_v
        self._max = max_v
        self._step = step

    @property
    def value(self):
        return self.coordinator.data.get(self._key)

    @property
    def min_value(self):
        return self._min

    @property
    def max_value(self):
        return self._max

    @property
    def step(self):
        return self._step

    async def async_set_value(self, value):
        session = async_get_clientsession(self.hass)

        await session.patch(
            f"http://{self.entry.data['host']}/api/system",
            json={self._key: int(value)}
        )

        await self.coordinator.async_request_refresh()