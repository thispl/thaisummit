import frappe
import json
from frappe.utils import (getdate, cint, add_months, date_diff, add_days,
    nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime)
from datetime import datetime
from datetime import date, timedelta,time

@frappe.whitelist()
def get_qr_details(user):
    employee_name = ''
    department = ''
    if user != 'Administrator':
        employee_name,department = frappe.get_value('Employee',{ 'user_id' : user }, ['employee_name','department'])
    nowtime = datetime.now()
    shift_date = date.today()
    scan_active = 1
    qr_details = {}
    shift_type =get_shift_type()
    if shift_type == '3':
        shift_date = shift_date + timedelta(days=-1)
    # shift_active_type = get_shift_active_type()
    if shift_type == 'NA':
        scan_active = 0
    planned_onroll_count = frappe.db.count('Shift Assignment',{'employee_type':('in',['BC','FT','NT']),'shift_type':shift_type,'start_date': shift_date, 'docstatus':1, 'department':department})
    planned_cl_count = frappe.db.count('Shift Assignment',{'employee_type':'CL','shift_type':shift_type,'start_date': shift_date, 'docstatus':1, 'department':department})
    actual_onroll_count = frappe.db.count('QR Checkin',{'employee_type':('in',['BC','FT','NT']),'ot':0,'qr_shift':shift_type,'shift_date': shift_date,'department':department})
    actual_cl_count = frappe.db.count('QR Checkin',{'employee_type':'CL','ot':0,'qr_shift':shift_type,'shift_date': shift_date,'department':department })
    ot_onroll_count = frappe.db.count('QR Checkin',{'employee_type':('in',['BC','FT','NT']),'ot':1,'qr_shift':shift_type,'shift_date': shift_date,'department':department })
    ot_cl_count = frappe.db.count('QR Checkin',{'employee_type':'CL','ot':1,'qr_shift':shift_type,'shift_date': shift_date,'department':department })
    

    qr_details['scan_active'] = scan_active
    qr_details['employee_name'] = employee_name
    qr_details['department'] = department
    qr_details['shift_type'] = shift_type
    qr_details['planned_onroll_count'] = planned_onroll_count
    qr_details['planned_cl_count'] = planned_cl_count
    qr_details['total_planned_count'] =  planned_onroll_count + planned_cl_count
    qr_details['actual_onroll_count'] = actual_onroll_count
    qr_details['actual_cl_count'] = actual_cl_count
    qr_details['total_actual_count'] = actual_onroll_count + actual_cl_count
    qr_details['ot_onroll_count'] = ot_onroll_count
    qr_details['ot_cl_count'] = ot_cl_count
    qr_details['total_ot_count'] = ot_onroll_count + ot_cl_count
    qr_details['total_onroll_count'] = planned_onroll_count +  actual_onroll_count +  ot_onroll_count
    qr_details['total_cl_count'] = planned_cl_count + actual_cl_count + ot_cl_count
    qr_details['nowtime'] = datetime.strftime(nowtime,'%d-%m-%Y %H:%M:%S')
    onroll_percentage = 0
    cl_percentage = 0
    total_percentage = 0
    onroll_shortage = 0
    cl_shortage = 0

    if planned_onroll_count:
        if actual_onroll_count < planned_onroll_count:
            onroll_shortage = planned_onroll_count - actual_onroll_count

        onroll_percentage = round(( actual_onroll_count / planned_onroll_count )* 100)

    if planned_cl_count:    
        if actual_cl_count < planned_cl_count:
            cl_shortage = planned_cl_count - actual_cl_count

        cl_percentage = round(((actual_cl_count) / (planned_cl_count))* 100)

    if planned_onroll_count or planned_cl_count:
        total_percentage = round(((actual_onroll_count + actual_cl_count) / (planned_onroll_count + planned_cl_count))*100)
    
    qr_details['onroll_percentage'] = onroll_percentage
    qr_details['cl_percentage'] = cl_percentage
    qr_details['total_percentage'] = total_percentage
    qr_details['onroll_shortage'] = onroll_shortage
    qr_details['cl_shortage'] = cl_shortage
        
    return qr_details

def is_between(time, time_range):
    if time_range[1] < time_range[0]:
        return time >= time_range[0] or time <= time_range[1]
    return time_range[0] <= time <= time_range[1]


