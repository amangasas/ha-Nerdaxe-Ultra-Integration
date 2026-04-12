import aiohttp

from homeassistant.components.button import ButtonEntity


async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([
        NerdaxeRestartButton(entry)
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