from tabnanny import check
from time import strptime
import frappe
import json
import datetime
from frappe.utils.csvutils import read_csv_content
from six.moves import range
from six import string_types
from frappe.utils import  formatdate
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
		mark_shift_status(from_date)
		mark_overtime(from_date)
		from_date = add_days(from_date,1)

@frappe.whitelist()
def mark_shift_status():
	d = datetime.strptime(today(),"%Y-%m-%d")
	if int(d.strftime("%d")) <= 30:
		from_date = add_days(get_first_day(today()),-6)
	else:
		from_date = add_days(get_first_day(today()),25)
	for s in range(31):
		mark_overtime(from_date)
		from_date = add_days(from_date,1)

def mark_att_manual():
	from_date = "2024-09-11"
	to_date = "2024-09-11"
	dates = get_dates(from_date,to_date)
	for date in dates:
		mark_att(date)

def mark_att_daily_hooks():
	from_date = add_days(today(),-1)
	mark_att(from_date)
	to_date = today()
	mark_att(from_date)
	# from_date = "2024-08-04"
	# to_date = "2024-08-04"
	dates = get_dates(from_date,to_date)
	for date in dates:
		mark_att(date)
	
def get_dates(from_date,to_date):
	no_of_days = date_diff(add_days(to_date, 1), from_date)
	dates = [add_days(from_date, i) for i in range(0, no_of_days)]
	return dates

@frappe.whitelist()
def enqueue_mark_att():
	enqueue(mark_att, queue='default', timeout=6000, event='mark_att',)

