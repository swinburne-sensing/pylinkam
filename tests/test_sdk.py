# -*- coding: utf-8 -*-
import ctypes
import os
import typing

import pytest

from pylinkam import interface, sdk

MessageHandler = typing.Callable[
    [int, interface.CommsHandle, typing.Any, typing.Tuple[interface.Variant, ...]],
    bool
]


class FakeSDK:
    """ Stand-in for the Linkam SDK binary, records calls and delegates responses to a handler. """

    def __init__(self, handler: typing.Optional[MessageHandler] = None):
        self.calls = []
        self.handler = handler
        self.exit_called = False

    def linkamProcessMessage(self, message: int, comm_handle: interface.CommsHandle,
                             result: typing.Any, *args: interface.Variant) -> bool:
        self.calls.append((message, comm_handle, result, args))

        if self.handler is not None:
            return self.handler(message, comm_handle, result, args)

        return True

    def linkamInitialiseSerialCommsInfo(self, comm_info: typing.Any, port: typing.Any) -> None:
        pass

    def linkamInitialiseUSBCommsInfo(self, comm_info: typing.Any, serial_number: typing.Any) -> None:
        pass

    def linkamExitSDK(self) -> None:
        self.exit_called = True


def boolean_handler(value: bool) -> MessageHandler:
    """ Build a handler that returns the given value in the vBoolean result field. """
    def handler(message: int, comm_handle: interface.CommsHandle,
                result: typing.Any, args: typing.Tuple[interface.Variant, ...]) -> bool:
        result.contents.vBoolean = value

        return True

    return handler


def connected_handler(message: int, comm_handle: interface.CommsHandle,
                      result: typing.Any, args: typing.Tuple[interface.Variant, ...]) -> bool:
    """ Handler that reports a successful connection for OPEN_COMMS messages. """
    if message == interface.Message.OPEN_COMMS:
        result.contents.vConnectionStatus.flags.connected = 1

    return True


def make_wrapper(handler: typing.Optional[MessageHandler] = None) -> sdk.SDKWrapper:
    """ Create an SDKWrapper with a fake SDK binary, bypassing the library load. """
    wrapper = sdk.SDKWrapper()
    wrapper._sdk = FakeSDK(handler)

    return wrapper


def make_connection(wrapper: sdk.SDKWrapper) -> sdk.SDKWrapper.Connection:
    return sdk.SDKWrapper.Connection(wrapper, interface.CommsHandle(1))


class TestExceptions:
    def test_sdk_error(self) -> None:
        assert issubclass(sdk.SDKError, Exception)

    def test_controller_connect_error(self) -> None:
        assert issubclass(sdk.ControllerConnectError, Exception)


class TestInit:
    def test_defaults(self) -> None:
        wrapper = sdk.SDKWrapper()

        assert wrapper.sdk_root_path == sdk.SDKWrapper._DEFAULT_SDK_ROOT_PATH

        if os.name == 'nt':
            assert wrapper.sdk_bin_name == 'LinkamSDK'
        else:
            assert wrapper.sdk_bin_name == 'libLinkamSDK.so'

        assert wrapper.sdk_log_path == os.path.join(wrapper.sdk_root_path, 'Linkam.log')
        assert wrapper.sdk_license_path == os.path.join(wrapper.sdk_root_path, 'Linkam.lsk')

    def test_custom(self) -> None:
        wrapper = sdk.SDKWrapper(sdk_root_path='root', sdk_bin_name='bin',
                                 sdk_log_path='log', sdk_license_path='lic')

        assert wrapper.sdk_root_path == 'root'
        assert wrapper.sdk_bin_name == 'bin'
        assert wrapper.sdk_log_path == 'log'
        assert wrapper.sdk_license_path == 'lic'


class TestProcessMessage:
    def test_argument_packing(self) -> None:
        wrapper = make_wrapper()

        wrapper.process_message(
            interface.Message.SET_VALUE,
            ('vStageValueType', interface.StageValueType.HEATER_SETPOINT.value),
            ('vFloat32', 30.0)
        )

        message, comm_handle, _, args = wrapper._sdk.calls[0]

        assert message == interface.Message.SET_VALUE
        assert comm_handle.value == 0

        # Arguments are padded out to 3 variants
        assert len(args) == 3
        assert all(isinstance(arg, interface.Variant) for arg in args)

        assert args[0].vStageValueType == interface.StageValueType.HEATER_SETPOINT.value
        assert args[1].vFloat32 == pytest.approx(30.0)

    def test_pointer_argument_packing(self) -> None:
        wrapper = make_wrapper()

        detail = interface.HeaterDetails()
        wrapper.process_message(interface.Message.GET_CONTROLLER_HEATER_DETAILS, ('vPtr', detail))

        args = wrapper._sdk.calls[0][3]

        assert args[0].vPtr == ctypes.addressof(detail)

    def test_result_extraction(self) -> None:
        wrapper = make_wrapper(boolean_handler(True))

        # SET_VALUE defines vBoolean as its result field
        assert wrapper.process_message(interface.Message.SET_VALUE) is True

    def test_result_variant_returned_when_no_field(self) -> None:
        wrapper = make_wrapper()

        # GET_VALUE defines no result field, so the whole Variant is returned
        assert isinstance(wrapper.process_message(interface.Message.GET_VALUE), interface.Variant)

    def test_oserror_raises_sdk_error(self) -> None:
        def handler(*_: typing.Any) -> bool:
            raise OSError('boom')

        wrapper = make_wrapper(handler)

        with pytest.raises(sdk.SDKError):
            wrapper.process_message(interface.Message.GET_VALUE)


