from email import message
import frappe
from frappe import _
from erpnext.payroll.doctype.salary_slip.salary_slip import SalarySlip
from erpnext.payroll.doctype.additional_salary.additional_salary import AdditionalSalary
from erpnext.payroll.doctype.payroll_entry.payroll_entry import PayrollEntry
from erpnext.hr.doctype.shift_assignment.shift_assignment import ShiftAssignment
from erpnext.hr.doctype.leave_application.leave_application import LeaveApplication
from erpnext.hr.doctype.employee.employee import Employee
from erpnext.hr.doctype.compensatory_leave_request.compensatory_leave_request import CompensatoryLeaveRequest
from thaisummit.thaisummit.doctype.overtime_request.overtime_request import OvertimeRequest
from frappe.utils import add_days, cint, cstr, flt, getdate, rounded, date_diff, money_in_words, formatdate, get_first_day,get_time
from erpnext.hr.utils import validate_dates, validate_overlap, get_leave_period, \
	get_holidays_for_employee, create_additional_leave_ledger_entry
from erpnext.payroll.doctype.payroll_entry.payroll_entry import get_start_end_dates

class CustomAdditionalSalary(AdditionalSalary):
	def before_save(self):
		add_salary = frappe.db.count('Additional Salary',{'employee':self.employee,'salary_component':self.salary_component,'department':self.department,'payroll_date':self.payroll_date})
		if add_salary >=1:
			frappe.throw(_('Employee %s  have already Additional Salary'%(self.employee)))
			message = ('Employee %s have already Additional Salary'%(self.employee))
			frappe.log_error('Additional Salary',message)

class CustomOvertimeRequest(OvertimeRequest):
	
	def before_save(self):
		if self.shift == 'PP2':
			self.from_time = get_time('04:00:00')
			self.to_time = get_time('08:00:00')
			self.ot_hours = get_time('03:30:00')

class CustomEmployee(Employee):
	def before_save(self):
		if self.status == 'Active':
			if self.ctc <= 0.0:
				frappe.throw(_('Please Fill the Salary Components Details'))
				frappe.log_error('Employe %s Please fill the salary Components'%(self.employee_number))


class CustomSalarySlip(SalarySlip):
	def get_date_details(self):
		if not self.end_date:
			date_details = get_start_end_dates(self.payroll_frequency, self.start_date or self.posting_date)
			self.start_date = date_details.start_date
			self.end_date = date_details.end_date
		row_exists = False
		ot = frappe.db.sql("""select sum(ot_amount) as ot_amount from `tabOvertime Request`
		where `tabOvertime Request`.employee = '%s' and `tabOvertime Request`.ot_date between '%s' and '%s' and `tabOvertime Request`.workflow_state = 'Approved' and `tabOvertime Request`.docstatus = '1' """%(self.employee,self.start_date,self.end_date),as_dict=True)[0].ot_amount or 0
		amount = round(ot)
		for row in self.earnings:
			if row.salary_component == "Others":
				row.amount = amount
				row_exists = True
				break

		if not row_exists:
			wages_row = {
				"salary_component": "Others",
				"abbr": frappe.db.get_value("Salary Component", "Others", "salary_component_abbr"),
				# "amount": self.hour_rate * self.total_working_hours,
				"amount": amount,
				"default_amount": 0.0,
				"additional_amount": 0.0
			}
			self.append('earnings', wages_row)


	def calculate_lwp_ppl_and_absent_days_based_on_attendance(self, holidays):
		lwp = 0
		absent = 0
		shift1 = 0
		shift2 = 0
		shift3 = 0
		shiftpp1 = 0
		shiftpp2 = 0
		transport_days = 0
		leave_days = 0

		daily_wages_fraction_for_half_day = \
			flt(frappe.db.get_value("Payroll Settings", None, "daily_wages_fraction_for_half_day")) or 0.5

		leave_types = frappe.get_all("Leave Type",
			or_filters=[["is_ppl", "=", 1], ["is_lwp", "=", 1]],
			fields =["name", "is_lwp", "is_ppl", "fraction_of_daily_salary_per_leave", "include_holiday"])

		leave_type_map = {}
		for leave_type in leave_types:
			leave_type_map[leave_type.name] = leave_type
		
		attendances = frappe.db.sql('''
			SELECT attendance_date, status, leave_type
			FROM `tabAttendance`
			WHERE
				status in ("Absent", "Half Day", "On leave")
				AND employee = %s
				AND docstatus = 1
				AND attendance_date between %s and %s
		''', values=(self.employee, self.start_date, self.end_date), as_dict=1)
		for d in attendances:
			if d.status == 'On Leave':
				if d.leave_type != 'Leave without Pay':
					leave_days += 1
			if d.status in ('Half Day', 'On Leave') and d.leave_type and d.leave_type not in leave_type_map.keys():
				continue

			if formatdate(d.attendance_date, "yyyy-mm-dd") in holidays:
				if d.status == "Absent" or \
					(d.leave_type and d.leave_type in leave_type_map.keys() and not leave_type_map[d.leave_type]['include_holiday']):
						continue
			if d.leave_type:
				fraction_of_daily_salary_per_leave = leave_type_map[d.leave_type]["fraction_of_daily_salary_per_leave"]

			if d.status == "Half Day":
				equivalent_lwp =  (1 - daily_wages_fraction_for_half_day)

				if d.leave_type in leave_type_map.keys() and leave_type_map[d.leave_type]["is_ppl"]:
					equivalent_lwp *= fraction_of_daily_salary_per_leave if fraction_of_daily_salary_per_leave else 1
				lwp += equivalent_lwp
				if d.leave_type != 'Leave without Pay':
					leave_days += 0.5
				# transport_days += 1
			if d.status == "On Leave":
				equivalent_lwp = 1
				if leave_type_map[d.leave_type]["is_ppl"]:
					equivalent_lwp *= fraction_of_daily_salary_per_leave if fraction_of_daily_salary_per_leave else 1
				lwp += equivalent_lwp
				
			elif d.status == "Absent":
				absent += 1
		present_attendances = frappe.db.sql('''
			SELECT attendance_date, status,shift,shift_status
			FROM `tabAttendance`
			WHERE
				status in ("Present","Half Day","Absent")
				AND employee = %s
				AND docstatus = 1
				AND shift_status is not null
				AND attendance_date between %s and %s
		''', values=(self.employee, self.start_date, self.end_date), as_dict=1)
		od_attendances = frappe.db.sql('''
			SELECT attendance_date, status,shift
			FROM `tabAttendance`
			WHERE
				status in ("Present","Half Day","Absent")
				AND employee = %s
				AND docstatus = 1
				# AND shift is null
				AND on_duty_application is not null
				AND attendance_date between %s and %s
		''', values=(self.employee, self.start_date, self.end_date), as_dict=1)
		for d in od_attendances:
			transport_days += 1
		for d in present_attendances:
			if d.shift_status in ("11",'1L1'):
				shift1 += 1
			if d.shift_status in ('2','22', '2L2', '2W', '2LW'):
				shift2 += 1
			if d.shift_status in ('3','33', '3L3', '3W', '3LW'):
				shift3 += 1
			if d.shift_status in ("PP1","PP1PP1","P1P1"):
				shiftpp1 += 1
			if d.shift_status in ("PP2","PP2PP2","P2P2"):   
				shiftpp2 += 1
			if d.shift_status in ('11','22','33','1L1','2L2','3L3','1W','1LW','2W','2LW','3W','3LW','ODW','1H','1LH','0.5LL','0.5LLL','1H','2H','3H','1LH','2LH','3LH','0.5Leave Without Pay','0.5Leave Without Pay','LLeave Without Pay/2','0.5Sick Leave','0.5Casual Leave','0.5Earned Leave','LSick Leave/2','0.5Compensatory Off','LCasual Leave/2'):
				transport_days += 1
		self.shift_1 = shift1
		self.shift_2 = shift2
		self.shift_3 = shift3
		self.shift_pp1 = shiftpp1
		self.shift_pp2 = shiftpp2
		self.transport_days = transport_days
		self.leave_days = leave_days
		self.transport_allowance = frappe.db.get_value('Designation',self.designation,'transport_allowance')
		if self.employee_type == 'WC':
			self.attendance_bonus_days = frappe.db.get_value('Payroll Settings',None,'wc_att_bonus')
		elif self.employee_type == 'BC':
			self.attendance_bonus_days = frappe.db.get_value('Payroll Settings',None,'bc_att_bonus')
		elif self.employee_type == 'NT':
			self.attendance_bonus_days = frappe.db.get_value('Payroll Settings',None,'nt_att_bonus')
		elif self.employee_type == 'FT':
			self.attendance_bonus_days = frappe.db.get_value('Payroll Settings',None,'ft_att_bonus')
		elif self.employee_type == 'CL':
			self.attendance_bonus_days = frappe.db.get_value('Payroll Settings',None,'cl_att_bonus')
		return lwp, absent