@frappe.whitelist()
def mark_att(from_date):
	mark_on_duty(from_date)
	checkins = frappe.db.sql(
		"""select * from `tabEmployee Checkin` where skip_auto_attendance = 0 and date(time) = '%s' order by time ASC"""%(from_date),as_dict=1)
	if checkins:
		for c in checkins:
			print(c.name)
			if frappe.db.exists("Employee",{'employee_number':c.employee,'status':"Active"}):
				att = mark_attendance_from_checkin(c.name,c.employee,c.log_type,c.time)
				if att:
					frappe.db.set_value("Employee Checkin",c.name, "attendance", att.name)
					frappe.db.set_value("Employee Checkin",c.name, "skip_auto_attendance", "1")
			if frappe.db.exists("Employee",{'employee_number':c.employee,'status':"Left",'relieving_date':['>=',from_date]}):
				att = mark_attendance_from_checkin(c.name,c.employee,c.log_type,c.time)
				if att:
					frappe.db.set_value("Employee Checkin",c.name, "attendance", att.name)
					frappe.db.set_value("Employee Checkin",c.name, "skip_auto_attendance", "1")
		mark_qr_checkin(from_date)
		mark_permission(from_date)  
		mark_absent(from_date)
		mark_overtime(from_date)
		mark_shift_status(from_date)
		frappe.msgprint("Attendance Marked Successfully")
		print("OK")
		return "ok"
	else:
		mark_qr_checkin(from_date)
		mark_permission(from_date)
		mark_absent(from_date)
		mark_overtime(from_date)
		mark_shift_status(from_date)
		frappe.msgprint("Attendance Marked Successfully")
		print("OK")
		return "ok"

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
		elif max_in_time2 >= att_time >= min_in_time2:
			shift = '2'
			min_in_time = datetime.strptime('13:00', '%H:%M').time()
			max_in_time = datetime.strptime('18:30', '%H:%M').time()
			if datetime.strptime('16:31', '%H:%M').time() < att_time:
				late = 1
		elif max_in_time3 >= att_time >= min_in_time3:
			shift = '3'
			att_date = add_days(att_date,-1)
			min_in_time = datetime.strptime('00:01', '%H:%M').time()
			max_in_time = datetime.strptime('03:00', '%H:%M').time()
			if datetime.strptime('01:01', '%H:%M').time() < att_time:
				late = 1
		elif max_in_timepp2 >= att_time >= min_in_timepp2:
			shift = 'PP2'
			min_in_time = datetime.strptime('18:30', '%H:%M').time()
			max_in_time = datetime.strptime('23:00', '%H:%M').time()
			if datetime.strptime('20:01', '%H:%M').time() < att_time:
				late = 1
		if late == 1:
			hh = check_holiday(att_date)
			if hh:
				late = 0
				status = "Present"
			else:
				status = 'Half Day'
		if min_in_time and max_in_time:
			att = frappe.db.exists("Attendance",{'employee':employee,'attendance_date':att_date,'docstatus': ['!=',2]})
			if not att:
				if shift != '3':
					checkins = frappe.db.sql("select name,time from `tabEmployee Checkin` where employee = '%s' and log_type = 'IN' and date(time) = '%s' and time(time) between '%s' and '%s' order by time ASC "%(employee,att_date,min_in_time,max_in_time),as_dict=True)
				else:
					yesterday = add_days(att_date,1)
					checkins = frappe.db.sql("select name,time from `tabEmployee Checkin` where employee = '%s' and log_type = 'IN' and date(time) = '%s' and time(time) between '%s' and '%s' order by time ASC"%(employee,yesterday,min_in_time,max_in_time),as_dict=True)
				if checkins:
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
					for c in checkins:
						frappe.db.set_value('Employee Checkin',c.name,'skip_auto_attendance','1')
						frappe.db.set_value("Employee Checkin",c.name, "attendance", att.name)
					return att
			else:
				if shift != '3':
					checkins = frappe.db.sql("select name,time from `tabEmployee Checkin` where employee = '%s' and log_type = 'IN' and date(time) = '%s' and time(time) between '%s' and '%s' order by time ASC"%(employee,att_date,min_in_time,max_in_time),as_dict=True)
				else:
					yesterday = add_days(att_date,1)
					checkins = frappe.db.sql("select name,time from `tabEmployee Checkin` where employee = '%s' and log_type = 'IN' and date(time) = '%s' and time(time) between '%s' and '%s' order by time ASC"%(employee,yesterday,min_in_time,max_in_time),as_dict=True)
				if checkins:
					att = frappe.get_doc("Attendance",att)
					if att.docstatus == 0:
						att.employee = employee
						att.attendance_date = att_date
						att.shift = shift
						att.status = status
						att.late_entry = late
						att.in_time = checkins[0].time
						att.save(ignore_permissions=True)
						frappe.db.commit()
						for c in checkins:
							frappe.db.set_value('Employee Checkin',c.name,'skip_auto_attendance','1')
							frappe.db.set_value("Employee Checkin",c.name, "attendance", att.name)
					return att	

	if log_type == 'OUT':
		max_out = datetime.strptime('11:30', '%H:%M').time()
		if att_time < max_out:
			yesterday = add_days(att_date,-1)
			checkins = frappe.db.sql("select name,time from `tabEmployee Checkin` where employee = '%s' and log_type = 'OUT' and date(time) = '%s' and time(time) < '%s' order by time ASC"%(employee,att_date,max_out),as_dict=True)
			att = frappe.db.exists("Attendance",{'employee':employee,'attendance_date':yesterday})
			if att:
				att = frappe.get_doc("Attendance",att)
				if att.docstatus == 0:
					if not att.out_time:
						if len(checkins) > 0:
							att.out_time = checkins[-1].time
						else:
							att.out_time = checkins[0].time
						att.save(ignore_permissions=True)
						frappe.db.commit()
						for c in checkins:
							frappe.db.set_value('Employee Checkin',c.name,'skip_auto_attendance','1')
							frappe.db.set_value("Employee Checkin",c.name, "attendance", att.name)
						return att
					else:
						return att
			else:
				att = frappe.new_doc("Attendance")
				att.employee = employee
				att.attendance_date = yesterday
				att.status = 'Absent'
				if len(checkins) > 0:
					att.out_time = checkins[-1].time
				else:
					att.out_time = checkins[0].time
				att.save(ignore_permissions=True)
				frappe.db.commit()
				for c in checkins:
					frappe.db.set_value('Employee Checkin',c.name,'skip_auto_attendance','1')
					frappe.db.set_value("Employee Checkin",c.name, "attendance", att.name)
				return att
		else:
			checkins = frappe.db.sql("select name,time,docstatus from `tabEmployee Checkin` where employee ='%s' and log_type = 'OUT' and date(time) = '%s' order by time ASC"%(employee,att_date),as_dict=True)
			att = frappe.db.exists("Attendance",{'employee':employee,'attendance_date':att_date})
			if att:
				att = frappe.get_doc("Attendance",att)
				if att.docstatus == 0:
					if not att.out_time:
						if len(checkins) > 0:
							att.out_time = checkins[-1].time
						else:
							att.out_time = checkins[0].time
						att.save(ignore_permissions=True)
						frappe.db.commit()
						for c in checkins:
							frappe.db.set_value('Employee Checkin',c.name,'skip_auto_attendance','1')
							frappe.db.set_value("Employee Checkin",c.name, "attendance", att.name)
						return att
					else:
						return att
			else:
				att = frappe.new_doc("Attendance")
				att.employee = employee
				att.attendance_date = att_date
				att.status = 'Absent'
				if len(checkins) > 0:
					att.out_time = checkins[-1].time
				else:
					att.out_time = checkins[0].time
				att.save(ignore_permissions=True)
				frappe.db.commit()
				for c in checkins:
					frappe.db.set_value('Employee Checkin',c.name,'skip_auto_attendance','1')
					frappe.db.set_value("Employee Checkin",c.name, "attendance", att.name)
				return att


