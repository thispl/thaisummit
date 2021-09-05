# Copyright (c) 2013, TEAMPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import cstr, cint, getdate, get_last_day, get_first_day, add_days, date_diff
from frappe import msgprint, _
from calendar import monthrange
from datetime import date, timedelta, datetime

def execute(filters=None):
    if not filters: filters = {}

    # conditions, filters = get_conditions(filters)
    columns, days = get_columns(filters)
    # data = [["WELD-RE - TSAIP","FORD - TSAIP","1","1","1","3","2"]]
    data = add_department(filters)

    return columns, data, None, None


def get_columns(filters):

    columns = []

    columns += [
        _("Department") + ":Department:150",
    ]
    days = []

    from_date = datetime.strptime(filters.from_date, "%Y-%m-%d")   # start date
    to_date = datetime.strptime(filters.to_date,  "%Y-%m-%d")       # end date

    delta = to_date - from_date       # as timedelta

    for i in range(delta.days + 1):
    # for i in range(2):
        day = from_date + timedelta(days=i)
        day_name = day_abbr[getdate(day).weekday()]
        days.append(cstr(day.day)+ " " +day_name + "::300")
        # for employee_type in ["WC","BC","FT","NT","CL","TT"]:
            # days.append(cstr(day.day)+ " " +day_name + "-" + employee_type + "::100")
    columns += days
    # frappe.errprint(columns)



    # # if filters.summarized_view:
    # 	columns += [_("Calendar Days") + ":Float:120", _("Worked Days") + ":Float:120",  
    # 	_("WW/HH") + ":Float:120", _("CL") + ":Float:120", _("SL") + ":Float:120", _("EL") + ":Float:120", _("LOP") + ":Float:120", 
    # 	_("Wrong Shift")+ ":Float:120",_("Payable Days")+ ":Float:120", ]
    
    return columns, days

def add_department(filters):
    direct_re = ["WELD-RE - TSAIP","Weld-RE P1E - TSAIP","Weld-RE J LINE - TSAIP","WELD-RE J LINE 2 - TSAIP","PRESS-RE - TSAIP"]
    data = add_data(filters,direct_re)
    data += add_total_data(filters,direct_re,"Total Direct RE")

    support_re = ["QA-RE - TSAIP","PPC-RE - TSAIP","BOP-RE - TSAIP","NPD-RE - TSAIP","JIGS MTN-RE - TSAIP","SALES-RE - TSAIP"]
    data += add_data(filters,support_re)
    data += add_total_data(filters,support_re,"Total Support RE")

    total_re = ["WELD-RE - TSAIP","Weld-RE P1E - TSAIP","Weld-RE J LINE - TSAIP","WELD-RE J LINE 2 - TSAIP","PRESS-RE - TSAIP","QA-RE - TSAIP","PPC-RE - TSAIP","BOP-RE - TSAIP","NPD-RE - TSAIP","JIGS MTN-RE - TSAIP","SALES-RE - TSAIP"]
    data += add_total_data(filters,total_re,"Total RE")

    direct_iym = ["WELD-IYM - TSAIP","HPS LINE - TSAIP","PRESS-IYM - TSAIP"]
    data = add_data(filters,direct_iym)
    data += add_total_data(filters,direct_iym,"Total Direct IYM")

    support_iym = ["QA-IYM - TSAIP","PPC-IYM - TSAIP","BOP-IYM - TSAIP","SALES-IYM - TSAIP","JIGS MTN-IYM - TSAIP","NPD-IYM - TSAIP"]
    data += add_data(filters,support_iym)
    data += add_total_data(filters,support_iym,"Total Support IYM")

    total_iym = ["WELD-IYM - TSAIP","HPS LINE - TSAIP","PRESS-IYM - TSAIP","QA-IYM - TSAIP","PPC-IYM - TSAIP","BOP-IYM - TSAIP","SALES-IYM - TSAIP","JIGS MTN-IYM - TSAIP","NPD-IYM - TSAIP"]
    data += add_total_data(filters,total_iym,"Total IYM")

    return data


def add_data(filters,depts):
    from_date = datetime.strptime(filters.from_date, "%Y-%m-%d")   # start date
    to_date = datetime.strptime(filters.to_date,  "%Y-%m-%d")       # end date

    no_of_days = date_diff(add_days(to_date, 1), from_date)
    dates = [add_days(from_date, i) for i in range(0, no_of_days)]

    count = []
    for dept in depts:
        row = []
        row.append(dept)
        for date in dates:
            d = ''
            for emp_type in ["WC","BC","FT","NT","CL","TT"]:
                if emp_type != "TT":
                    c = frappe.db.count("Attendance",{'employee_type':emp_type,"attendance_date":date,"department":dept,"status":"Present"})
                    d += '%s'%emp_type + ':' + str(c)+ ' | '
                else:
                    c = frappe.db.count("Attendance",{"attendance_date":date,"department":dept,"status":"Present"})
                    d += '%s'%emp_type + ':' + str(c)+ ' | '
            row.append(d)

        count += [row]

    return count

def add_total_data(filters,depts,title):
    from_date = datetime.strptime(filters.from_date, "%Y-%m-%d")   # start date
    to_date = datetime.strptime(filters.to_date,  "%Y-%m-%d")       # end date

    no_of_days = date_diff(add_days(to_date, 1), from_date)
    dates = [add_days(from_date, i) for i in range(0, no_of_days)]
    count = []
    row = []
    row.append(title)
    for date in dates:
        for emp_type in ["WC","BC","FT","NT","CL","TT"]:
            if emp_type != "TT":
                c = frappe.db.count("Attendance",{'employee_type':emp_type,"attendance_date":date,"department":['in',depts],"status":"Present"})
                row.append(c)
            else:
                c = frappe.db.count("Attendance",{"attendance_date":date,"department":['in',depts],"status":"Present"})
                row.append(c)

    count += [row]

    return count


# def get_conditions(filters):
# 	# if not (filters.get("month") and filters.get("year")):
# 	# 	msgprint(_("Please select month and year"), raise_exception=1)

# 	from_date = datetime.strptime(filters.from_date, "%Y-%m-%d")   # start date
# 	to_date = datetime.strptime(filters.to_date,  "%Y-%m-%d")       # end date

# 	delta = to_date - from_date       # as timedelta

# 	filters["total_days_in_month"] = delta.days + 1

# 	conditions = " and attendance_date between %s and %s"
# 	# conditions = " and attendance_date between %(from_date)s and %(to_date)s"

# 	if filters.get("company"): conditions += " and company = %s"
# 	if filters.get("employee"): conditions += " and employee = %s"

# 	# if filters.get("company"): conditions += " and company = %(company)s"
# 	# if filters.get("employee"): conditions += " and employee = %(employee)s"

# 	return conditions, filters

day_abbr = [
    "Mon",
    "Tue",
    "Wed",
    "Thu",
    "Fri",
    "Sat",
    "Sun"
]