import frappe
from frappe import _, msgprint
from frappe.utils import (fmt_money, formatdate, format_time, now_datetime,
	get_url_to_form, get_url_to_list, flt, get_link_to_report, add_to_date, today)
from datetime import timedelta

def execute(filters=None):
    columns = get_columns()
    data = []
    food_scan = get_data(filters)
    for first in food_scan:
        data.append(first)
    return columns, data

def get_columns():
    columns = [
        _('Date') +':Data:100',_('Time') +':Data:100',_('ID ') +':Data:100',_('Name') +':Data:250',
        _('Department') +':Data:200',_('Food') +':Data:200',_('Boarding Type') +':Data:100',_('Route No') +':Data:100',_('Type') +':Data:150',_('Party Name') +':Data:100',_('Reference TSA ID ') +':Data:175',
        _('Reference Employee Name') +':Data:200',_('Reference Employee Department') +':Data:200',_('Price') +':Currency:100'
		]
    return columns

def get_data(filters):
    data = []
    #data to get from food_scan doctype
    if filters.menu:
        food_scan = frappe.db.get_all('Food Scan',{'date':('between',(filters.date,filters.to_date)),'food':filters.menu},['*'],order_by='date asc')
    if not filters.menu:
        food_scan = frappe.db.get_all('Food Scan',{'date':('between',(filters.date,filters.to_date))},['*'],order_by='date asc')
    # if filters.employee:  
    #     food_scan = frappe.db.get_all('Food Scan',{'date':('between',(filters.date,filters.to_date)),'food':filters.menu,'id':filters.employee},['*'],order_by='date asc')  
    # if not filters.employee:
    #     food_scan = frappe.db.get_all('Food Scan',{'date':('between',(filters.date,filters.to_date)),'food':filters.menu},['*'],order_by='date asc')    
    for first in food_scan:
        emp = frappe.db.get_value('Employee',{'status':'Active','employee_number':first.id},['boarding_non_boarding','route_no'])
        if emp:
            row = [formatdate(first.date),format_time(first.time),first.id,first.name1,first.cdepartment,first.food,emp[0] or '',emp[1] or '',first.type,
            first.party_name,first.tsa_id,first.employee_name,first.department,first.price]
            data.append(row)
        else:
            row = [formatdate(first.date),format_time(first.time),first.id,first.name1,first.cdepartment,first.food,'', '',first.type,
            first.party_name,first.tsa_id,first.employee_name,first.department,first.price]
            data.append(row)

    return data 