def mark_qr_checkin(from_date):
	hh = check_holiday(from_date)
	if hh:
		qr_checkins = frappe.db.sql("select name, employee,qr_shift,qr_scan_time,shift_date from `tabQR Checkin` where shift_date = '%s' and ot = 1 order by qr_scan_time ASC"%(from_date),as_dict=True)
		for qr in qr_checkins:
			if frappe.db.exists('Attendance',{'attendance_date':qr.shift_date,'employee':qr.employee,'docstatus':'0'}):
				att = frappe.get_doc('Attendance',{'attendance_date':qr.shift_date,'employee':qr.employee,'docstatus':('!=',2)})
				frappe.errprint(att)
				att.qr_shift = qr.qr_shift
				att.qr_scan_time = qr.qr_scan_time
				att.save(ignore_permissions=True)
				frappe.db.commit()
				frappe.db.set_value("QR Checkin",qr.name, "attendance", att.name)
	else:
		qr_checkins = frappe.db.sql("select name, employee,qr_shift,qr_scan_time,shift_date from `tabQR Checkin` where shift_date = '%s' and ot = 0 order by qr_scan_time ASC"%(from_date),as_dict=True)
		for qr in qr_checkins:
			if frappe.db.exists('Attendance',{'attendance_date':qr.shift_date,'employee':qr.employee,'docstatus':'0'}):
				att = frappe.get_doc('Attendance',{'attendance_date':qr.shift_date,'employee':qr.employee,'docstatus':('!=',2)})
				frappe.errprint(att)
				att.qr_shift = qr.qr_shift
				att.qr_scan_time = qr.qr_scan_time
				att.save(ignore_permissions=True)
				frappe.db.commit()
				frappe.db.set_value("QR Checkin",qr.name, "attendance", att.name)


def check_holiday(date):
	holiday = frappe.db.sql("""select `tabHoliday`.holiday_date,`tabHoliday`.weekly_off from `tabHoliday List` 
	left join `tabHoliday` on `tabHoliday`.parent = `tabHoliday List`.name where `tabHoliday List`.name = 'Holiday List - 2021' and holiday_date = '%s' """%(date),as_dict=True)
	if holiday:
		if holiday[0].weekly_off == 1:
			return "WW"
		else:
			return "HH"

@frappe.whitelist()
def shift_status_single_day(doc,method):
	mark_shift_status(doc.from_date)

@frappe.whitelist()
def mark_shift_status(from_date):
	to_date = from_date
	from_date = add_days(from_date,-1)
	atts = frappe.get_all('Attendance',{'attendance_date':('between',(from_date,to_date))},['*'])
	for att in atts:
		hh = check_holiday(att.attendance_date)
		if hh:
			frappe.errprint("HI")
			if att.in_time and att.out_time and att.shift:
				if hh == 'WW':
					shift_status = att.shift + "W"
				else:
					shift_status = att.shift + "H"
				frappe.db.set_value('Attendance',att.name,'shift_status',shift_status)
				frappe.db.set_value('Attendance',att.name,'status',"Present")
			elif att.on_duty_application:
				if hh == 'WW':
					shift_status = "ODW"
				else:
					shift_status = "ODH"
				frappe.db.set_value('Attendance',att.name,'shift_status',shift_status)
				frappe.db.set_value('Attendance',att.name,'status',"Present")
			else:
				if hh == 'WW':
					shift_status = "WW"
				else:
					shift_status = "HH"
				frappe.db.set_value('Attendance',att.name,'shift_status',shift_status)
				frappe.db.set_value('Attendance',att.name,'status',"Absent")
		else:
			frappe.errprint("HII")
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
			else:
				if att.shift:
					if att.in_time and att.out_time:
						shift_status = str(att.shift) + late
					if not att.out_time or not att.in_time:
						shift_status = str(att.shift) + 'M'
				else:
					shift_status = "AA"
			if att.status == 'Half Day':
				if att.leave_type:
					shift_status = str(0.5) + att.leave_type
				else:
					shift_status = '0.5Leave Without Pay'
			elif att.status == 'On Leave':
				shift_status = att.leave_type
			elif att.on_duty_application:
				shift_status = "OD"
			if not att.manually_corrected:
				frappe.db.set_value('Attendance',att.name,'shift_status',shift_status)
				absent = ('12','13','21','23','31','32','1L2','1L3','2L1','2L3','3L1','3L2','PP1L2','PP2L3','1M','2M','3M','MM','M1','M2','M3','MPP2','AA','LA','LOP','1LM','2LM','3LM','PP2LM','PP2M')
				if att.status != 'On Leave':
					if att.status not in ('Half Day','On Leave'):
						frappe.db.set_value('Attendance',att.name,'status','Present')
					if shift_status in absent:
						frappe.db.set_value('Attendance',att.name,'status','Absent')
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
				frappe.db.commit()

