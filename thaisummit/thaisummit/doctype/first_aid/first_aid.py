# Copyright (c) 2022, TEAMPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import cstr
from datetime import date, timedelta, datetime, time
from frappe.utils import flt, cstr, cint, comma_and, today, getdate, formatdate, now


class FirstAid(Document):
	pass

@frappe.whitelist()
def get_previous_entry(emp,name):
    data  = ''
    previous_entry = frappe.db.exists('First Aid',{'id_no':emp},{'employee_name':name})
    first_aid_previous = frappe.db.get_value('First Aid',{'name':previous_entry},['id_no','employee_name','date','symptoms','prescription'])

    medicine_child_table = frappe.db.sql(""" select `tabMedicine Table` .medicine as medicine, `tabMedicine Table` .quantity as quantity,`tabMedicine Table` .uom as uom from `tabFirst Aid` 
                        left join `tabMedicine Table`  on `tabFirst Aid`.name = `tabMedicine Table`.parent where `tabFirst Aid`.id_no = '%s' and  `tabFirst Aid` .date = '%s'  """%(first_aid_previous[0],first_aid_previous[2]),as_dict=True)
    data = "<table class='table table-bordered=1>"
    data += "<tr style='font-size:10px;padding:1px'><td style ='background-color:#ffedcc;border:1px solid black'>Emp ID</td><td style ='background-color:#ffedcc;border:1px solid black'>Employee Name</td><td style ='background-color:#ffedcc;border:1px solid black'>Date</td><td style ='background-color:#ffedcc;border:1px solid black'>Symptoms</td><td style ='background-color:#ffedcc;border:1px solid black'>Prescription</td><td style ='background-color:#ffedcc;border:1px solid black'>Medicine</td><td style ='background-color:#ffedcc;border:1px solid black'>Quantity</td><td style ='background-color:#ffedcc;border:1px solid black'>UOM</td></tr>"
    for medicine in medicine_child_table: 
        data += "<tr style='font-size:10px;padding:1px'><td style ='background-color:#FFFFFF;border:1px solid black'>%s</td><td style ='background-color:#FFFFFF;border:1px solid black'>%s</td><td style ='background-color:#FFFFFF;border:1px solid black'>%s</td><td style ='background-color:#FFFFFF;border:1px solid black'>%s</td><td style ='background-color:#FFFFFF;border:1px solid black'>%s</td><td style ='background-color:#FFFFFF;border:1px solid black'>%s</td><td style ='background-color:#FFFFFF;border:1px solid black'>%s</td><td style ='background-color:#FFFFFF;border:1px solid black'>%s</td></tr>"%(first_aid_previous[0],first_aid_previous[1],formatdate(first_aid_previous[2]),first_aid_previous[3],first_aid_previous[4],medicine.medicine,medicine.quantity,medicine.uom)    
    data += "<table>"
    return data
