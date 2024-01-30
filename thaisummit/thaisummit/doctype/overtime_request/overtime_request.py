# -*- coding: utf-8 -*-
# Copyright (c) 2021, TEAMPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from bs4 import element
from erpnext.hr.doctype.employee.employee import deactivate_sales_person
import frappe
from frappe.model.document import Document
from datetime import datetime,timedelta,date,time
from frappe.utils import add_days,today
import pandas as pd
from frappe import _

from pytz import HOUR

class OvertimeRequest(Document):
    
    def on_submit(self):
        user = frappe.session.user
        employee = frappe.get_value("Employee",{'user_id':user},['name'])
        if self.employee == employee :
            frappe.throw(_("HODs can't approve their own Overtime Application"))
        if self.workflow_state == 'Approved':
            if not frappe.db.exists('Overtime Request',{'overtime_request':self.name}):
                doc = frappe.new_doc('Timesheet')
                doc.employee = self.employee
                doc.overtime_request = self.name
                from_time = datetime.strptime(str(self.from_time), "%H:%M:%S").time()
                to_time = datetime.strptime(str(self.to_time), "%H:%M:%S").time()
                ot_date = datetime.date(datetime.strptime(str(self.ot_date),'%Y-%m-%d'))
                ftr = [3600,60,1]
                hr = sum([a*b for a,b in zip(ftr, map(int,str(self.ot_hours).split(':')))])
                doc.append('time_logs',{
                    'activity_type': 'Over Time',
                    'from_time': datetime.combine(ot_date,from_time),
                    'hours': hr/3600
                })
                doc.save(ignore_permissions=True)
                doc.submit()
                frappe.db.commit()
                
                
    def validate(self):
        today = frappe.db.sql("select count(*) as count from `tabOvertime Request` where employee = '%s' and ot_date = '%s' and name != '%s' and workflow_state != 'Rejected' "%(self.employee,self.ot_date,self.name),as_dict=True)
        if today[0].count >= 1:
            frappe.throw("Only 1 Overtime Request is allowed for a day for Employee - '%s' "%(self.employee))
    
    def on_update(self):
        data = []
        if self.workflow_state == 'Approved':
            payroll_start_date = frappe.db.get_value('Payroll Dates',{'name':'PAYROLL OT PERIOD DATE 0001'},['payroll_start_date'])
            payroll_end_date = frappe.db.get_value('Payroll Dates',{'name':'PAYROLL OT PERIOD DATE 0001'},['payroll_end_date'])
            # employee = frappe.db.get_value('Employee',{'name':self.employee},['department'])
            get_ot_hour_dept = frappe.db.get_value('Department',{'name':self.department},['overtime_hours_limit'])
            ot_request = frappe.db.get_all('Overtime Request',{'department':self.department,'ot_date':('between',(payroll_start_date,payroll_end_date)),'workflow_state':'Approved'},['*'])
            for ot in ot_request:
                ftr = [3600,60,1]
                try:
                    hr = sum([a*b for a,b in zip(ftr, map(int,str(ot.ot_hours).split(':')))])
                    ot_hr = round(hr/3600,1)
                    data.append(ot_hr)
                except:
                    ot_hr = 0
            total_ot_hour = sum(data) 
            frappe.errprint(type(total_ot_hour))
            frappe.errprint(type(get_ot_hour_dept))
            if total_ot_hour > get_ot_hour_dept:
                
                frappe.throw(_('%s department has reached the OT Hours limit'%(self.department))) 
                frappe.log_error('%s department has reached the OT Hours limit'%(self.department))
            else:
                message = ('Less than dept ot hour') 
                frappe.log_error('Overtime Request',message)       

    @frappe.whitelist()
    def send_for_approval(self):
        if self.workflow_state == 'Draft':
            if self.ot_hours and self.total_wh and self.bio_in and self.bio_out :
                if self.employee_type != 'CL':
                    basic = ((frappe.db.get_value('Employee',self.employee,'basic')/26)/8)*2
                    frappe.db.set_value('Overtime Request',self.name,'ot_basic',basic)
                    ftr = [3600,60,1]
                    hr = sum([a*b for a,b in zip(ftr, map(int,str(self.ot_hours).split(':')))])
                    ot_hr = round(hr/3600,1)
                    frappe.db.set_value('Overtime Request',self.name,'ot_amount',ot_hr*basic)
                else:
                    basic = 0
                    designation = frappe.db.get_value('Employee',self.employee,'designation')
                    if designation == 'Skilled':
                        basic = frappe.db.get_single_value('HR Time Settings','skilled_amount_per_hour')
                    elif designation == 'Un Skilled':
                        basic = frappe.db.get_single_value('HR Time Settings','unskilled_amount_per_hour')
                    frappe.db.set_value('Overtime Request',self.name,'ot_basic',basic)
                    ftr = [3600,60,1]
                    hr = sum([a*b for a,b in zip(ftr, map(int,str(self.ot_hours).split(':')))])
                    ot_hr = round(hr/3600,1)
                    frappe.db.set_value('Overtime Request',self.name,'ot_amount',ot_hr*basic)
                frappe.db.set_value('Overtime Request',self.name,'workflow_state','Pending for HOD')
                # basic = ((frappe.db.get_value('Employee',self.employee,'basic')/26)/8)*2
                # frappe.db.set_value('Overtime Request',self.name,'ot_basic',basic)
                # ftr = [3600,60,1]
                # hr = sum([a*b for a,b in zip(ftr, map(int,str(self.ot_hours).split(':')))])
                # ot_hr = round(hr/3600,1)
                # frappe.db.set_value('Overtime Request',self.name,'ot_amount',ot_hr*basic)

    @frappe.whitelist()
    def get_ot_amount(self):
        if self.employee_type != 'CL':
            basic = ((frappe.db.get_value('Employee',self.employee,'basic')/26)/8)*2
            ftr = [3600,60,1]
            hr = sum([a*b for a,b in zip(ftr, map(int,str(self.ot_hours).split(':')))])
            ot_hr = round(hr/3600,1)
            ot_amount = ot_hr*basic
        else:
            basic = 0
            designation = frappe.db.get_value('Employee',self.employee,'designation')
            if designation == 'Skilled':
                basic = frappe.db.get_single_value('HR Time Settings','skilled_amount_per_hour')
            elif designation == 'Un Skilled':
                basic = frappe.db.get_single_value('HR Time Settings','unskilled_amount_per_hour')
            ftr = [3600,60,1]
            hr = sum([a*b for a,b in zip(ftr, map(int,str(self.ot_hours).split(':')))])
            ot_hr = round(hr/3600,1)
            ot_amount = ot_hr*basic
        return basic, ot_amount

    @frappe.whitelist()
    def get_bio_checkins(self):
        od = frappe.db.sql("""select `tabOn Duty Application`.name from `tabOn Duty Application` 
        left join `tabMulti Employee` on `tabOn Duty Application`.name = `tabMulti Employee`.parent where 
        `tabMulti Employee`.employee = '%s' and '%s' between `tabOn Duty Application`.from_date and `tabOn Duty Application`.to_date and `tabOn Duty Application`.workflow_state = 'Approved' """%(self.employee,self.ot_date),as_dict=True)
        if od:
            self.on_duty = od[0].name
        else:
            if frappe.db.exists("Attendance",{'attendance_date':self.ot_date,'employee':self.employee,'docstatus':('!=','2')}):
                att = frappe.get_doc("Attendance",{'attendance_date':self.ot_date,'employee':self.employee,'docstatus':('!=','2')})
                if att.shift != 'PP2':
                    if att.in_time and att.out_time:
                        twh = att.out_time - att.in_time
                        self.bio_in = att.in_time
                        self.bio_out = att.out_time
                        self.total_wh = twh
                        self.on_duty = ''
                        return att.out_time
                    else:
                        self.bio_in = ''
                        self.bio_out = ''
                        self.total_wh = ''
                        self.to_time = ''
                        self.on_duty = ''
                        frappe.msgprint('Overtime Cannot be applied without Biometric In time and Out time')
                else:
                    twh = att.out_time - att.in_time
                    self.bio_in = att.in_time
                    self.bio_out = att.out_time
                    self.total_wh = twh
                    self.to_time = ''
                    self.on_duty = ''        
            else:
                self.bio_in = ''
                self.bio_out = ''
                self.total_wh = ''
                self.to_time = ''
                self.on_duty = ''
                frappe.msgprint('Overtime Cannot be applied without Biometric In time and Out time')

    @frappe.whitelist()
    def get_ot_total(self):
        total = datetime.strptime(self.to_time, '%H:%M:%S') - datetime.strptime(self.from_time, '%H:%M:%S')
        return total 
    
    @frappe.whitelist()
    def check_shift_time(self):
        shift = frappe.get_doc('Shift Type',self.shift)
        start_time = datetime.strptime(str(shift.start_time), '%H:%M:%S')
        end_time = datetime.strptime(str(shift.end_time), '%H:%M:%S')
        from_time = datetime.strptime(self.from_time, '%H:%M:%S')
        if not start_time <= from_time:
            frappe.throw('From Time should be within Shift Timing')
        
    @frappe.whitelist()
    def get_ceo(self,employee):
        department = frappe.db.get_value('Employee',employee,"department")
        ceo = frappe.db.get_value('Department',department,"ceo")
        return ceo
    
    @frappe.whitelist()
    def get_gm(self,employee):
        department = frappe.db.get_value('Employee',employee,"department")
        gm = frappe.db.get_value('Department',department,"gm")
        return gm

    @frappe.whitelist()
    def get_hod(self,employee):
        department = frappe.db.get_value('Employee',employee,"department")
        hod = frappe.db.get_value('Department',department,"hod")
        return hod
    
    # @frappe.whitelist()
    # def get_shift(self):
    #     from_time = datetime.strptime(str(self.from_datetime), "%Y-%m-%d %H:%M:%S").time()
    #     shift = frappe.db.sql('select name from `tabShift Type` where "%s" between start_time and end_time and name not in ("PP1","PP2") '%(from_time),as_dict=True)
    #     if shift:
    #         if from_time == '16:30:00':
    #             self.shift = 2
    #         else:
    #             if shift[0].name == '1':
    #                 if self.ot_date:
    #                     holiday = frappe.db.sql("""select `tabHoliday`.holiday_date from `tabHoliday List`
    #                     left join `tabHoliday` on `tabHoliday`.parent = `tabHoliday List`.name where `tabHoliday List`.name = 'Holiday List - 2021' and holiday_date = '%s' """%(self.ot_date),as_dict=True)
    #                     if not holiday:
    #                         self.shift = ''
    #                         self.from_datetime = ''
    #                         frappe.throw("Overtime Request from 8:00 AM to 16:30 PM can be applied only on Sunday or Holiday")
    #             self.shift = shift[0].name
    #     else:
    #         self.shift = 2

    @frappe.whitelist()
    def check_holiday(self):
        if self.ot_date:
            holiday = frappe.db.sql("""select `tabHoliday`.holiday_date from `tabHoliday List`
            left join `tabHoliday` on `tabHoliday`.parent = `tabHoliday List`.name where `tabHoliday List`.name = 'Holiday List - 2021' and holiday_date = '%s' """%(self.ot_date),as_dict=True)

            if not holiday:
                return 'NO'

