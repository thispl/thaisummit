# -*- coding: utf-8 -*-
# Copyright (c) 2021, TEAMPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import datetime

class TAGIN(Document):
    def new_tag_slot(self):
        date = datetime.datetime.now()
        today_date = date.strftime("%d%m%Y")
        get_length = frappe.db.sql("""select count(slot_no) as count from `tabTAG Slot` """,as_dict =True)
        count = get_length[0].count + 1
        ts=frappe.new_doc("TAG Slot")
        ts.slot_no=today_date +"-"+str(count)
        ts.datetime =self.submit_time
        for ret in self.receipt_entry_table:
            ts.append("tag_wise_list",{
            "tag_no":ret.qr,
            "mat_no":ret.mat_no,
            "parts_no":ret.parts_no,
            "required_quantity":ret.quantity,
            "datetime":ret.date_and_time,
            "tag_type":ret.card_type
            })
            ts.save(ignore_permissions=True)
            frappe.db.commit()
        return "TAG Slot No - {} Created" .format(ts.slot_no)