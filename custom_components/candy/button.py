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
    UNIQUE_ID_PROGRAM_SELECT,
    UNIQUE_ID_DELAY_SELECT,
    SWITCH_TREINUNO_ID,
    DEVICE_NAME_DISHWASHER,
    DISHWASHER_PROGRAMS,
    OPTION_MAPPING,
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
        program_entity_id = f"select.candy_dishwasher_program_{self.config_id.replace('-', '_')}"
        delay_entity_id = f"select.candy_dishwasher_delay_start_{self.config_id.replace('-', '_')}"
        switch_3in1_entity_id = f"switch.candy_dishwasher_3_in_1_{self.config_id.replace('-', '_')}"
        
        # Note: The actual entity IDs in HA might differ slightly depending on name -> ID conversion.
        # This assumes standard slugify behavior.

        client = self.hass.data[DOMAIN][self.config_id].get(DATA_KEY_CLIENT)
        if not client:
            return

        payload = DEFAULT_DISHWASHER_PAYLOAD.copy()

        # Program
        program_state = self.hass.states.get(program_entity_id)
        if program_state:
            program_id = DISHWASHER_PROGRAMS.get(program_state.state)
            if program_id:
                payload["Program"] = program_id
                payload["w1"] = program_id.replace("P", "")

        # Delay
        delay_state = self.hass.states.get(delay_entity_id)
        if delay_state:
            payload["DelayStart"] = DELAY_MAPPING.get(delay_state.state, "0")

        # 3-in-1
        switch_state = self.hass.states.get(switch_3in1_entity_id)
        payload["TreinUno"] = "1" if switch_state and switch_state.state == "on" else "0"

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
