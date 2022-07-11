# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import cstr, cint, getdate, get_last_day, get_first_day, add_days
from frappe import msgprint, _
from calendar import monthrange
from datetime import date, timedelta, datetime

bc_status_map = {
	"Absent": "AA",
	"AA":"AA",
	"Half Day": "HD",
	"Holiday": "HH",
	"Weekly Off": "WW",
	"WW":"WW",
	"1H": "1H",
	"2H": "2H",
	"3H": "3H",
	"1W": "1W",
	"2W": "2W",
	"3W": "3W",
	"PP1W": "PP1W",
	"PP2W": "PP2W",
	"1LH": "1LH",
	"2LH": "2LH",
	"3LH": "3LH",
	"1LW": "1LW",
	"2LW": "2LW",
	"3LW": "3LW",
	"PP1LW": "PP1LW",
	"PP2LW": "PP2LW",
	"MW": "MW",
	"On Leave": "L",
	"Present": "P",
	"Work From Home": "WFH",
	"MM": "AA",
	"11": "11",
	"22": "22",
	"33": "33",
	"PP1PP1": "P1P1",
	"PP2PP2": "P2P2",
	"1L1": "1L1",
	"2L2": "2L2",
	"3L3": "3L3",
	"2L3": "2L3",
	"1L2": "1L2",
	"3L1": "3L1",
	"1LM": "1LM",
	"2LM": "2LM",
	"3LM": "3LM",
	"PP1LPP1": "P1LP1",
	"PP2LPP2": "P2LP2",
	"1M": "1M",
	"2M": "2M",
	"3M": "3M",
	"M1": "M1",
	"M2": "M2",
	"M3": "M3",
	"PP1M": "P1M",
	"PP2M": "P2M",
	"MPP1": "MP1",
	"MPP2": "MP2",
	"11": "11",
	"12": "12",
	"13": "13",
	"1PP1": "1P1",
	"1PP2": "1P2",
	"21": "21",
	"22": "22",
	"23": "23",
	"2PP1": "2P1",
	"2PP2": "2P2",
	"31": "31",
	"32": "32",
	"33": "33",
	"3PP1": "3P1",
	"3PP2": "3P2",
	"PP11": "P11",
	"PP12": "P12",
	"PP13": "P13",
	"PP1PP1": "P1P1",
	"PP1PP2": "P1P2",
	"PP21": "P2P1",
	"PP22": "P2P2",
	"PP23": "P2P3",
	"PP2PP1": "P2P1",
	"PP2PP2": "P2P2",
	"Earned Leave": "EL",
	"Casual Leave": "CL",
	"Sick Leave": "SL",
	"Special Leave": "SPL",
	"OD": "OD",
	"Compensatory Off": "CO",
	"Leave Without Pay": "LL",
	"0.5Earned Leave": "0.5EL",
	"0.5Casual Leave": "0.5CL",
	"0.5Sick Leave": "0.5SL",
	"0.5Special Leave": "0.5SPL",
	"0.5Compensatory Off": "0.5CO",
	"0.5Leave Without Pay": "0.5LL",
	"LEarned Leave/2": "0.5SL",
	"LCasual Leave/2": "0.5LCL",
	"LSick Leave/2": "0.5LSL",
	"LSpecial Leave/2": "0.5LSPL",
	"LCompensatory Off/2": "0.5LCO",
	"LLeave Without Pay/2": "0.5LLL",
	}

