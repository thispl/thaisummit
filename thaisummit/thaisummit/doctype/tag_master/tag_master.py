# -*- coding: utf-8 -*-
# Copyright (c) 2021, TEAMPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
# import numpy as np
from datetime import timedelta,datetime
from frappe.utils import cint, getdate, get_datetime

class TAGMaster(Document):
    def validate(self):
        if self.required_quantity and self.sap_quantity:
            self.difference = int(self.required_quantity) - int(self.sap_quantity)
        
    def parts(self):
        ch = []
        qr_code = self.qr
        y = qr_code.find('P')
        z = qr_code.find('V')
        parts_no = qr_code[y:z]
        # frappe.errprint(parts_no)
        q = qr_code.find('Q')
        k = qr_code.find('K')
        qty = qr_code[q:k]

        # frappe.errprint(qty)
        q = qr_code.find('Q')
        k = qr_code.rfind('K')
        qty = qr_code[q:k]

        # frappe.errprint(qty)
        return parts_no,qty

# @frappe.whitelist()
    def get_delay(self):
        status = 'On Time Sent'
        delay = frappe.db.get_value("TAG Monitoring Management",None,"delay_duration")
        tag_master_time = datetime.strptime(self.date_and_time, '%Y-%m-%d %H:%M:%S')
        submission_time = datetime.now()
        time_taken = submission_time - tag_master_time
        frappe.errprint(time_taken)
        allowed_delay_duration = timedelta(seconds=cint(delay))
        if time_taken > allowed_delay_duration:
            status = 'Delay'
        return status,time_taken