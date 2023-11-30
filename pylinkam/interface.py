from __future__ import annotations

import ctypes
import enum
import typing


class LoggingLevel(enum.IntEnum):
    MINIMAL = 0
    INFORMATIVE = 1
    VERBOSE = 2
    INVESTIGATION = 3


class Message(enum.IntEnum):
    if typing.TYPE_CHECKING:
        _value_: int
        variant_field: typing.Optional[str]

    def __new__(cls, value: int, variant_field: typing.Optional[str] = None) -> Message:
        # noinspection PyArgumentList
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.variant_field = variant_field

        return obj

    OPEN_COMMS = 0x01, 'vConnectionStatus'
    CLOSE_COMMS = 0x02, 'vBoolean'
    GET_CONTROLLER_CONFIG = 0x03, 'vControllerConfig'
    GET_CONTROLLER_ERROR = 0x04, 'vControllerError'
    GET_CONTROLLER_NAME = 0x05
    GET_CONTROLLER_SERIAL = 0x06
    GET_STATUS = 0x07, 'vControllerStatus'
    GET_STAGE_CONFIG = 0x08, 'vStageConfig'
    GET_STAGE_SERIAL = 0x09
    GET_STAGE_NAME = 0x0A
    GET_MAX_VALUE = 0x0B
    GET_MIN_VALUE = 0x0C
    GET_RESOLUTION = 0x0D
    APPLY_SAMPLE_CALS = 0x0E
    SAVE_SAMPLE_CALS = 0x0F
    START_HEATING = 0x10, 'vBoolean'
    START_VACUUM = 0x11, 'vBoolean'
    START_HUMIDITY = 0x12, 'vBoolean'
    START_HUMIDITY_DESICCANT_CONDITIONING = 0x13, 'vBoolean'
    START_MOTORS = 0x14, 'vBoolean'
    GET_VALUE = 0x15
    SET_VALUE = 0x16, 'vBoolean'
    TST_CALIBRATE_DISTANCE = 0x17, 'vBoolean'
    TST_SET_MODE = 0x18, 'vBoolean'
    TST_ZERO_FORCE = 0x19, 'vBoolean'
    TST_ZERO_POSITION = 0x1A, 'vBoolean'
    LNP_SET_MODE = 0x1B, 'vBoolean'
    LNP_SET_SPEED = 0x1C, 'vBoolean'
    CSS_APPLY_VALUES = 0x1D, 'vBoolean'
    CSS_CHECK_VALUES = 0x1E, 'vUint8'
    CSS_GOTO_REFERENCE = 0x1F, 'vBoolean'
    CSS_SENSOR_CAL = 0x20, 'vBoolean'
    CSS_START_JOG_GAP = 0x21, 'vBoolean'
    CSS_START_JOG_ROT = 0x22, 'vBoolean'
    ENABLE_LOGGING = 0x23, 'vBoolean'
    DISABLE_LOGGING = 0x24, 'vBoolean'
    GET_CONTROLLER_FIRMWARE_VERSION = 0x25
    GET_CONTROLLER_HARDWARE_VERSION = 0x26
    GET_STAGE_FIRMWARE_VERSION = 0x27
    GET_STAGE_HARDWARE_VERSION = 0x28
    GET_DATA_RATE = 0x29
    SET_DATA_RATE = 0x2A
    # GET_STAGE_CABLE_LIMITS = 0x2B, 'vStageCableLimit'
    SEND_DSC_GAIN_VALUES = 0x2C, 'vBoolean'
    SEND_DSC_POWER_VALUE = 0x2D, 'vBoolean'
    SEND_DSC_BASELINE_POWER_VALUES = 0x2E, 'vBoolean'
    SEND_DSC_TUA_CONSTANTS = 0x2F, 'vBoolean'
    SET_DSC_MODULATION_DATA = 0x30, 'vBoolean'
    # GET_OPTION_CARD_TYPE = 0x31, 'vOptionBoardType'
    # GET_OPTION_CARD_SLOT = 0x32, ?
    GET_OPTION_CARD_NAME = 0x33, 'vBoolean'
    GET_OPTION_CARD_SERIAL = 0x34, 'vBoolean'
    GET_OPTION_CARD_HARDWARE_VERSION = 0x35, 'vBoolean'
    DOES_OPTION_CARD_SUPPORT_SENSORS = 0x36, 'vUint32'
    GET_OPTION_CARD_SENSOR_NAME = 0x37, 'vBoolean'
    GET_OPTION_CARD_SENSOR_SERIAL = 0x38, 'vBoolean'
    GET_OPTION_CARD_SENSOR_HARDWARE_VERSION = 0x39, 'vBoolean'
    # GET_STAGE_GROUP = 0x3A, 'vStageGroup'
    HAVE_INSTRUMENT_BUS_DEVICE_TYPE = 0x3B, 'vBoolean'
    GET_INSTRUMENT_BUS_DEVICE_NAME = 0x3C, 'vBoolean'
    GET_INSTRUMENT_BUS_DEVICE_SERIAL = 0x3D, 'vBoolean'
    GET_INSTRUMENT_BUS_DEVICE_FIRMWARE_VERSION = 0x3E, 'vBoolean'
    GET_INSTRUMENT_BUS_DEVICE_HARDWARE_VERSION = 0x3F, 'vBoolean'
    GET_HUMIDITY_CONTROLLER_SENSOR_NAME = 0x40, 'vBoolean'
    GET_HUMIDITY_CONTROLLER_SENSOR_SERIAL = 0x41, 'vBoolean'
    GET_HUMIDITY_CONTROLLER_SENSOR_HARDWARE_VERSION = 0x42, 'vBoolean'
    IS_CONTROLLER_TYPE = 0x43, 'vBoolean'
    GET_CONTROLLER_PSU_DETAILS = 0x44, 'vBoolean'
    SET_CONTROLLER_TRIGGER_SIGNAL_ENABLE = 0x45, 'vBoolean'
    SET_CONTROLLER_TRIGGER_SIGNAL_DISABLE = 0x46, 'vBoolean'
    SET_CONTROLLER_MAINS_FREQUENCY = 0x47, 'vBoolean'
    INITIALISE_TRIGGER_SIGNAL_PULSE = 0x48, 'vBoolean'
    SET_TRIGGER_SIGNAL_PULSE = 0x49, 'vBoolean'
    SET_TRIGGER_SIGNAL_PLUSE_WIDTH = 0x4A, 'vBoolean'
    GET_PROGRAM_STATE = 0x4B, 'vBoolean'
    # GET_STAGE_CONFIGURATION = 0x4C, 'vStageCableConfig'
    GET_CONTROLLER_HEATER_DETAILS = 0x4D, 'vBoolean'
    CSS_SEND_GAP_VELOCITY = 0x4E, 'vBoolean'
    CSS_SEND_GAP_OVERRIDE = 0x4F, 'vBoolean'
    CSS_SEND_GAP = 0x50, 'vBoolean'
    CSS_SEND_VELOCITY = 0x51, 'vBoolean'
    CSS_SEND_RATE = 0x52, 'vBoolean'
    CSS_SEND_FREQUENCY = 0x53, 'vBoolean'
    CSS_SEND_STRAIN = 0x54, 'vBoolean'
    CSS_SEND_DIRECTION = 0x55, 'vBoolean'
    CSS_SEND_FORCE_STOP = 0x56, 'vBoolean'
    CSS_SEND_TORQUE = 0x57, 'vBoolean'
    TST_SET_CALIBRATE_FORCE_PROGRAM_MODE = 0x58, 'vBoolean'
    TST_SET_CALIBRATION_FORCE = 0x58, 'vBoolean'
    FORCE_HEATING = 0x59, 'vBoolean'
    FORCE_COOLING = 0x5A, 'vBoolean'
    FORCE_HOLD = 0x5B, 'vBoolean'
    # LINKAM ONLY GET_INSTRUMENT_BUS_DEVICE_IDENT = 0x5C
    # LINKAM ONLY GET_STAGE_IDENT = 0x5D
    # LINKAM ONLY GET_CONTROLLER_IDENT = 0x5F
    GET_CONNECTION_INFORMATION = 0x60, 'vBoolean'
    # LINKAM ONLY GET_STAGE_HEATER_IDENT = 0x61
    # LINKAM ONLY ENABLE_SERIAL_LOOPBACK_TEST = 0x62
    # LINKAM ONLY DISABLE_SERIAL_LOOPBACK_TEST = 0x63


