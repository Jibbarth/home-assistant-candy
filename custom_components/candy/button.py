from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, DATA_KEY_COORDINATOR, UNIQUE_ID_START_BUTTON

PROGRAMS = {
    "P1 (Intensif)": "1",
    "P2 (Universel)": "2",
    "P3 (Eco)": "3",
    "P4 (Rapide 24')": "4",
    "P12 (Prélavage)": "12",
    "P19 (Rapide 39')": "19",
}

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities):
    """Set up the Candy start button."""
    config_id = config_entry.entry_id
    coordinator = hass.data[DOMAIN][config_id][DATA_KEY_COORDINATOR]

    async_add_entities([
        CandyStartButton(coordinator, config_id, hass)
    ])

class CandyStartButton(CoordinatorEntity, ButtonEntity):
    """Candy start button entity."""

    def __init__(self, coordinator, config_id, hass):
        super().__init__(coordinator)
        self.config_id = config_id
        self.hass = hass
        self._attr_unique_id = UNIQUE_ID_START_BUTTON.format(config_id)
        self._attr_name = "Start"

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self.config_id)},
            name="Candy",
            manufacturer="Candy",
        )

    async def async_press(self) -> None:
        """Press the button."""
        # Get select entity from hass.data
        select = self.hass.data[DOMAIN][self.config_id].get("program_select")
        if select and select.current_option:
            program_id = PROGRAMS.get(select.current_option)
            if program_id:
                client = self.hass.data[DOMAIN][self.config_id].get("client")
                if client:
                    await client.write(f"StSt=1&PrNm={program_id}")
