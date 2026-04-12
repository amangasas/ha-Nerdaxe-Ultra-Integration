import aiohttp

from homeassistant.components.switch import SwitchEntity


async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([
        NerdaxeOCModeSwitch(entry, hass),
    ])


class NerdaxeOCModeSwitch(SwitchEntity):
    def __init__(self, entry, hass):
        self.entry = entry
        self.hass = hass

    @property
    def name(self):
        return "NerdAxe OC Mode"

    @property
    def is_on(self):
        return self.hass.data.get("nerdaxe_ultra_oc_mode", False)

    async def async_turn_on(self):
        self.hass.data["nerdaxe_ultra_oc_mode"] = True
        async with aiohttp.ClientSession() as session:
            await session.patch(
                f"http://{self.entry.data['host']}/api/system",
                json={"isOCMode": True}
            )

    async def async_turn_off(self):
        self.hass.data["nerdaxe_ultra_oc_mode"] = False
        async with aiohttp.ClientSession() as session:
            await session.patch(
                f"http://{self.entry.data['host']}/api/system",
                json={"isOCMode": False}
            )