# Type definitions
class CommsType(enum.IntEnum):
    NONE = 0
    SERIAL = 1
    USB = 2


class CommsInfoSerial(ctypes.Structure):
    _fields_ = [
        ('port', 64 * ctypes.c_char),
        ('baudrate', ctypes.c_uint32),
        ('bytesize', ctypes.c_uint32),
        ('parity', ctypes.c_uint32),
        ('stopbits', ctypes.c_uint32),
        ('flowcontrol', ctypes.c_uint32),
        ('timeout', ctypes.c_uint32),
        ('padding', 36 * ctypes.c_char)
    ]


class CommsInfoUSB(ctypes.Structure):
    _fields_ = [
        ('vendorID', ctypes.c_uint16),
        ('productID', ctypes.c_uint16),
        ('serialNumber', 17 * ctypes.c_char),
        ('padding', 83 * ctypes.c_char)
    ]


class CommsInfoUnion(ctypes.Union):
    _fields_ = [
        ('info', 124 * ctypes.c_char),
        ('serial', CommsInfoSerial),
        ('usb', CommsInfoUSB),
    ]


class CommsInfo(ctypes.Structure):
    _fields_ = [
        ('type', ctypes.c_uint32),
        ('info', CommsInfoUnion)
    ]


class ConnectionStatusFlags(ctypes.Structure):
    _fields_ = [(x, ctypes.c_uint32, 1) for x in [
        'connected',
        'errorNoDeviceFound',
        'errorMultipleDevicesFound',
        'errorTimeout',
        'errorHandleRegistrationFailed',
        'errorAllocationFailed',
        'errorSerialNumberRequired',
        'errorAlreadyOpen',
        'errorPropertiesIncorrect',
        'errorPortConfig',
        'errorCommsStreams',
        'errorUnhandled',
        'unused12',
        'unused13',
        'unused14',
        'unused15',
        'unused16',
        'unused17',
        'unused18',
        'unused19',
        'unused20',
        'unused21',
        'unused22',
        'unused23',
        'unused24',
        'unused25',
        'unused26',
        'unused27',
        'unused28',
        'unused29',
        'unused30',
        'unused31'
    ]]


