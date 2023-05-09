from tabnanny import check
from time import strptime
import frappe
import json
import datetime
from frappe.utils.csvutils import read_csv_content
from six.moves import range
from six import string_types
from frappe.utils import (getdate, cint, add_months, date_diff, add_days,get_time,
    nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime)
from datetime import datetime
from calendar import monthrange
from frappe import _, msgprint
from frappe.utils import flt
from frappe.utils import cstr, cint, getdate,get_first_day, get_last_day, today, time_diff_in_hours
import requests
from datetime import date, timedelta,time
from frappe.utils.csvutils import UnicodeWriter, read_csv_content
from frappe.utils.file_manager import get_file
from frappe.utils.background_jobs import enqueue

@frappe.whitelist()
def mark_attendance():
    i = 0
    for d in range(7):
        from_date = add_days('2022-10-26',i)
        i += 1
        mark_att(from_date)
       
@frappe.whitelist()
def mark_att_monthly_hooks():
    d = datetime.strptime(today(),"%Y-%m-%d")
    if int(d.strftime("%d")) <= 30:
        from_date = add_days(get_first_day(today()),-6)
    else:
        from_date = add_days(get_first_day(today()),25)
    for s in range(31):
        mark_att(from_date)
        # mark_shift_status(from_date)
        # mark_overtime(from_date)
        from_date = add_days(from_date,1)

@frappe.whitelist()
def mark_shift_status():
    d = datetime.strptime(today(),"%Y-%m-%d")
    if int(d.strftime("%d")) <= 30:
        from_date = add_days(get_first_day(today()),-6)
    else:
        from_date = add_days(get_first_day(today()),25)
    for s in range(31):
        # mark_att(from_date)
        # mark_shift_status(from_date)
        # mark_overtime(from_date)
        from_date = add_days(from_date,1)
    
def mark_att_daily_hooks():
    from_date = today()
    mark_att(from_date)
    from_date = add_days(today(),-1)
    mark_att(from_date)

@frappe.whitelist()
def enqueue_mark_att():
    enqueue(mark_att, queue='default', timeout=6000, event='mark_att',
                        )

@frappe.whitelist()
def mark_att(from_date):
    mark_on_duty(from_date)
    checkins = frappe.db.sql(
        """select * from `tabEmployee Checkin` where skip_auto_attendance = 0 and date(time) = '%s' order by time """%(from_date),as_dict=1)
    if checkins:
        for c in checkins:
            att = mark_attendance_from_checkin(c.name,c.employee,c.log_type,c.time)
            if att:
                frappe.db.set_value("Employee Checkin",
                                    c.name, "skip_auto_attendance", "1")
        mark_qr_checkin(from_date)
        # frappe.errprint('qr')
        mark_permission(from_date)  
        # frappe.errprint('per')
        mark_absent(from_date)
        mark_overtime(from_date)
        # frappe.errprint('ot')
        mark_shift_status(from_date)
        print('success')
        frappe.msgprint("Attendance Marked Successfully")
        return "ok"
    else:
        mark_qr_checkin(from_date)
        mark_permission(from_date)
        # enqueue(mark_absent, queue='default', timeout=6000, event='mark_absent')
        mark_absent(from_date)
        mark_overtime(from_date)
        # enqueue(mark_shift_status, queue='default', timeout=6000, event='mark_shift_status')
        mark_shift_status(from_date)
        frappe.msgprint("Attendance Marked Successfully")

