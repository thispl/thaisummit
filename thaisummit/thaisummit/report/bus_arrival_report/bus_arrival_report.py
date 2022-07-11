import frappe
from frappe import _, msgprint


def execute(filters=None):
    columns = get_columns()
    data = []
    bus_arrival_form = get_data(filters)
    for bus in bus_arrival_form :
        data.append(bus)
    return columns, data

def get_columns():
    columns = [
        _('Date') +':Data:100',_('Time') +':Data:100',_('Route No Route Name') +':Data:400',_('Bus Number') +':Data:150',
        _('Shift') + ':Data:150',_('Status') +':Data:100',_('Late Minutes') +':Data:100'
    ]
    return columns

def get_data(filters):
    data = []
    #data to get from bus_arrival_form doctype
    bus_arrival_form = frappe.db.get_all('Bus Arrival Form',{'date':('between',(filters.date,filters.to_date))},['*'],order_by='date asc')
    #using for loop to list the data 
    for bus in bus_arrival_form:
        row = [bus.date.strftime('%d-%m-%Y'),bus.time,bus.route_no_route_name,bus.bus_number,bus.shift,bus.status,bus.late_minutes]
        data.append(row)
    return data 