class ConnectionStatus(ctypes.Union):
    _fields_ = [
        ('flags', ConnectionStatusFlags),
        ('value', ctypes.c_uint32)
    ]


class ControllerErrorCode(enum.IntEnum):
    NONE = 0
    STAGE_CABLE_DISCONNECTED = 1
    STAGE_CABLE_ERROR = 2,
    STAGE_TEMP_SENSOR_OPEN_OVERRANGE = 3
    LOAD_POWER_OUTPUT_VOLTAGE_WRONG = 4
    T95_RELAY_MISSING = 5
    T95_OPTION_BOARD_WONG_CONFIG = 6
    OPTION_BOARD_CABLE_DISCONNECT = 7
    LOAD_POWER_INCORRECT_FOR_STAGE = 8
    OPTION_BOARD_INCORRECT_CABLE = 9
    OPTION_BOARD_SENSOR_OEN_OVERRANGE = 10
    T95_FAN_NOT_WORKING = 11
    LNP95_ERROR = 12
    COMMS_ERROR = 13
    COOLING_WATER_TOO_WARM_NOT_FLOWING = 14
    CSS450_MOTOR_DRIVE_OVER_TEMP = 15
    CSS450_MOTOR_WINDING_ERROR1 = 16
    CSS450_MOTOR_WINDING_ERROR2 = 17
    CMS196_CHAMBER_SENSOR_OPEN = 21
    CMS196_CHAMBER_SENSOR_OVERRANGE = 22
    CMS196_L_N2_SWITCH_SENSOR_OPEN = 23
    CMS196_L_N2_SWITCH_SENSOR_OVERRANGE = 24
    CMS196_DEWAR_SENSOR_OPEN = 25
    CMS196_DEWAR_SENSOR_OVERRANGE = 26
    CMS196_DEWAR_EMPTY = 27
    CMS196_BASE_SENSOR_OPEN = 28
    CMS196_BASE_SENSOR_OVERRANGE = 29
    CMS196_MOTOR_POSN_ERROR = 30


class ControllerConfigFlags(ctypes.Structure):
    _fields_ = [(x, ctypes.c_uint64, 1) for x in [
        'supportsHeater',
        'supportsDualHeater',
        'supportsDualHeaterIndependentLimits',
        'supportsDualHeaterIndependentRates',
        'unused4',
        'unused5',
        'unused6',
        'unused7',
        'unused8',
        'unused9',
        'vacuumOption',
        'unused11',
        'tensileForceCardReady',
        'dscCardReady',
        'xMotorCardReady',
        'yMotorCardReady',
        'zMotorCardReady',
        'motorValveCardReady',
        'tensileMotorCardReady',
        'gradedMotorCardReady',
        'dtcCardReady',
        'cssMotorCardReady',
        'unused22',
        'unused23',
        'unused24',
        'unused25',
        'unused26',
        'unused27',
        'unused28',
        'unused29',
        'unused30',
        'unused31',
        'unused32',
        'unused33',
        'unused34',
        'unused35',
        'lnpReady',
        'lnpDualReady',
        'unused38',
        'unused39',
        'unused40',
        'unused41',
        'unused42',
        'unused43',
        'unused44',
        'unused45',
        'humidityReady',
        'unused47',
        'unused48',
        'unused49',
        'unused50',
        'unused51',
        'unused52',
        'unused53',
        'unused54',
        'unused55',
        'unused56',
        'unused57',
        'unused58',
        'unused59',
        'unused60',
        'unused61',
        'unused62',
        'unused63'
    ]]


class ControllerConfig(ctypes.Union):
    _fields_ = [
        ('flags', ControllerConfigFlags),
        ('value', ctypes.c_uint64)
    ]


class ControllerProgramStatusFlags(ctypes.Structure):
    _fields_ = [(x, ctypes.c_uint32, 1) for x in [
        'dirn',
        'hold',
        'heat',
        'cool',
        'inLimitTime',
        'timeHold',
        'started',
        'newRate',
        'rampDone',
        'overRange',
        'linksys32Mode',
        'netDllMode',
        'coolTo300',
        'rateSlowDown',
        'linkMode',
        'unused15',
        'unused16',
        'unused17',
        'unused18',
        'unused19',
        'unused20',
        'unused21',
        'unused22',
        'unused23',
        'errPtr',
        'unused25',
        'unused26',
        'unused27',
        'unused28',
        'unused29',
        'unused30',
        'unused31'
    ]]


class ControllerProgramStatus(ctypes.Union):
    _fields_ = [
        ('flags', ControllerProgramStatusFlags),
        ('value', ctypes.c_uint32)
    ]


