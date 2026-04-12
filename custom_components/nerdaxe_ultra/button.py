import aiohttp
import voluptuous as vol

from homeassistant.components.button import ButtonEntity
from homeassistant.components.switch import SwitchEntity

from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([
        NerdaxeRestartButton(entry),
        NerdaxeOCModeSwitch(entry, hass),
    ])


class NerdaxeRestartButton(ButtonEntity):
    def __init__(self, entry):
        self.entry = entry

    @property
    def name(self):
        return "NerdAxe Restart"

    async def async_press(self):
        async with aiohttp.ClientSession() as session:
            await session.post(
                f"http://{self.entry.data['host']}/api/system/restart"
            )


class NerdaxeOCModeSwitch(SwitchEntity):
    def __init__(self, entry, hass):
        self.entry = entry
        self.hass = hass

    @property
    def name(self):
        return "NerdAxe OC Mode"

    @property
    def is_on(self):
        return self.hass.data.get(f"{DOMAIN}_{self.entry.entry_id}_oc_mode", False)

    async def async_turn_on(self):
        self.hass.data[f"{DOMAIN}_{self.entry.entry_id}_oc_mode"] = True
        await self._send_oc_mode(True)

    async def async_turn_off(self):
        self.hass.data[f"{DOMAIN}_{self.entry.entry_id}_oc_mode"] = False
        await self._send_oc_mode(False)

    async def _send_oc_mode(self, enabled):
        async with aiohttp.ClientSession() as session:
            await session.patch(
                f"http://{self.entry.data['host']}/api/system",
                json={"isOCMode": enabled}
            )
