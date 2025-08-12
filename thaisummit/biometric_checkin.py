import frappe
from datetime import date
import json
from frappe.utils.csvutils import read_csv_content
from frappe.utils.background_jobs import enqueue



@frappe.whitelist(allow_guest=True)
def get_checkins(**args):
    frappe.log_error(args)


@frappe.whitelist(allow_guest=True)
def mark_checkin(**args):
    if frappe.db.exists('Employee',{'biometric_pin':args['employee']}):
        if not frappe.db.sql("""
    SELECT name 
    FROM `tabEmployee Checkin`
    WHERE biometric_pin = %s AND time = %s
    LIMIT 1
""", (args['employee'], args['time'])):
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
                elif args['device_id'] == 'BC/FT IN':
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
                elif args['device_id'] == 'NT IN':
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
            return "Checkin Marked"
    else:
        if not frappe.db.exists('Unregistered Employee Checkin',{'biometric_pin':args['employee'],'time':args['time']}):
            if args['device_id'] == 'BC/NT IN':
                ec = frappe.new_doc('Unregistered Employee Checkin')
                ec.biometric_pin = args['employee'].upper()
                ec.biometric_time = args['time']
                ec.locationdevice_id = args['device_id']
                ec.log_type = 'IN'
                ec.save(ignore_permissions=True)
                frappe.db.commit()
                return "Checkin Marked"
            elif args['device_id'] == 'BC/FT IN':
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
                ec = frappe.new_doc('Unregistered Employee Checkin')
                ec.biometric_pin = args['employee'].upper()
                ec.biometric_time = args['time']
                ec.locationdevice_id = args['device_id']
                ec.log_type = 'IN'
                ec.save(ignore_permissions=True)
                frappe.db.commit()
                return "Checkin Marked"
            elif args['device_id'] == 'CL IN':
                ec = frappe.new_doc('Unregistered Employee Checkin')
                ec.biometric_pin = args['employee'].upper()
                ec.biometric_time = args['time']
                ec.locationdevice_id = args['device_id']
                ec.log_type = 'IN'
                ec.save(ignore_permissions=True)
                frappe.db.commit()
                return "Checkin Marked"
            elif args['device_id'] == 'NT IN':
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
                ec = frappe.new_doc('Unregistered Employee Checkin')
                ec.biometric_pin = args['employee'].upper()
                ec.biometric_time = args['time']
                ec.locationdevice_id = args['device_id']
                ec.log_type = 'OUT'
                ec.save(ignore_permissions=True)
                frappe.db.commit()
                return "Checkin Marked"
            elif args['device_id'] == 'WC/FT OUT':
                ec = frappe.new_doc('Unregistered Employee Checkin')
                ec.biometric_pin = args['employee'].upper()
                ec.biometric_time = args['time']
                ec.locationdevice_id = args['device_id']
                ec.log_type = 'OUT'
                ec.save(ignore_permissions=True)
                frappe.db.commit()
                return "Checkin Marked"
            else: 
                ec = frappe.new_doc('Unregistered Employee Checkin')
                ec.biometric_pin = args['employee'].upper()
                ec.biometric_time = args['time']
                ec.locationdevice_id = args['device_id']
                ec.log_type = 'OUT'
                ec.save(ignore_permissions=True)
                frappe.db.commit()
                return "Checkin Marked" 
        else:
            return "Checkin Marked"


