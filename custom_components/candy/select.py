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
        # Assuming delay is in hours in coordinator data?
        # Model says: delayed_start_hours: Optional[int]
        # We need to map back to the keys like "1h", "2h"...
        # But wait, DELAY_MAPPING maps "1h" to "2". "2" is the value sent to the machine?
        # Let's check const.py.
        # "1h": "2". This "2" is likely the value sent to the machine.
        # If model says delayed_start_hours, that might be the integer hour.
        # This part is tricky without knowing exactly what `DelayStart` raw value means vs `delayed_start_hours`.
        # `DELAY_MAPPING` maps "0 min" -> "0", "30 min" -> "1", "1h" -> "2".
        # It seems these are codes.
        # `delayed_start_hours` in model is `int(json["DelayStart"])`.
        # Wait, if json["DelayStart"] is "2", model says `delayed_start_hours` is 2.
        # But "2" maps to "1h".
        # So we should look for the value in mapping that equals str(delayed_start_hours).
        if self.coordinator.data and hasattr(self.coordinator.data, "delayed_start_hours"):
            # We access the raw value from the json if possible, or try to infer.
            # model.py: delayed_start_hours=int(json["DelayStart"]) if json["DelayStart"] != "0" else None
            # If it is None, it is 0.
            
            # Actually, `CandyDelaySelect` in original code did NOT update from coordinator at all!
            # It just had `return self._attr_current_option` and init to "0 min".
            # If I want to fix bouncing, I must assume it *should* update from coordinator.
            # But if I don't know the mapping back, I might break it.
            # However, `delayed_start_hours` seems to be the integer value.
            # Let's see if we can map it back.
            # If `delayed_start_hours` is 1, maybe it matches "1h"?
            # Let's look at DELAY_MAPPING again.
            # "1h": "2".
            # If `delayed_start_hours` is derived from `json["DelayStart"]`, and `json["DelayStart"]` is the code...
            # Then `delayed_start_hours` holds the code (as int).
            # So if `delayed_start_hours` is 2, we want "1h".
            
            val = self.coordinator.data.delayed_start_hours
            if val is None:
                val = 0
            
            val_str = str(val)
            key = next((k for k, v in DELAY_MAPPING.items() if v == val_str), None)
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
        if self.coordinator.data:
            opz_prog = str(self.coordinator.data.opz_prog)
            meta_carico = str(self.coordinator.data.meta_carico)

            for name, mapping in OPTION_MAPPING.items():
                if mapping["OpzProg"] == opz_prog and mapping["MetaCarico"] == meta_carico:
                    self._attr_current_option = name
                    break
            else:
            self._attr_current_option = "standard" # Fallback to default if data is missing

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