def  get_shift_type():
    nowtime = datetime.now()
    shift_date = date.today()
    shift1_time = [time(hour=6, minute=0, second=0),time(hour=14, minute=0, second=0)]
    shift2_time = [time(hour=14, minute=0, second=0),time(hour=21, minute=00, second=0)]
    shift2_cont_time = [time(hour=22, minute=1, second=0),time(hour=23, minute=59, second=0)]
    shift3_time = [time(hour=0, minute=0, second=1),time(hour=5, minute=0, second=0)]
    # shiftpp1_time = [time(hour=7, minute=0, second=0),time(hour=10, minute=0, second=0)]
    shiftpp2_time = [time(hour=21, minute=30, second=0),time(hour=22, minute=0, second=0)]
    curtime = time(hour=nowtime.hour, minute=nowtime.minute, second=nowtime.second)
    shift_type = 'NA'
    if is_between(curtime,shift1_time):
        shift_type = '1'
    if is_between(curtime,shift2_time):
        shift_type = '2'
    if is_between(curtime,shift2_cont_time):
        shift_type = '2'
    if is_between(curtime,shift3_time):
        shift_type = '3'
        shift_date = shift_date + timedelta(days=-1)
    if is_between(curtime,shiftpp2_time):
        shift_type = 'PP2'
    
    return shift_type

def  get_shift_active_type():
    nowtime = datetime.now()
    shift_date = date.today()
    shift1_time = [time(hour=6, minute=0, second=0),time(hour=13, minute=59, second=59)]
    shift2_time = [time(hour=14, minute=00, second=0),time(hour=11, minute=59, second=59)]
    shift3_time = [time(hour=0, minute=0, second=1),time(hour=6, minute=0, second=0)]
    # shiftpp1_time = [time(hour=7, minute=0, second=0),time(hour=10, minute=0, second=0)]
    shiftpp2_time = [time(hour=19, minute=30, second=0),time(hour=22, minute=0, second=0)]
    curtime = time(hour=nowtime.hour, minute=nowtime.minute, second=nowtime.second)
    shift_active_type = 'NA'
    if is_between(curtime,shift1_time):
        shift_active_type = '1'
    if is_between(curtime,shift2_time):
        shift_active_type = '2'
    if is_between(curtime,shift3_time):
        shift_active_type = '3'
        shift_date = shift_date + timedelta(days=-1)
    if is_between(curtime,shiftpp2_time):
        shift_active_type = 'PP2'
    
    return shift_active_type

@frappe.whitelist()
def get_qr_list(employee=None):
    department = frappe.get_value('Employee',{'user_id':frappe.session.user},'department')
    shift_type = get_shift_type()
    shift_date = date.today()
    if shift_type == '3':
        shift_date = shift_date + timedelta(days=-1)
    if employee:
        query = """ select employee,employee_name,name as checkinid from `tabQR Checkin` where  shift_date = '%s' and qr_shift='%s' and ot=0 and department='%s' and employee like '%%%s%%' """ % (shift_date,shift_type,department,employee)
    else:
        query = """ select employee,employee_name,name as checkinid from `tabQR Checkin` where  shift_date = '%s' and qr_shift='%s' and ot=0 and department='%s'""" % (shift_date,shift_type,department)
    checkin_list = frappe.db.sql(query,as_dict=True )
    return checkin_list

@frappe.whitelist()
def get_ot_qr_list(employee=None):
    department = frappe.get_value('Employee',{'user_id':frappe.session.user},'department')
    shift_type = get_shift_type()
    shift_date = date.today()
    if shift_type == '3':
        shift_date = shift_date + timedelta(days=-1)
    if employee:
        query = """ select employee,employee_name,name as checkinid from `tabQR Checkin` where  shift_date = '%s' and qr_shift='%s' and ot = 1 and department='%s' and employee like '%%%s%%' """ % (shift_date,shift_type,department,employee)
    else:
        query = """ select employee,employee_name,name as checkinid from `tabQR Checkin` where  shift_date = '%s' and qr_shift='%s' and ot = 1 and department='%s'""" % (shift_date,shift_type,department)
    checkin_list = frappe.db.sql(query,as_dict=True )
    return checkin_list


@frappe.whitelist()
def update_deleted_qr(checkin):
    qr_deleted_by = frappe.get_value('Employee',{'user_id':frappe.session.user},'name') + ':'
    qr_deleted_by += frappe.get_value('Employee',{'user_id':frappe.session.user},'employee_name')
    checkin_id = frappe.db.exists('QR Checkin',checkin)
    if checkin_id:
        qr_checkin = frappe.get_doc('QR Checkin',checkin_id)
        deleted_qr = frappe.new_doc('Deleted QR Checkin')
        deleted_qr.update({
            "employee":qr_checkin.employee,
            "employee_name":qr_checkin.employee_name,
            "department":qr_checkin.department,
            "employee_type":qr_checkin.employee_type,
            "qr_shift":qr_checkin.qr_shift,
            "created_date":qr_checkin.created_date,
            "shift_date":qr_checkin.shift_date,
            "qr_scan_time":qr_checkin.qr_scan_time,
            "deleted_by": qr_deleted_by,
            "deleted_datetime":datetime.now()
        })
        deleted_qr.save(ignore_permissions=True)
        frappe.db.commit()

        frappe.delete_doc('QR Checkin',checkin)
        return 'Deleted'
        


    
    