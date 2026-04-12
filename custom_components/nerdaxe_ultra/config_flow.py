import voluptuous as vol
from homeassistant import config_entries

from .const import DOMAIN


class NerdaxeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(
                title=f"NerdAxe {user_input['host']}",
                data={"host": user_input["host"]}
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("host"): str,
            })
        )