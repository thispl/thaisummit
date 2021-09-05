from __future__ import unicode_literals
from os import stat
import frappe
from frappe.utils import cstr, add_days, date_diff, getdate, touch_file
from frappe import _
from frappe.utils.csvutils import UnicodeWriter, build_csv_response, read_csv_content
from frappe.utils.file_manager import get_file
from frappe.model.document import Document
from frappe.utils.background_jobs import enqueue

from datetime import date, timedelta, datetime, time


def execute(filters=None):
    columns = get_columns(filters)
    data = get_data(filters)
    return columns ,data


def get_dates(filters):
    no_of_days = date_diff(add_days(filters.to_date, 1), filters.from_date)
    dates = [add_days(filters.from_date, i) for i in range(0, no_of_days)]
    return dates

def get_columns(filters):
    columns = [_("ID No") + ":Data/:100",_("NAME") + ":Data/:150",_("Department") + ":Data/:150",_("DOJ") + ":Date/:100",_("11") + ":Data/:70",_("22") + ":Data/:70",_("33") + ":Data/:70",_("12    ") + ":Data/:70",_("13") + ":Data/:70",_("21") + ":Data/:70",_("23") + ":Data/:70",_("31") + ":Data/:70",_("32  ") + ":Data/:70",_("1L1") + ":Data/:70",_("2L2") + ":Data/:70",_("3L3") + ":Data/:70",_("PP1") + ":Data/:70",_("PP2") + ":Data/:70",_("PP1L") + ":Data/:70",_("PP2L") + ":Data/:70",_("1M") + ":Data/:70",_("2M") + ":Data/:70",_("3M") + ":Data/:70",_("MM") + ":Data/:70",_("AA") + ":Data/:70",]
    return columns


def get_data(filters):
    data = []
    dates = get_dates(filters)
    emp = frappe.get_all('Employee',{'employee_type':filters.employee_type},['department','employee_number','employee_name','date_of_joining'])

    for i in emp:
        row = []
        count_11 = 0
        count_22 = 0
        count_33 = 0
        count_12 = 0
        count_13 = 0
        count_21 = 0
        count_23 = 0
        count_31 = 0
        count_32 = 0
        count_1l1 = 0
        count_2l2 = 0
        count_3l3 = 0
        count_pp1 = 0
        count_pp2 = 0
        count_pp1l = 0
        count_pp2l = 0
        count_1m = 0
        count_2m = 0
        count_3m = 0
        count_mm =  0
        count_aa = 0

        for date in dates:
            status = frappe.get_value('Attendance',{'employee':i.employee_number,'attendance_date':date},'shift_status')
            # att_shift = frappe.get_value('Attendance',{'employee':i.employee_number,'attendance_date':date,'employee_type':filters.employee_type},['shift'])
            # att_qr_shift = frappe.get_value('Attendance',{'employee':i.employee_number,'attendance_date':date,'employee_type':filters.employee_type},['qr_shift'])
            # att_late = frappe.get_value('Attendance',{'employee':i.employee_number,'attendance_date':date,'employee_type':filters.employee_type},['late_entry'])

            if filters.employee_type == "WC":
                shift_status = wc_status_map.get(status, "")
            else:
                shift_status = bc_status_map.get(status, "") 

            if shift_status == '11':
                count_11 += 1
            elif shift_status == '21':
                count_22 += 1
            elif shift_status == '33':
                count_33 += 1
            elif shift_status == '12':
                count_12 += 1
            elif shift_status == '13':
                count_13 += 1
            elif shift_status == '21':
                count_21 += 1
            elif shift_status == '23':
                count_23 += 1
            elif shift_status == '31':
                count_31 += 1
            elif shift_status == '32':
                count_32 += 1
            elif shift_status == '1L1':
                count_1l1 += 1
            elif shift_status == '2L2':
                count_2l2 += 1
            elif shift_status == '3L3':
                count_3l3 += 1
            elif shift_status == 'PP1':
               count_pp1 += 1
            elif shift_status == 'PP2':
               count_pp2 += 1
            elif shift_status == 'PP1L':
               count_pp1l += 1
            elif shift_status == 'PP2L':
               count_pp2l += 1
            elif shift_status == '1M':
                count_1m += 1
            elif shift_status == '2M': 
                count_2m += 1
            elif shift_status == '3M':
                count_3m += 1
            elif shift_status == 'MM':
                count_mm += 1
            elif shift_status == 'AA':
                count_aa += 1

        row = [i.employee_number,i.employee_name,i.department,i.date_of_joining,count_11,count_22,count_33,count_12,count_13,count_21,count_23,count_31,count_32,count_1l1,count_2l2,count_3l3,count_pp1,count_pp2,count_pp1l,count_pp2l,count_1m,count_2m,count_3m,count_mm,count_aa]
        data.append(row)
    return data
    