def mark_attendance_from_checkin(checkin,employee,log_type,time):
    att_time = time.time()
    att_date = time.date()
    month_start_date = get_first_day(att_date)
    month_end_date = get_last_day(att_date)
    shift = ''
    if log_type == 'IN':
        min_in_time = ''
        max_in_time = ''
        min_in_time1 = datetime.strptime('06:00', '%H:%M').time()
        max_in_time1 = datetime.strptime('13:00', '%H:%M').time()
        min_in_time2 = datetime.strptime('13:00', '%H:%M').time()
        max_in_time2 = datetime.strptime('18:30', '%H:%M').time()
        min_in_time3 = datetime.strptime('00:01', '%H:%M').time()
        max_in_time3 = datetime.strptime('03:00', '%H:%M').time()
        min_in_timepp1 = datetime.strptime('06:00', '%H:%M').time()
        max_in_timepp1 = datetime.strptime('10:00', '%H:%M').time()
        min_in_timepp2 = datetime.strptime('18:00', '%H:%M').time()
        max_in_timepp2 = datetime.strptime('23:00', '%H:%M').time()
        # late1 = datetime.strptime('08:10', '%H:%M').time()
        # late2 = datetime.strptime('16:40', '%H:%M').time()
        # late3 = datetime.strptime('01:10', '%H:%M').time()
        # latepp1 = datetime.strptime('08:10', '%H:%M').time()
        # latepp2 = datetime.strptime('20:10', '%H:%M').time()
        late = 0
        status = 'Present'
        if max_in_time1 >= att_time >= min_in_time1:
            if frappe.db.get_value('Employee',employee,"default_shift") == 'PP1':
                shift = 'PP1'
            else:
                shift = '1'
            min_in_time = datetime.strptime('06:00', '%H:%M').time()
            max_in_time = datetime.strptime('13:00', '%H:%M').time()
            if datetime.strptime('08:01', '%H:%M').time() < att_time:
                late = 1
            # elif att_time > datetime.strptime('08:10', '%H:%M').time():
            #     status = 'Half Day'
        elif max_in_time2 >= att_time >= min_in_time2:
            shift = '2'
            min_in_time = datetime.strptime('13:00', '%H:%M').time()
            max_in_time = datetime.strptime('18:30', '%H:%M').time()
            if datetime.strptime('16:31', '%H:%M').time() < att_time:
                late = 1
            # elif att_time > datetime.strptime('16:40', '%H:%M').time():
            #     status = 'Half Day'
            #     print(status)
        elif max_in_time3 >= att_time >= min_in_time3:
            shift = '3'
            att_date = add_days(att_date,-1)
            min_in_time = datetime.strptime('00:01', '%H:%M').time()
            max_in_time = datetime.strptime('03:00', '%H:%M').time()
            if datetime.strptime('01:01', '%H:%M').time() < att_time:
                late = 1
            # elif att_time > datetime.strptime('01:10', '%H:%M').time():
            #     status = 'Half Day'
        elif max_in_timepp2 >= att_time >= min_in_timepp2:
            shift = 'PP2'
            min_in_time = datetime.strptime('18:30', '%H:%M').time()
            max_in_time = datetime.strptime('23:00', '%H:%M').time()
            if datetime.strptime('20:01', '%H:%M').time() < att_time:
                late = 1
            # elif att_time > datetime.strptime('20:10', '%H:%M').time():
            #     status = 'Half Day'
        if late == 1:
            hh = check_holiday(att_date)
            if hh:
                late = 0
                status = "Present"
            # count = frappe.db.sql("select count(*) as count from `tabAttendance` where employee = '%s' and docstatus != 2 and late_entry =1 and attendance_date between '%s' and '%s' "%(employee,month_start_date,month_end_date),as_dict = True)
            # if count[0].count:    
            #     if int(count[0].count) >= 2:
            else:
                status = 'Half Day'
        if min_in_time and max_in_time:
            att = frappe.db.exists("Attendance",{'employee':employee,'attendance_date':att_date,'docstatus': ['!=',2]})
            if not att:
                if shift != '3':
                    checkins = frappe.db.sql("select name,time from `tabEmployee Checkin` where employee = '%s' and log_type = 'IN' and date(time) = '%s' and time(time) between '%s' and '%s' order by time "%(employee,att_date,min_in_time,max_in_time),as_dict=True)
                else:
                    yesterday = add_days(att_date,1)
                    checkins = frappe.db.sql("select name,time from `tabEmployee Checkin` where employee = '%s' and log_type = 'IN' and date(time) = '%s' and time(time) between '%s' and '%s' order by time "%(employee,yesterday,min_in_time,max_in_time),as_dict=True)
                if checkins:
                    # qr_checkin = frappe.db.sql("select name, employee,qr_shift,qr_scan_time,shift_date from `tabQR Checkin` where employee = '%s' and date(qr_scan_time) = '%s' order by qr_scan_time "%(employee,att_date),as_dict=True)
                    att = frappe.new_doc("Attendance")
                    att.employee = employee
                    att.attendance_date = att_date
                    att.shift = shift
                    att.status = status
                    if status == 'Half Day':
                        att.leave_type = 'Leave Without Pay'
                    att.late_entry = late
                    att.in_time = checkins[0].time
                    att.save(ignore_permissions=True)
                    frappe.db.commit()
                    frappe.db.set_value("Employee Checkin",checkins[0].name, "attendance", att.name)
                    return att
            else:
                if shift != '3':
                    # checkins = []
                    checkins = frappe.db.sql("select name,time from `tabEmployee Checkin` where employee = '%s' and log_type = 'IN' and date(time) = '%s' and time(time) between '%s' and '%s' order by time "%(employee,att_date,min_in_time,max_in_time),as_dict=True)
                else:
                    yesterday = add_days(att_date,1)
                    checkins = frappe.db.sql("select name,time from `tabEmployee Checkin` where employee = '%s' and log_type = 'IN' and date(time) = '%s' and time(time) between '%s' and '%s' order by time "%(employee,yesterday,min_in_time,max_in_time),as_dict=True)
                # print([min_in_time,max_in_time])
                # print(checkins)
                if checkins:
                    att = frappe.get_doc("Attendance",att)
                    if att.docstatus == 0:
                        att.employee = employee
                        att.attendance_date = att_date
                        att.shift = shift
                        att.status = status
                        # if status == 'Half Day':
                        #     att.leave_type = 'Leave Without Pay'
                        att.late_entry = late
                        att.in_time = checkins[0].time
                        att.save(ignore_permissions=True)
                        frappe.db.commit()
                        frappe.db.set_value("Employee Checkin",checkins[0].name, "attendance", att.name)
                        return att
                    

    if log_type == 'OUT':
        max_out = datetime.strptime('11:30', '%H:%M').time()
        if att_time < max_out:
            yesterday = add_days(att_date,-1)
            checkins = frappe.db.sql("select name,time from `tabEmployee Checkin` where employee = '%s' and log_type = 'OUT' and date(time) = '%s' and time(time) < '%s' order by time "%(employee,att_date,max_out),as_dict=True)
            att = frappe.db.exists("Attendance",{'employee':employee,'attendance_date':yesterday})
            if att:
                att = frappe.get_doc("Attendance",att)
                if att.docstatus == 0:
                    if not att.out_time:
                        if len(checkins) > 0:
                            att.out_time = checkins[-1].time
                        else:
                            att.out_time = checkins[-1].time
                        att.save(ignore_permissions=True)
                        frappe.db.commit()
                        frappe.db.set_value("Employee Checkin",checkins[0].name, "attendance", att.name)
                        return att
                    else:
                        return att
            else:
                att = frappe.new_doc("Attendance")
                att.employee = employee
                att.attendance_date = yesterday
                # att.shift_type = shift
                att.status = 'Absent'
                if len(checkins) > 0:
                    att.out_time = checkins[-1].time
                else:
                    att.out_time = checkins[-1].time
                att.save(ignore_permissions=True)
                frappe.db.commit()
                frappe.db.set_value("Employee Checkin",checkins[0].name, "attendance", att.name)
                return att
        else:
            checkins = frappe.db.sql("select name,time,docstatus from `tabEmployee Checkin` where employee ='%s' and log_type = 'OUT' and date(time) = '%s' order by time "%(employee,att_date),as_dict=True)
            att = frappe.db.exists("Attendance",{'employee':employee,'attendance_date':att_date})
            if att:
                att = frappe.get_doc("Attendance",att)
                if att.docstatus == 0:
                    if not att.out_time:
                        if len(checkins) > 0:
                            att.out_time = checkins[-1].time
                        else:
                            att.out_time = checkins[-1].time
                        att.save(ignore_permissions=True)
                        # if att.shift == att.qr_shift:
                            # att.submit()
                        frappe.db.commit()
                        frappe.db.set_value("Employee Checkin",checkins[0].name, "attendance", att.name)
                        return att
                    else:
                        return att
            else:
                att = frappe.new_doc("Attendance")
                att.employee = employee
                att.attendance_date = att_date
                # att.shift_type = shift
                att.status = 'Absent'
                if len(checkins) > 0:
                    att.out_time = checkins[-1].time
                else:
                    att.out_time = checkins[-1].time
                att.save(ignore_permissions=True)
                frappe.db.commit()
                frappe.db.set_value("Employee Checkin",checkins[0].name, "attendance", att.name)
                return att


