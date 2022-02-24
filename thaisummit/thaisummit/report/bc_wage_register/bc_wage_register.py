# Copyright (c) 2013, TEAMPRO and contributors
# For license information, please see license.txt

import frappe
from datetime import date, timedelta
from frappe import get_request_header, msgprint, _
from frappe.utils import cstr, cint, getdate
from frappe.utils import cstr, add_days, date_diff, getdate
from datetime import date, timedelta, datetime

def execute(filters=None):
    columns = get_columns(filters)
    data = get_data(filters)
    return columns ,data

def get_dates(filters):
    no_of_days = date_diff(filters.to_date,filters.from_date)
    dates = [add_days(filters.from_date,i) for i in range(0,no_of_days) ]


def get_columns(filters):
    columns = [_("Cost Centre") + ":Data/:100",_("Emp No") + ":Data/:100",_("Name") + ":Data/:150",_("DOJ") + ":Date/:100",_("Department") + ":Data/:150",_("Section") + ":Data/:100",_("Designation") + ":Data/:150",
    _("Category") + ":Data/:100",_("Paid days 100%") + ":Data/:100",_("Basic & DA") + ":Currency/:100",_("House Rent Allowance") + ":Currency/:100",_("Other Allowance") + ":Currency/:100",
    _("Position All") + ":Currency/:100",_("Gross Wage") + ":Currency/:100",_("Basic") + ":Currency/:100",_("HRA") + ":Currency/:100",_("Other Allowance") + ":Currency/:100",_("Position All") + ":Currency/:100",_("ATA") + ":Currency/:100",
    _("SHT") + ":Currency/:100",_("ARR") + ":Currency/:100",_("Additional Allowance") + ":Currency/:150",_("PP Allowance") + ":Currency/:100",_("Transport Allowance") + ":Currency/:100",_("Others") + ":Currency/:100",_("Gross") + ":Currency/:100",_("PF") + ":Currency/:100",_("ESI") + ":Currency/:100",
    _("Can") + ":Currency/:100",_("P Tax") + ":Currency/:100",_("LWF") + ":Currency/:100",_("TEL EXP") + ":Currency/:100",_("PPE") + ":Currency/:100",_("Advance") + ":Currency/:100",_("Total Deduction") + ":Currency/:100",_("Net Wage") + ":Currency/:100"]
    return columns

def get_data(filters):
    data =[]
    row = []
    basic_component_amount = earning_component_amount = deduction_component_amount = gross_wage = total_deduction = 0
    salary_comp = ['Basic','House Rent Allowance','Other Allowance','Position Allowance']

    earning_comp = ['Basic','House Rent Allowance','Other Allowance','Position Allowance','Attendance Bonus','Shift Allowance','Arrear','Additional Allowance','PPE Allowance','Transport Allowance']
    dedcution_comp = ['Provident Fund','Employee State Insurance','Canteen Charges','Professional Tax','LWF','TELEXP','PPE','ADV']

    if filters.department:
        salary_slips = frappe.get_all("Salary Slip",{'employee_type':'BC','department':filters.department,'start_date':filters.from_date,'end_date':filters.to_date},['*'])	

    if filters.employee:
        salary_slips = frappe.get_all("Salary Slip",{'employee_type':'BC','employee':filters.employee,'start_date':filters.from_date,'end_date':filters.to_date},['*'])	
    
    else:
        salary_slips = frappe.get_all("Salary Slip",{'employee_type':'BC','start_date':filters.from_date,'end_date':filters.to_date},['*'])	

    for ss in salary_slips:
        row = []
        cost_center = frappe.get_value('Department',ss.department,'cost_centre')
        section = ''
        emp = frappe.get_doc("Employee",ss.employee)
        paid_days = ss.payment_days
        row += [cost_center,emp.name,emp.employee_name,emp.date_of_joining,emp.department,section,emp.designation,emp.employee_type,paid_days,emp.basic,emp.house_rent_allowance,emp.other_allowance,emp.position_allowance,emp.basic+emp.house_rent_allowance+emp.other_allowance+emp.position_allowance]
        gross_wage_ec = 0
        
        for ec in earning_comp:
            
            earning_component_amount = frappe.get_value('Salary Detail',{'salary_component':ec,'parent':ss.name},['amount'])
            if earning_component_amount:
                row += [earning_component_amount]	
                gross_wage_ec += earning_component_amount
            else:
                row += ['']

        row += [frappe.get_value('Salary Detail',{'salary_component':'Others','parent':ss.name},['amount']),ss.gross_pay]
        total_deduction =0
        for dc in dedcution_comp:
            deduction_component_amount = frappe.get_value('Salary Detail',{'salary_component':dc,'parent':ss.name},['amount'])
            if deduction_component_amount:
                row += [deduction_component_amount]
                total_deduction += deduction_component_amount
            else:
                row += ['']
        
        
        row += [ total_deduction ]
        row += [ ss.net_pay ]

        data.append(row) 
    return data
    
    