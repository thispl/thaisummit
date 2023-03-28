# Copyright (c) 2013, TEAMPRO and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
import frappe
from frappe.utils import cstr, cint, getdate, get_last_day, get_first_day, add_days
from frappe.utils import cstr, add_days, date_diff, getdate, format_date
from math import floor
from frappe import msgprint, _
from calendar import month, monthrange
from datetime import date, timedelta, datetime

def execute(filters=None):
    columns = get_columns(filters)
    data = get_data(filters)
    return columns, data

def get_columns(filters):
    columns = []
    columns += [
        _("Employee ID") + ":Data/:150",_("Employee Name") + ":Data/:200",_("Department") + ":Data/:150",_("DOJ") + ":Date/:100",
    ]
    dates = get_dates(filters.from_date,filters.to_date)
    for date in dates:
        date = datetime.strptime(date,'%Y-%m-%d')
        day = datetime.date(date).strftime('%d')
        month = datetime.date(date).strftime('%b')
        columns.append(_(day + '/' + month) + ":Data/:70")
    columns.append(_("Total") + ":Data/:70")
    columns.append(_("Basic") + ":Data/:70")
    columns.append(_("OT_Amount") + ":Data/:100")
    return columns

def get_data(filters):
    data = []
    employees = get_employees(filters)
    if filters.employee_type != 'CL':
        frappe.errprint('yes')
        for emp in employees:
            dates = get_dates(filters.from_date,filters.to_date)
            if frappe.db.exists("Overtime Request",{'ot_date':('in',dates),'employee':emp.name,'workflow_state':'Approved'}):
                row = [emp.name,emp.employee_name,emp.department,emp.date_of_joining]
                total_ot = timedelta(0,0,0)
                for date in dates:
                    ot = frappe.db.get_value("Overtime Request",{'ot_date':date,'employee':emp.name,'workflow_state':'Approved'},'ot_hours') or ''
                    if ot:
                        total_ot += ot
                        day = ot.days * 24
                        hours = day + ot.seconds // 3600
                        minutes = (ot.seconds//60)%60
                        ftr = [3600,60,1]
                        hr = (sum([a*b for a,b in zip(ftr, map(int,str(str(hours) +':'+str(minutes)+':00').split(':')))]))/3600
                        row.append(hr)
                    else:
                        row.append('-')
                day = total_ot.days * 24
                hours = day + total_ot.seconds // 3600
                minutes = (total_ot.seconds//60)%60
                ftr = [3600,60,1]
                total_ot_hr = (sum([a*b for a,b in zip(ftr, map(int,str(str(hours) +':'+str(minutes)+':00').split(':')))]))/3600
                row.append(total_ot_hr)
                # if emp.employee_type != 'CL':
                ot_amount = (((emp.basic/26)/8)*2)*total_ot_hr
                # else:
                    # if emp.designation == 'Skilled':
                    #     ot_amount = 116 * total_ot_hr
                    # elif emp.designation == 'Un Skilled':
                    #     ot_amount = 112 * total_ot_hr
                row.append(emp.basic)
                row.append(floor(ot_amount))
                data.append(row)
    else:
        frappe.errprint('cl')
        for emp in employees:
            total_ot_hr = 0
            dates = get_dates(filters.from_date,filters.to_date)
            if frappe.db.exists("Overtime Request",{'ot_date':('in',dates),'employee':emp.name,'workflow_state':'Approved'}):
                row = [emp.name,emp.employee_name,emp.department,emp.date_of_joining]
                for date in dates:
                    ot = frappe.db.get_value("Overtime Request",{'ot_date':date,'employee':emp.name,'workflow_state':'Approved'},'ot_hours') or ''
                    if ot:
                        day = ot.days * 24
                        hours = day + ot.seconds // 3600
                        minutes = (ot.seconds//60)%60
                        ftr = [3600,60,1]
                        hr = (sum([a*b for a,b in zip(ftr, map(int,str(str(hours) +':'+str(minutes)+':00').split(':')))]))/3600
                        row.append(hr)
                        total_ot_hr += hr
                    else:
                        row.append('-')

                row.append(total_ot_hr)
                ot_amount = frappe.db.sql("select sum(ot_amount) as total from `tabOvertime Request` where ot_date between '%s' and '%s' and docstatus = 'Approved' and employee = '%s' "%(filters.from_date,filters.to_date,emp.name),as_dict=True)[0].total or 0
                row.append(emp.basic)
                row.append(floor(ot_amount))
                data.append(row)
    return data

def get_dates(from_date,to_date):
    no_of_days = date_diff(add_days(to_date, 1), from_date)
    dates = [add_days(from_date, i) for i in range(0, no_of_days)]
    return dates

def get_employees(filters):
    conditions = ''
    if filters.department:
        conditions += "and department = '%s' "%filters.department
    if filters.employee_type:
        conditions += "and employee_type = '%s' "%filters.employee_type
    if filters.employee:
        conditions += "and employee = '%s' "%filters.employee
    employees = frappe.db.sql("""select name, basic, employee_name, department, date_of_joining,employee_type,designation from `tabEmployee` where status = 'Active' %s and vacant = 0 """%(conditions),as_dict=True)
    left_employees = frappe.db.sql("""select name, basic, employee_name, department, date_of_joining,employee_type from `tabEmployee` where status = 'Left' and relieving_date >= %s %s and vacant = 0 """%(filters.from_date,conditions),as_dict=True)
    employees.extend(left_employees)
    return employees