def mark_qr_checkin(from_date):
    # from_date = '2022-04-15'
    hh = check_holiday(from_date)
    if hh:
        qr_checkins = frappe.db.sql("select name, employee,qr_shift,qr_scan_time,shift_date from `tabQR Checkin` where shift_date = '%s' and ot = 1 order by qr_scan_time "%(from_date),as_dict=True)
        # print(len(qr_checkins))
        for qr in qr_checkins:
            if frappe.db.exists('Attendance',{'attendance_date':qr.shift_date,'employee':qr.employee,'docstatus':'0'}):
                att = frappe.get_doc('Attendance',{'attendance_date':qr.shift_date,'employee':qr.employee})
                att.qr_shift = qr.qr_shift
                att.qr_scan_time = qr.qr_scan_time
                att.save(ignore_permissions=True)
                frappe.db.commit()
                frappe.db.set_value("QR Checkin",qr.name, "attendance", att.name)
    else:
        qr_checkins = frappe.db.sql("select name, employee,qr_shift,qr_scan_time,shift_date from `tabQR Checkin` where shift_date = '%s' and ot = 0 order by qr_scan_time "%(from_date),as_dict=True)
        for qr in qr_checkins:
            if frappe.db.exists('Attendance',{'attendance_date':qr.shift_date,'employee':qr.employee,'docstatus':'0'}):
                att = frappe.get_doc('Attendance',{'attendance_date':qr.shift_date,'employee':qr.employee})
                att.qr_shift = qr.qr_shift
                att.qr_scan_time = qr.qr_scan_time
                att.save(ignore_permissions=True)
                frappe.db.commit()
                frappe.db.set_value("QR Checkin",qr.name, "attendance", att.name)
                frappe.errprint("Created")

def check_holiday(date):
    holiday = frappe.db.sql("""select `tabHoliday`.holiday_date,`tabHoliday`.weekly_off from `tabHoliday List` 
    left join `tabHoliday` on `tabHoliday`.parent = `tabHoliday List`.name where `tabHoliday List`.name = 'Holiday List - 2021' and holiday_date = '%s' """%(date),as_dict=True)
    if holiday:
        if holiday[0].weekly_off == 1:
            return "WW"
        else:
            return "HH"

# def mark_shift_status_individual(att):
#     late = ''
#     shift_status = ''
#     att = frappe.get_doc('Attendance',att)
#     if att.late_entry:
#         late = 'L'
#     if att.employee_type != "WC":
#         if not att.in_time or not att.out_time:
#             if att.qr_shift:
#                 shift_status = "M" + str(att.qr_shift)
#             else:
#                 shift_status = "AA"
#         if att.in_time and att.out_time:
#             if not att.qr_shift:
#                 shift_status = str(att.shift) + late + "M"
#             else:
#                 shift_status = str(att.shift) + late + str(att.qr_shift)         
#         if att.status == 'Half Day':
#             if att.leave_type:
#                 if not late:
#                     shift_status = str(0.5) + att.leave_type
#                 else:
#                     shift_status = late + str(att.leave_type) + str('/2')
#         if att.status == 'On Leave':
#             shift_status = att.leave_type
#         if att.on_duty_application:
#             shift_status = "OD"
#     else:
#         if att.status == 'Half Day':
#             if att.leave_type:
#                 if not late:
#                     shift_status = str(0.5) + att.leave_type
#                 else:
#                     shift_status = late + str(att.leave_type) + str('/2')
#         if att.status == 'On Leave':
#             shift_status = att.leave_type
#         elif att.on_duty_application:
#             shift_status = "OD"
#         elif att.shift:
#             if att.in_time and att.out_time:
#                 shift_status = str(att.shift) + late
                    
#             if not att.out_time:
#                 shift_status = str(att.shift) + 'M'
#         else:
#             shift_status = 'AA'
#     frappe.db.set_value('Attendance',att.name,'shift_status',shift_status)

# def mark_shift_status(self,method):
#     late = ''
#     shift_status = ''
#     if self.late_entry:
#         late = 'L'
#     if self.employee_type != "WC":
#         if not self.in_time or not self.out_time:
#             if self.qr_shift:
#                 shift_status = "M" + str(self.qr_shift)
#             else:
#                 shift_status = "AA"
#         if self.in_time and self.out_time:
#             if not self.qr_shift:
#                 shift_status = str(self.shift) + late + "M"
#             else:
#                 shift_status = str(self.shift) + late + str(self.qr_shift)         
#         if self.status == 'Half Day':
#             if self.leave_type:
#                 if not late:
#                     shift_status = str(0.5) + self.leave_type
#                 else:
#                     shift_status = late + str(self.leave_type) + str('/2')
#         if self.status == 'On Leave':
#             shift_status = self.leave_type
#         if self.on_duty_application:
#             shift_status = "OD"
#     else:
#         if self.status == 'Half Day':
#             if self.leave_type:
#                 if not late:
#                     shift_status = str(0.5) + self.leave_type
#                 else:
#                     shift_status = late + str(self.leave_type) + str('/2')
#         if self.status == 'On Leave':
#             shift_status = self.leave_type
#         elif self.on_duty_application:
#             shift_status = "OD"
#         elif self.shift:
#             if self.in_time and self.out_time:
#                 shift_status = str(self.shift) + late
                    
#             if not self.out_time:
#                 shift_status = str(self.shift) + 'M'
#         else:
#             shift_status = 'AA'
#     frappe.db.set_value('Attendance',self.name,'shift_status',shift_status)

@frappe.whitelist()
def shift_status_single_day(doc,method):
    mark_shift_status(doc.from_date)

@frappe.whitelist()
def mark_shift_status(from_date):
    to_date = from_date
    from_date = add_days(from_date,-1)
    atts = frappe.get_all('Attendance',{'attendance_date':('between',(from_date,to_date))},['*'])
    for att in atts:
        late = ''
        shift_status = ''
        if att.late_entry:
            late = 'L'
        if att.employee_type != "WC":
            if not att.in_time or not att.out_time:
                if att.qr_shift:
                    shift_status = "M" + str(att.qr_shift)
                else:
                    shift_status = "AA"
            if att.in_time and att.out_time:
                if not att.qr_shift:
                    shift_status = str(att.shift) + late + "M"
                else:
                    shift_status = str(att.shift) + late + str(att.qr_shift)         
            if att.status == 'Half Day':
                if att.leave_type:
                    if not late:
                        shift_status = str(0.5) + att.leave_type
                    else:
                        shift_status = late + str(att.leave_type) + str('/2')
                else:
                    shift_status = '0.5Leave Without Pay'
            if att.status == 'On Leave':
                shift_status = att.leave_type   
            if att.on_duty_application:
                hh = check_holiday(from_date)
                if hh:
                    if hh == 'WW':
                        shift_status = "ODW"
                    else:
                        shift_status = "ODH"
                else:
                    shift_status = "OD"
        else:
            if att.status == 'Half Day':
                if att.leave_type:
                    shift_status = str(0.5) + att.leave_type
                else:
                    shift_status = '0.5Leave Without Pay'
            elif att.status == 'On Leave':
                shift_status = att.leave_type
            elif att.on_duty_application:
                shift_status = "OD"
            elif att.shift:
                if att.in_time and att.out_time:
                    shift_status = str(att.shift) + late
                        
                if not att.out_time:
                    shift_status = str(att.shift) + 'M'
            else:
                shift_status = 'AA'
        if not att.manually_corrected:
            frappe.db.set_value('Attendance',att.name,'shift_status',shift_status)
            absent = ('12','13','21','23','31','32','1L2','1L3','2L1','2L3','3L1','3L2','PP1L2','PP2L3','1M','2M','3M','MM','M1','M2','M3','MPP2','AA','LA','LOP','1LM','2LM','3LM','PP2LM','PP2M')
            if att.status != 'On Leave':
                if att.status not in ('Half Day','On Leave'):
                    frappe.db.set_value('Attendance',att.name,'status','Present')
                if shift_status in absent:
                    frappe.db.set_value('Attendance',att.name,'status','Absent')
    return 'ok'

