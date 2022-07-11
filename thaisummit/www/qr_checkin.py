# -*- coding: utf-8 -*-
# Copyright (c) 2021, TEAMPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import today,flt,cint, getdate, get_datetime,cstr,add_days
from datetime import timedelta,datetime,date,time

@frappe.whitelist()
def mark_checkin(employee=None):
    department = frappe.get_value('Employee',{'user_id':frappe.session.user},'department')
    qr_scanned_by = frappe.get_value('Employee',{'user_id':frappe.session.user},'name') + ':'
    qr_scanned_by += frappe.get_value('Employee',{'user_id':frappe.session.user},'employee_name')
    nowtime = datetime.now()
    shift_date = date.today()
    shift1_time = [time(hour=7, minute=0, second=0),time(hour=13, minute=00, second=0)]
    shift2_time = [time(hour=15, minute=30, second=0),time(hour=19, minute=30, second=0)]
    shift3_time = [time(hour=00, minute=0, second=1),time(hour=4, minute=0, second=0)]
    shiftpp2_time = [time(hour=19, minute=00, second=0),time(hour=23, minute=0, second=0)]
    # shiftpp1_time = [time(hour=7, minute=0, second=0),time(hour=10, minute=0, second=0)]
    # shift2_cont_time = [time(hour=22, minute=1, second=0),time(hour=22, minute=59, second=0)]
    curtime = time(hour=nowtime.hour, minute=nowtime.minute, second=nowtime.second)
    shift_type = 'NA'
    if is_between(curtime,shift1_time):
        shift_type = '1'
    if is_between(curtime,shift2_time):
        shift_type = '2'
    # if is_between(curtime,shift2_cont_time):
    #     shift_type = '2'
    if is_between(curtime,shift3_time):
        shift_type = '3'
        shift_date = shift_date + timedelta(days=-1)
    if is_between(curtime,shiftpp2_time):
        shift_type = 'PP2'
    
    if shift_type == 'NA':
        return 'Wrong Shift Time'
    
    planned_count = frappe.db.count('Shift Assignment',{'shift_type':shift_type,'start_date': shift_date, 'docstatus':1, 'department':department, 'employee_type':('!=','WC'),})
    actual_count = frappe.db.count('QR Checkin',{'qr_shift':shift_type,'ot':0,'shift_date': shift_date,'department':department})

    existing_employee = frappe.db.exists('Employee',{'employee':employee, 'status':'Active','employee_type':('!=','WC')})
    if not existing_employee:
        return 'Employee Not Found'
    existing_checkin = frappe.db.exists('QR Checkin',{'employee':employee, 'shift_date':shift_date, 'qr_shift': shift_type})
    if existing_checkin:
        return 'Checkin Already Exists'
    if get_ot_shift(shift_type,employee,shift_date) == 'OT':
        employee_name,employee_type = frappe.get_value('Employee',employee,['employee_name','employee_type'])
        qr_checkin = frappe.new_doc('QR Checkin')
        qr_checkin.update({
            'employee': employee,
            'employee_name': employee_name,
            'department': frappe.get_value('Employee',{'user_id':frappe.session.user},'department'),
            'employee_type': employee_type,
            'created_date': today(),
            'shift_date': shift_date,
            'qr_scan_time':nowtime,
            'qr_scanned_by':qr_scanned_by,
            'qr_shift': shift_type
        })
        qr_checkin.save(ignore_permissions=True)
        return 'Checkin Marked Successfully'
    if actual_count >= planned_count:
        return 'Planned Count Exceeded'
    else:
        employee_name,employee_type = frappe.get_value('Employee',employee,['employee_name','employee_type'])
        qr_checkin = frappe.new_doc('QR Checkin')
        qr_checkin.update({
            'employee': employee,
            'employee_name': employee_name,
            'department': frappe.get_value('Employee',{'user_id':frappe.session.user},'department'),
            'employee_type': employee_type,
            'created_date': today(),
            'shift_date': shift_date,
            'qr_scan_time':nowtime,
            'qr_scanned_by':qr_scanned_by,
            'qr_shift': shift_type
        })
        qr_checkin.save(ignore_permissions=True)
        return 'Checkin Marked Successfully'

def is_between(time, time_range):
    if time_range[1] < time_range[0]:
        return time >= time_range[0] or time <= time_range[1]
    return time_range[0] <= time <= time_range[1]

def get_ot_shift(qr_shift,employee,shift_date):
    if qr_shift == "2":
        if frappe.db.exists("QR Checkin",{'employee':employee,'qr_shift':'1','shift_date':shift_date}):
            return 'OT'
    if qr_shift == "3":
        if frappe.db.exists("QR Checkin",{'employee':employee,'qr_shift':'2','shift_date':shift_date}):
            return 'OT'
    if qr_shift == "1":
        shift_date = add_days(shift_date,-1)
        if frappe.db.exists("QR Checkin",{'employee':employee,'qr_shift':'3','shift_date':shift_date}):
            return 'OT'
        if frappe.db.exists("QR Checkin",{'employee':employee,'qr_shift':'PP2','shift_date':shift_date}):
            return 'OT'
