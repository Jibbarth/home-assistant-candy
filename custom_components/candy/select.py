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
    UNIQUE_ID_OPTION_SELECT,
    DISHWASHER_PROGRAMS,
    DEVICE_NAME_DISHWASHER,
    DELAY_MAPPING,
    OPTION_MAPPING,
)
from .client.model import DishwasherStatus, DishwasherState

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities):
    """Set up the Candy selects."""
    config_id = config_entry.entry_id
    coordinator = hass.data[DOMAIN][config_id][DATA_KEY_COORDINATOR]

    if isinstance(coordinator.data, DishwasherStatus):
        program_select = CandyProgramSelect(coordinator, config_id)
        delay_select = CandyDelaySelect(coordinator, config_id)
        option_select = CandyOptionSelect(coordinator, config_id)
        async_add_entities([program_select, delay_select, option_select])


class CandyProgramSelect(CoordinatorEntity, SelectEntity):
    """Candy program select entity."""

    def __init__(self, coordinator, config_id):
        super().__init__(coordinator)
        self.config_id = config_id
        self._attr_unique_id = UNIQUE_ID_PROGRAM_SELECT.format(config_id)
        self._attr_translation_key = "program"
        self._attr_has_entity_name = True
        self._attr_options = list(DISHWASHER_PROGRAMS.keys())
        self._attr_current_option = "eco"  # Eco as default
        # Initialize from coordinator if available
        self._update_from_coordinator()

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

    def _update_from_coordinator(self):
        if self.coordinator.data and hasattr(self.coordinator.data, "program"):
            program_id = self.coordinator.data.program
            key = next((k for k, v in DISHWASHER_PROGRAMS.items() if v == program_id), None)
            if key:
                self._attr_current_option = key

    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        if not self.coordinator.data:
            return

        machine_state = getattr(self.coordinator.data, "machine_state", None)
        is_running = machine_state != DishwasherState.IDLE

        if is_running or self._attr_current_option is None:
            self._update_from_coordinator()
        
        super()._handle_coordinator_update()

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
        self._update_from_coordinator() # Ensure this is called for initial state

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

    def _update_from_coordinator(self):
        if self.coordinator.data and hasattr(self.coordinator.data, "delayed_start_hours"):
            val = self.coordinator.data.delayed_start_hours
            if val is None: # Handle cases where delayed_start_hours might be None (meaning 0 delay)
                val = 0
            
            val_str = str(val)
            # Find the key in DELAY_MAPPING that corresponds to the value from the device
            key = next((k for k, v in DELAY_MAPPING.items() if v == val_str), None)
            if key:
                self._attr_current_option = key
            else:
                # Fallback if mapping not found, but keep it reasonable
                self._attr_current_option = "0 min" # Default to 0 min if mapping fails

    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        if not self.coordinator.data:
            return

        machine_state = getattr(self.coordinator.data, "machine_state", None)
        is_running = machine_state != DishwasherState.IDLE

        if is_running or self._attr_current_option is None:
            self._update_from_coordinator()
        
        super()._handle_coordinator_update()

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        self._attr_current_option = option
        self.async_write_ha_state()


class CandyOptionSelect(CoordinatorEntity, SelectEntity):
    """Candy option select entity."""

    def __init__(self, coordinator, config_id):
        super().__init__(coordinator)
        self.config_id = config_id
        self._attr_unique_id = UNIQUE_ID_OPTION_SELECT.format(config_id)
        self._attr_translation_key = "candy_dishwasher_option"
        self._attr_has_entity_name = True
        self._attr_options = list(OPTION_MAPPING.keys())
        self._attr_current_option = "standard"  # Default
        self._update_from_coordinator() # Ensure this is called for initial state

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
    
    def _update_from_coordinator(self):
        if self.coordinator.data:
            # Ensure comparison is string-based for OPTION_MAPPING keys
            opz_prog_val = getattr(self.coordinator.data, "opz_prog", 0)
            meta_carico_val = getattr(self.coordinator.data, "meta_carico", 0)

            opz_prog = str(opz_prog_val)
            meta_carico = str(meta_carico_val)

            # Iterate through the mapping to find the matching option name
            found_option = False
            for name, mapping in OPTION_MAPPING.items():
                if mapping.get("OpzProg") == opz_prog and mapping.get("MetaCarico") == meta_carico:
                    self._attr_current_option = name
                    found_option = True
                    break
            
            if not found_option:
                # Fallback to default if no exact match is found
                self._attr_current_option = "standard" 

    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        if not self.coordinator.data:
            return

        machine_state = getattr(self.coordinator.data, "machine_state", None)
        is_running = machine_state != DishwasherState.IDLE

        # Update only if machine is running or if the state hasn't been set yet
        if is_running or self._attr_current_option is None:
            self._update_from_coordinator()
        
        super()._handle_coordinator_update()

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        self._attr_current_option = option
        self.async_write_ha_state()