@frappe.whitelist()
def mark_shift_status_bulk():
    atts = frappe.get_all('Attendance',{'attendance_date':('between',('2021-08-26','2021-09-07')),'docstatus':('!=',2)},['*'])
    for att in atts:
        late = ''
        shift_status = ''
        if att.late_entry:
            late = 'L'
        if att.employee_type != "WC":
            if not att.in_time or not att.out_time:
                if att.qr_shift:
                    shift_status = "M" + str(att.qr_shift)
                else:
                    shift_status = "AA"
            if att.in_time and att.out_time:
                if not att.qr_shift:
                    shift_status = str(att.shift) + late + "M"
                else:
                    shift_status = str(att.shift) + late + str(att.qr_shift)         
            if att.status == 'Half Day':
                if att.leave_type:
                    if not late:
                        shift_status = str(0.5) + att.leave_type
                    else:
                        shift_status = late + str(att.leave_type) + str('/2')
            if att.status == 'On Leave':
                shift_status = att.leave_type
            if att.on_duty_application:
                shift_status = "OD"
        else:
            if att.status == 'Half Day':
                if att.leave_type:
                    if not late:
                        shift_status = str(0.5) + att.leave_type
                    else:
                        shift_status = late + str(att.leave_type) + str('/2')
            if att.status == 'On Leave':
                shift_status = att.leave_type
            elif att.on_duty_application:
                shift_status = "OD"
            elif att.shift:
                if att.in_time and att.out_time:
                    shift_status = str(att.shift) + late
                        
                if not att.out_time:
                    shift_status = str(att.shift) + 'M'
            else:
                shift_status = 'AA'
        frappe.db.set_value('Attendance',att.name,'shift_status',shift_status)
    return 'ok'


def mark_absent(from_date):
    emps = frappe.get_all("Employee",{'status':'Active','vacant':'0','date_of_joining':['<=',from_date]})
    for emp in emps:
        if not frappe.db.exists('Attendance',{'attendance_date':from_date,'employee':emp.name}):
            doc = frappe.new_doc('Attendance')
            doc.employee = emp.name
            doc.status = 'Absent'
            doc.attendance_date = from_date
            doc.save(ignore_permissions=True)
            frappe.db.commit()
    

def mark_on_duty(from_date):
    ods = frappe.db.sql("""select `tabOn Duty Application`.name, `tabOn Duty Application`.from_date,`tabOn Duty Application`.workflow_state,`tabOn Duty Application`.to_date,`tabMulti Employee`.employee
    from `tabOn Duty Application`
    left join `tabMulti Employee` on `tabOn Duty Application`.name = `tabMulti Employee`.parent
    where '%s' between from_date and to_date and workflow_state = 'Approved' and `tabOn Duty Application`.docstatus = 1 """%(from_date),as_dict=True)
    for od in ods:
        onduty = frappe.db.exists('Attendance',{'employee':od.employee,'attendance_date':from_date,'docstatus':('!=','2')})
        if not onduty:
            att = frappe.new_doc("Attendance")
            att.employee = od.employee
            att.status = "Present"
            att.attendance_date = from_date
            att.on_duty_application = od.name
            att.save(ignore_permissions=True)
            # att.submit()
            frappe.db.commit()
        else:
            frappe.db.set_value('Attendance',onduty,"on_duty_application",od.name)

