from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
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
        ent_reg = er.async_get(self.hass)

        program_entity_id = ent_reg.async_get_entity_id("select", DOMAIN, UNIQUE_ID_PROGRAM_SELECT.format(self.config_id))
        delay_entity_id = ent_reg.async_get_entity_id("select", DOMAIN, UNIQUE_ID_DELAY_SELECT.format(self.config_id))
        switch_3in1_entity_id = ent_reg.async_get_entity_id("switch", DOMAIN, SWITCH_TREINUNO_ID.format(self.config_id))

        client = self.hass.data[DOMAIN][self.config_id].get(DATA_KEY_CLIENT)
        if not client:
            return

        payload = DEFAULT_DISHWASHER_PAYLOAD.copy()

        # Program
        if program_entity_id:
            program_state = self.hass.states.get(program_entity_id)
            if program_state:
                program_id = DISHWASHER_PROGRAMS.get(program_state.state)
                if program_id:
                    payload["Program"] = program_id
                    payload["w1"] = program_id.replace("P", "")

        # Delay
        if delay_entity_id:
            delay_state = self.hass.states.get(delay_entity_id)
            if delay_state:
                payload["DelayStart"] = DELAY_MAPPING.get(delay_state.state, "0")

        # 3-in-1
        if switch_3in1_entity_id:
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
