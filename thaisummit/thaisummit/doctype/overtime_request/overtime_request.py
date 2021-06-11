# -*- coding: utf-8 -*-
# Copyright (c) 2021, TEAMPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from datetime import datetime,timedelta,date,time

class OvertimeRequest(Document):
    def on_submit(self):
        if self.workflow_state == 'Approved':
            doc = frappe.new_doc('Timesheet')
            doc.employee = self.employee
            from_time = datetime.strptime(str(self.from_time), "%H:%M:%S").time()
            to_time = datetime.strptime(str(self.to_time), "%H:%M:%S").time()
            from_date = datetime.date(datetime.strptime(str(self.from_date),'%Y-%m-%d'))
            to_date = datetime.date(datetime.strptime(str(self.from_date),'%Y-%m-%d'))
            ftr = [3600,60,1]
            hr = sum([a*b for a,b in zip(ftr, map(int,str(self.ot_hours).split(':')))])
            doc.append('time_logs',{
                'activity_type': 'Over Time',
                'from_time': datetime.combine(from_date,from_time),
                'to_time': datetime.combine(to_date,to_time),
                'hours': hr/3600
            })
            doc.save(ignore_permissions=True)
            doc.submit()
            frappe.db.commit()
    def validate(self):
        today = frappe.db.sql("select count(*) as count from `tabOvertime Request` where employee = '%s' and from_date = '%s' and name != '%s' and workflow_state != 'Rejected' "%(self.employee,self.from_date,self.name),as_dict=True)
        frappe.errprint(today)
        if today[0].count >= 1:
            frappe.throw("Only 1 Overtime Request are allowed for a day")

@frappe.whitelist()
def ot_hours(from_time,to_time):
    from_time = datetime.strptime(from_time, "%H:%M:%S")
    to_time = datetime.strptime(to_time, "%H:%M:%S")
    if from_time > to_time:
        frappe.throw('From Time should be lesser that To Time')
    else:
        t_diff = to_time - from_time
        time_diff = datetime.strptime(str(t_diff), '%H:%M:%S')
        ot_hours = time(0,0,0)
        if time_diff.hour >= 1:
            if time_diff.minute <= 29:
                ot_hours = time(time_diff.hour,0,0)
            else:
                ot_hours = time(time_diff.hour,30,0)
        if time_diff.hour >= 4:
            if time_diff.minute <= 29:
                ot_hours = time(time_diff.hour-1,30,0)
            else:
                ot_hours = time(time_diff.hour,0,0)
    return [str(t_diff),str(ot_hours)]