@frappe.whitelist(allow_guest=True)
def test_mark_checkin(**args):
    if not frappe.db.exists('Employee Checkin Test',{'biometric_pin':args['employee'],'time':args['time']}):
        if frappe.db.exists('Employee',{'biometric_pin':args['employee']}):
            try:
                if args['device_id'] == 'BC/NT IN':
                    ec = frappe.new_doc('Employee Checkin Test')
                    ec.biometric_pin = args['employee'].upper()
                    ec.employee = frappe.db.get_value('Employee',{'biometric_pin':args['employee']},['employee_number'])
                    ec.time = args['time']
                    ec.device_id = args['device_id']
                    ec.log_type = 'IN'
                    ec.save(ignore_permissions=True)
                    frappe.db.commit()
                    return "Already Checkin Marked"
                
                elif args['device_id'] == 'BC/FT IN':
                    ec = frappe.new_doc('Employee Checkin Test')
                    ec.biometric_pin = args['employee'].upper()
                    ec.employee = frappe.db.get_value('Employee',{'biometric_pin':args['employee']},['employee_number'])
                    ec.time = args['time']
                    ec.device_id = args['device_id']
                    ec.log_type = 'IN'
                    ec.save(ignore_permissions=True)
                    frappe.db.commit()
                    return "Already Checkin Marked"

                elif args['device_id'] == 'WC/FT IN':
                    ec = frappe.new_doc('Employee Checkin Test')
                    ec.biometric_pin = args['employee'].upper()
                    ec.employee = frappe.db.get_value('Employee',{'biometric_pin':args['employee']},['employee_number'])
                    ec.time = args['time']
                    ec.device_id = args['device_id']
                    ec.log_type = 'IN'
                    ec.save(ignore_permissions=True)
                    frappe.db.commit()
                    return "Already Checkin Marked"
                elif args['device_id'] == 'CL IN':
                    ec = frappe.new_doc('Employee Checkin Test')
                    ec.biometric_pin = args['employee'].upper()
                    ec.employee = frappe.db.get_value('Employee',{'biometric_pin':args['employee']},['employee_number'])
                    ec.time = args['time']
                    ec.device_id = args['device_id']
                    ec.log_type = 'IN'
                    ec.save(ignore_permissions=True)
                    frappe.db.commit()
                    return "Already Checkin Marked"
                elif args['device_id'] == 'BC/NT OUT':
                    ec = frappe.new_doc('Employee Checkin Test')
                    ec.biometric_pin = args['employee'].upper()
                    ec.employee = frappe.db.get_value('Employee',{'biometric_pin':args['employee']},['employee_number'])
                    ec.time = args['time']
                    ec.device_id = args['device_id']
                    ec.log_type = 'OUT'
                    ec.save(ignore_permissions=True)
                    frappe.db.commit()
                    return "Already Checkin Marked"
                elif args['device_id'] == 'WC/FT OUT':
                    ec = frappe.new_doc('Employee Checkin Test')
                    ec.biometric_pin = args['employee'].upper()
                    ec.employee = frappe.db.get_value('Employee',{'biometric_pin':args['employee']},['employee_number'])
                    ec.time = args['time']
                    ec.device_id = args['device_id']
                    ec.log_type = 'OUT'
                    ec.save(ignore_permissions=True)
                    frappe.db.commit()
                    return "Already Checkin Marked"
                else: 
                    ec = frappe.new_doc('Employee Checkin Test')
                    ec.biometric_pin = args['employee'].upper()
                    ec.employee = frappe.db.get_value('Employee',{'biometric_pin':args['employee']},['employee_number'])
                    ec.time = args['time']
                    ec.device_id = args['device_id']
                    ec.log_type = 'OUT'
                    ec.save(ignore_permissions=True)
                    frappe.db.commit()
                    return "Already Checkin Marked"
            except:
                frappe.log_error(title="checkin error",message=args)
    else:
        return "Already Checkin Marked"

  

def enqueue_bulk_update_checkin_from_csv():
    filename = 'checkin_26102511_1.csv'
    enqueue(bulk_update_checkin_from_csv, queue='default', timeout=6000, event='bulk_update_checkin_from_csv',filename=filename)


def bulk_update_checkin_from_csv():
    filename = 'checkin_26102511_1.csv'
    #below is the method to get file from Frappe File manager
    from frappe.utils.file_manager import get_file
    #Method to fetch file using get_doc and stored as _file
    _file = frappe.get_doc("File", {"file_name": filename})
    #Path in the system
    filepath = get_file(filename)
    #CSV Content stored as pps

    pps = read_csv_content(filepath[1])
    count = 0

    for pp in pps[1:]:
        if frappe.db.exists('Employee',{'biometric_pin':pp[0]}):
            if not frappe.db.exists('Employee Checkin',{'biometric_pin':pp[0],'time':pp[1]}):
                if pp[2] in ['BC/NT OUT','WC/FT OUT','CL OUT','NT OUT','BC/FT OUT']:
                    ec = frappe.new_doc('Employee Checkin')
                    ec.biometric_pin = pp[0]
                    ec.employee = frappe.db.get_value('Employee',{'biometric_pin':pp[0]},['employee_number'])
                    ec.time = pp[1]
                    ec.device_id = pp[2]
                    ec.log_type = 'OUT'
                    
                if pp[2] in ['BC/NT IN','WC/FT IN','CL IN','NT IN','BC/FT IN']: 
                    ec = frappe.new_doc('Employee Checkin')
                    ec.biometric_pin = pp[0]
                    ec.employee = frappe.db.get_value('Employee',{'biometric_pin':pp[0]},['employee_number'])
                    ec.time = pp[1]
                    ec.device_id = pp[2]
                    ec.log_type = 'IN'

                ec.save(ignore_permissions=True)   
        else:
            if not frappe.db.exists('Unregistered Employee Checkin',{'biometric_pin':pp[0],'time':pp[1]}):
                if pp[2] in ['BC/NT IN','WC/FT IN','CL IN','NT IN','BC/FT IN']:
                    ec = frappe.new_doc('Unregistered Employee Checkin')
                    ec.biometric_pin = pp[0]
                    ec.biometric_time = pp[1]
                    ec.locationdevice_id = pp[2]
                    ec.log_type = 'IN'
                if pp[2] in ['BC/NT OUT','WC/FT OUT','CL OUT','NT OUT','BC/FT OUT']:
                    ec = frappe.new_doc('Unregistered Employee Checkin')
                    ec.biometric_pin = pp[0]
                    ec.biometric_time = pp[1]
                    ec.locationdevice_id = pp[2]
                    ec.log_type = 'OUT'
                ec.save(ignore_permissions=True)
