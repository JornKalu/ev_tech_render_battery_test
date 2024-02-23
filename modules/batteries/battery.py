from typing import Any
from database.model import get_single_battery_by_code, update_battery, create_request_log, get_single_battery_by_id, get_single_station_battery_by_id, get_single_mobility_device_by_id, update_station_battery, get_last_battery_transaction, get_single_mobility_device_by_id, get_open_station_slot, get_single_station_by_id, update_request_log, create_battery_log, update_battery_log, get_single_battery_log_by_id, get_single_last_battery_log_by_id, create_battery, get_single_battery_type_by_code
from sqlalchemy.orm import Session
from fastapi_pagination.ext.sqlalchemy import paginate
from modules.utils.tools import json_loader, check_if_date_as_pass_now, get_response_datetime_format
from settings.constants import BATTERY_STATUS
import json

def process_last_battery_instruction_count(db: Session, battery_id: int=0):
    battery_log = get_single_last_battery_log_by_id(db=db, battery_id=battery_id)
    if battery_log is None:
        battery_log = create_battery_log(db=db, battery_id=battery_id, instruction_count=1, status=0)
        return 1
    else:
        if check_if_date_as_pass_now(date_str=battery_log.created_at) == True:
            create_battery_log(db=db, battery_id=battery_id, instruction_count=1, status=0)
            update_battery_log(db=db, id=battery_log.id, values={'status': 1})
            return 1
        else:
            instruction_count = int(battery_log.instruction_count) + 1
            update_battery_log(db=db, id=battery_log.id, values={'instruction_count': instruction_count, 'status': 0})
            return int(instruction_count)

def generate_response_code(host_id: str=None, instruction_code: int=0, status: int=0):
    if host_id is None:
        host_id = '0000000'
    new_instruction_code = str(instruction_code).zfill(2)
    time = get_response_datetime_format()
    status_char = ""
    if status == 1:
        status_char = "S"
    elif status == 2:
        status_char = "A"
    elif status == 3:
        status_char = "B"
    elif status == 4:
        status_char = "C"
    elif status == 5:
        status_char = "D"
    elif status == 6:
        status_char = "E"
    elif status == 7:
        status_char = "H"
    else:
        status_char = "F"
    return "B" + str(host_id) + new_instruction_code + time + status_char

def generate_response_code_new(battery_status: int=None, status: int=None):
    response_code = ""
    status_char = ""
    if status == 1:
        status_char = "S"
    elif status == 2:
        status_char = "A"
    elif status == 3:
        status_char = "B"
    elif status == 4:
        status_char = "C"
    elif status == 5:
        status_char = "D"
    elif status == 6:
        status_char = "E"
    elif status == 7:
        status_char = "H"
    else:
        status_char = "F"
    if battery_status == 2:
        response_code = "2222"
    elif response_code == 4:
        response_code = "1111"
    else:
        response_code = "0000"
    return response_code + status_char

def process_battery_request_string(xtring: str=None):
    if xtring is None:
        return []
    else:
        xlist = xtring.split(",")
        return xlist

