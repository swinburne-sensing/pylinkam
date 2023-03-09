import logging
import time

from pylinkam import interface, sdk


logging.basicConfig(level=logging.DEBUG)


with sdk.SDKWrapper() as handle:
    with handle.connect() as connection:
        print(f"Name: {connection.get_controller_name()}")
        print(f"Heater measurement: {connection.get_value(interface.StageValueType.HEATER1_TEMP)}")
        print(f"Heater set-point before: {connection.get_value(interface.StageValueType.HEATER_SETPOINT)}")

        if not connection.set_value(interface.StageValueType.HEATER_SETPOINT, 25):
            raise Exception('Something broke')
        connection.enable_heater(True)

        print(f"Heater set-point after: {connection.get_value(interface.StageValueType.HEATER_SETPOINT)}")

        for _ in range(10):
            print(f"Heater measurement: {connection.get_value(interface.StageValueType.HEATER1_TEMP)}")
            time.sleep(1)

        connection.enable_heater(False)
