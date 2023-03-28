# Copyright (c) 2022, TEAMPRO and contributors
# For license information, please see license.txt

from datetime import datetime
import frappe
from frappe.model.document import Document


class BusArrivalForm(Document):
    pass

@frappe.whitelist()
def get_bus_arrival_shift(time_apply):
    from datetime import datetime
    from datetime import date, timedelta,time
    std_shift_1_in_time = time(hour=7,minute=30,second=0)
    std_shift_2_in_time = time(hour=16,minute=15,second=0)
    std_shift_pp2_in_time = time(hour=19,minute=30,second=0)
    std_shift_3_in_time = time(hour=0,minute=45,second=0)
    shift1_time = [time(hour=6, minute=0, second=0),time(hour=15, minute=0, second=0)]
    shift2_time = [time(hour=15, minute=15, second=0),time(hour=18, minute=59, second=0)]
    shift3_time = [time(hour=23, minute=00, second=0),time(hour=2, minute=0, second=0)]
    shiftpp2_time = [time(hour=19, minute=0, second=1),time(hour=21, minute=59, second=0)]
    str_time = datetime.strptime(time_apply,'%H:%M:%S').time()
    shift_type = 'NA'
    status = 'On Time'
    late_minutes = 0
    if is_between(str_time,shift1_time):
        shift_type = '1'
        if str_time > std_shift_1_in_time:
            status = 'Late'
            late_minutes = datetime.strptime(str(str_time),'%H:%M:%S') - datetime.strptime(str(std_shift_1_in_time),'%H:%M:%S')
    if is_between(str_time,shift2_time):
        shift_type = '2'
        if str_time > std_shift_2_in_time:
            status = 'Late'
            late_minutes = datetime.strptime(str(str_time),'%H:%M:%S') - datetime.strptime(str(std_shift_2_in_time),'%H:%M:%S')
    if is_between(str_time,shift3_time):
        shift_type = '3'
        if str_time > std_shift_3_in_time:
            status = 'Late'
            late_minutes = datetime.strptime(str(str_time),'%H:%M:%S') - datetime.strptime(str(std_shift_3_in_time),'%H:%M:%S')

    if is_between(str_time,shiftpp2_time):
        shift_type = 'PP2'
        if str_time > std_shift_pp2_in_time:
            status = 'Late'
            late_minutes = datetime.strptime(str(str_time),'%H:%M:%S') - datetime.strptime(str(std_shift_pp2_in_time),'%H:%M:%S')

    return shift_type,status,late_minutes        
    




# @frappe.whitelist()
# def get_bus_arrival_shift():
#     from datetime import datetime
#     from datetime import date, timedelta,time
#     nowtime = datetime.now()
#     std_shift_1_in_time = time(hour=7,minute=30,second=0)
#     std_shift_2_in_time = time(hour=16,minute=15,second=0)
#     std_shift_pp2_in_time = time(hour=19,minute=30,second=0)
#     std_shift_3_in_time = time(hour=1,minute=0,second=0)
#     shift1_time = [time(hour=6, minute=0, second=0),time(hour=15, minute=0, second=0)]
#     shift2_time = [time(hour=15, minute=15, second=0),time(hour=18, minute=59, second=0)]
#     shift3_time = [time(hour=23, minute=00, second=0),time(hour=2, minute=0, second=0)]
#     shiftpp2_time = [time(hour=19, minute=0, second=1),time(hour=21, minute=59, second=0)]
#     curtime = time(hour=nowtime.hour, minute=nowtime.minute, second=nowtime.second)
#     shift_type = 'NA'
#     status = 'Ontime'
#     late_minutes = 0
#     if is_between(curtime,shift1_time):
#         shift_type = '1'
#         if curtime > std_shift_1_in_time:
#             status = 'Late'
#             late_minutes = datetime.strptime(str(curtime),'%H:%M:%S') - datetime.strptime(str(std_shift_1_in_time),'%H:%M:%S')
#     if is_between(curtime,shift2_time):
#         shift_type = '2'
#         if curtime > std_shift_2_in_time:
#             status = 'Late'
#             late_minutes = datetime.strptime(str(curtime),'%H:%M:%S') - datetime.strptime(str(std_shift_2_in_time),'%H:%M:%S')
#     # if is_between(curtime,shift2_cont_time):
#     #     shift_type = '2'
#     if is_between(curtime,shift3_time):
#         shift_type = '3'
#         if curtime > std_shift_3_in_time:
#             status = 'Late'
#             late_minutes = datetime.strptime(str(curtime),'%H:%M:%S') - datetime.strptime(str(std_shift_3_in_time),'%H:%M:%S')

#     if is_between(curtime,shiftpp2_time):
#         shift_type = 'PP2'
#         if curtime > std_shift_pp2_in_time:
#             status = 'Late'
#             late_minutes = datetime.strptime(str(curtime),'%H:%M:%S') - datetime.strptime(str(std_shift_pp2_in_time),'%H:%M:%S')

#     return shift_type,status,late_minutes


def is_between(time, time_range):
    if time_range[1] < time_range[0]:
        return time >= time_range[0] or time <= time_range[1]
    return time_range[0] <= time <= time_range[1]	