# def process_battery_request(db: Session, data: Any, ip_address: str=None):
#     req = create_request_log(db=db, server_type="battery", ip_address=ip_address, name="post", value=str(data))
#     if isinstance(data, bytes) == False:
#         # fin_data = {
#         #     's': 0,
#         #     'h': 0,
#         #     'sh': 0,
#         # }
#         fin_data = "BMA12D9C01230905163155"
#         update_request_log(db=db, id=req.id, values={'response_value': json.dumps(fin_data)})
#         return fin_data
#     else:
#         data = data.decode()
#         jdata = json_loader(jstr=data)
#         if jdata is None:
#             # fin_data = {
#             #     's': 0,
#             #     'h': 0,
#             #     'sh': 0,
#             # }
#             fin_data = "BMA12D9C01230905163155"
#             update_request_log(db=db, id=req.id, values={'response_value': json.dumps(fin_data)})
#             return fin_data
#         else:
#             if type(jdata) is not dict:
#                 # fin_data = {
#                 #     's': 0,
#                 #     'h': 0,
#                 #     'sh': 0,
#                 # }
#                 fin_data = "BMA12D9C01230905163155"
#                 update_request_log(db=db, id=req.id, values={'response_value': json.dumps(fin_data)})
#                 return fin_data
#             else:
#                 jlist = list(jdata.keys())
#                 clist = ['t', 'c', 'v', 'bID', 'SOC', 's', 'LT', 'LG']
#                 check =  all(item in jlist for item in clist)
#                 if check is False:
#                     # fin_data = {
#                     #     's': 0,
#                     #     'h': 0,
#                     #     'sh': 0,
#                     # }
#                     fin_data = "BMA12D9C01230905163155"
#                     update_request_log(db=db, id=req.id, values={'response_value': json.dumps(fin_data)})
#                     return fin_data
#                 else:
#                     battery = get_single_battery_by_code(db=db, code=str(jdata['bID']))
#                     if battery is None:
#                         # fin_data = {
#                         #     's': 0,
#                         #     'h': 0,
#                         #     'sh': 0,
#                         # }
#                         fin_data = "BMA12D9C01230905163155"
#                         update_request_log(db=db, id=req.id, values={'response_value': json.dumps(fin_data)})
#                         return fin_data
#                     else:
#                         values = {
#                             'voltage': jdata['v'],
#                             'temperature': jdata['t'],
#                             'charge': jdata['SOC'],
#                             'electric_current': jdata['c'],
#                             'latitude': jdata['LT'],
#                             'longitude': jdata['LG'],
#                         }
#                         b_status = jdata['s']
#                         is_shutdown = 0
#                         is_hotlisted = 0
#                         if battery.status == 2:
#                             is_shutdown = 1
#                         elif battery.status == 4:
#                             is_hotlisted = 1
#                         else:
#                             values['status'] = jdata['s']
#                         update_battery(db=db, id=battery.id, values=values)
#                         # fin_data = {
#                         #     's': 1,
#                         #     'h': is_hotlisted,
#                         #     'sh': is_shutdown,
#                         # }
#                         fin_data = "BMA12D9C01230905163155"
#                         update_request_log(db=db, id=req.id, values={'response_value': json.dumps(fin_data)})
#                         return fin_data

