from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, DATA_KEY_COORDINATOR, UNIQUE_ID_PROGRAM_SELECT, DISHWASHER_PROGRAMS, DEVICE_NAME_DISHWASHER
from .client.model import DishwasherStatus

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities):
    """Set up the Candy program select."""
    config_id = config_entry.entry_id
    coordinator = hass.data[DOMAIN][config_id][DATA_KEY_COORDINATOR]

    if isinstance(coordinator.data, DishwasherStatus):
        select = CandyProgramSelect(coordinator, config_id)
        async_add_entities([select])
        # Store reference to select entity in hass.data to be accessed by button
        hass.data[DOMAIN][config_id]["program_select"] = select


class CandyProgramSelect(CoordinatorEntity, SelectEntity):
    """Candy program select entity."""

    def __init__(self, coordinator, config_id):
        super().__init__(coordinator)
        self.config_id = config_id
        self._attr_unique_id = UNIQUE_ID_PROGRAM_SELECT.format(config_id)
        self._attr_name = "Program"
        self._attr_options = list(DISHWASHER_PROGRAMS.values())
        self._attr_current_option = self._attr_options[2] # P3 (Eco) as default

    @property
    def current_option(self) -> str | None:
        """Return the current selected option."""
        if self.coordinator.data and hasattr(self.coordinator.data, "program"):
            program_id = self.coordinator.data.program
            if program_id in DISHWASHER_PROGRAMS:
                return DISHWASHER_PROGRAMS[program_id]
        return self._attr_current_option

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self.config_id)},
            name=DEVICE_NAME_DISHWASHER,
            manufacturer="Candy",
        )

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        self._attr_current_option = option
        self.async_write_ha_state()
