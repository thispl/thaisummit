# Copyright (c) 2013, TEAMPRO and contributors
# For license information, please see license.txt

import frappe
from datetime import date, timedelta
from frappe import msgprint, _
from frappe.utils import cstr, cint, getdate
from frappe.utils import cstr, add_days, date_diff, getdate
from datetime import date, timedelta, datetime

def execute(filters=None):
    columns = get_columns(filters)
    data = get_shift(filters)
    return columns,data

def get_columns(filters):
    columns = [_("Department") + ":Data/:200"]
    no_of_days = date_diff(add_days(filters.to_date, 1), filters.from_date)
    dates = [add_days(filters.from_date, i) for i in range(0, no_of_days)]
    for date in dates:
        # date = datetime.strptime(date, "%Y-%m-%d") # start date
        columns.append(_(date) + ":Data/:150",)
    return columns

def get_shift(filters):
    data = []
    department = frappe.get_all("Department",{"is_group":"0"})
    for dept in department:
        no_of_days = date_diff(add_days(filters.to_date, 1), filters.from_date)
        dates = [add_days(filters.from_date, i) for i in range(0, no_of_days)]
        count_list = [dept.name]
        for d in dates:
            count = frappe.db.count("Shift Assignment",{"start_date":d,"department":dept.name ,"docstatus":'1' })
            # shifts = frappe.db.sql("""select count(shift_type) as count,department from `tabShift Assignment` where department = '%s' and docstatus = '1' """%(dept.name),as_dict=True)
            count_list.append(count)
        data.append(count_list)
        # frappe.errprint()
    return data
            
        
