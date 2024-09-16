# -*- coding: utf-8 -*-
# Copyright (c) 2021, TEAMPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import today,flt,cint, getdate, get_datetime
from datetime import timedelta,datetime

no_cache = 1

def get_context(context):
    frappe.log_error(title='taglist',message=get_tag_list())
    if frappe.session.user != 'Guest':
        context.tag_list = get_tag_list()
        
@frappe.whitelist()
def get_tag_list():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    month_start = (datetime.today()).strftime("%Y-%m-01 08:00:00")
    today_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
    total_tbs = frappe.db.sql("""select parts_no,recieved_time,parts_name,name,required_quantity,sap_quantity,difference,model,date_and_time,mat_no,delay_duration,reason_for_card_delay,model_number,readiness_qty,readiness_diff from `tabTAG Master` where item_delivered = 0 and delivery_status != 'Cancelled' order by name""",as_dict=True)
    total_tbs_today = frappe.db.sql("""select name from `tabTAG Master` where date(recieved_time) = CURDATE() and (hour(recieved_time) between 8 and '%s') and delivery_status != 'Cancelled' """ % (current_time),as_dict=True)
    total_tbs_month = frappe.db.sql("""SELECT name FROM `tabTAG Master` WHERE delivery_status != 'Cancelled' and recieved_time between '%s' and '%s' """%(str(month_start),str(today_datetime)),as_dict=True)
    updated_tbs_list = []
    updated_tbs_dict = {}
    failure = failure_percent = failure_month = failure_percent_month = 0
    tbs_ontime = tbs_delay = 0
    # recieved = month_start
    recieved = len(total_tbs_today)
    recieved_month = len(total_tbs_month)
    delay_percent = delay_percent_monthly = 0
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
        updated_tbs_dict['model'] = tbs['model_number']
        updated_tbs_dict['recieved_time'] = tbs['recieved_time'].strftime("%d/%m/%Y %H:%M:%S")
        updated_tbs_dict['mat_no'] = tbs['mat_no']
        updated_tbs_dict['delay_duration'] = tbs['delay_duration']
        updated_tbs_dict['time_taken'] = time_taken - timedelta(microseconds=time_taken.microseconds)
        updated_tbs_dict['status'] = status
        updated_tbs_dict['readiness_qty'] = tbs['readiness_qty']
        updated_tbs_dict['readiness_diff'] = cint(tbs['readiness_diff'])
        updated_tbs_dict['reason_for_card_delay'] = "" if tbs['reason_for_card_delay'] == None else tbs['reason_for_card_delay']
        updated_tbs_list.append(updated_tbs_dict.copy())
    
    on_time_sent = frappe.db.sql(""" select count(sent) as count from `tabTAG Master` where item_delivered = 1 and date(recieved_time) = CURDATE() and (hour(recieved_time) between 8 and '%s')"""% (current_time),as_dict=True)[0]
    on_time_sent_monthly = frappe.db.sql(""" select count(sent) as count from `tabTAG Master` where item_delivered = 1 and recieved_time between '%s' and '%s' """%(str(month_start),str(today_datetime)),as_dict=True)[0]
    delay_sent = frappe.db.sql(""" select count(sent) as count from `tabTAG Master` where item_delivered = 1 and sent = 'Delay' and date(recieved_time) = CURDATE() and (hour(recieved_time) between 8 and '%s')"""% (current_time),as_dict=True)[0]
    delay_sent_monthly = frappe.db.sql(""" select count(sent) as count from `tabTAG Master` where item_delivered = 1 and sent = 'Delay' and date_and_time between '%s' and '%s' """%(str(month_start),str(today_datetime)),as_dict=True)[0]
    # if recieved:
    #     delay_percent = round((tbs_delay/recieved)*100, 2)
   
    current_datetime =datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    if recieved:
        failure = recieved - on_time_sent['count'] - tbs_ontime
        failure_percent = round((failure/recieved)*100, 2) 
        failure_month = recieved_month - on_time_sent_monthly['count'] - tbs_ontime
        failure_percent_month = round((failure_month/recieved_month)*100, 2)

    data = [updated_tbs_list,current_datetime,recieved,on_time_sent['count'],tbs_ontime,failure,failure_percent,(failure + delay_sent['count']),recieved_month,on_time_sent_monthly['count'],failure_month,failure_percent_month,(failure_month + delay_sent_monthly["count"])]
    frappe.log_error(title='taglist',message=data)
    return data

@frappe.whitelist()
def chop_microseconds(delta):
    return delta - datetime.timedelta(microseconds=delta.microseconds)