# -*- coding: utf-8 -*-
# Copyright (c) 2021, TEAMPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _, msgprint
from frappe.utils import today,flt,cint, getdate, get_datetime,cstr,add_days,has_common
from datetime import timedelta,datetime,date,time
from erpnext.hr.utils import get_holiday_dates_for_employee
from frappe.utils import cint,today,flt,date_diff,add_days,add_months,date_diff,getdate,formatdate,cint,cstr
import json
import requests



@frappe.whitelist()
def mark_checkin(employee=None):
	per_day_ctc = 0
	per_day_basic = 0
	holidays = 0
	frappe.errprint(employee)
	department = frappe.get_value('Employee',{'user_id':frappe.session.user},'department')
	qr_scanned_by = frappe.get_value('Employee',{'user_id':frappe.session.user},'name') + ':'
	qr_scanned_by += frappe.get_value('Employee',{'user_id':frappe.session.user},'employee_name')
	nowtime = datetime.now()
	shift_date = date.today()
	shift1 = frappe.db.get_value('Shift Type',{'name':'1'},['qr_start_time','qr_end_time'])
	shift1_time = [time(hour=shift1[0].seconds//3600,minute=((shift1[0].seconds//60)%60),second=0),time(hour=shift1[1].seconds//3600,minute=((shift1[1].seconds//60)%60),second=0)]
	shift2 = frappe.db.get_value('Shift Type',{'name':'2'},['qr_start_time','qr_end_time'])
	shift2_time = [time(hour=shift2[0].seconds//3600,minute=((shift2[0].seconds//60)%60),second=0),time(hour=shift2[1].seconds//3600,minute=((shift2[1].seconds//60)%60),second=0)]
	shift3 = frappe.db.get_value('Shift Type',{'name':'3'},['qr_start_time','qr_end_time'])
	shift3_time = [time(hour=shift3[0].seconds//3600,minute=((shift3[0].seconds//60)%60),second=0),time(hour=shift3[1].seconds//3600,minute=((shift3[1].seconds//60)%60),second=0)]
	shiftpp2 = frappe.db.get_value('Shift Type',{'name':'PP2'},['qr_start_time','qr_end_time'])
	shiftpp2_time = [time(hour=shiftpp2[0].seconds//3600,minute=((shiftpp2[0].seconds//60)%60),second=0),time(hour=shiftpp2[1].seconds//3600,minute=((shiftpp2[1].seconds//60)%60),second=0)]
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
	# 	shift_date = shift_date + timedelta(days=-1)
	if shift_type == 'NA':
		return 'Wrong Shift Time'
	
	planned_count = frappe.db.count('Shift Assignment',{'shift_type':shift_type,'start_date': shift_date, 'docstatus':1, 'department':department, 'employee_type':('!=','WC'),})
	# frappe.errprint(planned_count)
	actual_count = frappe.db.count('QR Checkin',{'qr_shift':shift_type,'ot':0,'shift_date': shift_date,'department':department})
	# frappe.errprint(actual_count)
	emp = frappe.db.get_value('Employee',{'status':'Active','employee':employee},['name','basic','ctc','employee_type'])
	start_date = frappe.db.get_value('Payroll Dates',{'name':'PAYROLL OT PERIOD DATE 0001'},['payroll_start_date'])
	# frappe.errprint(type(start_date))
	end_date = frappe.db.get_value('Payroll Dates',{'name':'PAYROLL OT PERIOD DATE 0001'},['payroll_end_date'])
	# frappe.errprint(type(end_date))
	holidays = len(get_holiday_dates_for_employee(emp[0],start_date,end_date)) or 0
	# frappe.errprint(type(holidays))
	# frappe.errprint(holidays)
	total_working_days = date_diff(end_date,start_date) - holidays
	# frappe.errprint(type(total_working_days))
	if emp[3] != 'CL':
		if emp[1]:
			per_day_basic = emp[1] / total_working_days
		else:
			per_day_basic = 0   
		if emp[2]:    
			per_day_ctc = emp[2] / total_working_days 
		else:
			per_day_ctc = 0    
	else:
		if emp[1]: 
			per_day_basic = emp[1] 
		else: 
			per_day_basic = 0 
		if emp[2]:
			per_day_ctc = emp[2] 
		else: 
			per_day_ctc = 0      


	existing_employee = frappe.db.exists('Employee',{'employee':employee, 'status':'Active','employee_type':('!=','WC')})
	if not existing_employee:
		return 'Employee Not Found'
	existing_checkin = frappe.db.exists('QR Checkin',{'employee':employee, 'shift_date':shift_date, 'qr_shift': shift_type})
	if existing_checkin:
		return 'Checkin Already Exists'    
	if get_ot_shift(shift_type,employee,shift_date) == 'OT':
		emp = frappe.db.get_value('Employee',{'status':'Active','employee':employee},['name','basic','ctc','employee_type'])
		start_date = frappe.db.get_value('Payroll Dates',{'name':'PAYROLL OT PERIOD DATE 0001'},['payroll_start_date'])
		end_date = frappe.db.get_value('Payroll Dates',{'name':'PAYROLL OT PERIOD DATE 0001'},['payroll_end_date'])
		holidays = len(get_holiday_dates_for_employee(emp[0],start_date,end_date))
		total_working_days = date_diff(end_date,start_date) - holidays
		if emp[3] != 'CL':
			if emp[1]:
				per_day_basic = emp[1] / total_working_days
			else:
				per_day_basic = 0   
			if emp[2]:    
				per_day_ctc = emp[2] / total_working_days 
			else:
				per_day_ctc = 0    
		else:
			if emp[1]:
				per_day_basic = emp[1] 
			else:
				per_day_basic = 0
			if emp[2]:        
				per_day_ctc = emp[2] 
			else:
				per_day_ctc = 0 
		employee_name,employee_type = frappe.get_value('Employee',employee,['employee_name','employee_type'])
		qr_checkin = frappe.new_doc('QR Checkin')
		qr_checkin.update({
			'employee': employee,
			'employee_name': employee_name,
			'department': frappe.get_value('Employee',{'user_id':frappe.session.user},'department'),
			'employee_type': employee_type,
			'contractor': frappe.get_value('Employee',{'employee':employee},'contractor'),
			'basic':frappe.db.get_value('Employee',{'name':employee},['basic']),
			'ctc':frappe.db.get_value('Employee',{'name':employee},['ctc']),
			'per_day_basic':per_day_basic,
			'per_day_ctc':per_day_ctc,
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
		if emp[3] != 'CL':
			if emp[1]:
				per_day_basic = emp[1] / total_working_days
			else:
				per_day_basic = 0   
			if emp[2]:    
				per_day_ctc = emp[2] / total_working_days 
			else:
				per_day_ctc = 0    
		else:
			if emp[1]:
				per_day_basic = emp[1] 
			else:
				per_day_basic = 0
			if emp[2]:        
				per_day_ctc = emp[2] 
			else:
				per_day_ctc = 0 
		employee_name,employee_type = frappe.get_value('Employee',employee,['employee_name','employee_type'])
		qr_checkin = frappe.new_doc('QR Checkin')
		qr_checkin.update({
			'employee': employee,
			'employee_name': employee_name,
			'department': frappe.get_value('Employee',{'user_id':frappe.session.user},'department'),
			'employee_type': employee_type,
			'contractor': frappe.get_value('Employee',{'employee':employee},'contractor'),
			'basic':frappe.db.get_value('Employee',{'name':employee},['basic']),
			'ctc':frappe.db.get_value('Employee',{'name':employee},['ctc']),
			'per_day_basic':per_day_basic or 0,
			'per_day_ctc':per_day_ctc or 0,
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
	tag_card = frappe.db.sql("""select name from `tabTag Card` where name ='%s' and docstatus = 0 """%(tag_card_no),as_dict =1)[0]
	card_no = tag_card['name']
	if card_no:
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
	else:
		return "Tag Card is already submitted"

@frappe.whitelist()
def set_tag_card_work_flow_for_approve(tag_card_no):
	prod_line_emp = []
	user = frappe.session.user
	u_name = frappe.db.sql("""select username from `tabUser` where name='%s' """%(frappe.session.user),as_dict=1)[0]
	tag_card = frappe.db.sql("""select name,production_line from `tabTag Card` where name ='%s' and docstatus = 0 """%(tag_card_no),as_dict =1)[0]
	card_no = tag_card['name']
	if user in ['Administrator','gururaja528@gmail.com']:
		if card_no:
			current_row_no = frappe.db.sql("""select workflow,roleflow from `tabTag Card` where name = '%s' """%(card_no),as_dict=1)[0]
			current_no = current_row_no['workflow']
			current_roleflow = current_row_no['roleflow']
			current_row = int(current_no)
			current_roleno = int(current_roleflow)

			doc = frappe.get_doc('Tag Card', card_no)
			children = doc.get('workflow_table')
			user_roles = frappe.get_roles(user)
			required_role = children[current_roleno].role_name
			if (required_role in user_roles):
				frappe.db.set_value("Tag Card", card_no, "current_workflow", children[current_row].workflow )
				frappe.db.set_value("Tag Card", card_no, "previous_workflow", children[current_row].workflow )
				frappe.db.set_value("Tag Card", card_no, "allowed_role", children[current_roleno].allowed_for )
				
				cur_row = current_row + 1
				roleflow_no = current_roleno + 1
				frappe.db.set_value("Tag Card", card_no, "workflow", cur_row)
				frappe.db.set_value("Tag Card", card_no, "roleflow", roleflow_no)
				tag = frappe.get_doc('Tag Card', card_no)
				tag.append('workflow_tracker_table',{
					'flow_name': children[current_row].workflow,
					'time':datetime.now().strftime('%H:%M:%S'),
					'date':date.today(),
					'user_name':u_name['username']
				})
				tag.save(ignore_permissions=True)
				frappe.msgprint("Workflow Successfully updated")
				
				
			else:
				frappe.throw(_("You don't have enough permission"))
			sub_doc = frappe.db.sql("""select current_workflow from `tabTag Card` where name ='%s' """%(card_no),as_dict=1)[0]
			sub_flow = sub_doc['current_workflow']
			if sub_flow ==  children[-1].workflow:
				sub_file = frappe.db.sql("""update `tabTag Card` set docstatus = '1' where name ='%s' """%(card_no))
			
		else:
			frappe.throw(_("Tag Card is already submitted"))
	else:
		emp_details = frappe.db.sql("""select name from `tabEmployee Production Line Details` where user_id ='%s' """%(user),as_dict=1)[0]
		emp_name = emp_details['name']
		emp_doc = frappe.get_doc('Employee Production Line Details', emp_name)
		emp_prod_line = emp_doc.get('production_line')
		for e in emp_prod_line:
			prod_line_emp.append(e.production_line_no)
		
		tag_card_prod_line = tag_card['production_line']
		if (tag_card_prod_line in prod_line_emp):
			if card_no:
				current_row_no = frappe.db.sql("""select workflow,roleflow from `tabTag Card` where name = '%s' """%(card_no),as_dict=1)[0]
				current_no = current_row_no['workflow']
				current_roleflow = current_row_no['roleflow']
				current_row = int(current_no)
				current_role = int(current_roleflow)
				if current_role == 0:
					current_roleno = 1
				else:
					current_roleno = int(current_roleflow)
				doc = frappe.get_doc('Tag Card', card_no)
				children = doc.get('workflow_table')
				user_roles = frappe.get_roles(user)
				required_role = children[current_roleno].role_name
				if (required_role in user_roles):
					frappe.db.set_value("Tag Card", card_no, "current_workflow", children[current_row].workflow )
					frappe.db.set_value("Tag Card", card_no, "previous_workflow", children[current_row].workflow )
					frappe.db.set_value("Tag Card", card_no, "allowed_role", children[current_roleno].allowed_for )
					
					cur_row = current_row + 1
					roleflow_no = current_roleno + 1
					frappe.db.set_value("Tag Card", card_no, "workflow", cur_row)
					frappe.db.set_value("Tag Card", card_no, "roleflow", roleflow_no)
					tag = frappe.get_doc('Tag Card', card_no)
					tag.append('workflow_tracker_table',{
						'flow_name': children[current_row].workflow,
						'time':datetime.now().strftime('%H:%M:%S'),
						'date':date.today(),
						'user_name':u_name['username']
					})
					tag.save(ignore_permissions=True)
					frappe.msgprint("Workflow Successfully updated")  
				else:
					frappe.throw(_("You don't have enough permission"))
				sub_doc = frappe.db.sql("""select current_workflow from `tabTag Card` where name ='%s' """%(card_no),as_dict=1)[0]
				sub_flow = sub_doc['current_workflow']
				if sub_flow ==  children[-1].workflow:
					sub_file = frappe.db.sql("""update `tabTag Card` set docstatus = '1' where name ='%s' """%(card_no))
					
			else:
				frappe.throw(_("Tag Card is already submitted"))
		else:
			frappe.throw(_("You doesn't belongs to this production line"))


@frappe.whitelist()
def set_tag_card_work_flow_for_reject(tag_card_no):
	prod_line_emp = []
	user = frappe.session.user
	tag_card = frappe.db.sql("""select name,production_line from `tabTag Card` where name ='%s' and docstatus = 0 """%(tag_card_no),as_dict =1)[0]
	card_no = tag_card['name']
	if user in ['Administrator','gururaja528@gmail.com']:
		if card_no:
			current_row_no = frappe.db.sql("""select workflow,roleflow from `tabTag Card` where name = '%s' """%(card_no),as_dict=1)[0]
			current_no = current_row_no['workflow']
			current_roleflow = current_row_no['roleflow']
			current_role_no = int(current_roleflow)
			doc = frappe.get_doc('Tag Card', card_no)
			children = doc.get('workflow_table')
			user_roles = frappe.get_roles(user)
			required_role = children[current_role_no].role_name
			if (required_role in user_roles):
				current_roleno = int(current_roleflow) - 1
				current_row = int(current_no) - 1
				current_row_line = int(current_no) - 2
				frappe.errprint(current_row)
				frappe.errprint(children[current_row].workflow)
				frappe.db.set_value("Tag Card", card_no, "current_workflow", "Rejected" )
				if current_row_line > 0:
					frappe.db.set_value("Tag Card", card_no, "previous_workflow", children[current_row_line].workflow )
					frappe.db.set_value("Tag Card", card_no, "allowed_role", children[current_row_line].allowed_for )

				else:
					frappe.db.set_value("Tag Card", card_no, "previous_workflow", children[0].workflow )
					frappe.db.set_value("Tag Card", card_no, "allowed_role", children[0].allowed_for )
					
				if (current_row > 0 and current_roleno > 0):
					frappe.db.set_value("Tag Card", card_no, "workflow", current_row)
					frappe.db.set_value("Tag Card", card_no, "roleflow", current_roleno)
					frappe.msgprint("Rejected Successfully")
				else:
					frappe.db.set_value("Tag Card", card_no, "workflow", 1)
					frappe.db.set_value("Tag Card", card_no, "roleflow", 1)
					frappe.msgprint("Rejected Successfully")
			else:
				frappe.throw(_("You don't have enough permission"))
		else:
				frappe.throw(_("Tag Card is already submitted"))
	else:
		emp_details = frappe.db.sql("""select name from `tabEmployee Production Line Details` where user_id ='%s' """%(user),as_dict=1)[0]
		emp_name = emp_details['name']
		emp_doc = frappe.get_doc('Employee Production Line Details', emp_name)
		emp_prod_line = emp_doc.get('production_line')
		for e in emp_prod_line:
			prod_line_emp.append(e.production_line_no)
		tag_card_prod_line = tag_card['production_line']
		if (tag_card_prod_line in prod_line_emp):
			if card_no:
				current_row_no = frappe.db.sql("""select workflow,roleflow from `tabTag Card` where name = '%s' """%(card_no),as_dict=1)[0]
				current_no = current_row_no['workflow']
				current_roleflow = current_row_no['roleflow']
				current_role_no = int(current_roleflow)
				doc = frappe.get_doc('Tag Card', card_no)
				children = doc.get('workflow_table')
				user_roles = frappe.get_roles(user)
				required_role = children[current_role_no].role_name
				if (required_role in user_roles):
					current_roleno = int(current_roleflow) - 1
					current_row = int(current_no) - 1
					current_row_line = int(current_no) - 2
					frappe.errprint(current_row)
					frappe.errprint(children[current_row].workflow)
					frappe.db.set_value("Tag Card", card_no, "current_workflow", "Rejected" )
					if current_row_line > 0:
						frappe.db.set_value("Tag Card", card_no, "previous_workflow", children[current_row_line].workflow )
						frappe.db.set_value("Tag Card", card_no, "allowed_role", children[current_row_line].allowed_for )
					else:
						frappe.db.set_value("Tag Card", card_no, "previous_workflow", children[0].workflow )
						frappe.db.set_value("Tag Card", card_no, "allowed_role", children[0].allowed_for )
					if (current_row > 0 and current_roleno > 0):
						frappe.db.set_value("Tag Card", card_no, "workflow", current_row)
						frappe.db.set_value("Tag Card", card_no, "roleflow", current_roleno)
						frappe.msgprint("Rejected Successfully")
					else:
						frappe.db.set_value("Tag Card", card_no, "workflow", 1)
						frappe.db.set_value("Tag Card", card_no, "roleflow", 1)
						frappe.msgprint("Rejected Successfully")
				else:
					frappe.throw(_("You don't have enough permission"))
			else:
					frappe.throw(_("Tag Card is already submitted"))
		else:
			frappe.throw(_("You doesn't belongs to this production line"))