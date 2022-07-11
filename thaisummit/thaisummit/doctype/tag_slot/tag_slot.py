# -*- coding: utf-8 -*-
# Copyright (c) 2021, TEAMPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import requests
import json
from frappe.utils import cint
from datetime import datetime
from frappe.utils.csvutils import UnicodeWriter, read_csv_content
from frappe.utils import cstr, add_days, date_diff, getdate,today

class TAGSlot(Document):    
    @frappe.whitelist()
    def create_tag_master(self):
        for rq in self.tag_wise_list:
            tm = frappe.new_doc("TAG Master")
            tm.slot_no = self.name
            tm.qr = rq.tag_no 
            tm.recieved_time = self.datetime
            tm.parts_no = rq.parts_no
            tm.delay_duration = '00:00:00'
            tm.required_quantity = rq.required_quantity
            tm.sap_quantity = rq.sap_quantity
            tm.difference = rq.difference
            tm.tag_type = rq.tag_type
            tm.sp_purchase_price = rq.sp_purchase_price
            tm.vehicle_in = rq.vehicle
            tm.model_number = rq.model_number
            tm.save(ignore_permissions=True)
            frappe.db.commit()
            self.tag_master = tm.name
        return "TAG Masters Created"

    @frappe.whitelist()
    def validate(self):
        tag_list = self.tag_wise_list
        for tag in tag_list:
            tag.difference = cint(tag.sap_quantity) - cint(tag.required_quantity)
            # if tag.difference < 0:
            #     (tag.difference).indicator_color = 'blue'
                # <style="background-color:red"><center> <h4>'tag.difference'</h4></center></style>

    @frappe.whitelist()
    def calculate_quantity(self):
        tag_list = self.tag_wise_list
        sap_item_qty = 0
        difference = 0
        for tag in tag_list:
            required_quantity = cint(tag.required_quantity)
            sap_avl_qty = get_sap_qty(tag.parts_no)
            sap_item_qty = cint(sap_avl_qty)
            tag.sap_quantity = cint(sap_item_qty)
            sap_item_qty =  tag.sap_quantity - cint(required_quantity)
            if sap_item_qty < 0:
                sap_item_qty = 0
        return ['Quantity Updated',datetime.now()]


@frappe.whitelist()
def get_sap_qty(parts_no):
    avl_qty = 0
    mat_no = frappe.get_value('Part Master', parts_no,"mat_no")
    # url = "http://172.16.1.18/StockDetail/Service1.svc/GetItemInventory"
    url = "http://172.16.1.18/StockDetail/Service1.svc/GetItemInventory"
    payload = json.dumps({
    "ItemCode": mat_no
    })
    headers = {
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    wh_data = json.loads(response.text)
    frappe.errprint(wh_data)
    if wh_data:
        for whd in wh_data:
            if whd['Warehouse'] == 'FG':
                avl_qty = whd['Qty']
    return avl_qty

@frappe.whitelist()
def download_excel():
    args = frappe.local.form_dict

    w = UnicodeWriter()
    w = add_header(w)

    w = add_data(w, args)
    

    # write out response as a type csv
    frappe.response['result'] = cstr(w.getvalue())
    frappe.response['type'] = 'csv'
    frappe.response['doctype'] = "Tag Slot"

def add_header(w):
    w.writerow(["SL.No","CARD RECEIVED DATE & TIME","DISPATCH DATE & TIME","MAT NO","PART NO","PART NAME","DISPATCH QTY" ,"SAP STOCK","DISPATCH READINESS STATUS"])
    return w

def add_data(w, args):
    data = get_data(args)
    writedata(w, data)
    return w

def get_data(args):
    tag_slot = frappe.get_doc('TAG Slot',args['name'])
    data = []
    for idx,child in enumerate(tag_slot.tag_wise_list):
        row = [
            idx+1,child.datetime,child.dispatch_datetime,child.mat_no,child.parts_no,child.parts_no,child.required_quantity,child.sap_quantity
        ]
        data.append(row)
    return data


def writedata(w, data):
    for row in data:
        w.writerow(row)

#Old Calculation
# @frappe.whitelist()
#     def calculate_quantity(self):
#         tag_list = self.tag_wise_list
#         sap_item_qty = 0
#         difference = 0
#         for tag in tag_list:
#             required_quantity = cint(tag.required_quantity)
#             # sap_quantity = cint(tag.sap_quantity)
#             part = get_sap_qty(tag.parts_no)
#             # part = frappe.get_value('Part Master', tag.parts_no,['temp_avl_qty','name'])
#             sap_item_qty = cint(part[0])
#             # qty_diff = cint(sap_item_qty) - cint(required_quantity)
#             # tag.sap_quantity = sap_item_qty
#             tag.sap_quantity = cint(sap_item_qty)
#             sap_item_qty =  tag.sap_quantity - cint(required_quantity)

#             if sap_item_qty < 0:
#                 sap_item_qty = 0
#             # if sap_item_qty > cint(required_quantity):
#             #     tag.sap_quantity = required_quantity
#             #     sap_item_qty = cint(sap_item_qty) - cint(required_quantity)
#             # else:
#             #     tag.sap_quantity = sap_item_qty
#             #     sap_item_qty = cint(sap_item_qty) - cint(required_quantity)
#             #     if sap_item_qty < 0:
#             #         sap_item_qty = 0
#             # frappe.set_value('Part Master', tag.parts_no, 'temp_avl_qty', sap_item_qty)
#             frappe.db.commit()
#         return ['Quantity Updated',datetime.now()]