@frappe.whitelist()
def mark_overtime(from_date):
	ots = frappe.db.sql("select * from `tabOvertime Request` where ot_date = '%s' and docstatus != 1 "%(from_date),as_dict=True)
	for ot in ots:
		# frappe.errprint(ot.name)
		od = frappe.db.sql("""select `tabOn Duty Application`.name from `tabOn Duty Application` 
		left join `tabMulti Employee` on `tabOn Duty Application`.name = `tabMulti Employee`.parent where 
		`tabMulti Employee`.employee = '%s' and '%s' between `tabOn Duty Application`.from_date and `tabOn Duty Application`.to_date and `tabOn Duty Application`.workflow_state = 'Approved' """%(ot.employee,from_date),as_dict=True)
		if od:
			if ot.ot_hours:
				ftr = [3600,60,1]
				hr = sum([a * b for a, b in zip(ftr, map(float, str(ot.ot_hours).split(':')))])
				# hr = sum([a*b for a,b in zip(ftr, map(int,str(ot.ot_hours).split(':')))])
				ot_hr = round(hr/3600,1)
				if ot_hr > 0:
					frappe.db.set_value('Overtime Request',ot.name,'workflow_state','Pending for HOD')
			frappe.db.set_value('Overtime Request',ot.name,'on_duty',od[0].name)
			if ot.ot_hours:
				if ot.employee_type != 'CL':
					basic = ((frappe.db.get_value('Employee',ot.employee,'basic')/26)/8)*2
					frappe.db.set_value('Overtime Request',ot.name,'ot_basic',basic)
					ftr = [3600,60,1]
					hr = sum([a * b for a, b in zip(ftr, map(float, str(ot.ot_hours).split(':')))])
					# hr = sum([a*b for a,b in zip(ftr, map(int,str(ot.ot_hours).split(':')))])
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
					hr = sum([a * b for a, b in zip(ftr, map(float, str(ot.ot_hours).split(':')))])
				
					# hr = sum([a*b for a,b in zip(ftr, map(int,str(ot.ot_hours).split(':')))])
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
				basic = ((frappe.db.get_value('Employee',ot.employee,'basic')/26)/8)*2
				frappe.db.set_value('Overtime Request',ot.name,'ot_basic',basic)
				ftr = [3600,60,1]
				hr = sum([a * b for a, b in zip(ftr, map(float, str(ot.ot_hours).split(':')))])
				# hr = sum([a*b for a,b in zip(ftr, map(int,str(ot.ot_hours).split(':')))])
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
				hr = sum([a * b for a, b in zip(ftr, map(float, str(ot.ot_hours).split(':')))])

				# hr = sum([a*b for a,b in zip(ftr, map(int,str(ot.ot_hours).split(':')))])
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
						if time_diff.hour >= 23:
							ot_hours = time(23,0,0)
								
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


