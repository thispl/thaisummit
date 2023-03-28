import frappe
from datetime import date
import json

@frappe.whitelist(allow_guest=True)
def mark_checkin(**args):
    if not frappe.db.exists('Employee Checkin',{'biometric_pin':args['employee'],'time':args['time']}):
        if frappe.db.exists('Employee',{'biometric_pin':args['employee']}):
            try:
                if args['device_id'] == 'BC/NT IN':
                    ec = frappe.new_doc('Employee Checkin')
                    ec.biometric_pin = args['employee'].upper()
                    ec.employee = frappe.db.get_value('Employee',{'biometric_pin':args['employee']},['employee_number'])
                    ec.time = args['time']
                    ec.device_id = args['device_id']
                    ec.log_type = 'IN'
                    ec.save(ignore_permissions=True)
                    frappe.db.commit()
                    return "Checkin Marked"
                elif args['device_id'] == 'WC/FT IN':
                    ec = frappe.new_doc('Employee Checkin')
                    ec.biometric_pin = args['employee'].upper()
                    ec.employee = frappe.db.get_value('Employee',{'biometric_pin':args['employee']},['employee_number'])
                    ec.time = args['time']
                    ec.device_id = args['device_id']
                    ec.log_type = 'IN'
                    ec.save(ignore_permissions=True)
                    frappe.db.commit()
                    return "Checkin Marked"
                elif args['device_id'] == 'CL IN':
                    ec = frappe.new_doc('Employee Checkin')
                    ec.biometric_pin = args['employee'].upper()
                    ec.employee = frappe.db.get_value('Employee',{'biometric_pin':args['employee']},['employee_number'])
                    ec.time = args['time']
                    ec.device_id = args['device_id']
                    ec.log_type = 'IN'
                    ec.save(ignore_permissions=True)
                    frappe.db.commit()
                    return "Checkin Marked"
                elif args['device_id'] == 'BC/NT OUT':
                    ec = frappe.new_doc('Employee Checkin')
                    ec.biometric_pin = args['employee'].upper()
                    ec.employee = frappe.db.get_value('Employee',{'biometric_pin':args['employee']},['employee_number'])
                    ec.time = args['time']
                    ec.device_id = args['device_id']
                    ec.log_type = 'OUT'
                    ec.save(ignore_permissions=True)
                    frappe.db.commit()
                    return "Checkin Marked"
                elif args['device_id'] == 'WC/FT OUT':
                    ec = frappe.new_doc('Employee Checkin')
                    ec.biometric_pin = args['employee'].upper()
                    ec.employee = frappe.db.get_value('Employee',{'biometric_pin':args['employee']},['employee_number'])
                    ec.time = args['time']
                    ec.device_id = args['device_id']
                    ec.log_type = 'OUT'
                    ec.save(ignore_permissions=True)
                    frappe.db.commit()
                    return "Checkin Marked"
                else: 
                    ec = frappe.new_doc('Employee Checkin')
                    ec.biometric_pin = args['employee'].upper()
                    ec.employee = frappe.db.get_value('Employee',{'biometric_pin':args['employee']},['employee_number'])
                    ec.time = args['time']
                    ec.device_id = args['device_id']
                    ec.log_type = 'OUT'
                    ec.save(ignore_permissions=True)
                    frappe.db.commit()
                    return "Checkin Marked"
            except:
                frappe.log_error(title="checkin error",message=args)
        else:
            if args['device_id'] == 'BC/NT IN':
                ec = frappe.new_doc('Unregistered Employee Checkin')
                ec.biometric_pin = args['employee'].upper()
                ec.biometric_time = args['time']
                ec.locationdevice_id = args['device_id']
                ec.log_type = 'IN'
                ec.save(ignore_permissions=True)
                frappe.db.commit()
                return "Checkin Unmarked"
            elif args['device_id'] == 'WC/FT IN':
                ec = frappe.new_doc('Unregistered Employee Checkin')
                ec.biometric_pin = args['employee'].upper()
                ec.biometric_time = args['time']
                ec.locationdevice_id = args['device_id']
                ec.log_type = 'IN'
                ec.save(ignore_permissions=True)
                frappe.db.commit()
                return "Checkin Unmarked"
            elif args['device_id'] == 'CL IN':
                ec = frappe.new_doc('Unregistered Employee Checkin')
                ec.biometric_pin = args['employee'].upper()
                ec.biometric_time = args['time']
                ec.locationdevice_id = args['device_id']
                ec.log_type = 'IN'
                ec.save(ignore_permissions=True)
                frappe.db.commit()
                return "Checkin Unmarked"
            elif args['device_id'] == 'BC/NT OUT':
                ec = frappe.new_doc('Unregistered Employee Checkin')
                ec.biometric_pin = args['employee'].upper()
                ec.biometric_time = args['time']
                ec.locationdevice_id = args['device_id']
                ec.log_type = 'OUT'
                ec.save(ignore_permissions=True)
                frappe.db.commit()
                return "Checkin Unmarked"
            elif args['device_id'] == 'WC/FT OUT':
                ec = frappe.new_doc('Unregistered Employee Checkin')
                ec.biometric_pin = args['employee'].upper()
                ec.biometric_time = args['time']
                ec.locationdevice_id = args['device_id']
                ec.log_type = 'OUT'
                ec.save(ignore_permissions=True)
                frappe.db.commit()
                return "Checkin Unmarked"
            else: 
                ec = frappe.new_doc('Unregistered Employee Checkin')
                ec.biometric_pin = args['employee'].upper()
                ec.biometic_time = args['time']
                ec.device_id = args['device_id']
                ec.log_type = 'OUT'
                ec.save(ignore_permissions=True)
                frappe.db.commit()
                return "Checkin Unmarked" 
    else:
        return "Checkin Marked"


