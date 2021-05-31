import frappe
from erpnext.payroll.doctype.salary_slip.salary_slip import SalarySlip
from erpnext.payroll.doctype.payroll_entry.payroll_entry import PayrollEntry
from erpnext.hr.doctype.shift_assignment.shift_assignment import ShiftAssignment
from erpnext.hr.doctype.leave_application.leave_application import LeaveApplication
from frappe.utils import add_days, cint, cstr, flt, getdate, rounded, date_diff, money_in_words, formatdate, get_first_day

class CustomSalarySlip(SalarySlip):
    def calculate_lwp_ppl_and_absent_days_based_on_attendance(self, holidays):  
        lwp = 0
        absent = 0
        shift1 = 0
        shift2 = 0
        shift3 = 0
        shiftpp1 = 0
        shiftpp2 = 0
        transport_days = 0

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
            elif d.status == "On Leave" and d.leave_type and d.leave_type in leave_type_map.keys():
                equivalent_lwp = 1
                if leave_type_map[d.leave_type]["is_ppl"]:
                    equivalent_lwp *= fraction_of_daily_salary_per_leave if fraction_of_daily_salary_per_leave else 1
                lwp += equivalent_lwp
            elif d.status == "Absent":
                absent += 1
        present_attendances = frappe.db.sql('''
            SELECT attendance_date, status,shift
            FROM `tabAttendance`
            WHERE
                status = "Present"
                AND employee = %s
                AND docstatus = 1
                AND attendance_date between %s and %s
        ''', values=(self.employee, self.start_date, self.end_date), as_dict=1)
        for d in present_attendances:
            if d.shift == "1":
                shift1 += 1
            if d.shift == "2":
                shift2 += 1
            if d.shift == "3":
                shift3 += 1
            if d.shift == "PP1":
                shiftpp1 += 1
            if d.shift == "PP2":
                shiftpp2 += 1
            transport_days += 1
        self.shift_1 = shift1
        self.shift_2 = shift2
        self.shift_3 = shift3
        self.shift_pp1 = shiftpp1
        self.shift_pp2 = shiftpp2
        self.transport_days = transport_days
        return lwp, absent

class CustomPayrollEntry(PayrollEntry):
    def get_filter_condition(self):
        self.check_mandatory()
        cond = ''
        for f in ['company', 'branch', 'department', 'designation','employee_type']:
            if self.get(f):
                cond += " and t1." + f + " = " + frappe.db.escape(self.get(f))

        return cond

class CustomShiftAssignment(ShiftAssignment):
    def validate(self):
        self.validate_overlapping_dates()

        if self.end_date and self.end_date < self.start_date:
            frappe.throw(_("End Date must not be lesser than Start Date"))

class CustomLeaveApplication(LeaveApplication):
    def on_update(self):
        self.status = self.workflow_state
        if self.status == "Open" and self.docstatus < 1:
            # notify leave approver about creation
            self.notify_leave_approver()
        