def process_battery_request(db: Session, data: Any, ip_address: str=None):
    req = create_request_log(db=db, server_type="battery", ip_address=ip_address, name="post", value=str(data))
    if isinstance(data, bytes) == False:
        # fin_data = {
        #     's': 0,
        #     'h': 0,
        #     'sh': 0,
        # }
        fin_data = generate_response_code(instruction_code=BATTERY_STATUS['default'], status=0)
        update_request_log(db=db, id=req.id, values={'response_value': json.dumps(fin_data)})
        return fin_data
    else:
        data = data.decode()
        jdata = json_loader(jstr=data)
        if jdata is None:
            # fin_data = {
            #     's': 0,
            #     'h': 0,
            #     'sh': 0,
            # }
            fin_data = generate_response_code(instruction_code=BATTERY_STATUS['default'], status=2)
            update_request_log(db=db, id=req.id, values={'response_value': json.dumps(fin_data)})
            return fin_data
        else:
            if type(jdata) is not dict:
                # fin_data = {
                #     's': 0,
                #     'h': 0,
                #     'sh': 0,
                # }
                fin_data = generate_response_code(instruction_code=BATTERY_STATUS['default'], status=3)
                update_request_log(db=db, id=req.id, values={'response_value': json.dumps(fin_data)})
                return fin_data
            else:
                jlist = list(jdata.keys())
                clist = ['t', 'c', 'v', 'bID', 'SOC', 's', 'LT', 'LG', 'cs', 'ds', 'd']
                check =  all(item in jlist for item in clist)
                if check is False:
                    # fin_data = {
                    #     's': 0,
                    #     'h': 0,
                    #     'sh': 0,
                    # }
                    fin_data = generate_response_code(instruction_code=BATTERY_STATUS['default'], status=4)
                    update_request_log(db=db, id=req.id, values={'response_value': json.dumps(fin_data)})
                    return fin_data
                else:
                    battery = get_single_battery_by_code(db=db, code=str(jdata['bID']))
                    if battery is None:
                        code = jdata['bID']
                        if code is None or code == '':
                            fin_data = generate_response_code(instruction_code=BATTERY_STATUS['default'], status=5)
                            update_request_log(db=db, id=req.id, values={'response_value': json.dumps(fin_data)})
                            return fin_data
                        else:
                            battery_type_code = code[0]
                            battery_type = get_single_battery_type_by_code(db=db, code=battery_type_code)
                            if battery_type is None:
                                fin_data = generate_response_code(instruction_code=BATTERY_STATUS['default'], status=6)
                                update_request_log(db=db, id=req.id, values={'response_value': json.dumps(fin_data)})
                                return fin_data
                            else:
                                battery = create_battery(db=db, type_id=battery_type.id, code=code, voltage=jdata['v'], temperature=jdata['t'], charge=jdata['SOC'], electric_current=jdata['c'], latitude=jdata['LT'], longitude=jdata['LG'])
                                fin_data = generate_response_code(instruction_code=BATTERY_STATUS['default'], status=1)
                                update_request_log(db=db, id=req.id, values={'response_value': json.dumps(fin_data)})
                                return fin_data
                    else:
                        lt_int = float(jdata['LT'])
                        lg_int = float(jdata['LG'])
                        values = {
                            'voltage': jdata['v'],
                            'temperature': jdata['t'],
                            'charge': jdata['SOC'],
                            'electric_current': jdata['c'],
                            # 'latitude': jdata['LT'],
                            # 'longitude': jdata['LG'],
                        }
                        if lt_int > 0:
                            values['latitude'] = jdata['LT']
                        if lg_int > 0:
                            values['longitude'] = jdata['LG']
                        b_status = BATTERY_STATUS['default']
                        charge_status = jdata['cs']
                        discharge_status = jdata['ds']
                        dock_status = jdata['d']
                        instruction_code = b_status
                        host_id = battery.temp_host
                        temp_status = battery.temp_status
                        batt_status = battery.status
                        if host_id is not None:
                            values['temp_host'] = None
                        if dock_status == 1:
                            if temp_status is not None:
                                if temp_status == 3:
                                    b_status = BATTERY_STATUS['enable_charge']
                                    values['temp_status'] = None
                                    values['status'] = 3
                                elif temp_status == 1:
                                    b_status = BATTERY_STATUS['enable_discharge']
                                    values['temp_status'] = None
                                    values['status'] = 1
                        if temp_status is not None:
                            if temp_status == 4:
                                b_status = BATTERY_STATUS['disable_battery']
                            elif temp_status == 1:
                                b_status = BATTERY_STATUS['enable_battery']
                            values['temp_status'] = None
                            values['status'] = temp_status
                        if charge_status == 1 and batt_status != 3:
                            values['status'] = 3
                        if discharge_status == 1 and batt_status != 1:
                            values['status'] = 1
                        update_battery(db=db, id=battery.id, values=values)
                        fin_data = generate_response_code(host_id=host_id, instruction_code=instruction_code, status=b_status)
                        update_request_log(db=db, id=req.id, values={'response_value': json.dumps(fin_data)})
                        return fin_data

