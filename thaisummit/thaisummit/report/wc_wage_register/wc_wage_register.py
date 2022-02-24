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
    columns = [_("Emp No") + ":Data/:100",_("Cost Centre No") + ":Data/:150",_("Cost Centre Name") + ":Data/:150",_("DOJ") + ":Date/:100",_("Employee_Name") + ":Data/:150",_("Designation") + ":Data/:150",
    _("Payable") + ":Data/:100",_("CTC 100%") + ":Data/:100",_("Basic Salary") + ":Currency/:100",_("HRA") + ":Currency/:100",_("Conveyance") + ":Currency/:100",_("Special Allowance") + ":Currency/:150",_("Medical Allowance") + ":Currency/:150",
    _("LTA") + ":Currency/:100",_("Children Allowance") + ":Currency/:150",_("Chidren Hostel") + ":Currency/:100",_("Washing") + ":Currency/:100",_("Gross Salary") + ":Currency/:100",_("BAS") + ":Currency/:100",_("HRA") + ":Currency/:100",_("CON") + ":Currency/:100",_("SPA") + ":Currency/:100",_("MED") + ":Currency/:100",
    _("LTA") + ":Currency/:100",_("Children Allowance") + ":Currency/:150",_("Chidren Hostel") + ":Currency/:100",_("Washing") + ":Currency/:100",("Position Allowance") + ":Currency/:150",_("ARR") + ":Currency/:100",_(" Other ARR") + ":Currency/:100",_("ATA") + ":Currency/:100",_("SHT") + ":Currency/:100",_("Transport Allowance") + ":Currency/:100",_("Other(Extra hrs)") + ":Currency/:100",_("GROSS") + ":Currency/:100",_("PF") + ":Currency/:100",_("ESI") + ":Currency/:100",
    _("CAN") + ":Currency/:100",_("PTAX") + ":Currency/:100",_("LWF") + ":Currency/:100",_("TDS") + ":Currency/:100",_("Arrears TDS") + ":Currency/:150",_("TEL EXP") + ":Currency/:100",_("Other Dedu") + ":Currency/:100",_("TOTAL") + ":Currency/:100",_("Earned & Net Salary") + ":Currency/:150",_("Bonus") + ":Currency/:100",_("Other(Extra hrs)") + ":Currency/:150",_("For P Tax Earnings") + ":Currency/:200"]
    return columns

def get_data(filters):
    data =[]
    row = []
    basic_component_amount = earning_component_amount = deduction_component_amount = gross_wage = total_deduction = 0

    salary_comp = ['Basic','House Rent Allowance','Conveyance Allowance','Special Allowance','Medical Allowance','Leave Travel Allowance','Children Education','Children Hostel','Washing Allowance']

    earning_comp = ['Basic','House Rent Allowance','Conveyance Allowance','Special Allowance','Medical Allowance','Leave Travel Allowance','Children Education','Children Hostel','Washing Allowance','Position Allowance','Arrear','Other Arrear','Attendance Bonus','Shift Allowance','Transport Allowance','Others']

    dedcution_comp = ['Provident Fund','Employee State Insurance','Canteen Charges','Professional Tax','LWF','Tax Deducted at Source','Arrear TDS','TEL EXP','Other Deduction']

    if filters.department:
        salary_slips = frappe.get_all("Salary Slip",{'employee_type':'WC','department':filters.department,'start_date':filters.from_date,'end_date':filters.to_date},['*'])	

    if filters.employee:
        salary_slips = frappe.get_all("Salary Slip",{'employee_type':'WC','employee':filters.employee,'start_date':filters.from_date,'end_date':filters.to_date},['*'])	
    
    else:
        salary_slips = frappe.get_all("Salary Slip",{'employee_type':'WC','start_date':filters.from_date,'end_date':filters.to_date},['*'])	

    for ss in salary_slips:
        row = []
        cost_center = frappe.get_value('Department',ss.department,'cost_centre')
        emp = frappe.get_doc("Employee",ss.employee)
        row += [emp.name,cost_center,emp.department,emp.date_of_joining,emp.employee_name,emp.designation,ss.payment_days,emp.ctc,emp.basic,emp.house_rent_allowance,emp.conveyance_allowance,emp.special_allowance,emp.medical_allowance,emp.leave_travel_allowance,emp.children_education,emp.children_hostel,emp.washing_allowance,emp.basic+emp.house_rent_allowance+emp.conveyance_allowance+emp.special_allowance+emp.medical_allowance+emp.leave_travel_allowance+emp.children_education+emp.children_hostel+emp.washing_allowance]
            
        for ec in earning_comp:
            earning_component_amount = frappe.get_value('Salary Detail',{'salary_component':ec,'parent':ss.name},['amount'])
            if earning_component_amount:
                row.append(earning_component_amount)
            else:
                row.append('')
        row += [ss.gross_pay]
        total_deduction =0
        for dc in dedcution_comp:
            deduction_component_amount = frappe.get_value('Salary Detail',{'salary_component':dc,'parent':ss.name},['amount'])
            if deduction_component_amount:
                row += [deduction_component_amount]
                total_deduction += deduction_component_amount
            else:
                row += ['']
            bonus_vaue = frappe.get_value('Salary Detail',{'salary_component':'Basic','parent':ss.name},['amount']) or 0
            bonus = round(bonus_vaue/12)

        row += [ss.total_deduction]
        row += [ ss.net_pay ]
        row += [ bonus ]
        row += [ frappe.get_value('Salary Detail',{'salary_component':'Others','parent':ss.name},['amount']) ]
        row += [ss.gross_pay]

        data.append(row) 
    return data
    
    