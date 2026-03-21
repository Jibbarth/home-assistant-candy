from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    DATA_KEY_COORDINATOR,
    DATA_KEY_CLIENT,
    SWITCH_TREINUNO_ID,
    DEVICE_NAME_DISHWASHER,
)

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities):
    """Set up the Candy switches."""
    config_id = config_entry.entry_id
    coordinator = hass.data[DOMAIN][config_id][DATA_KEY_COORDINATOR]

    async_add_entities([
        Candy3In1Switch(coordinator, config_id),
    ])

class Candy3In1Switch(CoordinatorEntity, SwitchEntity):
    """Candy 3-in-1 switch entity."""

    def __init__(self, coordinator, config_id):
        super().__init__(coordinator)
        self.config_id = config_id
        self._attr_unique_id = SWITCH_TREINUNO_ID.format(config_id)
        self._attr_name = "Candy Dishwasher 3-in-1"

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self.config_id)},
            name=DEVICE_NAME_DISHWASHER,
            manufacturer="Candy",
        )

    @property
    def is_on(self) -> bool:
        """Return True if the switch is on."""
        return self.coordinator.data.TreinUno == "1"

    async def async_turn_on(self, **kwargs) -> None:
        """Turn the switch on."""
        client = self.hass.data[DOMAIN][self.config_id].get(DATA_KEY_CLIENT)
        if client:
            await client.write({"TreinUno": "1"})
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs) -> None:
        """Turn the switch off."""
        client = self.hass.data[DOMAIN][self.config_id].get(DATA_KEY_CLIENT)
        if client:
            await client.write({"TreinUno": "0"})
        await self.coordinator.async_request_refresh()
