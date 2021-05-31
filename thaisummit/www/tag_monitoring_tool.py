# -*- coding: utf-8 -*-
# Copyright (c) 2021, TEAMPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import today,flt,cint, getdate, get_datetime
from datetime import timedelta,datetime

no_cache = 1

def get_context(context):
	if frappe.session.user != 'Guest':
		context.tag_list = get_tag_list()
        
@frappe.whitelist()
def get_tag_list():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    month_start = (datetime.today()).strftime("%Y-%m-01 08:00:00")
    today_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
    # frappe.errprint(month_start)
    # frappe.errprint(today_datetime)
    total_tbs = frappe.db.sql("""select parts_no,recieved_time,parts_name,name,required_quantity,sap_quantity,difference,model,date_and_time,mat_no,delay_duration from `tabTAG Master` where item_delivered = 0 and delivery_status != 'Cancelled' order by name""",as_dict=True)
    total_tbs_today = frappe.db.sql("""select name from `tabTAG Master` where date(recieved_time) = CURDATE() and (hour(recieved_time) between 8 and '%s') and item_delivered = 0 and delivery_status != 'Cancelled' """ % (current_time),as_dict=True)
    total_tbs_month = frappe.db.sql("""SELECT name FROM `tabTAG Master` WHERE item_delivered = 0 and delivery_status != 'Cancelled' and recieved_time between '%s' and '%s' """%(str(month_start),str(today_datetime)),as_dict=True)
    # frappe.errprint(total_tbs)
    # frappe.errprint(total_tbs_month)
    updated_tbs_list = []
    updated_tbs_dict = {}
    tbs_ontime = tbs_delay = 0
    # recieved = month_start
    recieved = len(total_tbs_today)
    recieved_month = len(total_tbs_month)
    percent = 0
    allowed_delay_duration = timedelta(seconds=cint(frappe.db.get_value("TAG Monitoring Management",None,"delay_duration")))
    for tbs in total_tbs:
        tag_entry_time = tbs['recieved_time']
        sap_quantity = frappe.get_value('Part Master',tbs['parts_no'],'temp_avl_qty')
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
        updated_tbs_dict['parts_no'] = tbs['parts_no']
        updated_tbs_dict['required_quantity'] = cint(tbs['required_quantity'])
        updated_tbs_dict['sap_quantity'] = tbs['sap_quantity']
        updated_tbs_dict['difference'] = cint(tbs['difference'])
        updated_tbs_dict['model'] = tbs['model']
        updated_tbs_dict['recieved_time'] = tbs['recieved_time'].strftime("%d/%m/%Y %H:%M:%S")
        updated_tbs_dict['mat_no'] = tbs['mat_no']
        updated_tbs_dict['delay_duration'] = tbs['delay_duration']
        updated_tbs_dict['time_taken'] = time_taken - timedelta(microseconds=time_taken.microseconds)
        updated_tbs_dict['status'] = status
        updated_tbs_list.append(updated_tbs_dict.copy())
    
    on_time_sent = frappe.db.sql(""" select count(sent) as count from `tabTAG Master` where sent = 'On Time Sent' and item_delivered = 1 and date(date_and_time) = CURDATE() and (hour(date_and_time) between 8 and '%s')"""% (current_time),as_dict=True)[0]
    on_time_sent_monthly = frappe.db.sql(""" select count(sent) as count from `tabTAG Master` where sent = 'On Time Sent' and item_delivered = 1 and recieved_time between '%s' and '%s' """%(str(month_start),str(today_datetime)),as_dict=True)[0]
    if recieved:
        percent = round((tbs_delay/recieved)*100, 2)
    current_datetime =datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    data = [updated_tbs_list,current_datetime,recieved,recieved_month,on_time_sent['count'],on_time_sent_monthly['count'],tbs_ontime,tbs_delay,percent]
    return data

@frappe.whitelist()
def chop_microseconds(delta):
    return delta - datetime.timedelta(microseconds=delta.microseconds)