"""Constants for the Candy integration."""

DOMAIN = "candy"
PLATFORMS = ["sensor", "binary_sensor", "select", "button", "switch"]

DATA_KEY_COORDINATOR = "coordinator"
DATA_KEY_CLIENT = "client"
DATA_KEY_DEVICE_CODE = "device_code"

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
UNIQUE_ID_DISHWASHER_PROGRAM = "{0}-dishwasher_program"
UNIQUE_ID_DISHWASHER_DELAY = "{0}-dishwasher_delay"
UNIQUE_ID_DISHWASHER_OPTION = "{0}-dishwasher_option"
UNIQUE_ID_DISHWASHER_3IN1 = "{0}-dishwasher_3in1"

UNIQUE_ID_PROGRAM_SELECT = "{0}-program_select"
UNIQUE_ID_DELAY_SELECT = "{0}-delay_select"
UNIQUE_ID_OPTION_SELECT = "{0}-option_select"
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

RESET_PAYLOAD = {"Reset": "1"}
PAUSE_PAYLOAD = {"StartStop": "0"}

DELAY_MAPPING = {
    "0 min": "0",
    "30 min": "1",
    "1h": "2",
    "1h 30m": "3",
    "2h": "4",
    "2h 30m": "5",
    "3h": "6",
    "3h 30m": "7",
    "4h": "8",
    "4h 30m": "9",
    "5h": "10",
    "5h 30m": "11",
    "6h": "12",
    "6h 30m": "13",
    "7h": "14",
    "7h 30m": "15",
    "8h": "16",
    "8h 30m": "17",
    "9h": "18",
    "9h 30m": "19",
    "10h": "20",
    "10h 30m": "21",
    "11h": "22",
    "11h 30m": "23",
    "12h": "24",
    "12h 30m": "25",
    "13h": "26",
    "13h 30m": "27",
    "14h": "28",
    "14h 30m": "29",
    "15h": "30",
    "15h 30m": "31",
    "16h": "32",
    "16h 30m": "33",
    "17h": "34",
    "17h 30m": "35",
    "18h": "36",
    "18h 30m": "37",
    "19h": "38",
    "19h 30m": "39",
    "20h": "40",
    "20h 30m": "41",
    "21h": "42",
    "21h 30m": "43",
    "22h": "44",
    "22h 30m": "45",
    "23h": "46",
    "23h 30m": "47",
    "24h": "48",
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
