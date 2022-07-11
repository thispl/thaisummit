import frappe
from frappe import _, msgprint

def execute(filters=None):
    columns = get_columns()
    data = []
    cl_return_form = get_data(filters)
    for first in cl_return_form :
        data.append(first)
    return columns, data

def get_columns():
    columns = [
        _('Date') +':Data:100',_('Time') +':Data:100',_('Enter ID') +':Data:100',_('Employee Name') +':Data:200',_('Department') +':Data:200',
        _('Remarks') +':Data:1000'
    ]
    return columns

def get_data(filters):
    data = []
    #data to get from cl_return_form doctype
    cl_return_form = frappe.db.get_all('CL Return Form',{'date':('between',(filters.date,filters.to_date))},['*'],order_by='date asc')
    #using for loop to list the data 
    for first in cl_return_form:
        row = [first.date.strftime('%d-%m-%Y'),first.time,first.enter_id,first.employee_name,first.department,first.remarks]
        data.append(row)
    return data 


