# Copyright (c) 2021, TEAMPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import requests
import datetime
import json
from datetime import datetime
from frappe.utils import cstr, add_days, date_diff, getdate, today,get_first_day, get_last_day

class TSAIInvoice(Document):
    def after_insert(self):
        total_gst_amount = 0
        cgst = self.total_basic_amount * (self.cgst / 100)
        sgst = self.total_basic_amount * (self.sgst / 100)
        igst = self.total_basic_amount * (self.igst / 100)
        total_gst_amount = cgst + sgst + igst
        # self.total_gst_amount = total_gst_amount
        # self.total_invoice_amount = self.total_basic_amount + total_gst_amount
        total_invoice_amount = self.total_basic_amount + total_gst_amount
        frappe.db.set_value('TSAI Invoice',self.name,'total_gst_amount',total_gst_amount)
        frappe.db.set_value('TSAI Invoice',self.name,'total_invoice_amount',total_invoice_amount)
    
    # def on_update(self):
    #     total_gst_amount = 0
    #     cgst = self.total_basic_amount * (self.cgst / 100)
    #     sgst = self.total_basic_amount * (self.sgst / 100)
    #     igst = self.total_basic_amount * (self.igst / 100)
    #     total_gst_amount = cgst + sgst + igst
    #     # self.total_gst_amount = total_gst_amount
    #     # self.total_invoice_amount = self.total_basic_amount + total_gst_amount
    #     total_invoice_amount = self.total_basic_amount + total_gst_amount
    #     frappe.db.set_value('TSAI Invoice',self.name,'total_gst_amount',total_gst_amount)
    #     frappe.db.set_value('TSAI Invoice',self.name,'total_invoice_amount',total_invoice_amount)

    
    # def after_insert(self):
    #     # if self.name == 'G0024222300172':
    #     url = "http://172.16.1.18/StockDetail/Service1.svc/InsertTagCardDetails"
    #     headers = {
    #         'Content-Type': 'application/json'
    #     }
    #     date = datetime.strptime(today(), '%Y-%m-%d')
    #     month = datetime.strftime(date, "%m")
    #     year = datetime.strftime(date, "%Y")

    #     if int(month) <= 3 :
    #         fyear = str(int(year[-2:])-1) + str(year[-2:])
    #     else:
    #         fyear = str(year[-2:]) + str(int(year[-2:])+1)

    #     scenario_code = (str(get_first_day(today())) + str(get_last_day(today()))).replace('-','')

    #     for item in self.invoice_items:
    #         payload = {
    #             "ScenarioCode": scenario_code,
    #             "BaseEntry": self.po_no,
    #             "ItemCode": item.mat_no,
    #             "ItemName": item.parts_name,
    #             "VendorCode": self.supplier_code,
    #             "VendorName": self.supplier_name,
    #             "ReleaseDate": self.invoice_date,
    #             "Plan": item.key_qty,
    #             "Qty": item.key_qty,
    #             "Backlog": item.po_qty,
    #             "PackingStandard": item.packing_standard,
    #             "Rate": item.unit_price,
    #             "Amount": item.basic_amount,
    #             "SGST": item.sgst,
    #             "CGST": item.cgst,
    #             "IGST": item.igst,
    #             "TCS":"0.0",
    #             "InvoiceAmount": item.invoice_amount,
    #             "NextNumber": str(self.invoice_no)[-5:],
    #             "TagCardNumber": self.invoice_no,
    #             "FYID": fyear,
    #             "POEntry": self.po_entry,
    #             "PODate": self.po_date,
    #             "PONumber": self.po_no
    #         }
    #         # payload = {"ScenarioCode":"A","BaseEntry":"1","ItemCode":"C","ItemName":"D","VendorCode":"E","VendorName":"F","ReleaseDate":"2021-01-21","Plan":"1.00","Backlog":"2.00","PackingStandard":"2.00","Rate":"2.00","Amount":"2.20","SGST":"0.00","CGST":"0.00","IGST":"12.00","TCS":"5.50","InvoiceAmount":"1.2","NextNumber":"1","TagCardNumber":"422","FYID":"2122","POEntry":"110","PODate":"2022-01-21","PONumber":"10"}
    #         frappe.log_error(title="grn_test",message=json.dumps(payload))
    #         response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    #         # frappe.log_error(title='grn_response',message=response.text)



# calculating cgst and sgst for tsai invoice
@frappe.whitelist()
def get_gst_percent(doc,method):
    doc_name = frappe.get_doc("TSAI Invoice",doc.name)
    children = doc_name.invoice_items
    cgst = 0
    count = 0
    sgst = 0
    igst = 0
    for c in children:
        cgst += c.cgst
        count += 1
        sgst += c.sgst
        igst += c.igst
    tot_cgst = cgst/count
    tot_sgst = sgst/count
    tot_igst = igst/count
    if doc.igst > 0 :
        igst_amount = float(tot_igst / 100) * float(doc.total_basic_amount)
        tot_amount = igst_amount + doc.total_basic_amount
        frappe.db.set_value("TSAI Invoice",doc.name,"total_invoice_amount",tot_amount)
    else:
        total_gst_amount = (tot_cgst / 100) * 2
        grand_total_gst = ((float(doc.total_basic_amount) * (total_gst_amount)))
        tot_amount = (grand_total_gst + doc.total_basic_amount)
        frappe.db.set_value("TSAI Invoice",doc.name,"cgst",tot_cgst)
        frappe.db.set_value("TSAI Invoice",doc.name,"sgst",tot_sgst)
        frappe.db.set_value("TSAI Invoice",doc.name,"total_gst_amount",grand_total_gst)
        frappe.db.set_value("TSAI Invoice",doc.name,"total_invoice_amount",tot_amount)
