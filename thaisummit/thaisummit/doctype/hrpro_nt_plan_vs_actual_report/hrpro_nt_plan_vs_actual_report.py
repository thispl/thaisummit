# Copyright (c) 2023, TEAMPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class HRPRONTPlanvsActualReport(Document):
	@frappe.whitelist()
	def shiftwise_report(self):

		data = ''
		data += '<table class="table table-bordered table-sm"><tr style="font-size:8px"><th style="background-color:#ff9900;border: 1px solid black;"><b><center>DATE</center></b></th><th style="background-color:#00b33c;border: 1px solid black"><center><b>%s</b></center></th><th colspan="2" style="background-color:#ff9900;border: 1px solid black"><center><b>SHIFT</b></center></th><th style="background-color:#00b33c;border: 1px solid black"><center><b>%s</b></center></th><th rowspan="2" style="background-color:#ffff00;border: 1px solid black"><b><center>OT</center></b></th></tr>'%(frappe.utils.format_date(self.date),self.shift)
		data += '<tr height="10%" style="background-color:#d5dbdb;border: 1px solid black;font-size:8px"><td style="border: 1px solid black"><b><center>GROUP</center></b></td><td style="border: 1px solid black"><b><center>DEPARTMENT</center></b></td><td style="border: 1px solid black"><b><center>PLAN</center></b></td><td style="border: 1px solid black"><b><center>ACTUAL</center></b></td><td style="border: 1px solid black"><b><center>DIFF</center></b></td></tr>'
		# dept_group = frappe.get_all('Department',{'is_group':1,'name':('!=',"All Departments")})
		dept_group = ['IYM','RE','FORD','SUPPORT']
		for dg in dept_group:
			departments = frappe.get_all('Department',{'parent_department':dg,'live':1} )
			g = 1
			for dept in departments:
				plan=frappe.db.count("Shift Assignment",{'department':dept.name,'start_date':self.date,'shift_type':self.shift,'employee_type':'NT'})
				actual_shift=frappe.db.count("QR Checkin",{'department':dept.name,'shift_date':self.date,'qr_shift':self.shift,'ot':0,'employee_type':'NT'})
				shift_difference=plan-actual_shift
				ot_count=frappe.db.count("QR Checkin",{'department':dept.name,'shift_date':self.date,'qr_shift':self.shift,'ot':1,'employee_type':'NT'})
				if g == 1:
					data += '<tr style="font-size:5px;padding:0px"><td style="border: 1px solid black;padding:0px" rowspan="%s" ><b><center>%s</center></b></td><td style="border: 1px solid black;padding:2px"><b>%s</b></td><td style="border: 1px solid black;padding:0px"><b><center>%s</center></b></td><td style="border: 1px solid black;padding:0px"><b><center>%s</center></b></td><td style="border: 1px solid black;padding:0px"><b><center>%s</center></b></td><td style="border: 1px solid black;padding:0px"><b><center>%s</center></b></td></tr>'%(len(departments),dg,dept.name,plan,actual_shift,shift_difference,ot_count)
					g = 0
				else:
					data += '<tr style="font-size:5px;padding:0px"><td style="border: 1px solid black;padding:2px"><b>%s</b></td><td style="border: 1px solid black;padding:0px"><b><center>%s</center></b></td><td style="border: 1px solid black;padding:0px"><b><center>%s</center></b></td><td style="border: 1px solid black;padding:0px"><b><center>%s</center></b></td><td style="border: 1px solid black;padding:0px"><b><center>%s</center></b></td></tr>'%(dept.name,plan,actual_shift,shift_difference,ot_count)
			g = 1

		total_plan=frappe.db.count("Shift Assignment",{'start_date':self.date,'shift_type':self.shift,'employee_type':'NT'})
		total_actual_shift=frappe.db.count("QR Checkin",{'shift_date':self.date,'qr_shift':self.shift,'ot':0,'employee_type':'NT'})
		total_shift_difference=total_plan-total_actual_shift
		total_ot_count=frappe.db.count("QR Checkin",{'shift_date':self.date,'qr_shift':self.shift,'ot':1,'employee_type':'NT'})
		data += '<tr style="background-color:#ff9900;font-size:10px"><td style="border: 1px solid black" colspan="2"><center><b>Total</b><center></td><td style="border: 1px solid black"><b><center>%s</center></b></td><td style="border: 1px solid black"><b><center>%s</center></b></td><td style="border: 1px solid black"><b><center>%s</center></b></td><td style="border: 1px solid black"><b><center>%s</center></b></td></tr>'%(total_plan,total_actual_shift,total_shift_difference,total_ot_count)
		data +='</table>'
		return data
	
	@frappe.whitelist()
	def withoutshift_report(self):

		data = ''
		data += '<table class="table table-bordered table-sm"><tr style="font-size:8px"><th style="background-color:#ff9900;border: 1px solid black;"><b><center>DATE</center></b></th><th style="background-color:#00b33c;border: 1px solid black"><center><b>%s</b></center></th><th colspan="2" style="background-color:#ff9900;border: 1px solid black"><center><b>SHIFT</b></center></th><th style="background-color:#00b33c;border: 1px solid black"><center><b>%s</b></center></th><th rowspan="2" style="background-color:#ffff00;border: 1px solid black"><b><center>OT</center></b></th></tr>'%(frappe.utils.format_date(self.date),self.shift)
		data += '<tr height="10%" style="background-color:#d5dbdb;border: 1px solid black;font-size:8px"><td style="border: 1px solid black"><b><center>GROUP</center></b></td><td style="border: 1px solid black"><b><center>DEPARTMENT</center></b></td><td style="border: 1px solid black"><b><center>PLAN</center></b></td><td style="border: 1px solid black"><b><center>ACTUAL</center></b></td><td style="border: 1px solid black"><b><center>DIFF</center></b></td></tr>'
		# dept_group = frappe.get_all('Department',{'is_group':1,'name':('!=',"All Departments")})
		dept_group = ['IYM','RE','FORD','SUPPORT']
		for dg in dept_group:
			departments = frappe.get_all('Department',{'parent_department':dg,'live':1} )
			g = 1
			for dept in departments:
				plan=frappe.db.count("Shift Assignment",{'department':dept.name,'start_date':self.date,'employee_type':'NT'})
				actual_shift=frappe.db.count("QR Checkin",{'department':dept.name,'shift_date':self.date,'ot':0,'employee_type':'NT'})
				shift_difference=plan-actual_shift
				ot_count=frappe.db.count("QR Checkin",{'department':dept.name,'shift_date':self.date,'ot':1,'employee_type':'NT'})
				if g == 1:
					data += '<tr style="font-size:5px;padding:0px"><td style="border: 1px solid black;padding:0px" rowspan="%s" ><b><center>%s</center></b></td><td style="border: 1px solid black;padding:2px"><b>%s</b></td><td style="border: 1px solid black;padding:0px"><b><center>%s</center></b></td><td style="border: 1px solid black;padding:0px"><b><center>%s</center></b></td><td style="border: 1px solid black;padding:0px"><b><center>%s</center></b></td><td style="border: 1px solid black;padding:0px"><b><center>%s</center></b></td></tr>'%(len(departments),dg,dept.name,plan,actual_shift,shift_difference,ot_count)
					g = 0
				else:
					data += '<tr style="font-size:5px;padding:0px"><td style="border: 1px solid black;padding:2px"><b>%s</b></td><td style="border: 1px solid black;padding:0px"><b><center>%s</center></b></td><td style="border: 1px solid black;padding:0px"><b><center>%s</center></b></td><td style="border: 1px solid black;padding:0px"><b><center>%s</center></b></td><td style="border: 1px solid black;padding:0px"><b><center>%s</center></b></td></tr>'%(dept.name,plan,actual_shift,shift_difference,ot_count)
			g = 1

		total_plan=frappe.db.count("Shift Assignment",{'start_date':self.date,'employee_type':'NT'})
		total_actual_shift=frappe.db.count("QR Checkin",{'shift_date':self.date,'ot':0,'employee_type':'NT'})
		total_shift_difference=total_plan-total_actual_shift
		total_ot_count=frappe.db.count("QR Checkin",{'shift_date':self.date,'ot':1,'employee_type':'NT'})
		data += '<tr style="background-color:#ff9900;font-size:10px"><td style="border: 1px solid black" colspan="2"><center><b>Total</b><center></td><td style="border: 1px solid black"><b><center>%s</center></b></td><td style="border: 1px solid black"><b><center>%s</center></b></td><td style="border: 1px solid black"><b><center>%s</center></b></td><td style="border: 1px solid black"><b><center>%s</center></b></td></tr>'%(total_plan,total_actual_shift,total_shift_difference,total_ot_count)
		data +='</table>'
		return data