def check_holiday(date):
	holiday = frappe.db.sql("""select `tabHoliday`.holiday_date,`tabHoliday`.weekly_off from `tabHoliday List` 
	left join `tabHoliday` on `tabHoliday`.parent = `tabHoliday List`.name where `tabHoliday List`.name = 'Holiday List - 2021' and holiday_date = '%s' """%(date),as_dict=True)
	if holiday:
		if holiday[0].weekly_off == 1:
			return "WW"
		else:
			return "HH"

class CustomPayrollEntry(PayrollEntry):
	def get_filter_condition(filters):
		cond = ''
		for f in ['company', 'branch', 'department', 'designation','employee_type','contractor']:
			if filters.get(f):
				cond += " and t1." + f + " = " + frappe.db.escape(filters.get(f))
		return cond
	
	def make_filters(self):
		filters = frappe._dict()
		filters['company'] = self.company
		filters['branch'] = self.branch
		filters['department'] = self.department
		filters['designation'] = self.designation
		filters['employee_type'] = self.employee_type
		filters['contractor'] = self.contractor
		return filters

	def before_save(self):  
		if self.contractor == 'VAC':
			frappe.throw(_('VAC Contractor Not Allowed for Payroll entry'))

class CustomShiftAssignment(ShiftAssignment):
	def validate(self):
		self.validate_overlapping_dates()

		if self.end_date and self.end_date < self.start_date:
			frappe.throw(_("End Date must not be lesser than Start Date"))

# class CustomLeaveApplication(LeaveApplication):
# 	def on_update(self):
# 		self.status = self.workflow_state
# 		if self.status == "Open" and self.docstatus < 1:
# 			# notify leave approver about creation
# 			self.notify_leave_approver()

class CustomCompensatoryLeaveRequest(CompensatoryLeaveRequest):
	def validate(self):
		validate_dates(self, self.work_from_date, self.work_end_date)
		if self.half_day:
			if not self.half_day_date:
				frappe.throw(_("Half Day Date is mandatory"))
			if not getdate(self.work_from_date)<=getdate(self.half_day_date)<=getdate(self.work_end_date):
				frappe.throw(_("Half Day Date should be in between Work From Date and Work End Date"))
		validate_overlap(self, self.work_from_date, self.work_end_date)
		# self.validate_holidays()
		# self.validate_attendance()
		if not self.leave_type:
			frappe.throw(_("Leave Type is madatory"))
