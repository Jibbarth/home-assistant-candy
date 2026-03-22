from abc import abstractmethod
from typing import Any, Mapping

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    UnitOfTime,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import (CoordinatorEntity,
                                                      DataUpdateCoordinator)

from .client import WashingMachineStatus
from .client.model import (DishwasherState, DishwasherStatus,
                           DryerProgramState, MachineState, OvenStatus,
                           TumbleDryerStatus)
from .const import (
    DATA_KEY_COORDINATOR,
    DATA_KEY_DEVICE_CODE,
    DELAY_MAPPING,
    DEVICE_NAME_DISHWASHER,
    DEVICE_NAME_OVEN,
    DEVICE_NAME_TUMBLE_DRYER,
    DEVICE_NAME_WASHING_MACHINE,
    DOMAIN,
    OPTION_MAPPING,
    SUGGESTED_AREA_BATHROOM,
    SUGGESTED_AREA_KITCHEN,
    UNIQUE_ID_DISHWASHER,
    UNIQUE_ID_DISHWASHER_3IN1,
    UNIQUE_ID_DISHWASHER_DELAY,
    UNIQUE_ID_DISHWASHER_DOOR,
    UNIQUE_ID_DISHWASHER_OPTION,
    UNIQUE_ID_DISHWASHER_PROGRAM,
    UNIQUE_ID_DISHWASHER_REMAINING_TIME,
    UNIQUE_ID_DISHWASHER_RINSE,
    UNIQUE_ID_DISHWASHER_SALT,
    UNIQUE_ID_OVEN,
    UNIQUE_ID_OVEN_TEMP,
    UNIQUE_ID_TUMBLE_CYCLE_STATUS,
    UNIQUE_ID_TUMBLE_DRYER,
    UNIQUE_ID_TUMBLE_REMAINING_TIME,
    UNIQUE_ID_WASH_CYCLE_STATUS,
    UNIQUE_ID_WASHING_MACHINE,
    UNIQUE_ID_WASH_REMAINING_TIME,
)


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities):
    """Set up the Candy sensors from config entry."""

    config_id = config_entry.entry_id
    coordinator = hass.data[DOMAIN][config_id][DATA_KEY_COORDINATOR]
    device_code = hass.data[DOMAIN][config_id][DATA_KEY_DEVICE_CODE]

    if isinstance(coordinator.data, WashingMachineStatus):
        async_add_entities([
            CandyWashingMachineSensor(coordinator, config_id, device_code),
            CandyWashCycleStatusSensor(coordinator, config_id, device_code),
            CandyWashRemainingTimeSensor(coordinator, config_id, device_code)
        ])
    elif isinstance(coordinator.data, TumbleDryerStatus):
        async_add_entities([
            CandyTumbleDryerSensor(coordinator, config_id, device_code),
            CandyTumbleStatusSensor(coordinator, config_id, device_code),
            CandyTumbleRemainingTimeSensor(coordinator, config_id, device_code)
        ])
    elif isinstance(coordinator.data, OvenStatus):
        async_add_entities([
            CandyOvenSensor(coordinator, config_id, device_code),
            CandyOvenTempSensor(coordinator, config_id, device_code)
        ])
    elif isinstance(coordinator.data, DishwasherStatus):
        async_add_entities([
            CandyDishwasherSensor(coordinator, config_id, device_code),
            CandyDishwasherRemainingTimeSensor(coordinator, config_id, device_code),
            CandyDishwasherProgramSensor(coordinator, config_id, device_code),
            CandyDishwasherDelaySensor(coordinator, config_id, device_code),
            CandyDishwasherOptionSensor(coordinator, config_id, device_code),
            CandyDishwasher3In1Sensor(coordinator, config_id, device_code),
            CandySaltSensor(coordinator, config_id, device_code),
            CandyRinseSensor(coordinator, config_id, device_code)
        ])
    else:
        raise Exception(f"Unable to determine machine type: {coordinator.data}")


class CandyBaseSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: DataUpdateCoordinator, config_id: str, device_code: str):
        super().__init__(coordinator)
        self.config_id = config_id
        self.device_code = device_code

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self.config_id)},
            name=self.device_name(),
            manufacturer="Candy",
            serial_number=self.device_code,
            suggested_area=self.suggested_area(),
        )

    @abstractmethod
    def device_name(self) -> str:
        pass

    @abstractmethod
    def suggested_area(self) -> str:
        pass


