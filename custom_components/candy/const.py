"""Constants for the Candy integration."""

DOMAIN = "candy"
PLATFORMS = ["sensor", "binary_sensor", "select", "button", "switch"]

DATA_KEY_COORDINATOR = "coordinator"
DATA_KEY_CLIENT = "client"

CONF_INTEGRATION_TITLE = "Candy"
CONF_KEY_USE_ENCRYPTION = "use_encryption"

UNIQUE_ID_WASHING_MACHINE = "{0}-washing_machine"
UNIQUE_ID_WASH_CYCLE_STATUS = "{0}-wash_cycle_status"
UNIQUE_ID_WASH_REMAINING_TIME = "{0}-wash_remaining_time"
UNIQUE_ID_TUMBLE_DRYER = "{0}-tumble_dryer"
UNIQUE_ID_TUMBLE_CYCLE_STATUS = "{0}-tumble_cycle_status"
UNIQUE_ID_TUMBLE_REMAINING_TIME = "{0}-tumble_remaining_time"

UNIQUE_ID_OVEN = "{0}-oven"
UNIQUE_ID_OVEN_TEMP = "{0}-oven-temp"
UNIQUE_ID_DISHWASHER = "{0}-dishwasher"
UNIQUE_ID_DISHWASHER_REMAINING_TIME = "{0}-dishwasher_remaining_time"
UNIQUE_ID_DISHWASHER_SALT = "{0}-dishwasher_salt"
UNIQUE_ID_DISHWASHER_RINSE = "{0}-dishwasher_rinse"
UNIQUE_ID_DISHWASHER_DOOR = "{0}-dishwasher_door"

UNIQUE_ID_PROGRAM_SELECT = "{0}-program_select"
UNIQUE_ID_DELAY_SELECT = "{0}-delay_select"
UNIQUE_ID_START_BUTTON = "{0}-start_button"
UNIQUE_ID_PAUSE_BUTTON = "{0}-pause_button"
UNIQUE_ID_STOP_BUTTON = "{0}-stop_button"
SWITCH_TREINUNO_ID = "{0}-switch_3in1"

DEVICE_NAME_WASHING_MACHINE = "Washing machine"
DEVICE_NAME_TUMBLE_DRYER = "Tumble dryer"
DEVICE_NAME_OVEN = "Oven"
DEVICE_NAME_DISHWASHER = "Dishwasher"

DISHWASHER_PROGRAMS = {
    "intensive": "P1",
    "universal": "P2",
    "eco": "P3",
    "quick_24": "P4",
    "prewash": "P12",
    "quick_39": "P19",
}

OPTION_MAPPING = {
    "standard": {"OpzProg": "0", "MetaCarico": "0"},
    "extra_dry": {"OpzProg": "9", "MetaCarico": "0"},
    "half_load": {"OpzProg": "0", "MetaCarico": "1"},
    "eco": {"OpzProg": "12", "MetaCarico": "0"},
}
SELECT_OPTION_ID = "select.candy_dishwasher_option"

RESET_PAYLOAD = {"Reset": "1"}
PAUSE_PAYLOAD = {"StartStop": "0"}

DELAY_MAPPING = {
    "0 min": "0",
    "30 min": "30",
    "1h": "60",
    "2h": "120",
    "3h": "180",
    "4h": "240",
    "5h": "300",
    "6h": "360",
    "7h": "420",
    "8h": "480",
    "9h": "540",
}

SUGGESTED_AREA_BATHROOM = "Bathroom"
SUGGESTED_AREA_KITCHEN = "Kitchen"

DEFAULT_DISHWASHER_PAYLOAD = {
    "DelayStart": "0",
    "ExtraDry": "0",
    "OpenDoorOpt": "0",
    "TreinUno": "0",
    "Program": "P12",
    "MetaCarico": "0",
    "OpzProg": "0",
    "w1": "4",
    "StartStop": "1",
}
