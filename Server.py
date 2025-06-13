import datetime
import logging
import asyncio
import numpy
import sys
from Device import Device
import WorkStationSimulator
from asyncua import ua, Server
from WorkStation import WorkStation
from Measurement import Measurement
from asyncua.common.methods import uamethod
sys.path.insert(0, "..")


@uamethod
def reset_machine(parent, value):
    return value


@uamethod
def reset_drill(parent, value):
    return value


@uamethod
def reset_turntable(parent, value):
    return value


@uamethod
def reset_checker(parent, value):
    return value


@uamethod
def reset_ejector_A(parent, value):
    return value


@uamethod
def reset_ejector_B(parent, value):
    return value


def create_workstations():
    workstation = WorkStation("W1", "work_station")
    workstations["W1"] = workstation


def create_devices_and_measurements():

    # drill
    device = Device("D1", "drill")
    device.add_measurement(Measurement("M1", "drill_is_home_pos", "bool", False))
    device.add_measurement(Measurement("M2", "drill_is_drilling", "bool", False))
    device.add_measurement(Measurement("M3", "drill_lock", "bool", False))
    device.add_measurement(Measurement("M4", "heartbeat", "int", 0))
    workstations["W1"].add_device(device)

    # turn_table
    device = Device("D2", "turn_table")
    device.add_measurement(Measurement("M5", "piece_present_1", "bool", False))
    device.add_measurement(Measurement("M6", "piece_present_2_drill", "bool", False))
    device.add_measurement(Measurement("M7", "piece_present_3_checker", "bool", False))
    device.add_measurement(Measurement("M8", "turntable_pos", "int", 0))
    device.add_measurement(Measurement("M9", "heartbeat", "int", 0))
    workstations["W1"].add_device(device)

    # checker
    device = Device("D3", "checker")
    device.add_measurement(Measurement("M10", "checker_is_home_pos", "bool", False))
    device.add_measurement(Measurement("M11", "last_check_time", "DateTime", datetime.datetime.now()))
    device.add_measurement(Measurement("M12", "piece_OK", "bool", False))
    device.add_measurement(Measurement("M13", "heartbeat", "int", 0))
    workstations["W1"].add_device(device)

    # ejector_A
    device = Device("D4", "ejector_A")
    device.add_measurement(Measurement("M14", "ejector_A_is_home", "bool", False))
    device.add_measurement(Measurement("M15", "heartbeat", "int", 0))
    workstations["W1"].add_device(device)

    # ejector_B
    device = Device("D5", "ejector_B")
    device.add_measurement(Measurement("M16", "ejector_B_is_home", "bool", False))
    device.add_measurement(Measurement("M17", "heartbeat", "int", 0))
    workstations["W1"].add_device(device)


async def convert_data(val, val_type):
    if val_type == "bool":
        return True if val == "True" else False
    elif val_type == "DateTime":
        return datetime.datetime.strptime(val, "%Y-%m-%d %H:%M:%S.%f")
    elif val_type == "int":
        return int(val)


def get_type(val_type):
    if val_type == "bool":
        return ua.VariantType.Boolean
    elif val_type == "DateTime":
        return ua.VariantType.DateTime
    elif val_type == "int":
        return ua.VariantType.Int64


async def main():
    _logger = logging.getLogger('asyncua')
    # setup our server
    server = Server()
    await server.init()
    server.set_endpoint('opc.tcp://127.0.0.1:4840/freeopcua/server/')

    # setup our own namespace, not really necessary but should as spec
    uri = 'WorkStation'
    idx = await server.register_namespace(uri)

    # populating our address space
    # server.nodes, contains links to very common nodes like objects and root

    work_station = await server.nodes.objects.add_object(idx, 'WorkStation')

    drill = await work_station.add_object(idx, "drill")
    turn_table = await work_station.add_object(idx, "turn_table")
    checker = await work_station.add_object(idx, "checker")
    ejector_A = await work_station.add_object(idx, "ejector_A")
    ejector_B = await work_station.add_object(idx, "ejector_B")

    for ws in workstations.values():
        for dev in ws.devices.values():
            for mes in dev.measurements.values():
                if dev.iD == "D1":
                    temp = await drill.add_variable(idx, mes.tag, mes.value, get_type(mes.value_type))
                    await temp.set_writable()
                if dev.iD == "D2":
                    temp = await turn_table.add_variable(idx, mes.tag, mes.value,  get_type(mes.value_type))
                    await temp.set_writable()
                if dev.iD == "D3":
                    temp = await checker.add_variable(idx, mes.tag, mes.value,  get_type(mes.value_type))
                    await temp.set_writable()
                if dev.iD == "D4":
                    temp = await ejector_A.add_variable(idx, mes.tag, mes.value,  get_type(mes.value_type))
                    await temp.set_writable()
                if dev.iD == "D5":
                    temp = await ejector_B.add_variable(idx, mes.tag, mes.value,  get_type(mes.value_type))
                    await temp.set_writable()

    await work_station.add_method(ua.NodeId('ResetMachine', 1), ua.QualifiedName('ResetMachine', 1), reset_machine, [ua.VariantType.Int64], [ua.VariantType.Int64])
    await drill.add_method(ua.NodeId('ResetDrill', 1), ua.QualifiedName('ResetDrill', 1),
                                          reset_drill, [ua.VariantType.Int64], [ua.VariantType.Int64])
    await turn_table.add_method(ua.NodeId('ResetTurnTable', 1), ua.QualifiedName('ResetTurnTable', 1),
                           reset_turntable, [ua.VariantType.Int64], [ua.VariantType.Int64])
    await checker.add_method(ua.NodeId('ResetChecker', 1), ua.QualifiedName('ResetChecker', 1),
                           reset_checker, [ua.VariantType.Int64], [ua.VariantType.Int64])
    await ejector_A.add_method(ua.NodeId('ResetEjectorA', 1), ua.QualifiedName('ResetEjectorA', 1),
                           reset_ejector_A, [ua.VariantType.Int64], [ua.VariantType.Int64])
    await ejector_B.add_method(ua.NodeId('ResetEjectorB', 1), ua.QualifiedName('ResetEjectorB', 1),
                               reset_ejector_B, [ua.VariantType.Int64], [ua.VariantType.Int64])

    _logger.info('Starting server!')

    async with server:
        while True:
            await asyncio.sleep(5)

            for val in await WorkStationSimulator.get_sim_values():
                ids = val[0].split(":")
                workstations[ids[0]].devices[ids[1]].measurements[ids[2]].set_measurement(val[1])

            for ws in workstations.values():
                for dev in ws.devices.values():
                    for mes in dev.measurements.values():
                        if dev.iD == "D1":
                            x = await drill.get_child("2:"+mes.tag)
                        elif dev.iD == "D2":
                            x = await turn_table.get_child("2:" + mes.tag)
                        elif dev.iD == "D3":
                            x = await checker.get_child("2:" + mes.tag)
                        elif dev.iD == "D4":
                            x = await ejector_A.get_child("2:" + mes.tag)
                        elif dev.iD == "D5":
                            x = await ejector_B.get_child("2:" + mes.tag)
                        await x.write_value(await convert_data(workstations[ws.iD].devices[dev.iD].measurements[mes.iD].value, workstations[ws.iD].devices[dev.iD].measurements[mes.iD].value_type))


if __name__ == '__main__':
    workstations = {}
    create_workstations()
    create_devices_and_measurements()
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main(), debug=True)