class TestProcessMessageStr:
    def test_string_decoding(self) -> None:
        def handler(message: int, comm_handle: interface.CommsHandle,
                    result: typing.Any, args: typing.Tuple[interface.Variant, ...]) -> bool:
            ctypes.memmove(args[0].vPtr, b'  T96-controller\x00', 17)

            return True

        wrapper = make_wrapper(handler)

        assert wrapper.process_message_str(interface.Message.GET_CONTROLLER_NAME, 26) == 'T96-controller'

    def test_failure_raises_sdk_error(self) -> None:
        wrapper = make_wrapper(boolean_handler(False))

        # GET_HUMIDITY_CONTROLLER_SENSOR_NAME defines vBoolean as its result field
        with pytest.raises(sdk.SDKError):
            wrapper.process_message_str(interface.Message.GET_HUMIDITY_CONTROLLER_SENSOR_NAME, 26)


class TestLogging:
    def test_set_logging_level(self) -> None:
        wrapper = make_wrapper(boolean_handler(True))

        wrapper.set_logging_level(interface.LoggingLevel.VERBOSE)

        args = wrapper._sdk.calls[0][3]
        assert args[0].vUint32 == interface.LoggingLevel.VERBOSE

    def test_set_logging_level_failure(self) -> None:
        wrapper = make_wrapper(boolean_handler(False))

        with pytest.raises(sdk.SDKError):
            wrapper.set_logging_level(interface.LoggingLevel.VERBOSE)


class TestConnection:
    def test_get_value_without_unit(self) -> None:
        def handler(message: int, comm_handle: interface.CommsHandle,
                    result: typing.Any, args: typing.Tuple[interface.Variant, ...]) -> bool:
            result.contents.vFloat32 = 3.3

            return True

        connection = make_connection(make_wrapper(handler))

        assert connection.get_value(interface.StageValueType.TRIGGER_SIGNAL_BLUE) == pytest.approx(3.3)

    def test_get_value_with_unit(self) -> None:
        pint = pytest.importorskip('pint')

        def handler(message: int, comm_handle: interface.CommsHandle,
                    result: typing.Any, args: typing.Tuple[interface.Variant, ...]) -> bool:
            result.contents.vFloat32 = 25.0

            return True

        connection = make_connection(make_wrapper(handler))
        value = connection.get_value(interface.StageValueType.HEATER1_TEMP)

        assert isinstance(value, pint.Quantity)
        assert value.m_as('degC') == pytest.approx(25.0)

    def test_get_value_range(self) -> None:
        def handler(message: int, comm_handle: interface.CommsHandle,
                    result: typing.Any, args: typing.Tuple[interface.Variant, ...]) -> bool:
            result.contents.vFloat32 = 1.0 if message == interface.Message.GET_MIN_VALUE else 10.0

            return True

        connection = make_connection(make_wrapper(handler))
        value_min, value_max = connection.get_value_range(interface.StageValueType.VACUUM)

        assert value_min == pytest.approx(1.0)
        assert value_max == pytest.approx(10.0)

    def test_set_value(self) -> None:
        wrapper = make_wrapper(boolean_handler(True))
        connection = make_connection(wrapper)

        assert connection.set_value(interface.StageValueType.HEATER_SETPOINT, 30.0) is True

        args = wrapper._sdk.calls[0][3]
        assert args[0].vStageValueType == interface.StageValueType.HEATER_SETPOINT.value
        assert args[1].vFloat32 == pytest.approx(30.0)

    def test_set_value_pint_conversion(self) -> None:
        pint = pytest.importorskip('pint')

        wrapper = make_wrapper(boolean_handler(True))
        connection = make_connection(wrapper)

        # 86 degF == 30 degC, value should be converted to the parameter's unit
        assert connection.set_value(interface.StageValueType.HEATER_SETPOINT, pint.Quantity(86, 'degF'))

        args = wrapper._sdk.calls[0][3]
        assert args[1].vFloat32 == pytest.approx(30.0)

    def test_close(self) -> None:
        wrapper = make_wrapper()
        connection = make_connection(wrapper)

        connection.close()
        connection.close()  # Closing twice must be a no-op

        assert len(wrapper._sdk.calls) == 1

        message, comm_handle, _, _ = wrapper._sdk.calls[0]
        assert message == interface.Message.CLOSE_COMMS
        assert comm_handle.value == 1


class TestConnect:
    def test_connect_usb_context_manager(self) -> None:
        wrapper = make_wrapper(connected_handler)

        with wrapper.connect() as connection:
            assert isinstance(connection, sdk.SDKWrapper.Connection)

        messages = [call[0] for call in wrapper._sdk.calls]

        assert interface.Message.OPEN_COMMS in messages
        assert interface.Message.CLOSE_COMMS in messages

    def test_connect_serial_context_manager(self) -> None:
        wrapper = make_wrapper(connected_handler)

        with wrapper.connect('COM3', use_serial=True) as connection:
            assert isinstance(connection, sdk.SDKWrapper.Connection)

    def test_connect_error_no_device(self) -> None:
        def handler(message: int, comm_handle: interface.CommsHandle,
                    result: typing.Any, args: typing.Tuple[interface.Variant, ...]) -> bool:
            result.contents.vConnectionStatus.flags.errorNoDeviceFound = 1

            return True

        wrapper = make_wrapper(handler)

        with pytest.raises(sdk.ControllerConnectError, match='Device not found'):
            wrapper.connect_usb()
