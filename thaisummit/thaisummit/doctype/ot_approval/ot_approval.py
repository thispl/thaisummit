# -*- coding: utf-8 -*-
# Copyright (c) 2021, TEAMPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
# import datetime
# from frappe.utils import today

class OTApproval(Document):
    def get_default_data(self):
        att_data = frappe.db.sql(""" select * from `tabAttendance` where attendance_date BETWEEN '%s' and '%s' and ot IS NULL""" %(self.from_date,self.to_date),as_dict =True)
        for att in att_data:
            frappe.errprint(att.employee)
            self.append("ot_approval",{
                "attendance_name":att.name,
                "employee_id":att.employee,
                "in_time": att.in_time,
                "out_time" : att.out_time,
                "qr_scan_time":att.qr_scan_time,
                "total_working_hours":att.working_hours,
                "extra_hours":att.ot,
                "ot_hours":att.ot
            }).save(ignore_permissions=True)
            frappe.db.commit()
    def get_data_datewise(self):
        frappe.errprint("from date and to date")
        if self.employee_id:
            att_data = frappe.db.sql(""" select * from `tabAttendance` where employee = '%s' and attendance_date BETWEEN '%s' and '%s' and ot IS NULL""" %(self.employee_id,self.from_date,self.to_date),as_dict =True)
        else:
            att_data = frappe.db.sql(""" select * from `tabAttendance` where attendance_date BETWEEN '%s' and '%s' and ot IS NULL""" %(self.from_date,self.to_date),as_dict =True)
        for att in att_data:
            frappe.errprint(att.employee)
            self.append("ot_approval",{
                "attendance_name":att.name,
                "employee_id":att.employee,
                "in_time": att.in_time,
                "out_time" : att.out_time,
                "qr_scan_time":att.qr_scan_time,
                "total_working_hours":att.working_hours,
                "extra_hours":att.ot,
                "ot_hours":att.ot
            }).save(ignore_permissions=True)
            frappe.db.commit()
        return "ok"

    def get_data_id(self):
        frappe.errprint("employee")
        frappe.errprint(self.employee_id)
        frappe.errprint(self.from_date)
        frappe.errprint(self.to_date)
        att_data = frappe.db.sql(""" select * from `tabAttendance` where employee = '%s' and attendance_date BETWEEN '%s' and '%s' and ot IS NULL""" %(self.employee_id,self.from_date,self.to_date),as_dict =True)
        for att in att_data:
            frappe.errprint(att)
            self.append("ot_approval",{
                "attendance_name":att.name,
                "employee_id":att.employee,
                "in_time": att.in_time,
                "out_time" : att.out_time,
                "qr_scan_time":att.qr_scan_time,
                "total_working_hours":att.working_hours,
                "extra_hours":att.ot,
                "ot_hours":att.ot
            }).save(ignore_permissions=True)
            frappe.db.commit()
        return "ok"

    def update_attendance(self,row):
        frappe.db.set_value("Attendance",row["attendance_name"],"ot",row["ot_hours"])
        new_ts = frappe.new_doc("Timesheet")
        new_ts.employee = row['employee_id']
        
        new_ts.append("time_logs",{
            "hours":row['ot_hours'],
            "from_time":row['in_time'],
            "to_time":row['out_time']
        })
        new_ts.save(ignore_permissions=True)
        frappe.db.commit()
    