def process_battery_request_main(db: Session, data: Any, ip_address: str=None):
    req = create_request_log(db=db, server_type="battery", ip_address=ip_address, name="post", value=str(data))
    if isinstance(data, bytes) == False:
        fin_data = generate_response_code_new()
        update_request_log(db=db, id=req.id, values={'response_value': json.dumps(fin_data)})
        return fin_data
    else:
        data = data.decode()
        valdata = process_battery_request_string(xtring=data)
        if len(valdata) == 0 or len(valdata) != 7:
            fin_data = generate_response_code_new(status=2)
            update_request_log(db=db, id=req.id, values={'response_value': json.dumps(fin_data)})
            return fin_data
        else:
            battery_code = valdata[0]
            longitude = valdata[1]
            latitude = valdata[2]
            charge_status = int(valdata[3])
            discharge_status = int(valdata[4])
            voltage = valdata[5]
            state_of_charge = valdata[6]
            battery = get_single_battery_by_code(db=db, code=battery_code)
            if battery is None:
                if battery_code is None or battery_code == "":
                    fin_data = generate_response_code_new(status=3)
                    update_request_log(db=db, id=req.id, values={'response_value': json.dumps(fin_data)})
                    return fin_data
                else:
                    battery_type_code = battery_code[0]
                    battery_type = get_single_battery_type_by_code(db=db, code=battery_type_code)
                    if battery_type is None:
                        fin_data = generate_response_code_new(status=4)
                        update_request_log(db=db, id=req.id, values={'response_value': json.dumps(fin_data)})
                        return fin_data
                    else:
                        battery = create_battery(db=db, type_id=battery_type.id, code=battery_code, voltage=voltage, charge=state_of_charge, latitude=latitude, longitude=longitude)
                        fin_data = generate_response_code_new(status=1)
                        update_request_log(db=db, id=req.id, values={'response_value': json.dumps(fin_data)})
                        return fin_data
            else:
                battery_status = battery.status
                lt_int = float(latitude)
                lg_int = float(longitude)
                soc_int = float(state_of_charge)
                values = {
                    'voltage': voltage,
                    # 'charge': state_of_charge,
                }
                if lt_int > 0:
                    values['latitude'] = latitude
                if lg_int > 0:
                    values['longitude'] = longitude
                if soc_int != 999.90:
                    values['charge'] = state_of_charge
                if charge_status == 1:
                    values['status'] = 3
                if discharge_status == 1:
                    values['status'] = 1
                update_battery(db=db, id=battery.id, values=values)
                fin_data = generate_response_code_new(status=1, battery_status=battery_status)
                update_request_log(db=db, id=req.id, values={'response_value': json.dumps(fin_data)})
                return fin_data
                
        
def process_battery_request_get(db: Session, ip_address: str=None, initial_instruction: str=None, t: str=None, c: str=None, v: str=None, bID: str=None, SOC: str=None, s: str=None, LT: str=None, LG: str=None):
    data = {
        't': t,
        'c': c,
        'v': v,
        'bID': bID,
        'SOC': SOC,
        's': s,
        'LT': LT,
        'LG': LG,
    }
    req = create_request_log(db=db, server_type="battery", ip_address=ip_address, initial_instruction=initial_instruction, name="get", value=json.dumps(data))
    if bID is None:
        fin_data = "BMA12D9C01230905163155"
        update_request_log(db=db, id=req.id, values={'response_value': json.dumps(fin_data)})
        return fin_data
    else:
        battery = get_single_battery_by_code(db=db, code=bID)
        if battery is None:
            fin_data = "BMA12D9C01230905163155"
            update_request_log(db=db, id=req.id, values={'response_value': json.dumps(fin_data)})
            return fin_data
        else:
            values = {}
            if t is not None:
                values['temperature'] = t
            if c is not None:
                values['electric_current'] = c
            if v is not None:
                values['voltage'] = v
            if SOC is not None:
                values['charge'] = SOC
            if LT is not None:
                values['latitude'] = LT
            if LG is not None:
                values['longitude'] = LG
            is_shutdown = 0
            is_hotlisted = 0
            if battery.status == 2:
                is_shutdown = 1
            elif battery.status == 4:
                is_hotlisted = 1
            else:
                values['status'] = s
            update_battery(db=db, id=battery.id, values=values)
            fin_data = "BMA12D9C01230905163155"
            update_request_log(db=db, id=req.id, values={'response_value': json.dumps(fin_data)})
            return fin_data

