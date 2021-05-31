# Copyright (c) 2013, TEAMPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import msgprint, _
from datetime import date, timedelta,time

def execute(filters=None):
    columns, data = [], []
    planned_bc_count = planned_cl_count = 0
    qr_details = get_qr_details(filters.shift_type,filters.date)
    columns = [
        _("List") + ":Data:150", _("Onroll") + ":Data:200",_("CL") + ":Data:150", _("Total") + ":Data:200"
    ]
    planned = ['Planned', qr_details['planned_bc_count'],  qr_details['planned_cl_count'],  qr_details['total_planned_count']]
    actual = ['Actual',qr_details['actual_bc_count'],  qr_details['actual_cl_count'],  qr_details['total_actual_count']]
    ot = ['OT',qr_details['ot_bc_count'],  qr_details['ot_cl_count'],  qr_details['total_ot_count']]
    total = ['Total',qr_details['total_bc_count'],  qr_details['total_cl_count'],  qr_details['total_ot_count']]
    absent = ['Absent','0','0','0']
    percent = ['%',qr_details['bc_percentage'],  qr_details['cl_percentage'],  qr_details['total_percentage']]

    data.append(planned)
    data.append(actual)
    data.append(ot)
    data.append(total)
    data.append(absent)
    data.append(percent)

    return columns, data

def get_columns():
    columns += [
        _("List") + ":Data:150", _("Onroll") + ":Data/:200",_("CL") + ":Employee:150", _("Total") + ":Data/:200"
    ]
    return columns

@frappe.whitelist()
def get_qr_details(shift_type,shift_date):
    qr_details = {}

    planned_bc_count = frappe.db.count('Shift Assignment',{'employee_type':'BC','shift_type':shift_type,'start_date': shift_date })
    planned_ft_count = frappe.db.count('Shift Assignment',{'employee_type':'FT','shift_type':shift_type,'start_date': shift_date })
    planned_cl_count = frappe.db.count('Shift Assignment',{'employee_type':'CL','shift_type':shift_type,'start_date': shift_date })
    actual_bc_count = frappe.db.count('QR Checkin',{'employee_type':'BC','qr_shift':shift_type,'shift_date': shift_date })
    actual_ft_count = frappe.db.count('QR Checkin',{'employee_type':'FT','qr_shift':shift_type,'shift_date': shift_date })
    actual_cl_count = frappe.db.count('QR Checkin',{'employee_type':'CL','qr_shift':shift_type,'shift_date': shift_date })
    ot_bc_count = ot_ft_count = ot_cl_count = 0
    qr_details['shift_type'] = shift_type
    qr_details['planned_bc_count'] = planned_bc_count + planned_ft_count
    qr_details['planned_cl_count'] = planned_cl_count
    qr_details['total_planned_count'] =  planned_bc_count + planned_ft_count + planned_cl_count
    qr_details['actual_bc_count'] = actual_bc_count + actual_ft_count
    qr_details['actual_cl_count'] = actual_cl_count
    qr_details['total_actual_count'] = actual_bc_count + actual_ft_count + actual_cl_count
    qr_details['ot_bc_count'] = ot_bc_count + ot_ft_count
    qr_details['ot_cl_count'] = ot_cl_count
    qr_details['total_bc_count'] = actual_bc_count + actual_ft_count +  ot_bc_count + ot_ft_count
    qr_details['total_cl_count'] = actual_cl_count + ot_cl_count
    qr_details['total_ot_count'] = qr_details['total_bc_count'] + qr_details['total_cl_count']
    bc_percentage = 0
    cl_percentage = 0
    total_percentage = 0

    if planned_bc_count or planned_ft_count:
        planned_count = planned_bc_count + planned_ft_count
        actual_count =actual_bc_count + actual_ft_count
        bc_percentage = round(( actual_count / planned_count )* 100)
        cl_percentage = round(((actual_cl_count) / (planned_cl_count))* 100)
        total_percentage = round(((actual_count + actual_cl_count) / (planned_count + planned_cl_count))*100)
    
    qr_details['bc_percentage'] = bc_percentage
    qr_details['cl_percentage'] = cl_percentage
    qr_details['total_percentage'] = total_percentage
        
    
    return qr_details

