"""Select entity for Candy dishwasher options."""
from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import DOMAIN, OPTION_MAPPING, SELECT_OPTION_ID

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Candy select option from a config entry."""
    async_add_entities([CandyOptionSelect(hass)])

class CandyOptionSelect(SelectEntity):
    """Representation of a Candy dishwasher option selector."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the selector."""
        self.hass = hass
        self._attr_name = "Candy Dishwasher Option"
        self._attr_unique_id = SELECT_OPTION_ID
        self._attr_options = list(OPTION_MAPPING.keys())
        self._attr_current_option = self._attr_options[0]

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        self._attr_current_option = option
        self.async_write_ha_state()
