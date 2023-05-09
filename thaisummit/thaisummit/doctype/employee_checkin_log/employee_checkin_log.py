# Copyright (c) 2023, TEAMPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json
from frappe.utils.background_jobs import enqueue


class EmployeeCheckinLog(Document):
	@frappe.whitelist()
	def process_checkin_log(self):
		log_file_name = frappe.db.get_value(
                "File",
                {"attached_to_doctype": 'Employee Checkin Log',
                    "attached_to_name": self.name},
                "name",
            )
		log_file = frappe.get_doc("File", log_file_name)
		log_file_content = log_file.get_content()
		checkin_logs = json.loads(log_file_content)
		enqueue(mark_checkin, queue='default', timeout=9000, event='mark_checkin',checkin_logs=checkin_logs)

@frappe.whitelist()
def mark_checkin(checkin_logs):
	for args in checkin_logs:
		if not frappe.db.exists('Employee Checkin',{'biometric_pin':args['emp_code'],'time':args['punch_time']}):
			if frappe.db.exists('Employee',{'biometric_pin':args['emp_code']}):
				try:
					if args['terminal_alias'] == 'BC/NT IN':
						ec = frappe.new_doc('Employee Checkin')
						ec.biometric_pin = args['emp_code'].upper()
						ec.employee = frappe.db.get_value('Employee',{'biometric_pin':args['emp_code']},['employee_number'])
						ec.time = args['punch_time']
						ec.device_id = args['terminal_alias']
						ec.log_type = 'IN'
						ec.save(ignore_permissions=True)
						frappe.db.commit()
					elif args['terminal_alias'] == 'WC/FT IN':
						ec = frappe.new_doc('Employee Checkin')
						ec.biometric_pin = args['emp_code'].upper()
						ec.employee = frappe.db.get_value('Employee',{'biometric_pin':args['emp_code']},['employee_number'])
						ec.time = args['punch_time']
						ec.device_id = args['terminal_alias']
						ec.log_type = 'IN'
						ec.save(ignore_permissions=True)
						frappe.db.commit()
					elif args['terminal_alias'] == 'CL IN':
						ec = frappe.new_doc('Employee Checkin')
						ec.biometric_pin = args['emp_code'].upper()
						ec.employee = frappe.db.get_value('Employee',{'biometric_pin':args['emp_code']},['employee_number'])
						ec.time = args['punch_time']
						ec.device_id = args['terminal_alias']
						ec.log_type = 'IN'
						ec.save(ignore_permissions=True)
						frappe.db.commit()
					elif args['terminal_alias'] == 'BC/NT OUT':
						ec = frappe.new_doc('Employee Checkin')
						ec.biometric_pin = args['emp_code'].upper()
						ec.employee = frappe.db.get_value('Employee',{'biometric_pin':args['emp_code']},['employee_number'])
						ec.time = args['punch_time']
						ec.device_id = args['terminal_alias']
						ec.log_type = 'OUT'
						ec.save(ignore_permissions=True)
						frappe.db.commit()
					elif args['terminal_alias'] == 'WC/FT OUT':
						ec = frappe.new_doc('Employee Checkin')
						ec.biometric_pin = args['emp_code'].upper()
						ec.employee = frappe.db.get_value('Employee',{'biometric_pin':args['emp_code']},['employee_number'])
						ec.time = args['punch_time']
						ec.device_id = args['terminal_alias']
						ec.log_type = 'OUT'
						ec.save(ignore_permissions=True)
						frappe.db.commit()
					else: 
						ec = frappe.new_doc('Employee Checkin')
						ec.biometric_pin = args['emp_code'].upper()
						ec.employee = frappe.db.get_value('Employee',{'biometric_pin':args['emp_code']},['employee_number'])
						ec.time = args['punch_time']
						ec.device_id = args['terminal_alias']
						ec.log_type = 'OUT'
						ec.save(ignore_permissions=True)
						frappe.db.commit()
				except:
					frappe.log_error(title="checkin error",message=args)
			else:
				if args['terminal_alias'] == 'BC/NT IN':
					ec = frappe.new_doc('Unregistered Employee Checkin')
					ec.biometric_pin = args['emp_code'].upper()
					ec.biometric_time = args['punch_time']
					ec.locationdevice_id = args['terminal_alias']
					ec.log_type = 'IN'
					ec.save(ignore_permissions=True)
					frappe.db.commit()
				elif args['terminal_alias'] == 'WC/FT IN':
					ec = frappe.new_doc('Unregistered Employee Checkin')
					ec.biometric_pin = args['emp_code'].upper()
					ec.biometric_time = args['punch_time']
					ec.locationdevice_id = args['terminal_alias']
					ec.log_type = 'IN'
					ec.save(ignore_permissions=True)
					frappe.db.commit()
				elif args['terminal_alias'] == 'CL IN':
					ec = frappe.new_doc('Unregistered Employee Checkin')
					ec.biometric_pin = args['emp_code'].upper()
					ec.biometric_time = args['punch_time']
					ec.locationdevice_id = args['terminal_alias']
					ec.log_type = 'IN'
					ec.save(ignore_permissions=True)
					frappe.db.commit()
				elif args['terminal_alias'] == 'BC/NT OUT':
					ec = frappe.new_doc('Unregistered Employee Checkin')
					ec.biometric_pin = args['emp_code'].upper()
					ec.biometric_time = args['punch_time']
					ec.locationdevice_id = args['terminal_alias']
					ec.log_type = 'OUT'
					ec.save(ignore_permissions=True)
					frappe.db.commit()
				elif args['terminal_alias'] == 'WC/FT OUT':
					ec = frappe.new_doc('Unregistered Employee Checkin')
					ec.biometric_pin = args['emp_code'].upper()
					ec.biometric_time = args['punch_time']
					ec.locationdevice_id = args['terminal_alias']
					ec.log_type = 'OUT'
					ec.save(ignore_permissions=True)
					frappe.db.commit()
				else: 
					ec = frappe.new_doc('Unregistered Employee Checkin')
					ec.biometric_pin = args['emp_code'].upper()
					ec.biometic_time = args['punch_time']
					ec.device_id = args['terminal_alias']
					ec.log_type = 'OUT'
					ec.save(ignore_permissions=True)
					frappe.db.commit()
		
