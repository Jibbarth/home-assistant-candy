from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo

from .const import (
    DOMAIN,
    DATA_KEY_COORDINATOR,
    DATA_KEY_DEVICE_CODE,
    SWITCH_TREINUNO_ID,
    DEVICE_NAME_DISHWASHER,
)

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities):
    """Set up the Candy switches."""
    config_id = config_entry.entry_id
    coordinator = hass.data[DOMAIN][config_id][DATA_KEY_COORDINATOR]
    device_code = hass.data[DOMAIN][config_id][DATA_KEY_DEVICE_CODE]

    async_add_entities([
        Candy3In1Switch(config_id, device_code),
    ])

class Candy3In1Switch(SwitchEntity):
    """Candy 3-in-1 switch entity."""

    def __init__(self, config_id, device_code):
        self.config_id = config_id
        self.device_code = device_code
        self._attr_unique_id = SWITCH_TREINUNO_ID.format(config_id)
        self._attr_translation_key = "dishwasher_3in1"
        self._attr_has_entity_name = True
        self._attr_is_on = False

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self.config_id)},
            name=DEVICE_NAME_DISHWASHER,
            manufacturer="Candy",
            serial_number=self.device_code,
        )

    @property
    def is_on(self) -> bool:
        """Return True if the switch is on."""
        return self._attr_is_on

    async def async_turn_on(self, **kwargs) -> None:
        """Turn the switch on."""
        self._attr_is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs) -> None:
        """Turn the switch off."""
        self._attr_is_on = False
        self.async_write_ha_state()
