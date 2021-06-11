# -*- coding: utf-8 -*-
# Copyright (c) 2021, TEAMPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import add_days

class QRCheckin(Document):
	def after_insert(self):
		if self.qr_shift == "2":
			if frappe.db.exists("QR Checkin",{'employee':self.employee,'qr_shift':'1','shift_date':self.shift_date}):
				frappe.db.set_value("QR Checkin",self.name,'ot',1)
		if self.qr_shift == "3":
			if frappe.db.exists("QR Checkin",{'employee':self.employee,'qt_shift':'2','shift_date':self.shift_date}):
				frappe.db.set_value("QR Checkin",self.name,'ot',1)
		if self.qr_shift == "1":
			shift_date = add_days(self.shift_date,-1)
			if frappe.db.exists("QR Checkin",{'employee':self.employee,'qr_shift':'3','shift_date':shift_date}):
				frappe.db.set_value("QR Checkin",self.name,'ot',1)
			if frappe.db.exists("QR Checkin",{'employee':self.employee,'qr_shift':'PP2','shift_date':shift_date}):
				frappe.db.set_value("QR Checkin",self.name,'ot',1)