from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import today,flt,cint, getdate, get_datetime
from datetime import timedelta,datetime


@frappe.whitelist()
def get_content():
        frappe.errprint("hi")
        total_tbs = frappe.db.sql(""" select parts_name,name,required_quantity,sap_quantity,difference,model,date_and_time,mat_no,delay_duration from `tabTAG Master` where date(date_and_time) = CURDATE() and item_delivered = 0""",as_dict=True)
        total_tbs_monthly = frappe.db.sql(""" select parts_name,name,required_quantity,sap_quantity,difference,model,date_and_time,mat_no,delay_duration from `tabTAG Master` where month(date_and_time) = month(CURDATE()) and item_delivered = 0""",as_dict=True)
        frappe.errprint("hi")
        updated_tbs_list = []
        updated_tbs_dict = {}
        tbs_ontime = tbs_delay = 0
        recieved = len(total_tbs)
        percent = 0
        allowed_delay_duration = timedelta(seconds=cint(frappe.db.get_value("TAG Monitoring Management",None,"delay_duration")))
        for tbs in total_tbs:
            tag_entry_time = tbs['date_and_time']
            current_time = datetime.now()
            time_taken = current_time - tag_entry_time
            time_allowed = time_taken - allowed_delay_duration
            if time_taken > allowed_delay_duration:
                tbs_delay += 1
                status = 'delay'
            else:
                tbs_ontime += 1
                status = 'on-time'
            updated_tbs_dict['parts_name'] = tbs['parts_name']
            updated_tbs_dict['name'] = tbs['name']
            updated_tbs_dict['required_quantity'] = tbs['required_quantity']
            updated_tbs_dict['sap_quantity'] = tbs['sap_quantity']
            updated_tbs_dict['difference'] = tbs['difference']
            updated_tbs_dict['model'] = tbs['model']
            updated_tbs_dict['date_and_time'] = tbs['date_and_time'].strftime("%d/%m/%Y %H:%M:%S")
            updated_tbs_dict['mat_no'] = tbs['mat_no']
            updated_tbs_dict['delay_duration'] = tbs['delay_duration']
            updated_tbs_dict['time_taken'] = time_taken - timedelta(microseconds=time_taken.microseconds)
            updated_tbs_dict['status'] = status
            updated_tbs_list.append(updated_tbs_dict.copy())
        
        on_time_sent = frappe.db.sql(""" select count(sent) as count from `tabTAG Master` where sent = 'On Time Sent' and date(date_and_time) = CURDATE() and item_delivered = 1""",as_dict=True)[0]
        if recieved:
            percent = round((tbs_delay/recieved)*100, 2)
        current_datetime =datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        