def mark_permission(from_date):
    pr_list = frappe.db.sql("""SELECT employee,attendance_date,shift,session FROM `tabPermission Request` 
    WHERE docstatus=1 and workflow_state = 'Approved' and attendance_date = '%s' """%from_date,as_dict=True)
    for pr in pr_list:
        attendance = frappe.db.exists("Attendance",{"employee": pr.employee,"attendance_date":pr.attendance_date,"docstatus":['!=',2]})
        if attendance:
            att = frappe.get_doc("Attendance",attendance)
            if att.in_time and att.out_time:
                in_t = datetime.strptime(str(att.in_time.time()), '%H:%M:%S')
                out_t = datetime.strptime(str(att.out_time.time()), '%H:%M:%S')
                if pr.session == 'First Half':
                    if pr.shift == '1':
                        shift_in = datetime.strptime('08:00', '%H:%M')
                        diff = time_diff_in_hours(in_t,shift_in)
                    elif pr.shift == '2':
                        shift_in = datetime.strptime('16:30', '%H:%M')
                        diff = time_diff_in_hours(in_t,shift_in)
                    elif pr.shift == '3':
                        shift_in = datetime.strptime('01:00', '%H:%M')
                        diff = time_diff_in_hours(in_t,shift_in)
                    elif pr.shift == 'PP1':
                        shift_in = datetime.strptime('08:00', '%H:%M')
                        diff = time_diff_in_hours(in_t,shift_in)
                    elif pr.shift == 'PP2':
                        shift_in = datetime.strptime('20:00', '%H:%M')
                        diff = time_diff_in_hours(in_t,shift_in)
                    if diff <= 2:
                        status = 'Present'
                    else:
                        status = 'Half Day'
                elif pr.session == 'Second Half':
                    if pr.shift == '1':
                        shift_out = datetime.strptime('16:30', '%H:%M')
                        diff = time_diff_in_hours(shift_out,out_t)
                    elif pr.shift == '2':
                        shift_out = datetime.strptime('01:00', '%H:%M')
                        diff = time_diff_in_hours(shift_out,out_t)
                    elif pr.shift == '3':
                        shift_out = datetime.strptime('08:00', '%H:%M')
                        diff = time_diff_in_hours(shift_out,out_t)
                    elif pr.shift == 'PP1':
                        shift_out = datetime.strptime('20:00', '%H:%M')
                        diff = time_diff_in_hours(shift_out,out_t)
                    elif pr.shift == 'PP2':
                        shift_out = datetime.strptime('08:00', '%H:%M')
                        diff = time_diff_in_hours(shift_out,out_t)
                    if diff <= 2:
                        status = 'Present'
                    else:
                        status = 'Half Day'
                att.status = status
                att.permission_request = pr.name
                att.save(ignore_permissions =True)
                # att.submit()
                frappe.db.commit()
                # if att.status in ('Half Day'):
                #     from erpnext.hr.doctype.leave_application.leave_application import get_leave_details
                #     leave_balance = get_leave_details(att.employee,nowdate())
                #     leave_approver = component_amount = frappe.get_list("Department Approver",filters={'parent': att.department,'parentfield':"leave_approvers"},fields=["approver"])
                #     if leave_approver:
                #         lev_approver = leave_approver[0].approver
                #     try:
                #         if (leave_balance['leave_allocation']['Casual Leave']['remaining_leaves']) > 0:
                #             leave_app = frappe.new_doc("Leave Application")
                #             leave_app.employee = att.employee
                #             leave_app.from_date = att.attendance_date
                #             leave_app.to_date = att.attendance_date
                #             leave_app.leave_type = 'Casual Leave'
                #             leave_app.description = 'Auto-Leave for Exceeding Permission Hours'
                #             leave_app.leave_approver = lev_approver
                #             leave_app.save(ignore_permissions=True)
                #             frappe.db.commit()
                #         elif(leave_balance['leave_allocation']['Sick Leave']['remaining_leaves']) > 0:
                #             l_app = frappe.new_doc("Leave Application")
                #             l_app.employee = att.employee
                #             l_app.from_date = att.attendance_date
                #             l_app.to_date = att.attendance_date
                #             l_app.leave_type = 'Sick Leave'
                #             l_app.description = 'Auto-Leave for Exceeding Permission Hours'
                #             l_app.leave_approver = lev_approver
                #             l_app.save(ignore_permissions=True)
                #             frappe.db.commit()
                #         elif (leave_balance['leave_allocation']['Earned Leave']['remaining_leaves']) > 0:
                #             lea_app = frappe.new_doc("Leave Application")
                #             lea_app.employee = att.employee
                #             lea_app.from_date = att.attendance_date
                #             lea_app.to_date = att.attendance_date
                #             lea_app.leave_type = 'Earned Leave'
                #             lea_app.description = 'Auto-Leave for Exceeding Permission Hours'
                #             lea_app.leave_approver = lev_approver
                #             lea_app.save(ignore_permissions=True)
                #             frappe.db.commit()           
                #     except KeyError:
                #         leave_balance['leave_allocation']['Casual Leave'] = 0
                #         leave_balance['leave_allocation']['Sick Leave'] = 0
                        # leave_balance['leave_allocation']['Earned Leave'] = 0