def sync_battery_request(db: Session, initial_instruction: str=None, original_values: str=None, battery_id: int=0, voltage: str=None, temperature: str=None, charge: str=None, electric_current: str=None, latitude: str=None, longitude: str=None, is_docked_charging: int=None, is_docked_discharging: int=None):
    create_request_log(db=db, initial_instruction=initial_instruction, server_type="battery", name="post", value=original_values)
    battery = get_single_battery_by_id(db=db, id=battery_id)
    if battery is None:
        return {
            'status': False,
            'message': 'Battery not found',
            'data': None
        }
    else:
        values = {}
        if voltage is not None:
            values['voltage'] = voltage
        if temperature is not None:
            values['temperature'] = temperature
        if charge is not None:
            values['charge'] = charge
        if electric_current is not None:
            values['electric_current'] = electric_current
        if latitude is not None:
            values['latitude'] = latitude
        if longitude is not None:
            values['longitude'] = longitude
        data = {
            'host_id': None,
            'charge': None,
            'discharge': None,
            'hotlist': None,
            'shutdown': None,
        }
        transaction = get_last_battery_transaction(db=db, mobility_device_id=battery.mobility_device_id)
        station_battery = get_single_station_battery_by_id(db=db, id=battery.slot_id)
        if is_docked_charging is not None:
            if is_docked_charging == 0:
                if battery.slot_id > 0:
                    if station_battery is not None:
                        if station_battery.battery_eject == 1:
                            values['is_ejected'] = 1
                            values['ejected_by'] = station_battery.battery_ejected_by
                            update_station_battery(db=db, id=station_battery.id, values={'battery_eject': None, 'battery_ejected_by': None, 'status': 0})
                if battery.mobility_device_id > 0:
                    pass
                data['charge'] = 0
                values['status'] = 0
            if is_docked_charging == 1:
                if battery.slot_id > 0:
                    pass
                if battery.mobility_device_id > 0:
                    if transaction is not None:
                        station_id = transaction.station_id
                        open_station_slot = get_open_station_slot(db=db, station_id=station_id)
                        if open_station_slot is not None:
                            values['slot_id'] = open_station_slot.slot_id
                            values['mobility_device_id'] = 0
                        station = get_single_station_by_id(db=db, id=station_id)
                        if station is not None:
                            data['host_id'] = station.code
                            update_station_battery(db=db, id=station_battery.id, values={'station_allow_charge': None, 'status': 1})
                data['charge'] = 1
                values['status'] = 3
        if is_docked_discharging is not None:
            if is_docked_discharging == 0:
                if battery.slot_id > 0:
                    pass
                if battery.mobility_device_id > 0:
                    pass
                data['discharge'] = 0
                values['status'] = 0
            if is_docked_discharging == 1:
                if battery.slot_id > 0:
                    if battery.is_ejected == 1:
                        values['mobility_device_id'] = battery.ejected_by
                        values['is_ejected'] = 0
                        values['ejected_by'] = 0
                        values['slot_id'] = 0
                        e_mob_device = get_single_mobility_device_by_id(db=db, id=battery.ejected_by)
                        if e_mob_device is not None:
                            data['host_id'] = e_mob_device.code
                if battery.mobility_device_id > 0:
                    pass
                data['discharge'] = 1
                values['status'] = 1
        if battery.status == 2:
            data['shutdown'] = 1
        elif battery.status == 4:
            data['hotlist'] = 1
        update_battery(db=db, id=battery.id, values=values)
        return {
            'status': True,
            'message': 'Success',
            'data': data
        }