class CandyWashingMachineSensor(CandyBaseSensor):

    def device_name(self) -> str:
        return DEVICE_NAME_WASHING_MACHINE

    def suggested_area(self) -> str:
        return SUGGESTED_AREA_BATHROOM

    @property
    def name(self) -> str:
        return self.device_name()

    @property
    def unique_id(self) -> str:
        return UNIQUE_ID_WASHING_MACHINE.format(self.config_id)

    @property
    def state(self) -> StateType:
        status: WashingMachineStatus = self.coordinator.data
        return str(status.machine_state)

    @property
    def icon(self) -> str:
        return "mdi:washing-machine"

    @property
    def extra_state_attributes(self) -> Mapping[str, Any]:
        status: WashingMachineStatus = self.coordinator.data

        attributes = {
            "program": status.program,
            "temperature": status.temp,
            "spin_speed": status.spin_speed,
            "remaining_minutes": status.remaining_minutes if status.machine_state in [MachineState.RUNNING,
                                                                                      MachineState.PAUSED] else 0,
            "remote_control": status.remote_control,
        }

        if status.fill_percent is not None:
            attributes["fill_percent"] = status.fill_percent

        if status.program_code is not None:
            attributes["program_code"] = status.program_code

        return attributes


class CandyWashCycleStatusSensor(CandyBaseSensor):

    def device_name(self) -> str:
        return DEVICE_NAME_WASHING_MACHINE

    def suggested_area(self) -> str:
        return SUGGESTED_AREA_BATHROOM

    @property
    def name(self) -> str:
        return "Wash cycle status"

    @property
    def unique_id(self) -> str:
        return UNIQUE_ID_WASH_CYCLE_STATUS.format(self.config_id)

    @property
    def state(self) -> StateType:
        status: WashingMachineStatus = self.coordinator.data
        return str(status.program_state)

    @property
    def icon(self) -> str:
        return "mdi:washing-machine"


class CandyWashRemainingTimeSensor(CandyBaseSensor):

    def device_name(self) -> str:
        return DEVICE_NAME_WASHING_MACHINE

    def suggested_area(self) -> str:
        return SUGGESTED_AREA_BATHROOM

    @property
    def name(self) -> str:
        return "Wash cycle remaining time"

    @property
    def unique_id(self) -> str:
        return UNIQUE_ID_WASH_REMAINING_TIME.format(self.config_id)

    @property
    def state(self) -> StateType:
        status: WashingMachineStatus = self.coordinator.data
        if status.machine_state in [MachineState.RUNNING, MachineState.PAUSED]:
            return status.remaining_minutes
        else:
            return 0

    @property
    def unit_of_measurement(self) -> str:
        return UnitOfTime.MINUTES

    @property
    def icon(self) -> str:
        return "mdi:progress-clock"


class CandyTumbleDryerSensor(CandyBaseSensor):

    def device_name(self) -> str:
        return DEVICE_NAME_TUMBLE_DRYER

    def suggested_area(self) -> str:
        return SUGGESTED_AREA_BATHROOM

    @property
    def name(self) -> str:
        return self.device_name()

    @property
    def unique_id(self) -> str:
        return UNIQUE_ID_TUMBLE_DRYER.format(self.config_id)

    @property
    def state(self) -> StateType:
        status: TumbleDryerStatus = self.coordinator.data
        return str(status.machine_state)

    @property
    def icon(self) -> str:
        return "mdi:tumble-dryer"

    @property
    def extra_state_attributes(self) -> Mapping[str, Any]:
        status: TumbleDryerStatus = self.coordinator.data

        attributes = {
            "program": status.program,
            "remaining_minutes": status.remaining_minutes,
            "remote_control": status.remote_control,
            "dry_level": status.dry_level,
            "dry_level_now": status.dry_level_selected,
            "refresh": status.refresh,
            "need_clean_filter": status.need_clean_filter,
            "water_tank_full": status.water_tank_full,
            "door_closed": status.door_closed,
        }

        return attributes


class CandyTumbleStatusSensor(CandyBaseSensor):

    def device_name(self) -> str:
        return DEVICE_NAME_TUMBLE_DRYER

    def suggested_area(self) -> str:
        return SUGGESTED_AREA_BATHROOM

    @property
    def name(self) -> str:
        return "Dryer cycle status"

    @property
    def unique_id(self) -> str:
        return UNIQUE_ID_TUMBLE_CYCLE_STATUS.format(self.config_id)

    @property
    def state(self) -> StateType:
        status: TumbleDryerStatus = self.coordinator.data
        if status.program_state in [DryerProgramState.STOPPED]:
            return str(status.cycle_state)
        else:
            return str(status.program_state)

    @property
    def icon(self) -> str:
        return "mdi:tumble-dryer"