class ControllerStatusFlags(ctypes.Structure):
    _fields_ = [(x, ctypes.c_uint64, 1) for x in [
        'controllerError',
        'heater1RampSetPoint',
        'heater1Started',
        'heater2RampSetPoint',
        'heater2Started',
        'vacuumRampSetPoint',
        'vacuumCtrlStarted',
        'vacuumValveClosed',
        'vacuumValveOpen',
        'humidityRampSetPoint',
        'humidityCtrlStarted',
        'lnpCoolingPumpOn',
        'lnpCoolingPumpAuto',
        'unused13',
        'HumidityDesiccantConditioning',
        'unused15',
        'unused16',
        'unused17',
        'unused18',
        'unused19',
        'unused20',
        'unused21',
        'unused22',
        'unused23',
        'unused24',
        'unused25',
        'unused26',
        'unused27',
        'unused28',
        'unused29',
        'unused30',
        'unused31',
        'unused32',
        'unused33',
        'unused34',
        'unused35',
        'unused36',
        'unused37',
        'unused38',
        'unused39',
        'unused40',
        'motorTravelMinX',
        'motorTravelMaxX',
        'motorStoppedX',
        'motorTravelMinY',
        'motorTravelMaxY',
        'motorStoppedY',
        'motorTravelMinZ',
        'motorTravelMaxZ',
        'motorStoppedZ',
        'sampleCal',
        'motorDistanceCalTST',
        'cssRotMotorStopped',
        'cssGapMotorStopped',
        'cssLidOn',
        'cssRefLimit',
        'cssZeroLimit',
        'unused57',
        'unused58',
        'unused59',
        'unused60',
        'unused61',
        'unused62',
        'unused63'
    ]]


class ControllerStatus(ctypes.Union):
    _fields_ = [
        ('flags', ControllerStatusFlags),
        ('value', ctypes.c_uint64)
    ]


class HeaterDetails(ctypes.Structure):
    _fields_ = [
        ('minLimit', ctypes.c_float),
        ('maxLimit', ctypes.c_float),
        ('maxRate', ctypes.c_float),
        ('maxV', ctypes.c_float),
        ('maxI', ctypes.c_float)
    ]


class RHStatusFlags(ctypes.Structure):
    _fields_ = [
        ('colSel', ctypes.c_uint32, 4),
        ('present', ctypes.c_uint32, 1),
        ('reset', ctypes.c_uint32, 1),
        ('started', ctypes.c_uint32, 1),
        ('unitType', ctypes.c_uint32, 3),
        ('dessicantDryMode', ctypes.c_uint32, 1),
        ('rampLimitReached', ctypes.c_uint32, 1),
        ('unused12', ctypes.c_uint32, 1),
        ('unused13', ctypes.c_uint32, 1),
        ('unused14', ctypes.c_uint32, 1),
        ('unused15', ctypes.c_uint32, 1),
        ('unused16', ctypes.c_uint32, 1),
        ('unused17', ctypes.c_uint32, 1),
        ('unused18', ctypes.c_uint32, 1),
        ('unused19', ctypes.c_uint32, 1),
        ('unused20', ctypes.c_uint32, 1),
        ('unused21', ctypes.c_uint32, 1),
        ('unused22', ctypes.c_uint32, 1),
        ('unused23', ctypes.c_uint32, 1),
        ('unused24', ctypes.c_uint32, 1),
        ('unused25', ctypes.c_uint32, 1),
        ('unused26', ctypes.c_uint32, 1),
        ('unused27', ctypes.c_uint32, 1),
        ('unused28', ctypes.c_uint32, 1),
        ('unused29', ctypes.c_uint32, 1),
        ('unused30', ctypes.c_uint32, 1),
        ('unused31', ctypes.c_uint32, 1)
    ]


class RHStatus(ctypes.Union):
    _fields_ = [
        ('flags', RHStatusFlags),
        ('value', ctypes.c_uint32)
    ]


class RHUnit(ctypes.Structure):
    _fields_ = [
        ('rh', ctypes.c_float),
        ('rhSetpoint', ctypes.c_float),
        ('rhTemp', ctypes.c_float),
        ('dryTimeSecs', ctypes.c_int32),
        ('setDryTimeSecs', ctypes.c_int32),
        ('swapTimeSecs', ctypes.c_int32),
        ('setSwapTimeSecs', ctypes.c_int32),
        ('tubePercent', ctypes.c_float),
        ('tubeSetpoint', ctypes.c_float),
        ('waterTemp', ctypes.c_float),
        ('waterSetpoint', ctypes.c_float),
        ('columnDryModeCountTimeSecs', ctypes.c_int32),
        ('status', RHStatus)
    ]


class Running(ctypes.Structure):
    _fields_ = [
        ('timeLeft', ctypes.c_float),
        ('lnpSpeed', ctypes.c_float),
        ('voltage', ctypes.c_float),
        ('current', ctypes.c_float),
        ('pwm', ctypes.c_float),
        ('status', ControllerProgramStatus),
        ('auxStatus', ctypes.c_uint32),
        ('padding', ctypes.c_uint32),
        ('dllStatus', ControllerStatus)
    ]