# def sync_battery_details(db: Session, initial_instruction: str=None, original_values: str=None, battery_id: int=0, voltage: str=None, temperature: str=None, charge: str=None, electric_current: str=None, latitude: str=None, longitude: str=None, is_docked_charging: int=None, is_docked_discharging: int=None):
#     create_request_log(db=db, initial_instruction=initial_instruction, server_type="battery", name="post", value=original_values)
#     battery = get_single_battery_by_id(db=db, id=battery_id)
#     if battery is None:
#         return {
#             'status': False,
#             'message': 'Battery not found',
#             'data': None
#         }
#     else:
#         values = {}
#         if voltage is not None:
#             values['voltage'] = voltage
#         if temperature is not None:
#             values['temperature'] = temperature
#         if charge is not None:
#             values['charge'] = charge
#         if electric_current is not None:
#             values['electric_current'] = electric_current
#         if latitude is not None:
#             values['latitude'] = latitude
#         if longitude is not None:
#             values['longitude'] = longitude
#         data = {
#             'host_id': None,
#             'charge': None,
#             'discharge': None,
#             'hotlist': None,
#             'shutdown': None,
#         }
#         if is_docked_charging is not None:
#             if is_docked_charging == 0:
#                 data['charge'] = 0
#                 values['status'] = 0
#             if is_docked_charging == 1:
#                 data['charge'] = 1
#                 values['status'] = 3
#         if is_docked_discharging is not None:
#             if is_docked_discharging == 0:
#                 data['discharge'] = 0
#                 values['status'] = 0
#             if is_docked_discharging == 1:
#                 data['discharge'] = 1
#                 values['status'] = 1
#         if battery.status == 2:
#             data['shutdown'] = 1
#         elif battery.status == 4:
#             data['hotlist'] = 1
#         update_battery(db=db, id=battery.id, values=values)
#         return {
#             'status': True,
#             'message': 'Success',
#             'data': data
#         }

def sync_battery_details(db: Session, initial_instruction: str=None, original_values: str=None, battery_id: int=0, voltage: str=None, temperature: str=None, charge: str=None, electric_current: str=None, latitude: str=None, longitude: str=None, charge_status: int=None, discharge_status: int=None, enable_status: int=None, disable_status: int=None):
    create_request_log(db=db, initial_instruction=initial_instruction, server_type="battery", name="post", value=original_values)
    battery = get_single_battery_by_id(db=db, id=battery_id)
    if battery is None:
        return {
            'status': False,
            'message': 'Battery not found',
            'data': None
        }
    else:
        values = {}
        if voltage is not None:
            values['voltage'] = voltage
        if temperature is not None:
            values['temperature'] = temperature
        if charge is not None:
            values['charge'] = charge
        if electric_current is not None:
            values['electric_current'] = electric_current
        if latitude is not None:
            values['latitude'] = latitude
        if longitude is not None:
            values['longitude'] = longitude
        data = {
            'host_id': None,
            'charge': None,
            'discharge': None,
            'hotlist': None,
            'shutdown': None,
            'idle': None,
        }
        if battery.temp_status == 3:
            if charge_status is not None:
                if charge_status == 1:
                    data['charge'] = 1
                    values['temp_status'] = None
                    values['status'] = 3
        if charge_status is not None:
            if charge_status == 1 and battery.status != 3:
                values['status'] = 3
        if battery.temp_status == 1:
            if discharge_status is not None:
                if discharge_status == 1:
                    data['discharge'] = 1
                    values['temp_status'] = None
        if discharge_status is not None:
            if discharge_status == 1 and battery.status != 1:
                values['status'] = 1
        if battery.temp_status == 2:
            data['shutdown'] = 1
            values['temp_status'] = None
            values['status'] = 2
        if battery.temp_status == 4:
            # if disable_status == 1 and battery.status != 4:
            #     data['hotlist'] = 1
            #     values['temp_status'] = None
            #     values['status'] = 4
            data['hotlist'] = 1
            values['temp_status'] = None
            values['status'] = 4
        if disable_status is not None:
            if disable_status == 1 and battery.status != 4:
                values['status'] = 4
        if battery.temp_status == 0:
            values['temp_status'] = None
            values['status'] = 0
            data['idle'] = 1
        if enable_status is not None:
            if enable_status == 1 and battery.status != 0:
                values['status'] = 0
        if battery.temp_host is not None:
            data['host_id'] = battery.temp_host
            values['temp_host'] = None
        update_battery(db=db, id=battery.id, values=values)
        return {
            'status': True,
            'message': 'Success',
            'data': data
        }
