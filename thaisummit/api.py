import frappe
import json
from frappe.utils import add_days,today,nowdate
import requests
import pandas as pd
from frappe.utils.background_jobs import enqueue
import datetime
from datetime import datetime
from frappe.desk.query_report import background_enqueue_run

def fetch_ekanban_stock():
    frappe.db.sql("delete from `tabTSAI Stock`")
    url = "http://182.156.241.14/StockDetail/Service1.svc/GetItemInventory"
    payload = json.dumps({
    "ItemCode":""
    })
    headers = {
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    stocks = json.loads(response.text)
    if stocks:
        for ss in stocks:
            stk = frappe.new_doc("TSAI Stock")
            stk.update({
            "item_no" : ss['Item_No'],
            "part_no" : ss['Part_No'],
            "item_name" : ss['Item_Name'],
            "qty" : ss['Qty'],
            "amount" : ss['Amount'],
            "wh" : ss['Warehouse'],
            })
            stk.save(ignore_permissions=True)
            frappe.db.commit()


def fetch_ekanban_po():
    url = "http://182.156.241.14/StockDetail/Service1.svc/GetPOLineDetails"
    # from_date = str(add_days(today(),-1)).replace('-','')
    today = str(nowdate()).replace('-','')
    print(today)
    # from_date = '20211201'
    # to_date = '20220207'
    payload = json.dumps({
        "Fromdate": "",
        "Todate": "",
        "DeliveryDate": today,
        "SupplierCode":""
        })
    headers = {
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    pos = json.loads(response.text)
    print(len(pos))
    if pos:
        frappe.db.sql("delete from `tabTSAI PO` ")
        for p in pos:
            # print(p)
            po_date = pd.to_datetime(p['Po_Date']).date()
            delivery_date = pd.to_datetime(p['Delivery_Date']).date()
            existing_po = frappe.db.exists("TSAI PO",{'po_no':p['PoNo'],'mat_no':p['Mat_No'],'po_date':po_date,'supplier_name':p['Supplier_name']})
            po_qty = 0
            if existing_po:
                po_qty = frappe.db.get_value('TSAI PO',existing_po,'po_qty') or 0
                frappe.db.set_value('TSAI PO',existing_po,'po_qty',float(po_qty) + float(p['Po_Qty']))
            else:
                po = frappe.new_doc("TSAI PO")
                po.update({
                "mat_no" : p['Mat_No'],
                "parts_no" : p['Part_No'],
                "parts_name" : p['Part_Name'],
                "po_no" : p['PoNo'],
                "po_date" : po_date,
                "delivery_date" : delivery_date,
                "supplier_name" : p['Supplier_name'],
                "po_qty" : p['Po_Qty'],
                "po_status" : p['Po_Status'],
                "uom" : p['Uom'],
                "unit_price" : p['Unit_Pice'],
                })
                po.save(ignore_permissions=True)
                frappe.db.commit()



def enqueue_fetch_ekanban_bom():
    enqueue(fetch_ekanban_bom, queue='default', timeout=6000, event='fetch_ekanban_bom')

@frappe.whitelist()
def fetch_ekanban_bom():
    frappe.db.sql("delete from `tabTSAI BOM`")
    url = "http://182.156.241.14/StockDetail/Service1.svc/GetBOMDetails"
    payload = json.dumps({
    "ItemCode":"",
    })
    headers = {
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    bom_details = json.loads(response.text)
    for bom in bom_details:
        doc = frappe.new_doc("TSAI BOM")
        doc.item = bom["Item"]
        doc.item_description = bom["ItemDescription"]
        doc.uom = bom["UOM"]
        doc.item_quantity = bom["Quantity"]
        doc.whse = bom["Whse"]
        doc.price = bom["Price"]
        doc.depth = bom["Depth"]
        doc.bom_type = bom["BOMType"]
        doc.fm = bom["FG"]
        doc.save(ignore_permissions=True)
        frappe.db.commit()

@frappe.whitelist(allow_guest=True)
def test_api(**args):
    frappe.log_error(title='ESSL',message=args)
    return "Checkin Marked"

@frappe.whitelist(allow_guest=True)
def mark_checkin(**args):
    time = pd.to_datetime(args['time']).replace(second=0)
    frappe.log_error(title='time',message=[time,args['employee'].upper()])
    if frappe.db.exists("Employee",args['employee'].upper()):
        if not frappe.db.exists('Employee Checkin',{'employee':args['employee'].upper(),'time':time}):
            deviceid = int(args['deviceid'])
            if (deviceid % 2) == 0:
                log_type = 'OUT'
            else:
                log_type = 'IN'
            try:
                ec = frappe.new_doc('Employee Checkin')
                ec.employee = args['employee'].upper()
                ec.time = time
                ec.log_type = log_type
                ec.device_id = args['deviceid']
                ec.save(ignore_permissions=True)
                frappe.db.commit()
                return "Checkin Marked"
            except:
                frappe.log_error(title="checkin error",message=args)
                return "Checkin Marked"
        else:
            return "Checkin Marked"
    else:
        frappe.log_error(title="checkin error no emp",message=args)
        return "No Emp"

def generate_daily_order():
    report_name = "Daily Order"
    filters = "{}"
    background_enqueue_run(report_name, filters)


@frappe.whitelist(allow_guest=True)
def test_checkin():
    args = {'employee': '1234', 'time': '20220122082831', 'deviceid': '1', 'cmd': 'thaisummit.api.mark_checkin'}
    time = pd.to_datetime(args['time']).replace(second=0)
    print(time)
    # if frappe.db.exists("Employee",args['employee'].upper()):
    #     if not frappe.db.exists('Employee Checkin',{'employee':args['employee'].upper(),'time':time}):
    #         deviceid = int(args['deviceid'])
    #         if (deviceid % 2) == 0:
    #             log_type = 'OUT'
    #         else:
    #             log_type = 'IN'
    #         ec = frappe.new_doc('Employee Checkin')
    #         ec.employee = args['employee'].upper()
    #         ec.time = time
    #         ec.log_type = log_type
    #         ec.device_id = args['deviceid']
    #         ec.save(ignore_permissions=True)
    #         frappe.db.commit()

@frappe.whitelist()
def test_scheduler():
    frappe.log_error(title="Test Scheduler",message="Test Scheduler type")