bc_status_map = {
    "Absent": "AA",
    "AA":"AA",
    "Half Day": "HD",
    "Holiday": "HH",
    "Weekly Off": "WW",
    "WW":"WW",
    "1H": "1H",
    "2H": "2H",
    "3H": "3H",
    "1W": "1W",
    "2W": "2W",
    "3W": "3W",
    "PP1W": "PP1W",
    "PP2W": "PP2W",
    "1LH": "1LH",
    "2LH": "2LH",
    "3LH": "3LH",
    "1LW": "1LW",
    "2LW": "2LW",
    "3LW": "3LW",
    "PP1LW": "PP1LW",
    "PP2LW": "PP2LW",
    "MW": "MW",
    "On Leave": "L",
    "Present": "P",
    "Work From Home": "WFH",
    "MM": "AA",
    "11": "11",
    "22": "22",
    "33": "33",
    "PP1PP1": "P1P1",
    "PP2PP2": "P2P2",
    "1L1": "1L1",
    "2L2": "2L2",
    "3L3": "3L3",
    "2L3": "2L3",
    "1L2": "1L2",
    "3L1": "3L1",
    "1LM": "1LM",
    "2LM": "2LM",
    "3LM": "3LM",
    "PP1LPP1": "P1LP1",
    "PP2LPP2": "P2LP2",
    "1M": "1M",
    "2M": "2M",
    "3M": "3M",
    "M1": "M1",
    "M2": "M2",
    "M3": "M3",
    "PP1M": "P1M",
    "PP2M": "P2M",
    "MPP1": "MP1",
    "MPP2": "MP2",
    "11": "11",
    "12": "12",
    "13": "13",
    "1PP1": "1P1",
    "1PP2": "1P2",
    "21": "21",
    "22": "22",
    "23": "23",
    "2PP1": "2P1",
    "2PP2": "2P2",
    "31": "31",
    "32": "32",
    "33": "33",
    "3PP1": "3P1",
    "3PP2": "3P2",
    "PP11": "P11",
    "PP12": "P12",
    "PP13": "P13",
    "PP1PP1": "P1P1",
    "PP1PP2": "P1P2",
    "PP21": "P2P1",
    "PP22": "P2P2",
    "PP23": "P2P3",
    "PP2PP1": "P2P1",
    "PP2PP2": "P2P2",
    "Earned Leave": "EL",
    "Casual Leave": "CL",
    "Sick Leave": "SL",
    "Special Leave": "SPL",
    "OD": "OD",
    "Compensatory Off": "CO",
    "Leave Without Pay": "LL",
    "0.5Earned Leave": "0.5EL",
    "0.5Casual Leave": "0.5CL",
    "0.5Sick Leave": "0.5SL",
    "0.5Special Leave": "0.5SPL",
    "0.5Compensatory Off": "0.5CO",
    "0.5Leave Without Pay": "0.5LL",
    "LEarned Leave/2": "0.5SL",
    "LCasual Leave/2": "0.5LCL",
    "LSick Leave/2": "0.5LSL",
    "LSpecial Leave/2": "0.5LSPL",
    "LCompensatory Off/2": "0.5LCO",
    "LLeave Without Pay/2": "0.5LLL",
    }

wc_status_map = {
    "Absent": "AA",
    "AA": "AA",
    "Half Day": "HD",
    "Holiday": "HH",
    "WW":"WW",
    "1H": "1H",
    "2H": "2H",
    "3H": "3H",
    "1W": "1W",
    "2W": "2W",
    "3W": "3W",
    "PP1W": "PP1W",
    "PP2W": "PP2W",
    "PP1H": "P1H",
    "PP2H": "P2H",
    "Weekly Off": "WW",
    "On Leave": "L",
    # "Present": "11",
    "Work From Home": "WFH",
    "OD": "OD",
    "Earned Leave": "EL",
    "Casual Leave": "CL",
    "Sick Leave": "SL",
    "Special Leave": "SPL",
    "Compensatory Off": "CO",
    "Leave Without Pay": "LL",
    "1": "11",
    "2": "22",
    "3": "33",
    " ": "MM",
    "PP1": "P1P1",
    "PP2": "P2P2",
    "1L": "1L1",
    "2L": "2L2",
    "3L": "3L3",
    "PP1L": "P1LP1",
    "PP2L": "P2LP2",
    "1LH": "1LH",
    "2LH": "2LH",
    "3LH": "3LH",
    "1LW": "1LW",
    "2LW": "2LW",
    "3LW": "3LW",
    "PP1LW": "PP1LW",
    "PP2LW": "PP2LW",
    "1M": "1M",
    "2M": "2M",
    "3M": "3M",
    "M1": "M1",
    "M2": "M2",
    "M3": "M3",
    "PP1M": "P1M",
    "PP2M": "P2M",
    "MPP1": "MP1",
    "MPP2": "MP2",
    "0.5Earned Leave": "0.5EL",
    "0.5Casual Leave": "0.5CL",
    "0.5Sick Leave": "0.5SL",
    "0.5Special Leave": "0.5SPL",
    "0.5Compensatory Off": "0.5CO",
    "0.5Leave Without Pay": "0.5LL",
    "LEarned Leave/2": "0.5SL",
    "LCasual Leave/2": "0.5LCL",
    "LSick Leave/2": "0.5LSL",
    "LSpecial Leave/2": "0.5LSPL",
    "LCompensatory Off/2": "0.5LCO",
    "LLeave Without Pay/2": "0.5LLL"
    }