wc_status_map = {
	"Absent": "AA",
	"AA": "AA",
	"Half Day": "HD",
	"Holiday": "HH",
	"WW":"WW",
	"1H": "1H",
	"2H": "2H",
	"3H": "3H",
	"1W": "1W",
	"2W": "2W",
	"3W": "3W",
	"PP1W": "PP1W",
	"PP2W": "PP2W",
	"PP1H": "P1H",
	"PP2H": "P2H",
	"Weekly Off": "WW",
	"On Leave": "L",
	# "Present": "11",
	"Work From Home": "WFH",
	"OD": "OD",
	"Earned Leave": "EL",
	"Casual Leave": "CL",
	"Sick Leave": "SL",
	"Special Leave": "SPL",
	"Compensatory Off": "CO",
	"Leave Without Pay": "LL",
	"1": "11",
	"2": "22",
	"3": "33",
	" ": "MM",
	"PP1": "P1P1",
	"PP2": "P2P2",
	"1L": "1L1",
	"2L": "2L2",
	"3L": "3L3",
	"PP1L": "P1LP1",
	"PP2L": "P2LP2",
	"1LH": "1LH",
	"2LH": "2LH",
	"3LH": "3LH",
	"1LW": "1LW",
	"2LW": "2LW",
	"3LW": "3LW",
	"PP1LW": "PP1LW",
	"PP2LW": "PP2LW",
	"1M": "1M",
	"2M": "2M",
	"3M": "3M",
	"M1": "M1",
	"M2": "M2",
	"M3": "M3",
	"PP1M": "P1M",
	"PP2M": "P2M",
	"MPP1": "MP1",
	"MPP2": "MP2",
	"0.5Earned Leave": "0.5EL",
	"0.5Casual Leave": "0.5CL",
	"0.5Sick Leave": "0.5SL",
	"0.5Special Leave": "0.5SPL",
	"0.5Compensatory Off": "0.5CO",
	"0.5Leave Without Pay": "0.5LL",
	"LEarned Leave/2": "0.5SL",
	"LCasual Leave/2": "0.5LCL",
	"LSick Leave/2": "0.5LSL",
	"LSpecial Leave/2": "0.5LSPL",
	"LCompensatory Off/2": "0.5LCO",
	"LLeave Without Pay/2": "0.5LLL"
	}

day_abbr = [
	"Mon",
	"Tue",
	"Wed",
	"Thu",
	"Fri",
	"Sat",
	"Sun"
]

def execute(filters=None):
	if not filters: filters = {}

	if filters.hide_year_field == 1:
		filters.year = 2020

	conditions, filters = get_conditions(filters)
	columns, days = get_columns(filters)
	att_map = get_attendance_list(conditions, filters)
	if not att_map:
		return columns, [], None, None

	if filters.group_by:
		emp_map, group_by_parameters = get_employee_details(filters.employee_type,filters.department,filters.group_by, filters.company)
		holiday_list = []
		for parameter in group_by_parameters:
			h_list = [emp_map[parameter][d]["holiday_list"] for d in emp_map[parameter] if emp_map[parameter][d]["holiday_list"]]
			holiday_list += h_list
	else:
		emp_map = get_employee_details(filters.employee_type,filters.department,filters.group_by, filters.company)
		holiday_list = [emp_map[d]["holiday_list"] for d in emp_map if emp_map[d]["holiday_list"]]


	default_holiday_list = frappe.get_cached_value('Company',  filters.get("company"),  "default_holiday_list")
	holiday_list.append(default_holiday_list)
	holiday_list = list(set(holiday_list))
	holiday_map = get_holiday(holiday_list, filters.from_date,filters.to_date)
	data = []

	leave_list = None
	if filters.summarized_view:
		leave_types = frappe.db.sql("""select name from `tabLeave Type`""", as_list=True)
		leave_list = [d[0] + ":Float:120" for d in leave_types]
		columns.extend(leave_list)
		columns.extend([_("Total Late Entries") + ":Float:120", _("Total Early Exits") + ":Float:120"])

	if filters.group_by:
		emp_att_map = {}
		for parameter in group_by_parameters:
			emp_map_set = set([key for key in emp_map[parameter].keys()])
			att_map_set = set([key for key in att_map.keys()])
			if (att_map_set & emp_map_set):
				parameter_row = ["<b>"+ parameter + "</b>"] + ['' for day in range(filters["total_days_in_month"] + 2)]
				data.append(parameter_row)
				record, emp_att_data = add_data(emp_map[parameter], att_map, filters, holiday_map, conditions, default_holiday_list, leave_list=leave_list)
				emp_att_map.update(emp_att_data)
				data += record
	else:
		record, emp_att_map = add_data(emp_map, att_map, filters, holiday_map, conditions, default_holiday_list, leave_list=leave_list)
		data += record
	# chart_data = get_chart_data(emp_att_map, days)
	
	return columns, data, None, None

