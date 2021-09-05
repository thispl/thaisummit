# Copyright (c) 2021, TEAMPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class BulkOvertimeRequest(Document):
    @frappe.whitelist()
    def get_shift(self,ot_date,from_time):
        shift_type = frappe.db.sql('select name from `tabShift Type` where "%s" between start_time and end_time and name not in ("PP1","PP2") '%(from_time),as_dict=True)
        if shift_type:
            if from_time == '16:30:00':
                shift = 2
            else:
                if shift_type[0].name == '1':
                    if ot_date:
                        holiday = frappe.db.sql("""select `tabHoliday`.holiday_date from `tabHoliday List`
                        left join `tabHoliday` on `tabHoliday`.parent = `tabHoliday List`.name where `tabHoliday List`.name = 'Holiday List - 2021' and holiday_date = '%s' """%(ot_date),as_dict=True)
                        if not holiday:
                            shift = ''
                            from_time = ''
                            frappe.msgprint("Overtime Request from 8:00 AM to 16:30 PM can be applied only on Sunday or Holiday")
                            # return shift,from_time
                shift = shift_type[0].name
        else:
            shift = 2
        
        return shift,from_time
    
    @frappe.whitelist()
    def create_overtime_request(self):
        if self.employees:
            for emp in self.employees:
                if not emp.employee:
                    frappe.throw("Please select Employee ID")
                elif not emp.ot_date:
                    frappe.throw("Please select OT Date for Employee - %s"%emp.employee)
                elif not emp.from_time:
                    frappe.throw("Please select From Time for Employee - %s"%emp.employee)
                elif not emp.to_time:
                    frappe.throw("Please select To Time for Employee - %s"%emp.employee)

                today = frappe.db.sql("select count(*) as count from `tabOvertime Request` where employee = '%s' and ot_date = '%s' and name != '%s' and workflow_state != 'Rejected' "%(emp.employee,emp.ot_date,emp.name),as_dict=True)
                if today[0].count >= 1:
                    frappe.throw("Only 1 Overtime Request is allowed for a day for Employee - %s "%(emp.employee))

            for emp in self.employees:
                ot = frappe.new_doc("Overtime Request")
                ot.employee = emp.employee
                ot.ot_date = emp.ot_date
                ot.from_time = emp.from_time
                ot.to_time = emp.to_time
                ot.total_hours = emp.total_hours
                ot.ot_hours = emp.ot_hours
                ot.shift = emp.shift
                ot.approver = self.approver
                ot.approver_id = self.approver_id
                ot.approver_name = self.approver_name
                ot.requested_by = self.requested_by

                if frappe.db.exists("Attendance",{'attendance_date':emp.ot_date,'employee':emp.employee,'docstatus':('!=','2')}):
                    att = frappe.get_doc("Attendance",{'attendance_date':emp.ot_date,'employee':emp.employee,'docstatus':('!=','2')})
                    if att.in_time and att.out_time:
                        twh = att.out_time - att.in_time
                        ot.bio_in = att.in_time
                        ot.bio_out = att.out_time
                        ot.total_wh = twh
                ot.save(ignore_permissions=True)
                doc = frappe.get_doc("Overtime Request",ot.name)
                if doc.workflow_state == 'Draft':
                    if doc.ot_hours and doc.total_wh and doc.bio_in and doc.bio_out :
                        frappe.db.set_value('Overtime Request',doc.name,'workflow_state','Pending for HOD')
        frappe.msgprint("Overtime Request Submitted Successfully")
        self.employees = ''
        self.approver = ''
        self.approver_id = ''
        self.approver_name = ''
        self.requested_by = ''
    
    @frappe.whitelist()
    def check_holiday(self,ot_date):
        if ot_date:
            holiday = frappe.db.sql("""select `tabHoliday`.holiday_date from `tabHoliday List`
            left join `tabHoliday` on `tabHoliday`.parent = `tabHoliday List`.name where `tabHoliday List`.name = 'Holiday List - 2021' and holiday_date = '%s' """%(ot_date),as_dict=True)
            if not holiday:
                return 'NO'