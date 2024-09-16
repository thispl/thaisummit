# Copyright (c) 2024, TEAMPRO and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import frappe
class SalaryRevisionEntry(Document):
	
	def on_submit(self):
		emp = frappe.get_doc('Employee',self.employee)
		emp.basic = self.basic
		emp.house_rent_allowance = self.hra
		emp.conveyance_allowance = self.convey
		emp.special_allowance = self.spl
		emp.other_allowance = self.other
		emp.medical_allowance = self.ma
		emp.leave_travel_allowance = self.leave
		emp.position_allowance = self.pos
		emp.children_education = self.child
		emp.children_hostel = self.hostel
		emp.washing_allowance = self.wash
		emp.welding_allowance = self.weld
		emp.temp_allowance = self.temp
		emp.service_charge = self.service
		emp.ppe = self.ppe
		emp.epf_er =self.epf
		emp.esi_er=self.esi
		emp.gross=self.gross
		emp.ctc=self.ctc
		emp.save(ignore_permissions=True)
		frappe.db.commit()
