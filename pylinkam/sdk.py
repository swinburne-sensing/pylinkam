from __future__ import annotations

import ctypes
import logging
import os
import threading
import typing
from contextlib import contextmanager
from types import ModuleType

# Try and use pint for units if available
try:
    # noinspection PyPackageRequirements
    import pint
except ImportError:
    pint: typing.Optional[ModuleType] = None

from pylinkam import interface, util


_LOGGER = logging.getLogger(__name__)


# Locate SDK files and add to system path
SDK_PATH = os.path.dirname(os.path.abspath(__file__))
util.add_path(SDK_PATH)


class SDKError(Exception):
    pass


class ControllerConnectError(Exception):
    pass


class SDKWrapper:
    """ Wrapper for Linkam SDK. """

    # Assume SDK files are in the library root, can be overriden at instantiation
    _DEFAULT_SDK_ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

    _DEFAULT_BIN_NAME_LINUX = 'libLinkamSDK.so'

    # Strip the .dll suffix, this is re-added automatically
    _DEFAULT_BIN_NAME_WINDOWS = 'LinkamSDK'

    class Connection:
        """ Wrapper for connection to Linkam controller. """

        def __init__(self, parent: SDKWrapper, handle: interface.CommsHandle):
            """ Create a new connection object used to handle all messages to and from a controller.

            :param parent: handle to parent SDK wrapper
            :param handle: communication interface handle
            """
            self._parent = parent
            self._handle: typing.Optional[interface.CommsHandle] = handle

        def __del__(self) -> None:
            self.close()

        def close(self) -> None:
            """ Close communication channel.

            """
            if hasattr(self, '_handle') and self._handle is not None:
                self._parent.process_message(interface.Message.CLOSE_COMMS, comm_handle=self._handle)
                self._handle = None

        def enable_heater(self, enabled: bool) -> None:
            """ Enable/disable the temperature controller.

            :param enabled: if True start temperature controller, otherwise stop temperature controller
            """
            self._parent.process_message(
                interface.Message.START_HEATING,
                ('vBoolean', enabled),
                comm_handle=self._handle
            )

        def enable_humidity(self, enabled: bool) -> None:
            """ Enable/disable the humidity generator.

            :param enabled: if True start humidity generator, otherwise stop humidity generator
            """
            self._parent.process_message(
                interface.Message.START_HUMIDITY,
                ('vBoolean', enabled),
                comm_handle=self._handle
            )

        def get_controller_config(self) -> interface.ControllerConfig:
            """ Fetch controller configuration/metadata.

            :return: interface.ControllerConfig
            """
            return typing.cast(interface.ControllerConfig, self._parent.process_message(
                interface.Message.GET_CONTROLLER_CONFIG,
                comm_handle=self._handle
            ))

        def get_controller_firmware_version(self) -> str:
            """ Get controller firmware version.

            :return: str
            """
            return self._parent.process_message_str(
                interface.Message.GET_CONTROLLER_FIRMWARE_VERSION,
                64,
                self._handle
            )

        def get_controller_hardware_version(self) -> str:
            """ Get controller hardware version.

            :return: str
            """
            return self._parent.process_message_str(
                interface.Message.GET_CONTROLLER_HARDWARE_VERSION,
                64,
                self._handle
            )

        def get_controller_name(self) -> str:
            """ Get controller hardware version.

            :return: str
            """
            return self._parent.process_message_str(
                interface.Message.GET_CONTROLLER_NAME,
                26,
                self._handle
            )

        def get_controller_serial(self) -> str:
            """ Get controller serial number.

            :return: str
            """
            return self._parent.process_message_str(
                interface.Message.GET_CONTROLLER_SERIAL,
                18,
                self._handle
            )

        def get_heater_details(self, channel: int = 0) -> interface.HeaterDetails:
            """ Get temperature controller characteristics.

            :param channel: channel number for controllers with multiple temperature regulators
            :return: interface.HeaterDetails
            """
            detail = interface.HeaterDetails()

            self._parent.process_message(interface.Message.GET_CONTROLLER_HEATER_DETAILS,
                                         ('vPtr', detail),
                                         ('vUint32', channel + 1),
                                         comm_handle=self._handle)

            return detail

        def get_humidity_controller_sensor_name(self) -> str:
            """ Get humidity sensor name from humidity generator.

            :return: str
            """
            return self._parent.process_message_str(
                interface.Message.GET_HUMIDITY_CONTROLLER_SENSOR_NAME,
                26,
                self._handle
            )

        def get_humidity_controller_sensor_serial(self) -> str:
            """ Get humidity sensor serial number from humidity generator.

            :return: str
            """
            return self._parent.process_message_str(
                interface.Message.GET_HUMIDITY_CONTROLLER_SENSOR_SERIAL,
                18,
                self._handle
            )

        def get_humidity_controller_sensor_hardware_version(self) -> str:
            """ Get humidity sensor hardware version from humidity generator.

            :return: str
            """
            return self._parent.process_message_str(
                interface.Message.GET_HUMIDITY_CONTROLLER_SENSOR_HARDWARE_VERSION,
                7,
                self._handle
            )

        def get_humidity_details(self) -> interface.RHUnit:
            """ Get humidity generator characteristics.

            :return: interface.RHUnit
            """
            detail = interface.RHUnit()

            self._parent.process_message(
                interface.Message.GET_VALUE,
                ('vStageValueType', interface.StageValueType.STAGE_HUMIDITY_UNIT_DATA),
                ('vPtr', detail),
                comm_handle=self._handle
            )

            return detail

        def get_program_state(self) -> interface.Running:
            """ Get controller state.

            :return: interface.Running
            """
            state = interface.Running()

            self._parent.process_message(
                interface.Message.GET_PROGRAM_STATE,
                ('vUint32', 1),
                ('vPtr', state),
                comm_handle=self._handle
            )

            return state

        def get_stage_firmware_version(self) -> str:
            """ Get stage firmware version.

            :return: str
            """
            return self._parent.process_message_str(
                interface.Message.GET_STAGE_FIRMWARE_VERSION,
                64,
                self._handle
            )

        def get_stage_hardware_version(self) -> str:
            """ Get stage hardware version.

            :return: str
            """
            return self._parent.process_message_str(
                interface.Message.GET_STAGE_HARDWARE_VERSION,
                64,
                self._handle
            )

        def get_stage_name(self) -> str:
            """ Get stage name.

            :return: str
            """
            return self._parent.process_message_str(
                interface.Message.GET_STAGE_NAME,
                26,
                self._handle
            )

        def get_stage_serial(self) -> str:
            """ Get stage serial number.

            :return: str
            """
            return self._parent.process_message_str(
                interface.Message.GET_STAGE_SERIAL,
                18,
                self._handle
            )
            
        def get_status(self) -> interface.ControllerStatus:
            return typing.cast(interface.ControllerStatus, self._parent.process_message(
                interface.Message.GET_STATUS,
                comm_handle=self._handle
            ))

        def get_stage_config(self) -> interface.StageConfig:
            return typing.cast(interface.StageConfig, self._parent.process_message(
                interface.Message.GET_STAGE_CONFIG,
                comm_handle=self._handle
            ))

        def _get_value_msg(self, message: interface.Message, value_type: interface.StageValueType) -> typing.Any:
            value = self._parent.process_message(
                message,
                ('vStageValueType', value_type.value),
                comm_handle=self._handle
            )

            assert value_type.variant_field is not None

            # Get variant field
            value = getattr(value, value_type.variant_field)

            # If unit is available, then encapsulate it
            if pint is not None and value_type.unit is not None:
                return pint.Quantity(value, value_type.unit)

            return value

        def get_value(self, value_type: interface.StageValueType) -> typing.Any:
            """ Read parameter from Linkam controller/stage.

            :param value_type: parameter to read
            :return: various
            """
            return self._get_value_msg(interface.Message.GET_VALUE, value_type)

        def get_value_range(self, value_type: interface.StageValueType) -> typing.Tuple[typing.Any, typing.Any]:
            """ Read allowable range from Linkam controller/stage.

            :param value_type: parameter to read
            :return: tuple with 2 elements containing minimum and maximum, type varies
            """
            return self._get_value_msg(interface.Message.GET_MIN_VALUE, value_type),\
                self._get_value_msg(interface.Message.GET_MAX_VALUE, value_type)

        def set_value(self, value_type: interface.StageValueType, n: typing.Any) -> bool:
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

            assert value_type.variant_field is not None

            return bool(self._parent.process_message(
                interface.Message.SET_VALUE,
                ('vStageValueType', value_type.value),
                (value_type.variant_field, n),
                comm_handle=self._handle
            ))

    def __init__(self, sdk_root_path: typing.Optional[str] = None, sdk_bin_name: typing.Optional[str] = None,
                 sdk_log_path: typing.Optional[str] = None, sdk_license_path: typing.Optional[str] = None):
        """ Initialise the SDK, loading the required binary files.

        :param sdk_root_path: search path for SDK binary files, defaults to module directory
        :param sdk_bin_name: SDK binary name (on Windows remove .dll extension), defaults to platform-dependant name
        :param sdk_log_path: path for SDK logging, defaults to SDK directory
        :param sdk_license_path: path for SDL license file, defaults to SDK directory
        """
        self._sdk_root_path = sdk_root_path or self._DEFAULT_SDK_ROOT_PATH

        self._sdk: typing.Optional[ctypes.CDLL] = None
        self._sdk_lock = threading.RLock()

        # Setup DLL name and paths
        if sdk_bin_name is None:
            if os.name == 'nt':
                self._sdk_bin_name = self._DEFAULT_BIN_NAME_WINDOWS
            else:
                self._sdk_bin_name = self._DEFAULT_BIN_NAME_LINUX
        else:
            self._sdk_bin_name = sdk_bin_name

        self._sdk_log_path = sdk_log_path or os.path.join(self.sdk_root_path, 'Linkam.log')
        self._sdk_license_path = sdk_license_path or os.path.join(self.sdk_root_path, 'Linkam.lsk')

    def __del__(self) -> None:
        # Release SDK if connected
        self.close()

    def close(self) -> None:
        if hasattr(self, '_sdk') and self._sdk is not None:
            self._sdk.linkamExitSDK()
            _LOGGER.info(f"Cleaned up SDK")

        self._sdk = None

    @property
    def sdk(self) -> ctypes.CDLL:
        if self._sdk is None:
            if os.name == 'nt':
                loader: typing.Type[ctypes.CDLL] = ctypes.WinDLL
            else:
                loader = ctypes.CDLL

            try:
                sdk = loader(self.sdk_bin_name)
            except FileNotFoundError:
                # Re-attempt as an absolute path
                sdk = loader(os.path.join(self.sdk_root_path, self.sdk_bin_name))

            if sdk is None:
                raise SDKError('Linkam SDK was not loaded')

            # Provide type hints/restrictions
            sdk.linkamInitialiseSDK.argtypes = (ctypes.c_char_p, ctypes.c_char_p, ctypes.c_bool)
            sdk.linkamInitialiseSDK.restype = ctypes.c_bool

            sdk.linkamExitSDK.argtypes = ()
            sdk.linkamExitSDK.restype = None

            sdk.linkamInitialiseSerialCommsInfo.argtypes = (
                ctypes.POINTER(interface.CommsInfo), ctypes.c_char_p
            )
            sdk.linkamInitialiseSerialCommsInfo.restype = None

            sdk.linkamInitialiseUSBCommsInfo.argtypes = (
                ctypes.POINTER(interface.CommsInfo), ctypes.c_char_p
            )
            sdk.linkamInitialiseUSBCommsInfo.restype = None

            sdk.linkamGetVersion.argtypes = (
                ctypes.c_char_p, ctypes.c_uint64
            )
            sdk.linkamGetVersion.restype = ctypes.c_bool

            sdk.linkamProcessMessage.argtypes = (
                ctypes.c_int32, interface.CommsHandle, ctypes.POINTER(interface.Variant), interface.Variant,
                interface.Variant, interface.Variant
            )
            sdk.linkamProcessMessage.restype = ctypes.c_bool

            # Initialise SDK
            if not sdk.linkamInitialiseSDK(self.sdk_log_path.encode(), self.sdk_license_path.encode(), False):
                raise SDKError('Failed to initialize Linkam SDK')

            # Save handle
            with self._sdk_lock:
                self._sdk = sdk

            # Configure default logging
            self.set_logging_level(interface.LoggingLevel.MINIMAL)

            _LOGGER.info(f"Initialized Linkam SDK {self.get_version()}")

        return self._sdk

    @property
    def sdk_bin_name(self) -> str:
        return self._sdk_bin_name

    @property
    def sdk_license_path(self) -> str:
        return self._sdk_license_path

    @property
    def sdk_log_path(self) -> str:
        return self._sdk_log_path

    @property
    def sdk_root_path(self) -> str:
        return self._sdk_root_path

    def process_message(self, message: interface.Message, *args: typing.Tuple[str, typing.Any],
                        comm_handle: typing.Optional[interface.CommsHandle] = None) -> typing.Any:
        """ Process Linkam SDK message.

        :param message: message type to process
        :param args: arguments to pass to library (max 3), should be tuples that describe type
        :param comm_handle:
        :return:
        """
        # Cast arguments to variants
        variant_args = []

        if comm_handle is None:
            comm_handle = interface.CommsHandle(0)

        for arg_type, arg_value in args:
            var_arg = interface.Variant()

            # Cast pointers
            if arg_type == 'vPtr':
                arg_value = ctypes.cast(ctypes.pointer(arg_value), ctypes.c_void_p)

            setattr(var_arg, arg_type, arg_value)

            variant_args.append(var_arg)

        # Pad optional arguments
        for _ in range(3 - len(variant_args)):
            variant_args.append(interface.Variant())

        result = interface.Variant()

        with self._sdk_lock:
            try:
                self.sdk.linkamProcessMessage(
                    message.value,
                    comm_handle,
                    ctypes.pointer(result),
                    *variant_args
                )
            except OSError as exc:
                raise SDKError('Error occurred while accessing Linkam SDK library') from exc

        if message.variant_field is not None:
            return getattr(result, message.variant_field)

        return result

    def process_message_str(self, message: interface.Message, buffer_length: int,
                            comm_handle: typing.Optional[interface.CommsHandle] = None) -> str:
        """ Wrapped version of _sdk_process_message which includes string decoding.

        :param message: message type to process
        :param buffer_length: length of buffer to allocate for retrieval of string
        :param comm_handle:
        :return:
        """
        # Allocate buffer for return
        buffer = ctypes.create_string_buffer(buffer_length + 1)

        result = self.process_message(
            message,
            ('vPtr', buffer),
            ('vUint32', buffer_length),
            comm_handle=comm_handle
        )

        if type(result) is bool and not result:
            raise SDKError(f"Unable to read response to SDK message {message!s}")

        return buffer.value.decode().strip()

    def set_logging_level(self, level: interface.LoggingLevel) -> None:
        """ Set SDK logging level.

        :param level: integer logging level to use
        """
        if not self.process_message(interface.Message.ENABLE_LOGGING, ('vUint32', level.value)):
            raise SDKError('Unspecified error while configuring logging')

    def get_version(self) -> str:
        """ Get SDK version.

        :return: str
        """
        version_buffer = ctypes.create_string_buffer(256)

        with self._sdk_lock:
            if not self.sdk.linkamGetVersion(version_buffer, len(version_buffer)):
                raise SDKError('Unspecified error while getting Linkam SDK version')

        return version_buffer.value.decode()

    def _connect_common(self, comm_info: interface.CommsInfo) -> Connection:
        # Apparently this is ignored internally...
        comm_handle = interface.CommsHandle(0)

        with util.supress_stdout():
            connection_result = self.process_message(
                interface.Message.OPEN_COMMS,
                ('vPtr', comm_info),
                ('vPtr', comm_handle)
            )

        if not connection_result.flags.connected:
            if connection_result.flags.errorNoDeviceFound:
                raise ControllerConnectError('Device not found')
            elif connection_result.flags.errorMultipleDevicesFound:
                raise ControllerConnectError('Multiple devices found')
            elif connection_result.flags.errorTimeout:
                raise ControllerConnectError('Timeout')
            elif connection_result.flags.errorHandleRegistrationFailed:
                raise ControllerConnectError('Handle registration failed')
            elif connection_result.flags.errorAllocationFailed:
                raise ControllerConnectError('Allocation failed')
            elif connection_result.flags.errorSerialNumberRequired:
                raise ControllerConnectError('Serial number required')
            elif connection_result.flags.errorAlreadyOpen:
                raise ControllerConnectError('Already open')
            elif connection_result.flags.errorPropertiesIncorrect:
                raise ControllerConnectError('Properties incorrect')
            elif connection_result.flags.errorPortConfig:
                raise ControllerConnectError('Invalid port configuration')
            elif connection_result.flags.errorCommsStreams:
                raise ControllerConnectError('Communication error')
            elif connection_result.flags.errorUnhandled:
                raise ControllerConnectError('Unhandled error')

        return self.Connection(self, comm_handle)

    def _connect_serial(self, port: str) -> Connection:
        """ Use SDK to connect to an instrument over RS-232. Not tested.

        :param port: serial port name
        :return: Connection
        """
        # Configure serial connection
        comm_info = interface.CommsInfo()

        port_enc = ctypes.create_string_buffer(port.encode())
        self.sdk.linkamInitialiseSerialCommsInfo(ctypes.pointer(comm_info), port_enc)

        return self._connect_common(comm_info)

    def _connect_usb(self, serial_number: typing.Optional[str] = None) -> Connection:
        """ Use SDK to connect to an instrument over USB.

        :param serial_number: optional serial number of desired instrument
        :return: Connection
        """
        # Configure USB connection
        comm_info = interface.CommsInfo()

        if serial_number is not None:
            serial_number_enc = ctypes.create_string_buffer(serial_number.encode())
        else:
            serial_number_enc = None

        self.sdk.linkamInitialiseUSBCommsInfo(ctypes.pointer(comm_info), serial_number_enc)

        return self._connect_common(comm_info)

    @contextmanager
    def connect(self, *args, use_serial: bool = False, **kwargs) -> typing.Generator[Connection, None, None]:
        if use_serial:
            connection = self._connect_serial(*args, **kwargs)
        else:
            connection = self._connect_usb(*args, **kwargs)

        yield connection

        connection.close()

    def __enter__(self) -> SDKWrapper:
        # Initialise SDK
        _ = self.sdk

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Cleanup SDK
        self.close()