class CandyTumbleRemainingTimeSensor(CandyBaseSensor):

    def device_name(self) -> str:
        return DEVICE_NAME_TUMBLE_DRYER

    def suggested_area(self) -> str:
        return SUGGESTED_AREA_BATHROOM

    @property
    def name(self) -> str:
        return "Dryer cycle remaining time"

    @property
    def unique_id(self) -> str:
        return UNIQUE_ID_TUMBLE_REMAINING_TIME.format(self.config_id)

    @property
    def state(self) -> StateType:
        status: TumbleDryerStatus = self.coordinator.data
        if status.machine_state in [MachineState.RUNNING, MachineState.PAUSED]:
            return status.remaining_minutes
        else:
            return 0

    @property
    def unit_of_measurement(self) -> str:
        return UnitOfTime.MINUTES

    @property
    def icon(self) -> str:
        return "mdi:progress-clock"


class CandyOvenSensor(CandyBaseSensor):

    def device_name(self) -> str:
        return DEVICE_NAME_OVEN

    def suggested_area(self) -> str:
        return SUGGESTED_AREA_KITCHEN

    @property
    def name(self) -> str:
        return self.device_name()

    @property
    def unique_id(self) -> str:
        return UNIQUE_ID_OVEN.format(self.config_id)

    @property
    def state(self) -> StateType:
        status: OvenStatus = self.coordinator.data
        return str(status.machine_state)

    @property
    def icon(self) -> str:
        return "mdi:stove"

    @property
    def extra_state_attributes(self) -> Mapping[str, Any]:
        status: OvenStatus = self.coordinator.data

        attributes = {
            "program": status.program,
            "selection": status.selection,
            "temperature": status.temp,
            "temperature_reached": status.temp_reached,
            "remote_control": status.remote_control,
        }

        if status.program_length_minutes is not None:
            attributes["program_length_minutes"] = status.program_length_minutes

        return attributes


class CandyOvenTempSensor(CandyBaseSensor):

    def device_name(self) -> str:
        return DEVICE_NAME_OVEN

    def suggested_area(self) -> str:
        return SUGGESTED_AREA_KITCHEN

    @property
    def name(self) -> str:
        return "Oven temperature"

    @property
    def unique_id(self) -> str:
        return UNIQUE_ID_OVEN_TEMP.format(self.config_id)

    @property
    def state(self) -> StateType:
        status: OvenStatus = self.coordinator.data
        return status.temp

    @property
    def unit_of_measurement(self) -> str:
        return UnitOfTemperature.CELSIUS

    @property
    def icon(self) -> str:
        return "mdi:thermometer"


class CandyDishwasherSensor(CandyBaseSensor):

    _attr_translation_key = "status"

    def device_name(self) -> str:
        return DEVICE_NAME_DISHWASHER

    def suggested_area(self) -> str:
        return SUGGESTED_AREA_KITCHEN

    @property
    def name(self) -> str:
        return self.device_name()

    @property
    def unique_id(self) -> str:
        return UNIQUE_ID_DISHWASHER.format(self.config_id)

    @property
    def state(self) -> StateType:
        status: DishwasherStatus = self.coordinator.data
        return str(status.machine_state)

    @property
    def icon(self) -> str:
        return "mdi:glass-wine"

    @property
    def extra_state_attributes(self) -> Mapping[str, Any]:
        status: DishwasherStatus = self.coordinator.data

        attributes = {
            "program": status.program,
            "remaining_minutes": 0 if status.machine_state in
                                      [DishwasherState.IDLE, DishwasherState.FINISHED] else status.remaining_minutes,
            "remote_control": status.remote_control,
            "door_open": status.door_open,
            "eco_mode": status.eco_mode,
            "salt_empty": status.salt_empty,
            "rinse_aid_empty": status.rinse_aid_empty
        }

        if status.door_open_allowed is not None:
            attributes["door_open_allowed"] = status.door_open_allowed

        if status.delayed_start_hours is not None:
            attributes["delayed_start_hours"] = status.delayed_start_hours

        attributes["raw_response"] = status.raw_response

        return attributes


class CandyDishwasherRemainingTimeSensor(CandyBaseSensor):

    _attr_translation_key = "remaining_time"
    _attr_has_entity_name = True

    def device_name(self) -> str:
        return DEVICE_NAME_DISHWASHER

    def suggested_area(self) -> str:
        return SUGGESTED_AREA_KITCHEN

    @property
    def unique_id(self) -> str:
        return UNIQUE_ID_DISHWASHER_REMAINING_TIME.format(self.config_id)

    @property
    def state(self) -> StateType:
        status: DishwasherStatus = self.coordinator.data
        if status.machine_state in [DishwasherState.IDLE, DishwasherState.FINISHED]:
            return 0
        else:
            return status.remaining_minutes

    @property
    def unit_of_measurement(self) -> str:
        return UnitOfTime.MINUTES

    @property
    def icon(self) -> str:
        return "mdi:progress-clock"