def method():
	ots = frappe.get_all('Overtime Request',{'ot_date':('>=','2021-06-25')},['name','employee','ot_hours','employee_type'])
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
def get_urc_to_ec(from_date):
	frappe.errprint(from_date)
	frappe.errprint("HI")
	urc = frappe.db.sql("""select biometric_pin,biometric_time,log_type,locationdevice_id,name from `tabUnregistered Employee Checkin` where date(biometric_time) = '%s' """%(from_date),as_dict=True)
	for uc in urc:
		pin = uc.biometric_pin
		time = uc.biometric_time
		dev = uc.locationdevice_id
		typ = uc.log_type
		nam = uc.name
		if time != "":
			if frappe.db.exists('Employee',{'biometric_pin':pin}):
				if not frappe.db.exists('Employee Checkin',{'biometric_pin':pin,"time":time}):
					frappe.errprint(pin)
					ec = frappe.new_doc('Employee Checkin')
					ec.biometric_pin = pin
					ec.employee = frappe.db.get_value('Employee',{'biometric_pin':pin},['employee_number'])
					ec.time = time
					ec.device_id = dev
					ec.log_type = typ
					ec.save(ignore_permissions=True)
					frappe.db.commit()
					frappe.errprint("Created")
					attendance = frappe.db.sql(""" delete from `tabUnregistered Employee Checkin` where name = '%s' """%(nam))      
	return "OK"

@frappe.whitelist()
def delete_urc_automatically():
	from_date = add_days(today(),-100)  
	to_date = add_days(today(),-34)  
	urc = frappe.db.sql("""delete from `tabUnregistered Employee Checkin` where date(biometric_time) between '%s' and '%s'  """%(from_date,to_date),as_dict = True)
	
from erpnext.buying.doctype.supplier_scorecard.supplier_scorecard import daterange
@frappe.whitelist()
def update_leave_att():
	from_date = add_days(today(),-10)  
	to_date = add_days(today(),-0)  
	date_list = get_dates(from_date,to_date)
	for d in date_list:
		leave_list = frappe.db.sql("""select * from `tabLeave Application` where docstatus != '2' and from_date between '%s' and '%s' and to_date between '%s' and '%s' """%(d,d,d,d), as_dict=True)
		for l in leave_list:
			if l.status == "Approved":
				for dt in daterange(getdate(l.from_date), getdate(l.to_date)):
					date = dt.strftime("%Y-%m-%d")
					status = "Half Day" if l.half_day_date and getdate(date) == getdate(l.half_day_date) else "On Leave"
					attendance_name = frappe.db.exists('Attendance', dict(employee = l.employee,
						attendance_date = date, docstatus = ('!=', 2)))
					if attendance_name:
						doc = frappe.get_doc('Attendance', attendance_name)
						if status:
							doc.db_set('status', status)
							doc.db_set('leave_type', l.leave_type)
							doc.db_set('leave_application', l.name)
							if status == "On Leave":
								doc.db_set('shift_status', l.leave_type)
							else:
								doc.db_set('shift_status', "0.5" + l.leave_type)
							doc.db_set('docstatus', 1)
					else:
						doc = frappe.new_doc("Attendance")
						doc.employee = l.employee
						doc.employee_name = l.employee_name
						doc.attendance_date = date
						doc.company = l.company
						doc.leave_type = l.leave_type
						doc.leave_application = l.name
						doc.status = status
						if status == "On Leave":
							doc.db_set('shift_status', l.leave_type)
						else:
							doc.db_set('shift_status', "0.5" + l.leave_type)
						doc.flags.ignore_validate = True
						doc.save(ignore_permissions=True)
						doc.db_set('docstatus', 1)

		miss_punch = frappe.db.sql("""select * from `tab Miss Punch Application` where docstatus != '2' and attendance_date between '%s' and '%s' """%(d,d), as_dict=True)
		for m in miss_punch:
			if m.workflow_state == "Approved":
				frappe.db.set_value("Attendance",m.attendance,"in_time",m.in_time)
				frappe.db.set_value("Attendance",m.attendance,"out_time",m.out_time)
				frappe.db.set_value("Attendance",m.attendance,"qr_shift",m.qr_shift)
				frappe.db.set_value("Attendance",m.attendance,"status","Present")
				if not frappe.db.get_value("Attendance",m.attendance,"shift"):
					if m.qr_shift:
						frappe.db.set_value("Attendance",m.attendance,"shift",m.qr_shift)
					else:
						frappe.db.set_value("Attendance",m.attendance,"shift",'1')

@frappe.whitelist()
def cron_job2():
	job = frappe.db.exists('Scheduled Job Type', 'delete_urc_automatically')
	if not job:
		sjt = frappe.new_doc("Scheduled Job Type")  
		sjt.update({
			"method" : 'thaisummit.mark_attendance.delete_urc_automatically',
			"frequency" : 'Cron',
			"cron_format" : '30 00 * * *'
		})
		sjt.save(ignore_permissions=True)

