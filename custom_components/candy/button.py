from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, DATA_KEY_COORDINATOR, DATA_KEY_CLIENT, UNIQUE_ID_START_BUTTON, DEVICE_NAME_DISHWASHER, DISHWASHER_PROGRAMS
from .client.model import DishwasherStatus

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities):
    """Set up the Candy start button."""
    config_id = config_entry.entry_id
    coordinator = hass.data[DOMAIN][config_id][DATA_KEY_COORDINATOR]

    if isinstance(coordinator.data, DishwasherStatus):
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
            name=DEVICE_NAME_DISHWASHER,
            manufacturer="Candy",
        )

    async def async_press(self) -> None:
        """Press the button."""
        program_select = self.hass.data[DOMAIN][self.config_id].get("program_select")
        if program_select:
            selected_program_name = program_select.current_option
            # Find program ID from name
            program_id = next((k for k, v in DISHWASHER_PROGRAMS.items() if v == selected_program_name), None)
            if program_id:
                client = self.hass.data[DOMAIN][self.config_id].get(DATA_KEY_CLIENT)
                if client:
                    await client.write(f"StSt=1&PrNm={program_id}")
