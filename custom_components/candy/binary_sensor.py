from abc import abstractmethod
from typing import Any

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import (CoordinatorEntity,
                                                      DataUpdateCoordinator)

from .client.model import DishwasherStatus
from .const import DOMAIN, DEVICE_NAME_DISHWASHER, SUGGESTED_AREA_KITCHEN, UNIQUE_ID_DISHWASHER_DOOR, DATA_KEY_COORDINATOR


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities):
    """Set up the Candy binary sensors."""
    config_id = config_entry.entry_id
    coordinator = hass.data[DOMAIN][config_id][DATA_KEY_COORDINATOR]

    if isinstance(coordinator.data, DishwasherStatus):
        async_add_entities([CandyDoorSensor(coordinator, config_id)])


class CandyBaseBinarySensor(CoordinatorEntity, BinarySensorEntity):
    def __init__(self, coordinator: DataUpdateCoordinator, config_id: str):
        super().__init__(coordinator)
        self.config_id = config_id

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self.config_id)},
            name=self.device_name(),
            manufacturer="Candy",
            suggested_area=self.suggested_area(),
        )

    @abstractmethod
    def device_name(self) -> str:
        pass

    @abstractmethod
    def suggested_area(self) -> str:
        pass


class CandyDoorSensor(CandyBaseBinarySensor):

    def device_name(self) -> str:
        return DEVICE_NAME_DISHWASHER

    def suggested_area(self) -> str:
        return SUGGESTED_AREA_KITCHEN

    @property
    def unique_id(self) -> str:
        return UNIQUE_ID_DISHWASHER_DOOR.format(self.config_id)

    @property
    def translation_key(self) -> str:
        return "door_sensor"

    @property
    def is_on(self) -> bool:
        status: DishwasherStatus = self.coordinator.data
        return status.door_open

    @property
    def device_class(self) -> str:
        return "door"

    @property
    def icon(self) -> str:
        return "mdi:door"
