from homeassistant import config_entries

DOMAIN = "nerdaxe_ultra"

class NerdaxeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        return self.async_create_entry(title="Test", data={})