class StageConfigFlags(ctypes.Structure):
    _fields_ = [(x, ctypes.c_uint64, 1) for x in [
        'standardStage',
        'highTempStage',
        'peltierStage',
        'gradedStage',
        'tensileStage',
        'dscStage',
        'warmStage',
        'itoStage',
        'css450Stage',
        'correlativeStage',
        'unused10',
        'unused11',
        'unused12',
        'unused13',
        'unused14',
        'unused15',
        'unused16',
        'unused17',
        'unused18',
        'unused19',
        'unused20',
        'coolingManual',
        'coolingAutomatic',
        'coolingDual',
        'coolingDualSpeedIndependent',
        'unused25',
        'heater1',
        'heater1TempCtrl',
        'heater1TempCtrlProbe',
        'unused29',
        'unused30',
        'unused31',
        'unused32',
        'unused33',
        'unused34',
        'unused35',
        'heater2',
        'heater12IndependentLimits',
        'unused38',
        'unused39',
        'unused40',
        'unused41',
        'unused42',
        'unused43',
        'unused44',
        'unused45',
        'waterCoolingSensorFitted',
        'home',
        'supportsVacuum',
        'motorX',
        'motorY',
        'motorZ',
        'supportsHumidity',
        'unused53',
        'unused54',
        'unused55',
        'unused56',
        'unused57',
        'unused58',
        'unused59',
        'unused60',
        'unused61',
        'unused62',
        'unused63'
    ]]


class StageConfig(ctypes.Union):
    _fields_ = [
        ('flags', StageConfigFlags),
        ('value', ctypes.c_uint64)
    ]


