import frappe
from frappe import _, msgprint

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
        _('Department') +':Data:200',_('Food') +':Data:200',_('Type') +':Data:150',_('Party Name') +':Data:100',_('Reference TSA ID ') +':Data:175',
        _('Reference Employee Name') +':Data:200',_('Reference Employee Department') +':Data:200',_('Price') +':Currency:100'
		]
    return columns

def get_data(filters):
    data = []
    #data to get from food_scan doctype
    food_scan = frappe.db.get_all('Food Scan',{'date':('between',(filters.date,filters.to_date))},['*'],order_by='date asc')
    for first in food_scan:
        row = [first.date.strftime('%d-%m-%Y'),first.time,first.id,first.name1,first.cdepartment,first.food,first.type,
        first.party_name,first.tsa_id,first.employee_name,first.department,first.price]
        data.append(row)
    return data 