class CandyDishwasherProgramSensor(CandyBaseSensor):

    _attr_translation_key = "program_status"
    _attr_has_entity_name = True

    def device_name(self) -> str:
        return DEVICE_NAME_DISHWASHER

    def suggested_area(self) -> str:
        return SUGGESTED_AREA_KITCHEN

    @property
    def unique_id(self) -> str:
        return UNIQUE_ID_DISHWASHER_PROGRAM.format(self.config_id)

    @property
    def state(self) -> StateType:
        status: DishwasherStatus = self.coordinator.data
        return status.program

    @property
    def icon(self) -> str:
        return "mdi:dishwasher"


class CandyDishwasherDelaySensor(CandyBaseSensor):

    _attr_translation_key = "delay_status"
    _attr_has_entity_name = True

    def device_name(self) -> str:
        return DEVICE_NAME_DISHWASHER

    def suggested_area(self) -> str:
        return SUGGESTED_AREA_KITCHEN

    @property
    def unique_id(self) -> str:
        return UNIQUE_ID_DISHWASHER_DELAY.format(self.config_id)

    @property
    def state(self) -> StateType:
        status: DishwasherStatus = self.coordinator.data
        value = status.delayed_start_hours
        if value is None:
            return "0 min"

        return next((key for key, mapped in DELAY_MAPPING.items() if mapped == str(value)), str(value))

    @property
    def extra_state_attributes(self) -> Mapping[str, Any]:
        status: DishwasherStatus = self.coordinator.data
        return {
            "raw_delay_value": 0 if status.delayed_start_hours is None else status.delayed_start_hours,
        }

    @property
    def icon(self) -> str:
        return "mdi:timer-cog-outline"


class CandyDishwasherOptionSensor(CandyBaseSensor):

    _attr_translation_key = "option_status"
    _attr_has_entity_name = True

    def device_name(self) -> str:
        return DEVICE_NAME_DISHWASHER

    def suggested_area(self) -> str:
        return SUGGESTED_AREA_KITCHEN

    @property
    def unique_id(self) -> str:
        return UNIQUE_ID_DISHWASHER_OPTION.format(self.config_id)

    @property
    def state(self) -> StateType:
        status: DishwasherStatus = self.coordinator.data
        opz_prog = str(status.opz_prog)
        meta_carico = str(status.meta_carico)
        for name, mapping in OPTION_MAPPING.items():
            if mapping.get("OpzProg") == opz_prog and mapping.get("MetaCarico") == meta_carico:
                return name

        return f"{opz_prog}/{meta_carico}"

    @property
    def icon(self) -> str:
        return "mdi:tune-variant"


class CandyDishwasher3In1Sensor(CandyBaseSensor):

    _attr_translation_key = "dishwasher_3in1_status"
    _attr_has_entity_name = True

    def device_name(self) -> str:
        return DEVICE_NAME_DISHWASHER

    def suggested_area(self) -> str:
        return SUGGESTED_AREA_KITCHEN

    @property
    def unique_id(self) -> str:
        return UNIQUE_ID_DISHWASHER_3IN1.format(self.config_id)

    @property
    def state(self) -> StateType:
        status: DishwasherStatus = self.coordinator.data
        return "on" if status.trein_uno else "off"

    @property
    def icon(self) -> str:
        return "mdi:checkbox-marked-circle-outline"


class CandySaltSensor(CandyBaseSensor):

    _attr_translation_key = "salt_level"
    _attr_has_entity_name = True

    def device_name(self) -> str:
        return DEVICE_NAME_DISHWASHER

    def suggested_area(self) -> str:
        return SUGGESTED_AREA_KITCHEN

    @property
    def unique_id(self) -> str:
        return UNIQUE_ID_DISHWASHER_SALT.format(self.config_id)

    @property
    def state(self) -> StateType:
        status: DishwasherStatus = self.coordinator.data
        return "problem" if status.salt_empty else "ok"

    @property
    def icon(self) -> str:
        return "mdi:shaker"


class CandyRinseSensor(CandyBaseSensor):

    _attr_translation_key = "rinse_aid_level"
    _attr_has_entity_name = True

    def device_name(self) -> str:
        return DEVICE_NAME_DISHWASHER

    def suggested_area(self) -> str:
        return SUGGESTED_AREA_KITCHEN

    @property
    def unique_id(self) -> str:
        return UNIQUE_ID_DISHWASHER_RINSE.format(self.config_id)

    @property
    def state(self) -> StateType:
        status: DishwasherStatus = self.coordinator.data
        return "problem" if status.rinse_aid_empty else "ok"

    @property
    def icon(self) -> str:
        return "mdi:water-opacity"
