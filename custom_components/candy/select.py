from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo

from .const import (
    DOMAIN,
    DATA_KEY_COORDINATOR,
    DATA_KEY_DEVICE_CODE,
    UNIQUE_ID_PROGRAM_SELECT,
    UNIQUE_ID_DELAY_SELECT,
    UNIQUE_ID_OPTION_SELECT,
    DISHWASHER_PROGRAMS,
    DEVICE_NAME_DISHWASHER,
    DELAY_MAPPING,
    OPTION_MAPPING,
)
from .client.model import DishwasherStatus

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities):
    """Set up the Candy selects."""
    config_id = config_entry.entry_id
    coordinator = hass.data[DOMAIN][config_id][DATA_KEY_COORDINATOR]
    device_code = hass.data[DOMAIN][config_id][DATA_KEY_DEVICE_CODE]

    if isinstance(coordinator.data, DishwasherStatus):
        program_select = CandyProgramSelect(config_id, device_code)
        delay_select = CandyDelaySelect(config_id, device_code)
        option_select = CandyOptionSelect(config_id, device_code)
        async_add_entities([program_select, delay_select, option_select])


class CandyProgramSelect(SelectEntity):
    """Candy program select entity."""

    def __init__(self, config_id, device_code):
        self.config_id = config_id
        self.device_code = device_code
        self._attr_unique_id = UNIQUE_ID_PROGRAM_SELECT.format(config_id)
        self._attr_translation_key = "program"
        self._attr_has_entity_name = True
        self._attr_options = list(DISHWASHER_PROGRAMS.keys())
        self._attr_current_option = "eco"  # Eco as default

    @property
    def current_option(self) -> str | None:
        """Return the current selected option."""
        return self._attr_current_option

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self.config_id)},
            name=DEVICE_NAME_DISHWASHER,
            manufacturer="Candy",
            serial_number=self.device_code,
        )

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        self._attr_current_option = option
        self.async_write_ha_state()


class CandyDelaySelect(SelectEntity):
    """Candy delay select entity."""

    def __init__(self, config_id, device_code):
        self.config_id = config_id
        self.device_code = device_code
        self._attr_unique_id = UNIQUE_ID_DELAY_SELECT.format(config_id)
        self._attr_translation_key = "delay_start"
        self._attr_has_entity_name = True
        self._attr_options = list(DELAY_MAPPING.keys())
        self._attr_current_option = "0 min"

    @property
    def current_option(self) -> str | None:
        """Return the current selected option."""
        return self._attr_current_option

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self.config_id)},
            name=DEVICE_NAME_DISHWASHER,
            manufacturer="Candy",
            serial_number=self.device_code,
        )

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        self._attr_current_option = option
        self.async_write_ha_state()


class CandyOptionSelect(SelectEntity):
    """Candy option select entity."""

    def __init__(self, config_id, device_code):
        self.config_id = config_id
        self.device_code = device_code
        self._attr_unique_id = UNIQUE_ID_OPTION_SELECT.format(config_id)
        self._attr_translation_key = "candy_dishwasher_option"
        self._attr_has_entity_name = True
        self._attr_options = list(OPTION_MAPPING.keys())
        self._attr_current_option = "standard"  # Default

    @property
    def current_option(self) -> str | None:
        """Return the current selected option."""
        return self._attr_current_option

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self.config_id)},
            name=DEVICE_NAME_DISHWASHER,
            manufacturer="Candy",
            serial_number=self.device_code,
        )

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        self._attr_current_option = option
        self.async_write_ha_state()
