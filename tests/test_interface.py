# -*- coding: utf-8 -*-
import ctypes
import typing

import pytest

from pylinkam import interface

MIXIN_CLASSES = [
    obj for obj in vars(interface).values()
    if isinstance(obj, type)
    and issubclass(obj, interface._InterfaceMixin)
    and obj is not interface._InterfaceMixin
]


class TestMessage:
    def test_variant_fields_exist(self) -> None:
        variant_fields = {name for name, _ in interface.Variant._fields_}

        for message in interface.Message:
            if message.variant_field is not None:
                assert message.variant_field in variant_fields

    def test_known_values(self) -> None:
        assert interface.Message.OPEN_COMMS == 0x01
        assert interface.Message.OPEN_COMMS.variant_field == 'vConnectionStatus'
        assert interface.Message.GET_VALUE.variant_field is None

    def test_values_unique_except_documented_alias(self) -> None:
        values = [member.value for member in interface.Message.__members__.values()]
        duplicates = {value for value in values if values.count(value) > 1}

        # TST_SET_CALIBRATE_FORCE_PROGRAM_MODE and TST_SET_CALIBRATION_FORCE share an ID
        assert duplicates == {0x58}


class TestStageValueType:
    def test_variant_fields_exist(self) -> None:
        variant_fields = {name for name, _ in interface.Variant._fields_}

        for value_type in interface.StageValueType:
            assert value_type.variant_field in variant_fields

    def test_values_unique(self) -> None:
        values = [member.value for member in interface.StageValueType.__members__.values()]
        assert len(values) == len(set(values))

    def test_known_values(self) -> None:
        assert interface.StageValueType.HEATER1_TEMP == 0
        assert interface.StageValueType.HEATER1_TEMP.variant_field == 'vFloat32'
        assert interface.StageValueType.HEATER1_TEMP.unit == 'degC'
        assert interface.StageValueType.VACUUM.unit is None

    def test_units_parseable_by_pint(self) -> None:
        pint = pytest.importorskip('pint')

        for value_type in interface.StageValueType:
            if value_type.unit is not None:
                pint.Quantity(1.0, value_type.unit)


class TestStructLayout:
    """ Verify sizes of the ctypes structures/unions exchanged with the SDK binary. """

    def test_comms_info(self) -> None:
        assert ctypes.sizeof(interface.CommsInfoSerial) == 124
        assert ctypes.sizeof(interface.CommsInfoUSB) == 104
        assert ctypes.sizeof(interface.CommsInfoUnion) == 124
        assert ctypes.sizeof(interface.CommsInfo) == 128

    def test_flag_unions(self) -> None:
        assert ctypes.sizeof(interface.ConnectionStatus) == 4
        assert ctypes.sizeof(interface.ControllerConfig) == 8
        assert ctypes.sizeof(interface.ControllerProgramStatus) == 4
        assert ctypes.sizeof(interface.ControllerStatus) == 8
        assert ctypes.sizeof(interface.RHStatus) == 4
        assert ctypes.sizeof(interface.StageConfig) == 8

    def test_data_structures(self) -> None:
        assert ctypes.sizeof(interface.HeaterDetails) == 20
        assert ctypes.sizeof(interface.RHUnit) == 52
        assert ctypes.sizeof(interface.Running) == 40
        assert ctypes.sizeof(interface.Variant) == 8

    def test_comms_handle(self) -> None:
        assert interface.CommsHandle is ctypes.c_uint64


class TestInterfaceMixin:
    @pytest.mark.parametrize('cls', MIXIN_CLASSES, ids=lambda c: c.__name__)
    def test_to_mapping_all_structures(self, cls: type) -> None:
        # Regression test: unions without a flags member (e.g. CommsInfoUnion) raised AttributeError
        mapping = cls().to_mapping()

        assert isinstance(mapping, typing.Mapping)
        assert all(isinstance(key, str) for key in mapping)

    @pytest.mark.parametrize('cls', MIXIN_CLASSES, ids=lambda c: c.__name__)
    def test_repr_all_structures(self, cls: type) -> None:
        text = repr(cls())

        assert text.startswith(f'<{cls.__name__}(')
        assert text.endswith(')>')

    def test_to_mapping_strips_unused_and_padding(self) -> None:
        status = interface.ConnectionStatus()
        status.flags.connected = 1

        mapping = status.to_mapping()

        assert mapping['connected'] is True
        assert 'unused12' not in mapping
        assert len(mapping) == 12

    def test_to_mapping_keeps_unused_when_requested(self) -> None:
        mapping = interface.ConnectionStatus().to_mapping(strip_unused=False)

        assert len(mapping) == 32
        assert 'unused31' in mapping

    def test_to_mapping_casts_bitfields_to_bool(self) -> None:
        config = interface.ControllerConfig()
        config.flags.supportsHeater = 1

        mapping = config.to_mapping()

        assert mapping['supportsHeater'] is True
        assert mapping['vacuumOption'] is False

    def test_to_mapping_nested_structures(self) -> None:
        mapping = interface.CommsInfo().to_mapping()

        assert 'type' in mapping
        assert 'info' in mapping