class StageValueType(enum.IntEnum):
    if typing.TYPE_CHECKING:
        _value_: int
        variant_field: typing.Optional[str]
        unit: typing.Optional[str]

    def __new__(cls, value: int, variant_field: str, unit: typing.Optional[str] = None) -> StageValueType:
        # noinspection PyArgumentList
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.variant_field = variant_field
        obj.unit = unit

        return obj

    HEATER1_TEMP = 0, 'vFloat32', 'degC'
    HEATER_RATE = 1, 'vFloat32', 'degC/min'
    HEATER_SETPOINT = 2, 'vFloat32', 'degC'
    HEATER1_POWER = 3, 'vFloat32', 'percent'
    HEATER1_LNP_SPEED = 4, 'vFloat32', 'percent'
    HEATER2_TEMP = 5, 'vFloat32', 'degC'
    # RESERVED1 = 6,
    # RESERVED2 = 7,
    HEATER2_POWER = 8, 'vFloat32', 'percent'
    HEATER2_LNP_SPEED = 9, 'vFloat32', 'percent'
    WATER_COOLING_TEMP = 10, 'vFloat32', 'degC'
    HUMIDITY_TEMP = 11, 'vFloat32', 'degC'
    VACUUM = 12, 'vFloat32'
    VACUUM_SETPOINT = 13, 'vFloat32'
    HUMIDITY = 14, 'vFloat32', 'percent'
    HUMIDITY_SETPOINT = 15, 'vFloat32', 'percent'
    MOTOR_POS_X = 16, 'vFloat32', 'um'
    MOTOR_VEL_X = 17, 'vFloat32', 'um/s'
    MOTOR_SETPOINT_X = 18, 'vFloat32', 'um'
    MOTOR_POS_Y = 19, 'vFloat32', 'um'
    MOTOR_VEL_Y = 20, 'vFloat32', 'um/s'
    MOTOR_SETPOINT_Y = 21, 'vFloat32', 'um'
    MOTOR_POS_Z = 22, 'vFloat32', 'um'
    MOTOR_VEL_Z = 23, 'vFloat32', 'um/s'
    MOTOR_SETPOINT_Z = 24, 'vFloat32', 'um'
    # MOTOR_DRIVEN_STAGE_STATUS = 25, 'vMDSStatus'
    VACUUM_BOARD_UNIT_OF_MEASURE = 26, 'vUint32'
    # VAC_MOTOR_VALVE_STATUS = 27, 'vMVStatus'
    VAC_MOTOR_VALVE_POS = 28, 'vFloat32', 'um'
    VAC_MOTOR_VALVE_VEL = 29, 'vFloat32', 'um/s'
    VAC_MOTOR_VALVE_SETPOINT = 30, 'vFloat32', 'um'
    GRADED_MOTOR_POS = 31, 'vFloat32', 'um'
    GRADED_MOTOR_VEL = 32, 'vFloat32', 'um/s'
    GRADED_MOTOR_DISTANCE_SETPOINT = 33, 'vFloat32', 'um'
    SAMPLE_REF1 = 34, 'vFloat32', 'degC'
    SAMPLE_ACT1 = 35, 'vFloat32', 'degC'
    SAMPLE_REF2 = 36, 'vFloat32', 'degC'
    SAMPLE_ACT2 = 37, 'vFloat32', 'degC'
    SAMPLE_REF3 = 38, 'vFloat32', 'degC'
    SAMPLE_ACT3 = 39, 'vFloat32', 'degC'
    SAMPLE_REF4 = 40, 'vFloat32', 'degC'
    SAMPLE_ACT4 = 41, 'vFloat32', 'degC'
    SAMPLE_REF5 = 42, 'vFloat32', 'degC'
    SAMPLE_ACT5 = 43, 'vFloat32', 'degC'
    HEATER3_TEMP = 44, 'vFloat32', 'degC'
    DSC = 45, 'vUint32'
    TRIGGER_SIGNAL_BLUE = 46, 'vFloat32'
    TRIGGER_SIGNAL_GREEN = 47, 'vFloat32'
    TRIGGER_SIGNAL_PINK = 48, 'vFloat32'
    TRIGGER_SIGNALS_ENABLED = 49, 'vBoolean'
    TEMPERATURE_RESOLUTION = 50, 'vUint32'
    HEATER4_TEMP = 51, 'vFloat32', 'degC'
    CMS_LIGHT = 52, 'vBoolean'
    CMS_WARMING_HEATER = 53, 'vBoolean'
    CMS_SOLENOID_REFILL = 54, 'vBoolean'
    CMS_SAMPLE_DEWAR_FILL_SIG = 55, 'vBoolean'
    # CMS_STATUS = 56, 'vCMSStatus'
    # CMS_ERROR = 57, 'vCMSError'
    RAMP_HOLD_TIME = 58, 'vFloat32', 's'
    RAMP_HOLD_REMAINING = 59, 'vFloat32', 's'
    CMS_MAIN_DEWAR_FILL_SIG = 60, 'vBoolean'
    CMS_CONDENSER_LED_LEVEL = 61, 'vUint16'
    # UNSUPPORTED TEST_MOTION = 62,
    # UNSUPPORTED MOTOR_FEEDBACK_Y_X = 63,
    TST_MOTOR_POS = 64, 'vFloat32', 'um'
    TST_MOTOR_VEL = 65, 'vFloat32', 'um/s'
    TST_MOTOR_DISTANCE_SETPOINT = 66, 'vFloat32', 'um'
    TST_FORCE = 67, 'vFloat32', 'N'
    TST_FORCE_SETPOINT = 68, 'vFloat32', 'N'
    TST_PID_KP = 69, 'vFloat32'
    TST_PID_KI = 70, 'vFloat32'
    TST_PID_KD = 71, 'vFloat32'
    TST_FORCE_GAUGE = 72, 'vFloat32', 'N'
    # CSS_MODE = 73, 'vCSSMode'
    CSS_GAP_SETPOINT = 74, 'vFloat32', 'um'
    CSS_GAP_POS = 75, 'vFloat32', 'um'
    CSS_STRAIN_SETPOINT = 76, 'vFloat32'
    CSS_RATE_SETPOINT = 77, 'vFloat32'
    CSS_OCS_FREQ = 78, 'vFloat32', 'Hz'
    CSS_DIRN = 79, 'vBoolean'
    CSS_JOG_ROT_VEL = 80, 'vFloat32'
    CSS_JOG_GAP_DIS = 81, 'vFloat32', 'um'
    CSS_DEFAULT_GAP_REF_VEL = 82, 'vFloat32', 'um'
    CSS_DEFAULT_ROT_REF_VEL = 83, 'vFloat32'
    CSS_STEP_DONE = 84, 'vBoolean'
    CSS_STEP_SUCCESS = 85, 'vBoolean'
    # CSS_STATUS = 86, 'vCSSStatus'
    CSS_FORCE = 87, 'vFloat32'
    CSS_SHARE_TIME = 88, 'vFloat32', 's'
    CSS_ROT_MOTOR_VELOCITY_SETPOINT = 89, 'vFloat32', 'um/s'
    CSS_GAP_MOTOR_VELOCITY_SETPOINT = 90, 'vFloat32', 'um/s'
    # NOT-COMPATIBLE CSS_OPTION_BOARD_SENSOR_DATA = 91,
    RS232_OPTION_BOARD_SENSOR_ENABLED = 92, 'vBoolean'
    # NOT-COMPATIBLE VACUUM_OPTION_BOARD_SENSOR1_DATA = 93,
    VACUUM_OPTION_BOARD_SENSOR1_ENABLED = 94, 'vBoolean'
    # NOT-COMPATIBLE VACUUM_OPTION_BOARD_SENSOR2_DATA = 95,
    VACUUM_OPTION_BOARD_SENSOR2_ENABLED = 96, 'vBoolean'
    VTO_OPTION_BOARD_ENABLED = 97, 'vBoolean'
    CMS_DEWAR_TOP_TEMPERATURE = 98, 'vFloat32', 'degC'
    CMS_AUTO_DEWAR_FILL = 99, 'vBoolean'
    DSC_POWER = 100, 'vFloat32'
    DSC_GAIN1 = 101, 'vFloat32'
    DSC_GAIN2 = 102, 'vFloat32'
    DSC_GAIN3 = 103, 'vFloat32'
    DSC_CONSTANT_TERM = 104, 'vFloat32'
    DSC_POWER_TERM1 = 105, 'vFloat32'
    DSC_POWER_TERM2 = 106, 'vFloat32'
    DSC_POWER_TERM3 = 107, 'vFloat32'
    DSC_POWER_TERM4 = 108, 'vFloat32'
    DSC_POWER_TERM5 = 109, 'vFloat32'
    DSC_POWER_TERM6 = 110, 'vFloat32'
    DSC_BASELINE_CONST_TERM = 111, 'vFloat32'
    DSC_BASELINE_POWER_TERM1 = 112, 'vFloat32'
    DSC_BASELINE_POWER_TERM2 = 113, 'vFloat32'
    DSC_BASELINE_POWER_TERM3 = 114, 'vFloat32'
    DSC_BASELINE_POWER_TERM4 = 115, 'vFloat32'
    DSC_TUA_CONST1 = 116, 'vFloat32'
    DSC_TUA_CONST2 = 117, 'vFloat32'
    DSC_OPTION_BOARD_SENSOR_ENABLED = 118, 'vBoolean'
    TST_JAW_TO_JAW_SIZE = 119, 'vFloat32', 'um'
    TST_TABLE_DIRECTION = 120, 'vBoolean'
    # TST_SAMPLE_SIZE = 121, 'vTSTSampleSize'
    TST_STRAIN_ENGINEERING_UNITS = 122, 'vBoolean'
    TST_STRAIN_PERCENTAGE = 123, 'vBoolean'
    TST_SHOW_AS_FORCE_DISTANCE = 124, 'vBoolean'
    TST_CAL_FORCE_VALUE = 125, 'vFloat32', 'N'
    TST_OPTION_BOARD_SENSOR_ENABLED = 126, 'vBoolean'
    TST_SHOW_CALB_DATA = 127, 'vBoolean'
    # TST_STATUS = 128, 'vTSTStatus'
    TST_JAW_POSITION = 129, 'vFloat32'
    TST_STRAIN = 130, 'vFloat32'
    TST_STRESS = 131, 'vFloat32'
    # TST_TABLE_MODE = 132, 'vTSTMode'
    STAGE_HUMIDITY_UNIT_DATA = 133, 'vPtr'
    PRESSURE = 134, 'vFloat32', 'mbar'
    MOTOR_X_OPTION_BOARD_SENSOR_ENABLED = 135, 'vBoolean'
    MOTOR_Y_OPTION_BOARD_SENSOR_ENABLED = 136, 'vBoolean'
    MOTOR_Z_OPTION_BOARD_SENSOR_ENABLED = 137, 'vBoolean'
    MOTOR_VACUUM_OPTION_BOARD_SENSOR_ENABLED = 138, 'vBoolean'
    MOTOR_F_D_VACUUM_OPTION_BOARD_SENSOR_ENABLED = 139, 'vBoolean'
    MOTOR_TST_OPTION_BOARD_SENSOR_ENABLED = 140, 'vBoolean'
    MOTOR_GRADIENT_OPTION_BOARD_SENSOR_ENABLED = 141, 'vBoolean'
    # NOT-COMPATIBLE MOTOR_X_OPTION_BOARD_SENSOR_DATA = 142,
    # NOT-COMPATIBLE MOTOR_Y_OPTION_BOARD_SENSOR_DATA = 143,
    # NOT-COMPATIBLE MOTOR_Z_OPTION_BOARD_SENSOR_DATA = 144,
    # NOT-COMPATIBLE MOTOR_VACUUM_OPTION_BOARD_SENSOR_DATA = 145,
    # NOT-COMPATIBLE MOTOR_F_D_VACUUM_OPTION_BOARD_SENSOR_DATA = 146,
    # NOT-COMPATIBLE MOTOR_TST_OPTION_BOARD_SENSOR_DATA = 147,
    # NOT-COMPATIBLE MOTOR_GRADIENT_OPTION_BOARD_SENSOR_DATA = 148,
    TTC_OPTION_BOARD_ENABLED = 149, 'vBoolean'
    TTC_OPTION_BOARD_SENSOR1_ENABLED = 150, 'vBoolean'
    TTC_OPTION_BOARD_SENSOR2_ENABLED = 151, 'vBoolean'
    TTC_OPTION_BOARD_SENSOR3_ENABLED = 152, 'vBoolean'
    DTC_OPTION_BOARD_SENSOR1_ENABLED = 153, 'vBoolean'
    DTC_OPTION_BOARD_SENSOR2_ENABLED = 154, 'vBoolean'
    MOTOR_X_DEFAULT_SPEED = 155, 'vFloat32'
    MOTOR_Y_DEFAULT_SPEED = 156, 'vFloat32'
    MOTOR_Z_DEFAULT_SPEED = 157, 'vFloat32'
    MOTOR_TST_DEFAULT_SPEED = 158, 'vFloat32'
    MOTOR_GS_DEFAULT_SPEED = 159, 'vFloat32'
    MOTOR_VAC_DEFAULT_SPEED = 160, 'vFloat32'
    MOTOR_FD_VAC_DEFAULT_SPEED = 161, 'vFloat32'
    HUMIDITY_DRYING_TIME_SETPOINT = 162, 'vInt32', 's'
    HUMIDITY_SWAP_TIME_SETPOINT = 163, 'vInt32', 's'
    HUMIDITY_PIPE_TEMP_SETPOINT = 164, 'vFloat32', 'degC'
    HUMIDITY_WATER_TEMP_SETPOINT = 165, 'vFloat32', 'degC'
    HUMIDITY_DRYING_TIME_LEFT = 166, 'vInt32', 's'
    HUMIDITY_SWAP_TIME_LEFT = 167, 'vInt32', 's'
    HUMIDITY_WATER_TEMP = 168, 'vFloat32', 'degC'
    VTO_VIDEO_STANDARD = 169, 'vUint32',
    TRIGGER_SIGNAL_PULSE_WIDTH = 170, 'vInt32', 's'
    CONNECTION_TYPE = 171, 'vCommsType'
    # DIFFERENT IN/OUT VACUUM_SIMULATOR_PLUG = 172,
    # DIFFERENT IN/OUT PRESSURE_SIMULATOR_PLUG = 173,
    LNP_SINGLE = 174, 'vBoolean'
    LNP_DUAL = 175, 'vBoolean'
    LNP95 = 176, 'vBoolean'
    LNP96 = 177, 'vBoolean'
    # XENCOS ONLY USING_XENOCS_STAGE_TEST_CABLES = 178,
    # XENCOS ONLY USING_XENOCS_STAGE_TEST_CABLE_TYPE1 = 179,
    # XENCOS ONLY USING_XENOCS_STAGE_TEST_CABLE_TYPE2 = 180,
    # LINKAM ONLY USING_CALIBRATION_PLUG = 181,
    # LINKAM ONLY USING_CALIBRATION_CABLE_B = 182,
    # LINKAM ONLY USING_CALIBRATION_CABLE_C = 183,
    # LINKAM ONLY USING_CALIBRATION_CABLE_A = 184,
    # VTO_TEXT = 185,
    # VTO_TIME = 186,
    # MOTOR_ZERO_REF_X = 187,
    # MOTOR_ZERO_REF_Y = 188,
    # CMS_XAXIS_GRID_CENTRE = 189,
    # CMS_YAXIS_GRID_CENTRE = 190,
    # CMS_LASH_WARNING = 191,
    # CMS_BASE_HEATER_LIMIT = 192,
    # CMS_ALARM_VOLUME = 193,
    MANUAL_HUMIDITY_SETPOINT = 194, 'vFloat32', 'percent'
    FDVS_COLD_TRAP_PUMP_SPEED = 195, 'vFloat32'
    # FDVS_SCAN_MOTOR_POSITION = 196,
    IMAGING_STATION_BRIGHTNESS = 197, 'vFloat32'
    # ENABLE_JOY_STICK = 198,
    # DISABLE_JOY_STICK = 199,
    # INVERT_JOY_STICK_AXIS_X = 200,
    # INVERT_JOY_STICK_AXIS_Y = 201,
    FDVS_MOTOR_VEL = 202, 'vFloat32', 'um/s'
    FDVS_MOTOR_DISTANCE_SETPOINT = 203, 'vFloat32', 'um'
    CSS_DEFAULT_GAP_CHANGE_VEL = 204, 'vFloat32', 'um/s'
    TST_GAUGE_COMPLIANCY = 205, 'vFloat32', 'mm'
    # TST_ENABLE_GAUGE_COMPLIANCY = 206,
    # TST_DISABLE_GAUGE_COMPLIANCY = 207,
    # TST_IS_GAUGE_COMPLIANCY_ENABLED = 208,
    # TST_MAX_EXTENT_POSITION = 209,
    # TST_MIN_EXTENT_POSITION = 210,
    # TST_RAW_MOTOR_POS = 211,
    # TST_ENABLE_JAW_MONITOR = 212,
    # TST_DISABLE_JAW_MONITOR = 213,
    # TST_IS_JAW_MONITOR_ENABLED = 214,
    # TST_CYCLE_COUNT_LIMIT = 215,
    # TST_CYCLES_REMAINING = 216,
    # MAX_VALUE = 65535