@frappe.whitelist()
def check_holidays(ot_date):
    if ot_date:
        holiday = frappe.db.sql("""select `tabHoliday`.holiday_date from `tabHoliday List`
        left join `tabHoliday` on `tabHoliday`.parent = `tabHoliday List`.name where `tabHoliday List`.name = 'Holiday List - 2021' and holiday_date = '%s' """%(ot_date),as_dict=True)
        # return holiday
        if holiday:
            return holiday
        



@frappe.whitelist()
def ot_hours(shift,from_time,to_time,ot_date):
    ot_date = datetime.strptime(ot_date, "%Y-%m-%d").date()
    from_time = datetime.strptime(from_time, "%H:%M:%S").time()
    to_time = datetime.strptime(to_time, "%H:%M:%S").time()
    if shift == '3':
        ot_date = add_days(ot_date,1)
        from_datetime = datetime.combine(ot_date,from_time)
        to_datetime = datetime.combine(ot_date,to_time)
    elif shift == 'PP2':
        if to_time.hour > 20:
            from_datetime = datetime.combine(ot_date,from_time)
            to_datetime = datetime.combine(ot_date,to_time)
        else:
            from_datetime = datetime.combine(ot_date,from_time)
            # ot_date = add_days(ot_date,1)
            to_datetime = datetime.combine(ot_date,to_time)
    elif shift == '2':
        if to_time > time(16,30,0):
            from_datetime = datetime.combine(ot_date,from_time)
            to_datetime = datetime.combine(ot_date,to_time)
        else:
            from_datetime = datetime.combine(ot_date,from_time)
            ot_date = add_days(ot_date,1)
            to_datetime = datetime.combine(ot_date,to_time)
    else:
        from_datetime = datetime.combine(ot_date,from_time)
        to_datetime = datetime.combine(ot_date,to_time)
    if from_datetime > to_datetime:
        frappe.throw('From Time should be lesser that To Time')
    else:
        if shift == 'PP2':
            t_diff = datetime.strptime(str('03:30:00'), '%H:%M:%S').time()
        else:    
            t_diff = to_datetime - from_datetime
        time_diff = datetime.strptime(str(t_diff), '%H:%M:%S')
        if time_diff.hour > 24:
            frappe.throw('OT cannot applied for more than 24 hours')
    ot_hours = time(0,0,0)
    if time_diff.hour >= 1:
        if time_diff.minute <= 29:
            ot_hours = time(time_diff.hour,0,0)
        else:
            ot_hours = time(time_diff.hour,30,0)
    if time_diff.hour > 3:
        if shift == '1':
            if time_diff.minute <= 29:
                ot_hours = time(time_diff.hour-1,30,0)
            else:
                ot_hours = time(time_diff.hour,0,0)
        elif shift == '2':
            if time_diff.minute <= 29:
                ot_hours = time(time_diff.hour-1,30,0)
            else:
                ot_hours = time(time_diff.hour,0,0)
        elif  shift == '3':
            if time_diff.minute <= 29:
                ot_hours = time(time_diff.hour,0,0)
            else:
                ot_hours = time(time_diff.hour,30,0)
    if time_diff.hour > 12:
        # ot_hours = time(time_diff.hour-1,0,0)
        if shift == '1':
            if time_diff.minute <= 29:
                ot_hours = time(time_diff.hour-1,0,0)
            else:
                ot_hours = time(time_diff.hour-1,30,0)
        elif shift == '2':
            if time_diff.minute <= 29:
                ot_hours = time(time_diff.hour-1,30,0)
            else:
                ot_hours = time(time_diff.hour,0,0)
        elif  shift == '3':
            if time_diff.minute <= 29:
                ot_hours = time(time_diff.hour,0,0)
            else:
                ot_hours = time(time_diff.hour,30,0)
                
    return [str(t_diff),str(ot_hours)]
