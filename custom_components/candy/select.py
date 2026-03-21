from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    DATA_KEY_COORDINATOR,
    UNIQUE_ID_PROGRAM_SELECT,
    UNIQUE_ID_DELAY_SELECT,
    DISHWASHER_PROGRAMS,
    DEVICE_NAME_DISHWASHER,
    DELAY_MAPPING,
)
from .client.model import DishwasherStatus

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities):
    """Set up the Candy selects."""
    config_id = config_entry.entry_id
    coordinator = hass.data[DOMAIN][config_id][DATA_KEY_COORDINATOR]

    if isinstance(coordinator.data, DishwasherStatus):
        program_select = CandyProgramSelect(coordinator, config_id)
        delay_select = CandyDelaySelect(coordinator, config_id)
        async_add_entities([program_select, delay_select])


class CandyProgramSelect(CoordinatorEntity, SelectEntity):
    """Candy program select entity."""

    def __init__(self, coordinator, config_id):
        super().__init__(coordinator)
        self.config_id = config_id
        self._attr_unique_id = UNIQUE_ID_PROGRAM_SELECT.format(config_id)
        self._attr_name = "Candy Dishwasher Program"
        self._attr_options = list(DISHWASHER_PROGRAMS.keys())
        self._attr_current_option = "eco"  # Eco as default

    @property
    def current_option(self) -> str | None:
        """Return the current selected option."""
        if self.coordinator.data and hasattr(self.coordinator.data, "program"):
            program_id = self.coordinator.data.program
            key = next((k for k, v in DISHWASHER_PROGRAMS.items() if v == program_id), None)
            if key:
                return key
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


class CandyDelaySelect(CoordinatorEntity, SelectEntity):
    """Candy delay select entity."""

    def __init__(self, coordinator, config_id):
        super().__init__(coordinator)
        self.config_id = config_id
        self._attr_unique_id = UNIQUE_ID_DELAY_SELECT.format(config_id)
        self._attr_name = "Candy Dishwasher Delay Start"
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
        )

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        self._attr_current_option = option
        self.async_write_ha_state()