@frappe.whitelist()
def cron_job3():
	job = frappe.db.exists('Scheduled Job Type', 'mark_att_daily_hooks')
	if not job:
		sjt = frappe.new_doc("Scheduled Job Type")  
		sjt.update({
			"method" : 'thaisummit.mark_attendance.mark_att_daily_hooks',
			"frequency" : 'Cron',
			"cron_format" : '0 */1 * * *'
		})
		sjt.save(ignore_permissions=True)

@frappe.whitelist()
def cron_job4():
	job = frappe.db.exists('Scheduled Job Type', 'update_leave_att')
	if not job:
		sjt = frappe.new_doc("Scheduled Job Type")  
		sjt.update({
			"method" : 'thaisummit.mark_attendance.update_leave_att',
			"frequency" : 'Cron',
			"cron_format" : '30 09 * * *'
		})
		sjt.save(ignore_permissions=True)


@frappe.whitelist()
def att_status_auto_email(): 
	ec = 0
	from_date = add_days(today(),-1) 
	ec_count = frappe.db.sql("""select count(*) as count from `tabEmployee Checkin` where date(time) = '%s' """%(from_date),as_dict=True)[0]
	uec_count = frappe.db.sql("""select count(*) as count from `tabUnregistered Employee Checkin` where date(biometric_time) = '%s' """%(from_date),as_dict=True)[0]
	att_count = frappe.db.sql("""select count(*) as count from `tabAttendance` where attendance_date = '%s' """%(from_date),as_dict=True)[0]
	pre_count = frappe.db.sql("""select count(*) as count from `tabAttendance` where attendance_date = '%s' and status = "Present" and on_duty_application = '' """%(from_date),as_dict=True)[0]
	pre_od_count = frappe.db.sql("""select count(*) as count from `tabAttendance` where attendance_date = '%s' and status = "Present" and on_duty_application != ''"""%(from_date),as_dict=True)[0]
	abs_count = frappe.db.sql("""select count(*) as count from `tabAttendance` where attendance_date = '%s' and status = "Absent" """%(from_date),as_dict=True)[0]
	leav_count = frappe.db.sql("""select count(*) as count from `tabAttendance` where attendance_date = '%s' and status = "On Leave" """%(from_date),as_dict=True)[0]
	skec_count = frappe.db.sql("""select * from `tabEmployee Checkin` where date(time) = '%s' and skip_auto_attendance = 0 """%(from_date),as_dict=True)
	d = 0
	for c in skec_count:
		if frappe.db.exists("Employee",{'employee_number':c.employee,'status':"Active"}):
			d += 1
	ec == ((d/ec_count['count'])*100)
	if ec > 95 :
		status = "Success"
	else:
		status = "Failure"
	data = ''
	data += """<tr><td>Description</td><td>Count</td></tr>"""
	data += """<tr><td>Total Attendance Count</td><td>'%s'</td></tr>"""%(att_count['count'])
	data += """<tr><td>Total Att-Present Count</td><td>'%s'</td></tr>"""%(pre_count['count'])
	data += """<tr><td>Total Att-OnDuty Count</td><td>'%s'</td></tr>"""%(pre_od_count['count'])
	data += """<tr><td>Total Att-Absent Count</td><td>'%s'</td></tr>"""%(abs_count['count'])
	data += """<tr><td>Total Att-On Leave Count</td><td>'%s'</td></tr>"""%(leav_count['count'])
	data += """<tr><td>Overall Status</td><td>'%s'</td></tr>"""%(status)
	data_1 = "<table border='1' " + data + "</table>"
	frappe.sendmail(
		recipients=['veeramayandi.p@groupteampro.com'],
		subject= '%s' " Attendance Status"%(formatdate(from_date)),
		message=data_1)


@frappe.whitelist()
def update_att_shift_status(doc,method):
	if doc.leave_application:
		leave = doc.leave_type
		ss = ''
		if doc.status == "On Leave":
			if leave != '':
				ss = leave
			else:
				ss = ''
		elif doc.status == "Half Day":
			if leave:
				ss = str(0.5) + leave
			else:
				ss = '0.5 Leave Without Pay'
		frappe.db.set_value('Attendance',doc.name,'shift_status',str(ss))
		
			