def add_data(employee_map, att_map, filters, holiday_map, conditions, default_holiday_list, leave_list=None):

	record = []
	emp_att_map = {}
	for emp in employee_map:
		emp_det = employee_map.get(emp)
		if not emp_det or emp not in att_map:
			continue

		row = []
		if filters.group_by:
			row += [" "]
		row += [emp, emp_det.employee_name]

		total_p = total_a = total_l = total_h = total_um= 0.0
		emp_status_map = []
		from_date = datetime.strptime(filters.from_date, "%Y-%m-%d")   # start date
		to_date = datetime.strptime(filters.to_date,  "%Y-%m-%d")       # end date

		delta = to_date - from_date       # as timedelta
		filterdate = from_date
		for day in range(filters['total_days_in_month']):
			status = None
			filtered_date = int(filterdate.strftime("%d"))
			status = att_map.get(emp).get(filtered_date)
			shift = ''
			if holiday_map:
				emp_holiday_list = emp_det.holiday_list if emp_det.holiday_list else default_holiday_list
				if emp_holiday_list in holiday_map:
					for idx, ele in enumerate(sorted(holiday_map[emp_holiday_list])):
						if filtered_date == holiday_map[emp_holiday_list][idx][0]:
							if frappe.db.exists('Attendance',{'attendance_date':filterdate,'employee':emp,'status':('!=','Absent')}):
								shift = frappe.get_value('Attendance',{'attendance_date':filterdate,'employee':emp },['employee_type','shift','qr_shift','late_entry']) or ''
								late = ''
								# if shift[3] == 1:
								# 	late = 'L'
								if holiday_map[emp_holiday_list][idx][1]:
									if shift[0] == 'WC':
										if shift[1]:
											status = shift[1] + late + "W"
										else:
											status = "WW"
									else:
										if shift[2]:
											status = shift[2] + late + "W"
										else:
											status = "WW"
								else:
									if shift[0] == 'WC':
										if shift[1]:
											status = shift[1] + late+ "H"
									else:
										if shift[2]:
											status = shift[2] + late + "H"
							else:
								if holiday_map[emp_holiday_list][idx][1]:
									status = "Weekly Off"
								else:
									status = "Holiday"
							total_h += 1
			if emp_det.employee_type == "WC":
				abbr = wc_status_map.get(status, "")
			else:
				abbr = bc_status_map.get(status, "")
			emp_status_map.append(abbr)
			filterdate += timedelta(days=1)
			
			if  filters.summarized_view:
				if status == "Present" or status == "Work From Home":
					total_p += 1
				elif status == "Absent":
					total_a += 1
				elif status == "On Leave":
					total_l += 1
				elif status == "Half Day":
					total_p += 0.5
					total_a += 0.5
					total_l += 0.5
				elif not status:
					total_um += 1

		if not filters.summarized_view:
			row += emp_status_map

		if filters.summarized_view:
			row += [total_p, total_l, total_a, total_h, total_um]

		if not filters.get("employee"):
			filters.update({"employee": emp})
			conditions += " and employee = %(employee)s"
		elif not filters.get("employee") == emp:
			filters.update({"employee": emp})

		if filters.summarized_view:
			leave_details = frappe.db.sql("""select leave_type, status, count(*) as count from `tabAttendance`\
				where leave_type is not NULL %s group by leave_type, status""" % conditions, filters, as_dict=1)

			time_default_counts = frappe.db.sql("""select (select count(*) from `tabAttendance` where \
				late_entry = 1 %s) as late_entry_count, (select count(*) from tabAttendance where \
				early_exit = 1 %s) as early_exit_count""" % (conditions, conditions), filters)

			leaves = {}
			for d in leave_details:
				if d.status == "Half Day":
					d.count = d.count * 0.5
				if d.leave_type in leaves:
					leaves[d.leave_type] += d.count
				else:
					leaves[d.leave_type] = d.count

			for d in leave_list:
				if d in leaves:
					row.append(leaves[d])
				else:
					row.append("0.0")

			row.extend([time_default_counts[0][0],time_default_counts[0][1]])
		total_worked_days = total_weekoffs = total_holidays = total_cl = total_el = total_sl = total_co = total_spl = total_la = total_lop = total_wrong_shifts = total_payable_days = 0
		
		actual_shifts = ['11','22','33','P2P2','P1P1','12','13','23','21','32','OD','1L1','1L2','1L3','2L1','2L2','2L3','3L1','3L2','3L3']
		holidays = ['HH','1H','2H','3H','1LH','2LH','3LH',]
		weekoffs = ['WW','1W','2W','3W','1LW','2LW','3LW']
		lops = ['AA','1M','MM','M1','','LL']
		wrong_shifts = ['12','13','21','23','31','32','2P2','1L2','1L3','2L1','2L3','3L1','3L2']
		half_days = ["0.5EL","0.5CL","0.5SL","0.5CO","0.5SPL","0.5LL","LEL/2","LCL/2","LSL/2","LCO/2","LLL/2","LA/2","0.5LLL"]

		for r in row:
			if r in actual_shifts:
				total_worked_days += 1
			if r in half_days:
				total_worked_days += 0.5
			if r == 'LA/2':
				total_worked_days += 0.5
			if r in holidays:
				total_holidays += 1
			if r in weekoffs:
				total_weekoffs += 1
			if r == 'CL':
				total_cl += 1
			if r == 'EL':
				total_el += 1
			if r == 'SL':
				total_sl += 1
			if r == 'CO':
				total_co += 1
			if r == 'SPL':
				total_spl += 1
			if r == '0.5CL':
				total_cl += 0.5
			if r == '0.5EL':
				total_el += 0.5
			if r == '0.5SL':
				total_sl += 0.5
			if r == '0.5CO':
				total_co += 0.5
			if r == '0.5SPL':
				total_spl += 0.5
			if r in lops:
				total_lop += 1
			if r in wrong_shifts:
				total_wrong_shifts += 1
			if r == 'LA/2':
				total_la += 0.5
			if r == '0.5LLL':
				total_la += 0.5

		if datetime.strptime(filters.from_date, "%Y-%m-%d").date()  < emp_det.date_of_joining:
			hds = frappe.db.sql_list('''select holiday_date from `tabHoliday`
					where
						weekly_off = 0 and
						parent=%(holiday_list)s
						and holiday_date >= %(start_date)s
						and holiday_date < %(end_date)s''', {
							"holiday_list": 'Holiday List - 2021',
							"start_date": filters.from_date,
							"end_date": emp_det.date_of_joining,
						})
			wof = frappe.db.sql_list('''select holiday_date from `tabHoliday`
					where
						weekly_off = 1 and
						parent=%(holiday_list)s
						and holiday_date >= %(start_date)s
						and holiday_date < %(end_date)s''', {
							"holiday_list": 'Holiday List - 2021',
							"start_date": filters.from_date,
							"end_date": emp_det.date_of_joining,
						})

			total_holidays = total_holidays - len(hds)
			total_weekoffs = total_weekoffs - len(wof)

		total_payable_days = total_worked_days + total_holidays + total_cl + total_el + total_sl + total_co + total_spl - total_wrong_shifts
		calendar_days = filters['total_days_in_month']
		row.extend([calendar_days,total_worked_days,total_weekoffs,total_holidays,total_cl ,total_el,total_sl,total_spl,total_la,total_lop,total_wrong_shifts,total_payable_days])
		emp_att_map[emp] = emp_status_map
		record.append(row)

	return record, emp_att_map

