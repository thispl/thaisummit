import frappe
from frappe.utils import data
from frappe.utils import cstr, add_days, date_diff, getdate
from frappe.utils import format_date

@frappe.whitelist()
def get_cl_count(from_date,to_date):
    dates = get_dates(from_date,to_date)
    data = ""
    for date in dates:
        contractors = frappe.get_all('Contractor')
        for contractor in contractors:
            shift_1 = 0
            shift_2 = 0
            shift_3 = 0
            shift_pp1 = 0
            shift_pp2 = 0
            if frappe.db.exists('CL Head Count Plan',{'date':date,'contractor':contractor.name}):
                plan = frappe.get_doc('CL Head Count Plan',{'date':date,'contractor':contractor.name})
                shift_1 = plan.shift_1
                shift_2 = plan.shift_2
                shift_3 = plan.shift_3
                shift_pp1 = plan.shift_pp1
                shift_pp2 = plan.shift_pp2
            data += "<tr><td style = 'border: 1px solid black'>%s</td><td style = 'border: 1px solid black'>%s</td><td style = 'border: 1px solid black'>%s</td><td style = 'border: 1px solid black'>%s</td><td style = 'border: 1px solid black'>%s</td><td style = 'border: 1px solid black'>%s</td><td style = 'border: 1px solid black'>%s</td></tr>"%(format_date(date),contractor.name,shift_1,shift_2,shift_3,shift_pp1,shift_pp2)
    return data

def get_dates(from_date,to_date):
    no_of_days = date_diff(add_days(to_date, 1), from_date)
    dates = [add_days(from_date, i) for i in range(0, no_of_days)]
    return dates