@frappe.whitelist()
def mark_overtime(from_date):
    ots = frappe.db.sql("select * from `tabOvertime Request` where ot_date = '%s' and docstatus != 1 "%(from_date),as_dict=True)
    for ot in ots:
        frappe.errprint(ot.name)
        od = frappe.db.sql("""select `tabOn Duty Application`.name from `tabOn Duty Application` 
        left join `tabMulti Employee` on `tabOn Duty Application`.name = `tabMulti Employee`.parent where 
        `tabMulti Employee`.employee = '%s' and '%s' between `tabOn Duty Application`.from_date and `tabOn Duty Application`.to_date and `tabOn Duty Application`.workflow_state = 'Approved' """%(ot.employee,from_date),as_dict=True)
        if od:
            if ot.ot_hours:
                ftr = [3600,60,1]
                hr = sum([a*b for a,b in zip(ftr, map(int,str(ot.ot_hours).split(':')))])
                ot_hr = round(hr/3600,1)
                if ot_hr > 0:
                    frappe.db.set_value('Overtime Request',ot.name,'workflow_state','Pending for HOD')
            frappe.db.set_value('Overtime Request',ot.name,'on_duty',od[0].name)
            if ot.ot_hours:
                if ot.employee_type != 'CL':
                    basic = ((frappe.db.get_value('Employee',ot.employee,'basic')/26)/8)*2
                    frappe.db.set_value('Overtime Request',ot.name,'ot_basic',basic)
                    ftr = [3600,60,1]
                    frappe.errprint(ot.name)
                    hr = sum([a*b for a,b in zip(ftr, map(int,str(ot.ot_hours).split(':')))])
                    ot_hr = round(hr/3600,1)
                    frappe.db.set_value('Overtime Request',ot.name,'ot_amount',round(ot_hr*basic))
                else:
                    basic = 0
                    designation = frappe.db.get_value('Employee',ot.employee,'designation')
                    if designation == 'Skilled':
                        # basic = 116
                        basic = frappe.db.get_single_value('HR Time Settings','skilled_amount_per_hour')
                    elif designation == 'Un Skilled':
                        # basic = 127
                        basic = frappe.db.get_single_value('HR Time Settings','unskilled_amount_per_hour')
                    frappe.db.set_value('Overtime Request',ot.name,'ot_basic',basic)
                    ftr = [3600,60,1]
                    hr = sum([a*b for a,b in zip(ftr, map(int,str(ot.ot_hours).split(':')))])
                    ot_hr = round(hr/3600,1)
                    frappe.db.set_value('Overtime Request',ot.name,'ot_amount',round(ot_hr*basic))
        else:
            if frappe.db.exists("Attendance",{'attendance_date':from_date,'employee':ot.employee,'docstatus':('!=','2')}):
                att = frappe.get_doc("Attendance",{'attendance_date':from_date,'employee':ot.employee,'docstatus':('!=','2')})
                if att.in_time and att.out_time:
                    twh = att.out_time - att.in_time
                    frappe.db.set_value('Overtime Request',ot.name,'bio_in',att.in_time)
                    frappe.db.set_value('Overtime Request',ot.name,'bio_out',att.out_time)
                    frappe.db.set_value('Overtime Request',ot.name,'to_time',att.out_time)
                    frappe.db.set_value('Overtime Request',ot.name,'total_wh',twh)
                    frappe.db.set_value('Overtime Request',ot.name,'workflow_state','Pending for HOD')
                    
                    from_time = datetime.strptime(str(ot.from_time), "%H:%M:%S").time()
                    to_time = frappe.db.get_value('Overtime Request',ot.name,"to_time")
                    try:
                        to_time = datetime.strptime(str(to_time), "%H:%M:%S").time()
                    except:
                        frappe.throw(_('Employee %s have no to time in Overtime Request kindly clear then only OT Will Process'%(ot.employee)))        
                    ot_date = frappe.db.get_value('Overtime Request',ot.name,"ot_date")
                    shift = frappe.db.get_value('Overtime Request',ot.name,"shift")
                    if from_time and to_time:
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
                            if to_time >= time(16,30,0):
                                from_datetime = datetime.combine(ot_date,from_time)
                                to_datetime = datetime.combine(ot_date,to_time)
                            else:
                                # print('hi')
                                from_datetime = datetime.combine(ot_date,from_time)
                                ot_date = add_days(ot_date,1)
                                to_datetime = datetime.combine(ot_date,to_time)
                        elif shift == '1':
                            if to_time <= time(8,0,0):
                                from_datetime = datetime.combine(ot_date,from_time)
                                ot_date = add_days(ot_date,1)
                                to_datetime = datetime.combine(ot_date,to_time)
                            else:
                                from_datetime = datetime.combine(ot_date,from_time)
                                to_datetime = datetime.combine(ot_date,to_time)
                        else:
                            from_datetime = datetime.combine(ot_date,from_time)
                            to_datetime = datetime.combine(ot_date,to_time)
                        if from_datetime > to_datetime:
                            frappe.throw(_('From Time should be lesser that To Time in %s'%(ot.name))) 
                        else:
                            if shift == 'PP2':
                                t_diff = datetime.strptime(str('03:30:00'), '%H:%M:%S').time()
                            else:    
                                t_diff = to_datetime - from_datetime
                            try:
                                time_diff = datetime.strptime(str(t_diff), '%H:%M:%S')
                            except:
                                time_diff = datetime.strptime(str('23:59:00'), '%H:%M:%S')
                            if time_diff.hour > 24:
                                frappe.throw('OT cannot applied for more than 24 hours')
                            
                            ot_hours = time(0,0,0)
                            if time_diff.hour >= 1:
                                if time_diff.minute <= 29:
                                    ot_hours = time(time_diff.hour,0,0)
                                else:
                                    ot_hours = time(time_diff.hour,30,0)
                            if time_diff.hour > 4:
                                if shift != '3':
                                    if time_diff.minute <= 29:
                                        ot_hours = time(time_diff.hour-1,30,0)
                                    else:
                                        ot_hours = time(time_diff.hour,0,0)
                                else:
                                    if time_diff.minute <= 29:
                                        ot_hours = time(time_diff.hour,0,0)
                                    else:
                                        ot_hours = time(time_diff.hour,30,0)
                            if time_diff.hour > 13:
                                ot_hours = time(time_diff.hour-1,0,0)
                            if time_diff.hour >= 23:
                                ot_hours = time(23,0,0)
                                # if shift != '3':
                                #     if time_diff.minute <= 29:
                                #         ot_hours = time(time_diff.hour-1,30,0)
                                #     else:
                                #         ot_hours = time(time_diff.hour,0,0)
                                # else:
                                #     if time_diff.minute <= 29:
                                #         ot_hours = time(time_diff.hour,0,0)
                                #     else:
                                #         ot_hours = time(time_diff.hour,30,0)
                        frappe.db.set_value('Overtime Request',ot.name,'total_hours',t_diff)
                        frappe.db.set_value('Overtime Request',ot.name,'ot_hours',ot_hours)
                        frappe.db.set_value('Overtime Request',ot.name,'workflow_state','Pending for HOD')

                        if ot.employee_type != 'CL':
                            basic = ((frappe.db.get_value('Employee',ot.employee,'basic')/26)/8)*2
                            frappe.db.set_value('Overtime Request',ot.name,'ot_basic',basic)
                            ftr = [3600,60,1]
                            hr = sum([a*b for a,b in zip(ftr, map(int,str(ot_hours).split(':')))])
                            ot_hr = round(hr/3600,1)
                            frappe.db.set_value('Overtime Request',ot.name,'ot_amount',round(ot_hr*basic))
                        else:
                            basic = 0
                            designation = frappe.db.get_value('Employee',ot.employee,'designation')
                            if designation == 'Skilled':
                                basic = frappe.db.get_single_value('HR Time Settings','skilled_amount_per_hour')
                            elif designation == 'Un Skilled':
                                basic = frappe.db.get_single_value('HR Time Settings','unskilled_amount_per_hour')
                            frappe.db.set_value('Overtime Request',ot.name,'ot_basic',basic)
                            ftr = [3600,60,1]
                            hr = sum([a*b for a,b in zip(ftr, map(int,str(ot_hours).split(':')))])
                            ot_hr = round(hr/3600,1)
                            frappe.db.set_value('Overtime Request',ot.name,'ot_amount',round(ot_hr*basic))
                
    ots = frappe.get_all('Overtime Request',{'ot_date':from_date},['name','employee','ot_hours','employee_type','ot_date'])
    for ot in ots:
        if ot.employee_type != 'CL':
            if ot.ot_hours:
                frappe.errprint(ot.employee)
                frappe.errprint(ot.ot_date)
                basic = ((frappe.db.get_value('Employee',ot.employee,'basic')/26)/8)*2
                frappe.db.set_value('Overtime Request',ot.name,'ot_basic',basic)
                ftr = [3600,60,1]
                hr = sum([a*b for a,b in zip(ftr, map(int,str(ot.ot_hours).split(':')))])
                ot_hr = round(hr/3600,1)
                frappe.db.set_value('Overtime Request',ot.name,'ot_amount',round(ot_hr*basic))
        else:
            basic = 0
            designation = frappe.db.get_value('Employee',ot.employee,'designation')
            if designation == 'Skilled':
                basic = frappe.db.get_single_value('HR Time Settings','skilled_amount_per_hour')
            elif designation == 'Un Skilled':
                basic = frappe.db.get_single_value('HR Time Settings','unskilled_amount_per_hour')
            frappe.db.set_value('Overtime Request',ot.name,'ot_basic',basic)
            if ot.ot_hours:
                ftr = [3600,60,1]
                hr = sum([a*b for a,b in zip(ftr, map(int,str(ot.ot_hours).split(':')))])
                ot_hr = round(hr/3600,1)
                frappe.db.set_value('Overtime Request',ot.name,'ot_amount',round(ot_hr*basic))       


