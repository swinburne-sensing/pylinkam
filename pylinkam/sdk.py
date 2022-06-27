from __future__ import annotations

import logging
import os
import time
import threading

try:
    # Try and use pint for units if available
    import pint
except ImportError:
    pint = None

from pylinkam.interface import *
from pylinkam.util import add_path


_LOGGER = logging.getLogger(__name__)


# Locate SDK files and add to system path
SDK_PATH = os.path.dirname(os.path.abspath(__file__))
add_path(SDK_PATH)


class SDKError(Exception):
    pass


class SDKConnectionError(SDKError):
    pass


class SDKWrapper(object):
    """ Wrapper for Linkam SDK. """

    _DEFAULT_SDK_PATH = os.path.dirname(os.path.abspath(__file__))

    class Connection(object):
        """ Wrapper for connection to Linkam controller. """

        def __init__(self, parent: SDKWrapper, handle: CommsHandle):
            """

            :param parent:
            :param handle:
            """
            super().__init__()

            self._parent = parent
            self._handle: typing.Optional[CommsHandle] = handle

        def __del__(self):
            if hasattr(self, '_handle'):
                self.close()

        def close(self) -> None:
            """ Close communication channel.

            """
            if self._handle is not None:
                self._parent.process_message(Message.CLOSE_COMMS, comm_handle=self._handle)
                self._handle = None

        def enable_heater(self, enabled: bool) -> None:
            """ Enable/disable the temperature controller.

            :param enabled: if True start temperature controller, otherwise stop temperature controller
            """
            self._parent.process_message(Message.START_HEATING, ('vBoolean', enabled), comm_handle=self._handle)

        def enable_humidity(self, enabled: bool) -> None:
            """ Enable/disable the humidity generator.

            :param enabled: if True start humidity generator, otherwise stop humidity generator
            """
            self._parent.process_message(Message.START_HUMIDITY, ('vBoolean', enabled), comm_handle=self._handle)

        def get_controller_config(self) -> ControllerConfig:
            """ Fetch controller configuration/metadata.

            :return: ControllerConfig
            """
            return self._parent.process_message(Message.GET_CONTROLLER_CONFIG, comm_handle=self._handle)

        def get_controller_firmware_version(self) -> str:
            """ Get controller firmware version.

            :return: str
            """
            return self._parent.process_message_str(Message.GET_CONTROLLER_FIRMWARE_VERSION, 64, self._handle)

        def get_controller_hardware_version(self) -> str:
            """ Get controller hardware version.

            :return: str
            """
            return self._parent.process_message_str(Message.GET_CONTROLLER_HARDWARE_VERSION, 64, self._handle)

        def get_controller_name(self) -> str:
            """ Get controller hardware version.

            :return: str
            """
            return self._parent.process_message_str(Message.GET_CONTROLLER_NAME, 26, self._handle)

        def get_controller_serial(self) -> str:
            """ Get controller serial number.

            :return: str
            """
            return self._parent.process_message_str(Message.GET_CONTROLLER_SERIAL, 18, self._handle)

        def get_heater_details(self, channel: int = 0) -> HeaterDetails:
            """ Get temperature controller characteristics.

            :param channel: channel number for controllers with multiple temperature regulators
            :return: HeaterDetails
            """
            detail = HeaterDetails()

            self._parent.process_message(Message.GET_CONTROLLER_HEATER_DETAILS,
                                         ('vPtr', detail),
                                         ('vUint32', channel + 1),
                                         comm_handle=self._handle)

            return detail

        def get_humidity_controller_sensor_name(self) -> str:
            """ Get humidity sensor name from humidity generator.

            :return: str
            """
            return self._parent.process_message_str(Message.GET_HUMIDITY_CONTROLLER_SENSOR_NAME, 26, self._handle)

        def get_humidity_controller_sensor_serial(self) -> str:
            """ Get humidity sensor serial number from humidity generator.

            :return: str
            """
            return self._parent.process_message_str(Message.GET_HUMIDITY_CONTROLLER_SENSOR_SERIAL, 18,
                                                    self._handle)

        def get_humidity_controller_sensor_hardware_version(self) -> str:
            """ Get humidity sensor hardware version from humidity generator.

            :return: str
            """
            return self._parent.process_message_str(Message.GET_HUMIDITY_CONTROLLER_SENSOR_HARDWARE_VERSION, 7,
                                                    self._handle)

        def get_humidity_details(self) -> RHUnit:
            """ Get humidity generator characteristics.

            :return: RHUnit
            """
            detail = RHUnit()

            self._parent.process_message(Message.GET_VALUE,
                                         ('vStageValueType', StageValueType.STAGE_HUMIDITY_UNIT_DATA),
                                         ('vPtr', detail),
                                         comm_handle=self._handle)

            return detail

        def get_program_state(self) -> Running:
            """ Get controller state.

            :return: Running
            """
            state = Running()

            self._parent.process_message(Message.GET_PROGRAM_STATE,
                                         ('vUint32', 1),
                                         ('vPtr', state),
                                         comm_handle=self._handle)

            return state

        def get_stage_firmware_version(self) -> str:
            """ Get stage firmware version.

            :return: str
            """
            return self._parent.process_message_str(Message.GET_STAGE_FIRMWARE_VERSION, 64, self._handle)

        def get_stage_hardware_version(self) -> str:
            """ Get stage hardware version.

            :return: str
            """
            return self._parent.process_message_str(Message.GET_STAGE_HARDWARE_VERSION, 64, self._handle)

        def get_stage_name(self) -> str:
            """ Get stage name.

            :return: str
            """
            return self._parent.process_message_str(Message.GET_STAGE_NAME, 26, self._handle)

        def get_stage_serial(self) -> str:
            """ Get stage serial number.

            :return: str
            """
            return self._parent.process_message_str(Message.GET_STAGE_SERIAL, 18, self._handle)
            
        def get_status(self) -> ControllerStatus:
            return self._parent.process_message(Message.GET_STATUS, comm_handle=self._handle)

        def get_stage_config(self) -> StageConfig:
            return self._parent.process_message(Message.GET_STAGE_CONFIG, comm_handle=self._handle)

        def _get_value_msg(self, message: Message, value_type: StageValueType) -> typing.Any:
            value = self._parent.process_message(message, ('vStageValueType', value_type.value),
                                                 comm_handle=self._handle)

            # Get variant field
            value = getattr(value, value_type.variant_field)

            # If unit is available, then encapsulate it
            if pint is not None and value_type.unit is not None:
                return pint.Quantity(value, value_type.unit)

            return value

        def get_value(self, value_type: StageValueType) -> typing.Any:
            """ Read parameter from Linkam controller/stage.

            :param value_type: parameter to read
            :return: various
            """
            return self._get_value_msg(Message.GET_VALUE, value_type)

        def get_value_range(self, value_type: StageValueType) -> typing.Tuple[typing.Any, typing.Any]:
            """ Read allowable range from Linkam controller/stage.

            :param value_type: parameter to read
            :return: tuple with 2 elements containing minimum and maximum, type varies
            """
            return self._get_value_msg(Message.GET_MIN_VALUE, value_type), self._get_value_msg(Message.GET_MAX_VALUE,
                                                                                               value_type)

        def set_value(self, value_type: StageValueType, n: typing.Any) -> bool:
            """

            :param value_type:
            :param n:
            :return:
            """
            if pint is not None and isinstance(n, pint.Quantity):
                if value_type.unit is not None:
                    n = n.m_as(value_type.unit)
                else:
                    n = n.magnitude

            return self._parent.process_message(Message.SET_VALUE, ('vStageValueType', value_type.value),
                                                (value_type.variant_field, n),
                                                comm_handle=self._handle)

    def __init__(self, sdk_path: typing.Optional[str] = None, log_path: typing.Optional[str] = None,
                 license_path: typing.Optional[str] = None, debug: bool = False):
        """ Initialise the SDK, loading the required binary files.

        :param sdk_path: search path for SDK binary files, defaults to module directory
        :param log_path: path for SDK logging, defaults to SDK directory
        :param license_path: path for SDL license file, defaults to SDK directory
        :param debug: if True use DLL for debugging, else use release version
        """
        self._sdk_path = sdk_path or self._DEFAULT_SDK_PATH

        self._sdk = None
        self._sdk_lock = threading.RLock()

        super(SDKWrapper, self).__init__()

        # Locate DLL
        dll_name = f"LinkamSDK_{'debug' if debug else 'release'}.dll"

        if log_path is None:
            log_path = os.path.join(self._sdk_path, 'Linkam.log')

        self._log_path = log_path

        # Generate temporary license file if none is provided
        if license_path is None:
            license_path = os.path.join(self._sdk_path, 'Linkam.lsk')

        # This might be a little crazy, but the Linkam SDK crashes occasionally (maybe 1 out of every 100 loads) and
        # it looks like it's because the library attempts to open the license file before it's available. This delay
        # makes that less likely 🤷
        time.sleep(0.2)

        self._license_path = license_path

        # Load SDK DLL
        try:
            self._sdk = ctypes.WinDLL(dll_name)
        except FileNotFoundError:
            # Try absolute path
            self._sdk = ctypes.WinDLL(os.path.join(self._sdk_path, dll_name))

        # Provide type hints/restrictions
        self._sdk.linkamInitialiseSDK.argtypes = (ctypes.c_char_p, ctypes.c_char_p, ctypes.c_bool)
        self._sdk.linkamInitialiseSDK.restype = ctypes.c_bool

        self._sdk.linkamExitSDK.argtypes = ()
        self._sdk.linkamExitSDK.restype = None

        self._sdk.linkamInitialiseSerialCommsInfo.argtypes = (ctypes.POINTER(CommsInfo), ctypes.c_char_p)
        self._sdk.linkamInitialiseSerialCommsInfo.restype = None

        self._sdk.linkamInitialiseUSBCommsInfo.argtypes = (ctypes.POINTER(CommsInfo), ctypes.c_char_p)
        self._sdk.linkamInitialiseUSBCommsInfo.restype = None

        self._sdk.linkamGetVersion.argtypes = (ctypes.c_char_p, ctypes.c_uint64)
        self._sdk.linkamGetVersion.restype = ctypes.c_bool

        self._sdk.linkamProcessMessage.argtypes = (ctypes.c_int32, CommsHandle, ctypes.POINTER(Variant), Variant,
                                                   Variant, Variant)
        self._sdk.linkamProcessMessage.restype = ctypes.c_bool

        # Initialise SDK
        if not self._sdk.linkamInitialiseSDK(self._log_path.encode(), self._license_path.encode(), False):
            raise SDKError('Failed to initialize Linkam SDK')

        _LOGGER.info(f"Initialized Linkam SDK {self.get_version()}")

        # Configure default logging
        self.set_logging_level(LoggingLevel.MINIMAL)

    def __del__(self):
        # Release SDK
        if hasattr(self, '_sdk') and self._sdk is not None:
            self._sdk.linkamExitSDK()

        self._sdk = None

    def process_message(self, message: Message, *args: typing.Tuple[str, typing.Any],
                        comm_handle: typing.Optional[CommsHandle] = None) -> typing.Any:
        """ Process Linkam SDK message.

        :param message: message type to process
        :param args: arguments to pass to library (max 3), should be tuples that describe type
        :param comm_handle:
        :return:
        """
        # Cast arguments to variants
        variant_args = []

        if comm_handle is None:
            raise SDKConnectionError('Connection to Linkam instrument closed')

        for arg_type, arg_value in args:
            var_arg = Variant()

            # Cast pointers
            if arg_type == 'vPtr':
                arg_value = ctypes.cast(ctypes.pointer(arg_value), ctypes.c_void_p)

            setattr(var_arg, arg_type, arg_value)

            variant_args.append(var_arg)

        # Pad optional arguments
        for _ in range(3 - len(variant_args)):
            variant_args.append(Variant())

        result = Variant()

        with self._sdk_lock:
            try:
                self._sdk.linkamProcessMessage(message.value, comm_handle, ctypes.pointer(result), *variant_args)
            except OSError as exc:
                raise SDKError('Error occurred while accessing Linkam SDK library') from exc

        if message.variant_field is not None:
            return getattr(result, message.variant_field)

        return result

    def process_message_str(self, message: Message, buffer_length: int,
                            comm_handle: typing.Optional[CommsHandle] = None) -> str:
        """ Wrapped version of _sdk_process_message which includes string decoding.

        :param message: message type to process
        :param buffer_length: length of buffer to allocate for retrieval of string
        :param comm_handle:
        :return:
        """
        # Allocate buffer for return
        buffer = ctypes.create_string_buffer(buffer_length + 1)

        result = self.process_message(message, ('vPtr', buffer), ('vUint32', buffer_length),
                                      comm_handle=comm_handle)

        if type(result) is bool and not result:
            raise SDKError(f"Unable to read response to SDK message {message!s}")

        return buffer.value.decode().strip()

    def set_logging_level(self, level: LoggingLevel) -> None:
        """ Set SDK logging level.

        :param level: integer logging level to use
        """
        if not self.process_message(Message.ENABLE_LOGGING, ('vUint32', level.value)):
            raise SDKError('Cannot configure logging')

    def get_version(self) -> str:
        """ Get SDK version.

        :return: str
        """
        version_buffer = ctypes.create_string_buffer(256)

        with self._sdk_lock:
            if not self._sdk.linkamGetVersion(version_buffer, len(version_buffer)):
                raise SDKError('Failed to retrieve Linkam SDK version')

        return version_buffer.value.decode()

    def _connect_common(self, comm_info: CommsInfo) -> Connection:
        # Apparently this is ignored internally...
        comm_handle = CommsHandle(0)

        connection_result = self.process_message(Message.OPEN_COMMS, ('vPtr', comm_info), ('vPtr', comm_handle))

        if not connection_result.flags.connected:
            if connection_result.flags.errorNoDeviceFound:
                raise SDKConnectionError('Device not found')
            elif connection_result.flags.errorMultipleDevicesFound:
                raise SDKConnectionError('Multiple devices found')
            elif connection_result.flags.errorTimeout:
                raise SDKConnectionError('Timeout')
            elif connection_result.flags.errorHandleRegistrationFailed:
                raise SDKConnectionError('Handle registration failed')
            elif connection_result.flags.errorAllocationFailed:
                raise SDKConnectionError('Allocation failed')
            elif connection_result.flags.errorSerialNumberRequired:
                raise SDKConnectionError('Serial number required')
            elif connection_result.flags.errorAlreadyOpen:
                raise SDKConnectionError('Already open')
            elif connection_result.flags.errorPropertiesIncorrect:
                raise SDKConnectionError('Properties incorrect')
            elif connection_result.flags.errorPortConfig:
                raise SDKConnectionError('Invalid port configuration')
            elif connection_result.flags.errorCommsStreams:
                raise SDKConnectionError('Communication error')
            elif connection_result.flags.errorUnhandled:
                raise SDKConnectionError('Unhandled error')

        return self.Connection(self, comm_handle)

    def connect_serial(self, port: str) -> Connection:
        """ Use SDK to connect to an instrument over RS-232. Not tested.

        :param port: serial port name
        :return: Connection
        """
        # Configure serial connection
        comm_info = CommsInfo()

        port = ctypes.create_string_buffer(port.encode())
        self._sdk.linkamInitialiseSerialCommsInfo(ctypes.pointer(comm_info), port)

        return self._connect_common(comm_info)

    def connect_usb(self, serial_number: typing.Optional[str] = None) -> Connection:
        """ Use SDK to connect to an instrument over USB.

        :param serial_number: optional serial number of desired instrument
        :return: Connection
        """
        # Configure USB connection
        comm_info = CommsInfo()

        if serial_number is not None:
            serial_number = ctypes.create_string_buffer(serial_number.encode())

        self._sdk.linkamInitialiseUSBCommsInfo(ctypes.pointer(comm_info), serial_number)

        return self._connect_common(comm_info)
