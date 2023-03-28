import frappe
from frappe import _, msgprint

def execute(filters=None):
	columns = get_columns()
	data = []
	first_aid = get_data(filters)
	for first in first_aid:
		data.append(first)
	return columns, data


def get_columns():
	columns = [
		_('Date') +':Data:100',_('Time') +':Data:100',_('ID No') +':Data:100',_('Employee Name') + ':Data:100',_('Department') + ':Data:100',
		_('Date of Birth') + ':Data:100',_('Age') + ':Data:100',_('Employee Type') + ':Data:100',_('Emergency Contact Person') + ':Data:100',
		_('Relationship') + ':Data:100',_('Emergency Phone') + ':Data:100',_('Blood Group') + ':Data:100',_('Symptoms') +':Data:200',_('Prescription') + ':Data:200',
		_('Medicine 1') +':Data:100',_('Quantity 1') +':Data:100',_('UOM 1') +':Data:100',
	

	]
	return columns

def get_data(filters):
	data = []
	aid = []
	#data to get from first_aid doctype
	if filters.id_no:
		frappe.db.get_all('First Aid',{'date':('between',(filters.date,filters.to_date)),'id_no':filters.id_no},['*'],order_by='date asc')
	else:
		frappe.db.get_all('First Aid',{'date':('between',(filters.date,filters.to_date))},['*'],order_by='date asc')
	#using for loop to list the data 
	first_aid = frappe.db.get_all('First Aid',{'date':('between',(filters.date,filters.to_date))},['*'])
	    
	
	for first in first_aid:
		medicine_list = frappe.db.sql(""" select `tabMedicine Table`.medicine , `tabMedicine Table`.quantity,`tabMedicine Table`.uom  from `tabFirst Aid` 
                        left join `tabMedicine Table` on `tabMedicine Table`.parent = `tabFirst Aid`.name """)
		for med in medicine_list:	
			row = [first.date.strftime('%d-%m-%Y'),first.time,first.id_no,first.employee_name,first.department,first.date_of_birth,first.age,first.employee_type,
				first.emergency_contact_person,first.relationship,first.emergency_phone,first.blood_group,first.symptoms,first.prescription,]
			med_list = [med[0],med[1],med[2]]
				
		# data.append(first_aid_med)
	return data	