@frappe.whitelist()
def process_overtime(from_date):
    ots = frappe.db.sql("select * from `tabOvertime Request` where ot_date = '%s' and docstatus != 1 "%(from_date),as_dict=True)
    for ot in ots:
        od = frappe.db.sql("""select `tabOn Duty Application`.name from `tabOn Duty Application` 
        left join `tabMulti Employee` on `tabOn Duty Application`.name = `tabMulti Employee`.parent where 
        `tabMulti Employee`.employee = '%s' and '%s' between `tabOn Duty Application`.from_date and `tabOn Duty Application`.to_date and `tabOn Duty Application`.workflow_state = 'Approved' """%(ot.employee,from_date),as_dict=True)
        if od:
            if ot.ot_hours:
                ftr = [3600,60,1]
                hr = sum([a*b for a,b in zip(ftr, map(int,str(ot.ot_hours).split(':')))])
                ot_hr = round(hr/3600,1)
                if ot_hr > 0:
                    frappe.db.set_value('Overtime Request',ot.name,'workflow_state','Pending for HOD')
            frappe.db.set_value('Overtime Request',ot.name,'on_duty',od[0].name)
            if ot.ot_hours:
                if ot.employee_type != 'CL':
                    basic = ((frappe.db.get_value('Employee',ot.employee,'basic')/26)/8)*2
                    frappe.db.set_value('Overtime Request',ot.name,'ot_basic',basic)
                    ftr = [3600,60,1]
                    hr = sum([a*b for a,b in zip(ftr, map(int,str(ot.ot_hours).split(':')))])
                    ot_hr = round(hr/3600,1)
                    frappe.db.set_value('Overtime Request',ot.name,'ot_amount',round(ot_hr*basic))
                else:
                    basic = 0
                    designation = frappe.db.get_value('Employee',ot.employee,'designation')
                    if designation == 'Skilled':
                        basic = frappe.db.get_single_value('HR Time Settings','skilled_amount_per_hour')
                    elif designation == 'Un Skilled':
                        basic = frappe.db.get_single_value('HR Time Settings','unskilled_amount_per_hour')
                    frappe.db.set_value('Overtime Request',ot.name,'ot_basic',basic)
                    ftr = [3600,60,1]
                    hr = sum([a*b for a,b in zip(ftr, map(int,str(ot.ot_hours).split(':')))])
                    ot_hr = round(hr/3600,1)
                    frappe.db.set_value('Overtime Request',ot.name,'ot_amount',round(ot_hr*basic))
        else:
            if frappe.db.exists("Attendance",{'attendance_date':from_date,'employee':ot.employee,'docstatus':('!=','2')}):
                att = frappe.get_doc("Attendance",{'attendance_date':from_date,'employee':ot.employee,'docstatus':('!=','2')})
                if att.in_time and att.out_time:
                    twh = att.out_time - att.in_time
                    frappe.db.set_value('Overtime Request',ot.name,'bio_in',att.in_time)
                    frappe.db.set_value('Overtime Request',ot.name,'bio_out',att.out_time)
                    frappe.db.set_value('Overtime Request',ot.name,'to_time',att.out_time)
                    frappe.db.set_value('Overtime Request',ot.name,'total_wh',twh)
                    frappe.db.set_value('Overtime Request',ot.name,'workflow_state','Pending for HOD')
                    
                    from_time = datetime.strptime(str(ot.from_time), "%H:%M:%S").time()
                    to_time = frappe.db.get_value('Overtime Request',ot.name,"to_time")
                    try:
                        to_time = datetime.strptime(str(to_time), "%H:%M:%S").time()
                    except:
                        frappe.throw(_('Employee %s have no to time in Overtime Request kindly clear then only OT Will Process'%(ot.employee)))        
                    ot_date = frappe.db.get_value('Overtime Request',ot.name,"ot_date")
                    shift = frappe.db.get_value('Overtime Request',ot.name,"shift")
                    if from_time and to_time:
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
                            if to_time >= time(16,30,0):
                                from_datetime = datetime.combine(ot_date,from_time)
                                to_datetime = datetime.combine(ot_date,to_time)
                            else:
                                from_datetime = datetime.combine(ot_date,from_time)
                                ot_date = add_days(ot_date,1)
                                to_datetime = datetime.combine(ot_date,to_time)
                        elif shift == '1':
                            if to_time <= time(8,0,0):
                                from_datetime = datetime.combine(ot_date,from_time)
                                ot_date = add_days(ot_date,1)
                                to_datetime = datetime.combine(ot_date,to_time)
                            else:
                                from_datetime = datetime.combine(ot_date,from_time)
                                to_datetime = datetime.combine(ot_date,to_time)
                        else:
                            from_datetime = datetime.combine(ot_date,from_time)
                            to_datetime = datetime.combine(ot_date,to_time)
                        if from_datetime > to_datetime:
                            frappe.throw(_('From Time should be lesser that To Time in %s'%(ot.name))) 
                        else:
                            if shift == 'PP2':
                                t_diff = datetime.strptime(str('03:30:00'), '%H:%M:%S').time()
                            else:    
                                t_diff = to_datetime - from_datetime
                            try:
                                time_diff = datetime.strptime(str(t_diff), '%H:%M:%S')
                            except:
                                time_diff = datetime.strptime(str('23:59:00'), '%H:%M:%S')
                            if time_diff.hour > 24:
                                frappe.throw('OT cannot applied for more than 24 hours')
                            
                            ot_hours = time(0,0,0)
                            if time_diff.hour >= 1:
                                if time_diff.minute <= 29:
                                    ot_hours = time(time_diff.hour,0,0)
                                else:
                                    ot_hours = time(time_diff.hour,30,0)
                            if time_diff.hour > 4:
                                if shift != '3':
                                    if time_diff.minute <= 29:
                                        ot_hours = time(time_diff.hour-1,30,0)
                                    else:
                                        ot_hours = time(time_diff.hour,0,0)
                                else:
                                    if time_diff.minute <= 29:
                                        ot_hours = time(time_diff.hour,0,0)
                                    else:
                                        ot_hours = time(time_diff.hour,30,0)
                            if time_diff.hour > 13:
                                ot_hours = time(time_diff.hour-1,0,0)
                            if time_diff.hour >= 23:
                                ot_hours = time(23,0,0)
                                # if shift != '3':
                                #     if time_diff.minute <= 29:
                                #         ot_hours = time(time_diff.hour-1,30,0)
                                #     else:
                                #         ot_hours = time(time_diff.hour,0,0)
                                # else:
                                #     if time_diff.minute <= 29:
                                #         ot_hours = time(time_diff.hour,0,0)
                                #     else:
                                #         ot_hours = time(time_diff.hour,30,0)
                        frappe.db.set_value('Overtime Request',ot.name,'total_hours',t_diff)
                        frappe.db.set_value('Overtime Request',ot.name,'ot_hours',ot_hours)
                        frappe.db.set_value('Overtime Request',ot.name,'workflow_state','Pending for HOD')

                        if ot.employee_type != 'CL':
                            basic = ((frappe.db.get_value('Employee',ot.employee,'basic')/26)/8)*2
                            frappe.db.set_value('Overtime Request',ot.name,'ot_basic',basic)
                            ftr = [3600,60,1]
                            hr = sum([a*b for a,b in zip(ftr, map(int,str(ot_hours).split(':')))])
                            ot_hr = round(hr/3600,1)
                            frappe.db.set_value('Overtime Request',ot.name,'ot_amount',round(ot_hr*basic))
                        else:
                            basic = 0
                            designation = frappe.db.get_value('Employee',ot.employee,'designation')
                            if designation == 'Skilled':
                                basic = frappe.db.get_single_value('HR Time Settings','skilled_amount_per_hour')
                            elif designation == 'Un Skilled':
                                basic = frappe.db.get_single_value('HR Time Settings','unskilled_amount_per_hour')
                            frappe.db.set_value('Overtime Request',ot.name,'ot_basic',basic)
                            ftr = [3600,60,1]
                            hr = sum([a*b for a,b in zip(ftr, map(int,str(ot_hours).split(':')))])
                            ot_hr = round(hr/3600,1)
                            frappe.db.set_value('Overtime Request',ot.name,'ot_amount',round(ot_hr*basic))
                
    ots = frappe.get_all('Overtime Request',{'ot_date':from_date},['name','employee','ot_hours','employee_type'])
    for ot in ots:
        if ot.employee_type != 'CL':
            if ot.ot_hours:
                basic = ((frappe.db.get_value('Employee',ot.employee,'basic')/26)/8)*2
                frappe.db.set_value('Overtime Request',ot.name,'ot_basic',basic)
                ftr = [3600,60,1]
                hr = sum([a*b for a,b in zip(ftr, map(int,str(ot.ot_hours).split(':')))])
                ot_hr = round(hr/3600,1)
                frappe.db.set_value('Overtime Request',ot.name,'ot_amount',round(ot_hr*basic))
        else:
            basic = 0
            designation = frappe.db.get_value('Employee',ot.employee,'designation')
            if designation == 'Skilled':
                basic = frappe.db.get_single_value('HR Time Settings','skilled_amount_per_hour')
            elif designation == 'Un Skilled':
                basic = frappe.db.get_single_value('HR Time Settings','unskilled_amount_per_hour')
            frappe.db.set_value('Overtime Request',ot.name,'ot_basic',basic)
            if ot.ot_hours:
                ftr = [3600,60,1]
                hr = sum([a*b for a,b in zip(ftr, map(int,str(ot.ot_hours).split(':')))])
                ot_hr = round(hr/3600,1)
                frappe.db.set_value('Overtime Request',ot.name,'ot_amount',round(ot_hr*basic)) 
                
                
