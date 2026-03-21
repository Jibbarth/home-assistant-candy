from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    DATA_KEY_COORDINATOR,
    DATA_KEY_CLIENT,
    UNIQUE_ID_START_BUTTON,
    UNIQUE_ID_PAUSE_BUTTON,
    UNIQUE_ID_STOP_BUTTON,
    SWITCH_TREINUNO_ID,
    DEVICE_NAME_DISHWASHER,
    DISHWASHER_PROGRAMS,
    OPTION_MAPPING,
    SELECT_OPTION_ID,
    DEFAULT_DISHWASHER_PAYLOAD,
    RESET_PAYLOAD,
    PAUSE_PAYLOAD,
    DELAY_MAPPING,
)
from .client.model import DishwasherStatus

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities):
    """Set up the Candy buttons."""
    config_id = config_entry.entry_id
    coordinator = hass.data[DOMAIN][config_id][DATA_KEY_COORDINATOR]

    if isinstance(coordinator.data, DishwasherStatus):
        async_add_entities([
            CandyStartButton(coordinator, config_id, hass),
            CandyPauseButton(coordinator, config_id, hass),
            CandyStopButton(coordinator, config_id, hass),
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
            selected_program_key = program_select.current_option
            # Get program ID from key mapping
            program_id = DISHWASHER_PROGRAMS.get(selected_program_key)
            if program_id:
                client = self.hass.data[DOMAIN][self.config_id].get(DATA_KEY_CLIENT)
                if client:
                    payload = DEFAULT_DISHWASHER_PAYLOAD.copy()
                    payload["Program"] = program_id
                    # Need to extract numeric part for w1 if needed
                    # w1 was program_id previously, now program_id is P1 etc.
                    # Previous code used: payload["w1"] = program_id (where program_id was '1')
                    # Now program_id is 'P1'. Need to strip 'P'.
                    w1_val = program_id.replace("P", "")
                    payload["w1"] = w1_val

                    # Get delay start
                    delay_start_entity = self.hass.states.get("input_select.delai_demarrage")
                    delay_value = "0"
                    if delay_start_entity:
                        delay_value = DELAY_MAPPING.get(delay_start_entity.state, "0")
                    payload["DelayStart"] = delay_value

                    # Get 3-en-1 status
                    switch_3in1_entity_id = f"switch.{SWITCH_TREINUNO_ID.format(self.config_id)}"
                    switch_3in1_state = self.hass.states.get(switch_3in1_entity_id)
                    payload["TreinUno"] = "1" if switch_3in1_state and switch_3in1_state.state == "on" else "0"

                    # Get dishwasher options
                    option_select_state = self.hass.states.get(SELECT_OPTION_ID)
                    if option_select_state and option_select_state.state in OPTION_MAPPING:
                        option_values = OPTION_MAPPING[option_select_state.state]
                        payload.update(option_values)

                    await client.write(payload)

class CandyPauseButton(CoordinatorEntity, ButtonEntity):
    """Candy pause button entity."""

    def __init__(self, coordinator, config_id, hass):
        super().__init__(coordinator)
        self.config_id = config_id
        self.hass = hass
        self._attr_unique_id = UNIQUE_ID_PAUSE_BUTTON.format(config_id)
        self._attr_name = "Pause"

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self.config_id)},
            name=DEVICE_NAME_DISHWASHER,
            manufacturer="Candy",
        )

    async def async_press(self) -> None:
        """Press the button."""
        client = self.hass.data[DOMAIN][self.config_id].get(DATA_KEY_CLIENT)
        if client:
            await client.write(PAUSE_PAYLOAD)

class CandyStopButton(CoordinatorEntity, ButtonEntity):
    """Candy stop button entity."""

    def __init__(self, coordinator, config_id, hass):
        super().__init__(coordinator)
        self.config_id = config_id
        self.hass = hass
        self._attr_unique_id = UNIQUE_ID_STOP_BUTTON.format(config_id)
        self._attr_name = "Stop"

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self.config_id)},
            name=DEVICE_NAME_DISHWASHER,
            manufacturer="Candy",
        )

    async def async_press(self) -> None:
        """Press the button."""
        client = self.hass.data[DOMAIN][self.config_id].get(DATA_KEY_CLIENT)
        if client:
            await client.write(RESET_PAYLOAD)