def get_columns(filters):

	columns = []

	if filters.group_by:
		columns = [_(filters.group_by)+ ":Link/Branch:120"]

	columns += [
		_("Employee ID") + ":Employee:150", _("Employee Name") + ":Data/:200"
	]
	days = []

	from_date = datetime.strptime(filters.from_date, "%Y-%m-%d")   # start date
	to_date = datetime.strptime(filters.to_date,  "%Y-%m-%d")       # end date

	delta = to_date - from_date       # as timedelta

	for i in range(delta.days + 1):
		day = from_date + timedelta(days=i)
		day_name = day_abbr[getdate(day).weekday()]
		days.append(cstr(day.day)+ " " +day_name +"::65")

	if not filters.summarized_view:
		columns += days 

	# if filters.summarized_view:
		columns += [_("Calendar Days") + ":Int:120", _("Worked Days") + ":Data:120",  
		_("WW") + ":Data:60",_("HH") + ":Data:60", _("CL") + ":Data:120", _("EL") + ":Data:120", _("SL") + ":Data:120", _("SPL") + ":Data:120", _("LA") + ":Data:120", _("LOP") + ":Data:120", 
		_("Wrong Shift")+ ":Data:120",_("Payable Days")+ ":Data:120", ]
	
	return columns, days

def get_attendance_list(conditions, filters):

	query = """select employee, day(attendance_date) as day_of_month,attendance_date,status,shift,qr_shift,shift_status,late_entry,leave_type,on_duty_application,in_time,out_time,employee_type from tabAttendance where docstatus != 2 and attendance_date between '%s' and '%s' and company = '%s' order by employee, attendance_date""" % (filters.from_date,filters.to_date,filters.company)
	# query = """ select employee, day(attendance_date) as day_of_month,status,shift,qr_shift,leave_type,shift_status,on_duty_application from tabAttendance where docstatus = 1  and attendance_date between '2021-03-01' and '2021-03-31' order by employee, attendance_date"""
	if filters.employee:
		query = """select employee, day(attendance_date) as day_of_month,attendance_date,status,shift,shift_status,late_entry,qr_shift,leave_type,on_duty_application,in_time,out_time,employee_type from tabAttendance where docstatus != 2 and attendance_date between '%s' and '%s' and employee='%s' and company = '%s' order by employee, attendance_date""" % (filters.from_date,filters.to_date,filters.employee,filters.company)

	attendance_list = frappe.db.sql(query,as_dict=1)

	if not attendance_list:
		msgprint(_("No attendance record found"), alert=True, indicator="orange")

	att_map = {}
	for d in attendance_list:
		att_map.setdefault(d.employee, frappe._dict()).setdefault(d.day_of_month, "")
		att_map[d.employee][d.day_of_month] = d.shift_status
		# late = ''
		# if d.late_entry:
		# 	late = 'L'
		# if filters.employee_type != "WC":
		# 	if not d.in_time or not d.out_time:
		# 		if d.qr_shift:
		# 			att_map[d.employee][d.day_of_month] = "M" + str(d.qr_shift)
		# 		else:
		# 			att_map[d.employee][d.day_of_month] = "AA"
		# 	if d.in_time and d.out_time:
		# 		if not d.qr_shift:
		# 			att_map[d.employee][d.day_of_month] = str(d.shift) + late + "M"
		# 		else:
		# 			att_map[d.employee][d.day_of_month] = str(d.shift) + late + str(d.qr_shift)
				
		# 	if d.status == 'Half Day':
		# 		if d.leave_type:
		# 			if not late:
		# 				att_map[d.employee][d.day_of_month] = str(0.5) + d.leave_type
		# 			else:
		# 				att_map[d.employee][d.day_of_month] = late + str(d.leave_type) + str('/2')
		# 	if d.status == 'On Leave':
		# 		att_map[d.employee][d.day_of_month] = d.leave_type
		# 	if d.on_duty_application:
		# 		att_map[d.employee][d.day_of_month] = "OD"
		# else:
		# 	if d.status == 'Half Day':
		# 		if d.leave_type:
		# 			if not late:
		# 				att_map[d.employee][d.day_of_month] = str(0.5) + d.leave_type
		# 			else:
		# 				att_map[d.employee][d.day_of_month] = late + str(d.leave_type) + str('/2')
		# 	if d.status == 'On Leave':
		# 		att_map[d.employee][d.day_of_month] = d.leave_type
		# 	elif d.on_duty_application:
		# 		att_map[d.employee][d.day_of_month] = "OD"
		# 	elif d.shift:
		# 		if d.in_time and d.out_time:
		# 			att_map[d.employee][d.day_of_month] = str(d.shift) + late
						
		# 		if not d.out_time:
		# 			att_map[d.employee][d.day_of_month] = str(d.shift) + 'M'
		# 	else:
		# 		att_map[d.employee][d.day_of_month] = 'AA'

	return att_map

