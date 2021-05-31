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
            to_date = datetime.date(datetime.strptime(str(self.to_date),'%Y-%m-%d'))
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

@frappe.whitelist()
def ot_hours(from_time,to_time):
    from_time = datetime.strptime(from_time, "%H:%M:%S")
    to_time = datetime.strptime(to_time, "%H:%M:%S")
    # start_time = time - timedelta(hours=2)
    if from_time > to_time:
        frappe.throw('From Time should be lesser that To Time')
    else:
        ot_hours = to_time - from_time
        frappe.errprint(ot_hours)
    # frappe.errprint(to_time)
    # frappe.errprint(ot_hours)
    return ot_hours