class Variant(ctypes.Union):
    _fields_ = [
        ('vChar', ctypes.c_char),
        ('vUint8', ctypes.c_uint8),
        ('vUint16', ctypes.c_uint),
        ('vUint32', ctypes.c_uint32),
        ('vUint64', ctypes.c_uint64),
        ('vInt8', ctypes.c_int8),
        ('vInt16', ctypes.c_int16),
        ('vInt32', ctypes.c_int32),
        ('vInt64', ctypes.c_int64),
        ('vFloat32', ctypes.c_float),
        ('vFloat64', ctypes.c_double),
        ('vPtr', ctypes.c_void_p),
        ('vBoolean', ctypes.c_bool),
        ('vControllerConfig', ControllerConfig),
        ('vControllerError', ctypes.c_uint),
        ('vControllerStatus', ControllerStatus),
        ('vConnectionStatus', ConnectionStatus),
        ('vStageValueType', ctypes.c_uint),
        # ('vStageCableConfig', None),
        ('vStageConfig', StageConfig),
        # ('vStageGroup', None),
        # ('vStageCableLimit', None),
        # ('vCSSStatus', None),
        # ('vCSSCheckCodes', None),
        # ('vCSSMode', None),
        # ('vCSSState', None),
        # ('vCMSStatus', None),
        # ('vCMSError', None),
        # ('vOptionBoardType', None),
        # ('vInstrumentBusDeviceType', None),
        # ('vControllerType', None),
        # ('vTSTStatus', None),
        # ('vTSTMode', None),
        # ('vTSTSampleSize', None),
        # ('vMVStatus', None),
        # ('vMDSStatus', None),
        ('vCommsType', ctypes.c_uint32)
    ]


CommsHandle = ctypes.c_uint64