@frappe.whitelist()
def submit_attendance(employee_type,from_date):
    enqueue(submit_att, queue='default', timeout=6000, event='submit_att',
                    from_date=from_date)

@frappe.whitelist()
def submit_att(employee_type,from_date):
    atts = frappe.get_all("Attendance",{'docstatus':'0','employee_type':employee_type,'attendance_date':('between',(from_date,'2021-10-25'))})
    for att in atts:
        att = frappe.get_doc("Attendance",att.name)
        att.submit()
        frappe.db.commit()


# return [str(t_diff),str(ot_hours)]

        # if qr.qr_scan_time:
        #     max_out_time = qr.qr_scan_time + timedelta(hours=8)
        #     bio_checkins = frappe.db.sql("select * from `tabEmployee Checkin` where employee = '%s' and time between '%s' and '%s' and log_type = 'OUT' order by time "%(qr.employee,qr.qr_scan_time,max_out_time),as_dict=True)
        #     if bio_checkins:
        #         t_diff = bio_checkins[0].time - qr.qr_scan_time
        #         try:
        #             time_diff = datetime.strptime(str(t_diff), '%H:%M:%S.%f')
        #         except:
        #             time_diff = datetime.strptime(str(t_diff), '%H:%M:%S')
        #         if time_diff.hour >= 1:
        #             if time_diff.minute <= 29:
        #                 ot_hours = time(time_diff.hour,0,0)
        #             else:
        #                 ot_hours = time(time_diff.hour,30,0)
        #         if time_diff.hour >= 4:
        #             if time_diff.minute <= 29:
        #                 ot_hours = time(time_diff.hour-1,30,0)
        #             else:
        #                 ot_hours = time(time_diff.hour,0,0)
        #         if ot_hours:
        #             req = frappe.new_doc("Overtime Request")
        #             req.employee = qr.employee
        #             req.from_date = from_date
        #             req.from_time = qr.qr_scan_time
        #             req.to_time = bio_checkins[0].time
        #             req.ot_hours = ot_hours
        #             req.save(ignore_permissions=True)
        #             frappe.db.set_value("QR Checkin",qr.name,'overtime_request',req.name)



# def add_checkin():
#     doc = frappe.new_doc("QR Checkin")
#     doc.employee = '1234'
#     doc.qr_shift = 'PP2'
#     doc.qr_scan_time = '2021-07-17 20:04:23'
#     doc.shift_date = '2021-07-16'
#     doc.save(ignore_permissions=True)


def method():
    import pandas as pd
    ots = frappe.get_all('Overtime Request',{'ot_date':('>=','2021-06-25')},['name','employee','ot_hours','employee_type'])
    for ot in ots:
        # print(ot)
        if ot.employee_type != 'CL':
            if ot.ot_hours:
                basic = ((frappe.db.get_value('Employee',ot.employee,'basic')/26)/8)*2
                frappe.db.set_value('Overtime Request',ot.name,'ot_basic',basic)
                ftr = [3600,60,1]
                hr = sum([a*b for a,b in zip(ftr, map(int,str(ot.ot_hours).split(':')))])
                ot_hr = round(hr/3600,1)
                frappe.db.set_value('Overtime Request',ot.name,'ot_amount',round(ot_hr*basic))
        else:
            basic = 0
            designation = frappe.db.get_value('Employee',ot.employee,'designation')
            if designation == 'Skilled':
                basic = frappe.db.get_single_value('HR Time Settings','skilled_amount_per_hour')
            elif designation == 'Un Skilled':
                basic = frappe.db.get_single_value('HR Time Settings','unskilled_amount_per_hour')
            frappe.db.set_value('Overtime Request',ot.name,'ot_basic',basic)
            if ot.ot_hours:
                ftr = [3600,60,1]
                hr = sum([a*b for a,b in zip(ftr, map(int,str(ot.ot_hours).split(':')))])
                ot_hr = round(hr/3600,1)
                frappe.db.set_value('Overtime Request',ot.name,'ot_amount',round(ot_hr*basic))