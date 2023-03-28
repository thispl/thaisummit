# -*- coding: utf-8 -*-
# Copyright (c) 2021, TEAMPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import today,flt,cint, getdate, get_datetime,cstr,add_days
from datetime import timedelta,datetime,date,time
from erpnext.hr.utils import get_holiday_dates_for_employee
from frappe.utils import cint,today,flt,date_diff,add_days,add_months,date_diff,getdate,formatdate,cint,cstr



@frappe.whitelist()
def mark_checkin(employee=None):
    department = frappe.get_value('Employee',{'user_id':frappe.session.user},'department')
    qr_scanned_by = frappe.get_value('Employee',{'user_id':frappe.session.user},'name') + ':'
    qr_scanned_by += frappe.get_value('Employee',{'user_id':frappe.session.user},'employee_name')
    nowtime = datetime.now()
    shift_date = date.today()
    shift = frappe.db.get_value('Shift Type',{'name':'1'},['qr_start_time','qr_end_time'])
    shift1_time = [time(hour=shift[0].seconds//3600,minute=((shift[0].seconds//60)%60),second=0),time(hour=shift[1].seconds//3600,minute=((shift[1].seconds//60)%60),second=0)]
    shift2_time = [time(hour=15, minute=31, second=0),time(hour=19, minute=30, second=0)]
    shift3_time = [time(hour=00, minute=0, second=1),time(hour=4, minute=0, second=0)]
    shiftpp2_time = [time(hour=19, minute=31, second=0),time(hour=22, minute=30, second=0)]
    # shiftpp1_time = [time(hour=7, minute=0, second=0),time(hour=10, minute=0, second=0)]
    # shift2_cont_time = [time(hour=22, minute=1, second=0),time(hour=22, minute=59, second=0)]
    curtime = time(hour=nowtime.hour, minute=nowtime.minute, second=nowtime.second)
    shift_type = 'NA'
    if is_between(curtime,shift1_time):
        shift_type = '1'
    if is_between(curtime,shift2_time):
        shift_type = '2'
    if is_between(curtime,shift3_time):
        shift_type = '3'
        shift_date = shift_date + timedelta(days=-1)
    if is_between(curtime,shiftpp2_time):
        shift_type = 'PP2'
    
    if shift_type == 'NA':
        return 'Wrong Shift Time'
    
    planned_count = frappe.db.count('Shift Assignment',{'shift_type':shift_type,'start_date': shift_date, 'docstatus':1, 'department':department, 'employee_type':('!=','WC'),})
    actual_count = frappe.db.count('QR Checkin',{'qr_shift':shift_type,'ot':0,'shift_date': shift_date,'department':department})

    # emp = frappe.db.get_value('Employee',{'status':'Active','employee':employee},['name','basic','ctc','employee_type'])
    # start_date = frappe.db.get_value('Payroll Dates',{'name':'PAYROLL OT PERIOD DATE 0001'},['payroll_start_date'])
    # end_date = frappe.db.get_value('Payroll Dates',{'name':'PAYROLL OT PERIOD DATE 0001'},['payroll_end_date'])
    # holidays = len(get_holiday_dates_for_employee(emp[0],start_date,end_date))
    # total_working_days = date_diff(end_date,start_date) - holidays
    # if emp[3] != 'CL':
    #     if emp[1]:
    #         per_day_basic = emp[1] / total_working_days
    #     else:
    #         per_day_basic = 0   
    #     if emp[2]:    
    #         per_days_ctc = emp[2] / total_working_days 
    #     else:
    #         per_day_ctc = 0    
    # else:
    #     if emp[1]:
    #         per_day_basic = emp[1]
    #     else:
    #         per_day_basic = 0
    #     if emp[2]:        
    #         per_day_ctc = emp[2]  
    #     else:
    #         per_day_ctc = 0      


    existing_employee = frappe.db.exists('Employee',{'employee':employee, 'status':'Active','employee_type':('!=','WC')})
    if not existing_employee:
        return 'Employee Not Found'
    existing_checkin = frappe.db.exists('QR Checkin',{'employee':employee, 'shift_date':shift_date, 'qr_shift': shift_type})
    if existing_checkin:
        return 'Checkin Already Exists'    
    if get_ot_shift(shift_type,employee,shift_date) == 'OT':
        # emp = frappe.db.get_value('Employee',{'status':'Active','employee':employee},['name','basic','ctc','employee_type'])
        # start_date = frappe.db.get_value('Payroll Dates',{'name':'PAYROLL OT PERIOD DATE 0001'},['payroll_start_date'])
        # end_date = frappe.db.get_value('Payroll Dates',{'name':'PAYROLL OT PERIOD DATE 0001'},['payroll_end_date'])
        # holidays = len(get_holiday_dates_for_employee(emp[0],start_date,end_date))
        # total_working_days = date_diff(end_date,start_date) - holidays
        # if emp[3] != 'CL':
        #     if emp[1]:
        #         per_day_basic = emp[1] / total_working_days
        #     else:
        #         per_day_basic = 0   
        #     if emp[2]:    
        #         per_days_ctc = emp[2] / total_working_days 
        #     else:
        #         per_day_ctc = 0    
        # else:
        #     if emp[1]:
        #         per_day_basic = emp[1]
        #     else:
        #         per_day_basic = 0
        #     if emp[2]:        
        #         per_day_ctc = emp[2]  
        #     else:
        #         per_day_ctc = 0 
        employee_name,employee_type = frappe.get_value('Employee',employee,['employee_name','employee_type'])
        qr_checkin = frappe.new_doc('QR Checkin')
        qr_checkin.update({
            'employee': employee,
            'employee_name': employee_name,
            'department': frappe.get_value('Employee',{'user_id':frappe.session.user},'department'),
            'employee_type': employee_type,
            # 'basic':frappe.db.get_value('Employee',{'name':employee},['basic']),
            # 'ctc':frappe.db.get_value('Employee',{'name':employee},['ctc']),
            # 'per_day_basic':per_day_basic,
            # 'per_day_ctc':per_day_ctc,
            'created_date': today(),
            'shift_date': shift_date,
            'qr_scan_time':nowtime,
            'qr_scanned_by':qr_scanned_by,
            'qr_shift': shift_type
        })
        qr_checkin.save(ignore_permissions=True)
        return 'Checkin Marked Successfully'
    if actual_count >= planned_count:
        return 'Planned Count Exceeded'
    else:
        emp = frappe.db.get_value('Employee',{'status':'Active','employee':employee},['name','basic','ctc','employee_type'])
        start_date = frappe.db.get_value('Payroll Dates',{'name':'PAYROLL OT PERIOD DATE 0001'},['payroll_start_date'])
        end_date = frappe.db.get_value('Payroll Dates',{'name':'PAYROLL OT PERIOD DATE 0001'},['payroll_end_date'])
        holidays = len(get_holiday_dates_for_employee(emp[0],start_date,end_date))
        total_working_days = date_diff(end_date,start_date) - holidays
        # if emp[3] != 'CL':
        #     if emp[1]:
        #         per_day_basic = emp[1] / total_working_days
        #     else:
        #         per_day_basic = 0   
        #     if emp[2]:    
        #         per_days_ctc = emp[2] / total_working_days 
        #     else:
        #         per_day_ctc = 0    
        # else:
        #     if emp[1]:
        #         per_day_basic = emp[1]
        #     else:
        #         per_day_basic = 0
        #     if emp[2]:        
        #         per_day_ctc = emp[2]  
        #     else:
        #         per_day_ctc = 0 
        employee_name,employee_type = frappe.get_value('Employee',employee,['employee_name','employee_type'])
        qr_checkin = frappe.new_doc('QR Checkin')
        qr_checkin.update({
            'employee': employee,
            'employee_name': employee_name,
            'department': frappe.get_value('Employee',{'user_id':frappe.session.user},'department'),
            'employee_type': employee_type,
            # 'basic':frappe.db.get_value('Employee',{'name':employee},['basic']),
            # 'ctc':frappe.db.get_value('Employee',{'name':employee},['ctc']),
            # 'per_day_basic':per_day_basic,
            # 'per_day_ctc':per_day_ctc,
            'created_date': today(),
            'shift_date': shift_date,
            'qr_scan_time':nowtime,
            'qr_scanned_by':qr_scanned_by,
            'qr_shift': shift_type
        })
        qr_checkin.save(ignore_permissions=True)
        return 'Checkin Marked Successfully'

def is_between(time, time_range):
    if time_range[1] < time_range[0]:
        return time >= time_range[0] or time <= time_range[1]
    return time_range[0] <= time <= time_range[1]

def get_ot_shift(qr_shift,employee,shift_date):
    if qr_shift == "2":
        if frappe.db.exists("QR Checkin",{'employee':employee,'qr_shift':'1','shift_date':shift_date}):
            return 'OT'
    if qr_shift == "3":
        if frappe.db.exists("QR Checkin",{'employee':employee,'qr_shift':'2','shift_date':shift_date}):
            return 'OT'
    if qr_shift == "1":
        shift_date = add_days(shift_date,-1)
        if frappe.db.exists("QR Checkin",{'employee':employee,'qr_shift':'3','shift_date':shift_date}):
            return 'OT'
        if frappe.db.exists("QR Checkin",{'employee':employee,'qr_shift':'PP2','shift_date':shift_date}):
            return 'OT'

@frappe.whitelist()
def get_tag_card(tag_card_no):
    tag_card_details = {}
    tag_card = frappe.db.sql("""select name from `tabTag Card` where name ='%s' """%(tag_card_no),as_dict =1)[0]
    card_no = tag_card['name']
    tag_card_data = frappe.db.sql("""select name,mat_number,mat_name,part_number,production_order_qty,quantity from `tabTag Card` where name ='%s' """%(tag_card_no),as_dict =1)[0]
    tag_card_details['name'] = tag_card_data['name']
    tag_card_details['mat_number'] = tag_card_data['mat_number']
    tag_card_details['mat_name'] = tag_card_data['mat_name']
    tag_card_details['part_number'] = tag_card_data['part_number']
    tag_card_details['production_order_qty'] = tag_card_data['production_order_qty']
    tag_card_details['quantity'] = tag_card_data['quantity']

    if card_no:
        return "Tag Card Found",tag_card_details
    else:
        return "Tag Card Not Found"


@frappe.whitelist()
def set_tag_card_work_flow_for_approve(tag_card_no):
    tag_card = frappe.db.sql("""select name from `tabTag Card` where name ='%s' """%(tag_card_no),as_dict =1)[0]
    card_no = tag_card['name']
    current_row_no = frappe.db.sql("""select workflow from `tabTag Card` where name = '%s' """%(card_no),as_dict=1)[0]
    current_no = current_row_no['workflow']
    current_row = int(current_no)
    frappe.errprint(current_row)
    doc = frappe.get_doc('Tag Card', card_no)
    children = doc.get('workflow_table')
    frappe.errprint(children[current_row].workflow)
    frappe.db.set_value("Tag Card", card_no, "current_workflow", children[current_row].workflow )
    frappe.db.set_value("Tag Card", card_no, "previous_workflow", children[current_row].workflow )
    cur_row = current_row + 1
    frappe.db.set_value("Tag Card", card_no, "workflow", cur_row)
    sub_doc = frappe.db.sql("""select current_workflow from `tabTag Card` where name ='%s' """%(card_no),as_dict=1)[0]
    sub_flow = sub_doc['current_workflow']
    if sub_flow ==  children[-1].workflow:
        sub_file = frappe.db.sql("""update `tabTag Card` set docstatus = '1' where name ='%s' """%(card_no))


@frappe.whitelist()
def set_tag_card_work_flow_for_reject(tag_card_no):
    tag_card = frappe.db.sql("""select name from `tabTag Card` where name ='%s' """%(tag_card_no),as_dict =1)[0]
    card_no = tag_card['name']
    current_row_no = frappe.db.sql("""select workflow from `tabTag Card` where name = '%s' """%(card_no),as_dict=1)[0]
    current_no = current_row_no['workflow']
    current_row = int(current_no) - 1
    frappe.errprint(current_row)
    doc = frappe.get_doc('Tag Card', card_no)
    children = doc.get('workflow_table')
    frappe.errprint(children[current_row].workflow)
    frappe.db.set_value("Tag Card", card_no, "current_workflow", "Rejected" )
    frappe.db.set_value("Tag Card", card_no, "previous_workflow", children[current_row].workflow )
    cur_row = current_row
    frappe.db.set_value("Tag Card", card_no, "workflow", cur_row)










#      var workflow_table = frm.doc.workflow_table || [];
#         var num_rows = workflow_table.length;
        
#         var current_row = frm.doc.workflow || 0;
        

#         function display_button() {
#             if (frm.doc.current_workflow == "Rejected"){
#              var custom_button_approve = frm.add_custom_button(__('Approve: ' + frm.doc.previous_workflow), function() {
#     frm.set_value('previous_workflow', frm.doc.previous_workflow);
#     frm.set_value('current_workflow', frm.doc.previous_workflow);
#     frm.save();
#     frappe.show_alert({message: 'State updated to ' + frm.doc.previous_workflow, indicator: 'green'});
#     custom_button_approve.css('display', 'none');
#     custom_button_reject.css('display', 'none');
#     current_row++;
#     frm.doc.workflow = current_row-1;
#     if (current_row < num_rows) {
#         display_button();
#     }
# }).css({'color':'white','background-color':"#008000"});
#         }
#         else{
#             var custom_button_approve = frm.add_custom_button(__('Approve: ' + workflow_table[current_row].workflow), function() {
#     frm.set_value('previous_workflow', workflow_table[current_row].workflow);
#     frm.set_value('current_workflow', workflow_table[current_row].workflow);
#     frm.save();
#     frappe.show_alert({message: 'State updated to ' + workflow_table[current_row].workflow, indicator: 'green'});
#     custom_button_approve.css('display', 'none');
#     custom_button_reject.css('display', 'none');
#     current_row++;
#     frm.doc.workflow = current_row;
#     if (current_row < num_rows) {
#         display_button();
#     }
# }).css({'color':'white','background-color':"#008000"});
#         }
          

# var custom_button_reject = frm.add_custom_button(__('Reject'), function() {
    
#     frm.set_value('current_workflow', "Rejected");
#     frm.save();
    
   
# }).css({'color':'white','background-color':"red"});
# if (frm.doc.current_workflow == 'Rejected')  {
#     var first_workflow = workflow_table[0].workflow;
#     frm.add_custom_button(__('Set to: ' + first_workflow),function(){
#          frm.set_value('previous_workflow',first_workflow );
#     frm.set_value('current_workflow', first_workflow);
#     frm.set_value('workflow','1')
#     frm.save();
        
#     }).css({'color':'white','background-color':"black"});
   
# }
