# Copyright (c) 2013, TEAMPRO and contributors
# For license information, please see license.txt

from datetime import datetime
import frappe
from frappe import _, msgprint
from frappe.utils import cstr, cint, getdate, get_last_day, get_first_day,add_days
from frappe.utils import cstr, add_days, date_diff, getdate, format_date

def execute(filters=None):
    columns,data = [],[]
    columns = get_columns(filters)
    data = get_data(filters)
    return columns, data


def get_columns(filters):
    columns = [
        _('Doc No') +':Data:100',_('Date') +':Data:100',_('Meal Type') +':Data:100',_('Plan Head Count') +':Data:100',_('Party Name') +':Data:100',
        _('Requester ID') +':Data:100',_('Requester Name') +':Data:100',_('Requester Department') +':Data:100'
    ]
    return columns
    

def get_data(filters):
    data = []
    dates = get_dates(filters.from_date,filters.to_date)
    for date in dates:
        if filters.menu:
            food_scan = frappe.db.get_all('Food Scan',{'date':date,'food':filters.menu},['name','id','food','party_name','tsa_id','employee_name','department'])
        if not filters.menu:
            food_scan = frappe.db.get_all('Food Scan',{'date':date,},['name','id','food','party_name','tsa_id','employee_name','department'])
        for food in food_scan:
            if food.food == 'Break Fast':
                if food.party_name:
                    bf_count = frappe.db.get_value('Food Plan',{'date':date},['bf_head_count'])
                    row1 = [food.name,date,food.food,bf_count,food.party_name,food.tsa_id,food.employee_name,food.department]
                    data.append(row1)
                    
            if food.food == 'Lunch':
                if food.party_name:
                    lu_count = frappe.db.get_value('Food Plan',{'date':date},['lu_head_count'])
                    row2 = [food.name,date,food.food,lu_count,food.party_name,food.tsa_id,food.employee_name,food.department]
                    data.append(row2)    
        
    return data




def get_dates(from_date,to_date):
    no_of_days = date_diff(add_days(to_date, 1), from_date)
    dates = [add_days(from_date, i) for i in range(0, no_of_days)]
    return dates