def get_conditions(filters):
	# if not (filters.get("month") and filters.get("year")):
	# 	msgprint(_("Please select month and year"), raise_exception=1)

	from_date = datetime.strptime(filters.from_date, "%Y-%m-%d")   # start date
	to_date = datetime.strptime(filters.to_date,  "%Y-%m-%d")       # end date

	delta = to_date - from_date       # as timedelta

	filters["total_days_in_month"] = delta.days + 1

	conditions = " and attendance_date between %s and %s"
	# conditions = " and attendance_date between %(from_date)s and %(to_date)s"

	if filters.get("company"): conditions += " and company = %s"
	if filters.get("employee"): conditions += " and employee = %s"

	# if filters.get("company"): conditions += " and company = %(company)s"
	# if filters.get("employee"): conditions += " and employee = %(employee)s"

	return conditions, filters

def get_employee_details(employee_type,department,group_by, company):
	emp_map = {}
	if employee_type:
		query = """select name, employee_name, designation, department, branch, company, employee_type, date_of_joining,
		holiday_list from `tabEmployee` where company = %s and employee_type = '%s' and vacant = '0' """ % (frappe.db.escape(company),employee_type)
	else:
		query = """select name, employee_name, designation, department, branch, company, employee_type, date_of_joining,
		holiday_list from `tabEmployee` where company = %s and vacant = '0' """ % (frappe.db.escape(company))

	if group_by:
		group_by = group_by.lower()
		query += " order by " + group_by + " ASC"
	if department:
		query += "and department = '%s' "%department

	employee_details = frappe.db.sql(query , as_dict=1)

	group_by_parameters = []
	if group_by:

		group_by_parameters = list(set(detail.get(group_by, "") for detail in employee_details if detail.get(group_by, "")))
		for parameter in group_by_parameters:
				emp_map[parameter] = {}


	for d in employee_details:
		if group_by and len(group_by_parameters):
			if d.get(group_by, None):

				emp_map[d.get(group_by)][d.name] = d
		else:
			emp_map[d.name] = d

	if not group_by:
		return emp_map
	else:
		return emp_map, group_by_parameters

def get_holiday(holiday_list, from_date,to_date):
	holiday_map = frappe._dict()
	for d in holiday_list:
		if d:
			holiday_map.setdefault(d, frappe.db.sql('''select day(holiday_date), weekly_off from `tabHoliday`
				where parent=%s and holiday_date between %s and %s''', (d, from_date,to_date)))

	return holiday_map

@frappe.whitelist()
def get_attendance_years():
	year_list = frappe.db.sql_list("""select distinct YEAR(attendance_date) from tabAttendance ORDER BY YEAR(attendance_date) DESC""")
	if not year_list:
		year_list = [getdate().year]

	return "\n".join(str(year) for year in year_list)

@frappe.whitelist()
def get_to_date(from_date):
	day = from_date[-2:]
	if int(day) > 25:
		return add_days(get_last_day(from_date),25)
	if int(day) <= 25:
		return add_days(get_first_day(from_date),25)
