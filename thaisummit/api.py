import frappe
import json
from frappe.utils import add_days, today, nowdate
import requests
import pandas as pd
from frappe.utils.background_jobs import enqueue
from frappe.utils import cstr, add_days, date_diff, getdate, today
import datetime
from datetime import datetime
from frappe.desk.query_report import background_enqueue_run


def fetch_ekanban_stock():
    frappe.db.sql("delete from `tabTSAI Stock`")
    url = "http://172.16.1.18/StockDetail/Service1.svc/GetItemInventory"
    payload = json.dumps({
        "ItemCode": ""
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
                "item_no": ss['Item_No'],
                "part_no": ss['Part_No'],
                "item_name": ss['Item_Name'],
                "qty": ss['Qty'],
                "amount": ss['Amount'],
                "wh": ss['Warehouse'],
            })
            stk.save(ignore_permissions=True)
            frappe.db.commit()


def fetch_ekanban_po():
    url = "http://172.16.1.18/StockDetail/Service1.svc/GetPOLineDetails"
    # from_date = str(add_days(today(),-1)).replace('-','')
    today = str(nowdate()).replace('-', '')
    print(today)
    # from_date = '20211201'
    # to_date = '20220207'
    payload = json.dumps({
        "Fromdate": "",
        "Todate": "",
        "DeliveryDate": today,
        "SupplierCode": ""
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    pos = json.loads(response.text)
    print(response)
    if pos:
        frappe.db.sql(
            "delete from `tabTSAI PO` where plan_date = '%s' " % nowdate())
        for p in pos:
            # print(p)
            po_date = pd.to_datetime(p['Po_Date']).date()
            delivery_date = pd.to_datetime(p['Delivery_Date']).date()
            # existing_po = frappe.db.exists("TSAI PO",{'po_no':p['PoNo'],'mat_no':p['Mat_No'],'po_date':po_date,'supplier_name':p['Supplier_name']})
            # po_qty = 0
            # if existing_po:
            #     po_qty = frappe.db.get_value('TSAI PO',existing_po,'po_qty') or 0
            #     frappe.db.set_value('TSAI PO',existing_po,'po_qty',float(po_qty) + float(p['Po_Qty']))
            # else:
            po = frappe.new_doc("TSAI PO")
            po.update({
                "mat_no": p['Mat_No'],
                "parts_no": p['Part_No'],
                "parts_name": p['Part_Name'],
                "po_no": p['PoNo'],
                "po_date": po_date,
                "plan_date": nowdate(),
                "delivery_date": delivery_date,
                "supplier_name": p['Supplier_name'],
                "po_qty": p['Po_Qty'],
                "open_qty": p['Open_Qty'],
                "po_status": p['Po_Status'],
                "uom": p['Uom'],
                "unit_price": p['Unit_Pice'],
                "hsn_code":p['HSN_code'],
                "packing_std": frappe.db.get_value("TSAI Part Master", p['Mat_No'], 'packing_std'),
                "cgst":p['CGST'],
                "sgst":p['SGST'],
                "igst":p['IGST']
            })
            po.save(ignore_permissions=True)
            frappe.db.commit()


def enqueue_fetch_ekanban_bom():
    enqueue(fetch_ekanban_bom, queue='default',
            timeout=6000, event='fetch_ekanban_bom')


@frappe.whitelist()
def fetch_ekanban_bom():
    frappe.db.sql("delete from `tabTSAI BOM`")
    url = "http://172.16.1.18/StockDetail/Service1.svc/GetBOMDetails"
    payload = json.dumps({
        "ItemCode": "",
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
    frappe.log_error(title='ESSL', message=args)
    return "Checkin Marked"


@frappe.whitelist(allow_guest=True)
def mark_checkin(**args):
    time = pd.to_datetime(args['time']).replace(second=0)
    frappe.log_error(title='time', message=[time, args['employee'].upper()])
    if frappe.db.exists("Employee", args['employee'].upper()):
        if not frappe.db.exists('Employee Checkin', {'employee': args['employee'].upper(), 'time': time}):
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
                frappe.log_error(title="checkin error", message=args)
                return "Checkin Marked"
        else:
            return "Checkin Marked"
    else:
        frappe.log_error(title="checkin error no emp", message=args)
        return "No Emp"


def generate_daily_order():
    report_name = "Supplier Daily Order"
    filters = "{}"
    background_enqueue_run(report_name, filters)

def generate_production_daily_order():
    report_name = "Production Daily Order"
    filters = "{}"
    background_enqueue_run(report_name, filters)


@frappe.whitelist(allow_guest=True)
def test_checkin():
    args = {'employee': '1234', 'time': '20220122082831',
            'deviceid': '1', 'cmd': 'thaisummit.api.mark_checkin'}
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
def fetch_grn_details_8am():
    invs = frappe.db.sql("""select `tabInvoice Items`.mat_no as mat_no, `tabTSAI Invoice`.name as name, `tabTSAI Invoice`.po_no from `tabTSAI Invoice`
    left join `tabInvoice Items` on `tabTSAI Invoice`.name = `tabInvoice Items`.parent where `tabInvoice Items`.grn = 0 """, as_dict=True)
    for inv in invs:
        print(inv)
        url = "http://172.16.1.18/StockDetail/Service1.svc/GetPODetails"
        payload = json.dumps({
            "Fromdate": "", "Todate": "", "MatNo": inv.mat_no, "PONO": inv.po_no
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request(
            "POST", url, headers=headers, data=payload)
        grns = json.loads(response.text)
        for grn in grns:
            if grn['NumAtCard'] == inv.name:
                doc = frappe.get_doc('TSAI Invoice', inv.name)
                for d in doc.invoice_items:
                    if d.mat_no == inv.mat_no:
                        d.grn = 1
                        d.grn_qty = grn["GrnQty"]
                        d.grn_date = pd.to_datetime(grn["GrnDate"]).date()
                        d.grn_no = grn["GrnNo"]
                doc.save(ignore_permissions=True)
                frappe.db.commit()


@frappe.whitelist()
def fetch_grn_details_1am():
    invs = frappe.db.sql("""select `tabInvoice Items`.mat_no as mat_no, `tabTSAI Invoice`.name as name, `tabTSAI Invoice`.po_no from `tabTSAI Invoice`
    left join `tabInvoice Items` on `tabTSAI Invoice`.name = `tabInvoice Items`.parent where `tabInvoice Items`.grn = 0 """, as_dict=True)
    for inv in invs:
        print(inv)
        url = "http://172.16.1.18/StockDetail/Service1.svc/GetPODetails"
        payload = json.dumps({
            "Fromdate": "", "Todate": "", "MatNo": inv.mat_no, "PONO": inv.po_no
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request(
            "POST", url, headers=headers, data=payload)
        grns = json.loads(response.text)
        for grn in grns:
            if grn['NumAtCard'] == inv.name:
                doc = frappe.get_doc('TSAI Invoice', inv.name)
                for d in doc.invoice_items:
                    if d.mat_no == inv.mat_no:
                        d.grn = 1
                        d.grn_qty = grn["GrnQty"]
                        d.grn_date = pd.to_datetime(grn["GrnDate"]).date()
                        d.grn_no = grn["GrnNo"]
                doc.save(ignore_permissions=True)
                frappe.db.commit()


# def test_method():
#     grns = [
#         ["HEM/21-22/3798", "31000485", "700", "40041", "3/29/2022", ],
#         ["M0006212203579", "38300026", "1200", "39893", "3/28/2022", ],
#         ["M0006212203579", "32300068", "900", "39893", "3/28/2022", ],
#         ["M0006212203579", "38300033", "800", "39893", "3/28/2022", ],
#         ["M0006212203579", "31000487", "400", "39893", "3/28/2022", ],
#         ["M0006212203579", "31000488", "200", "39893", "3/28/2022", ],
#         ["M0006212203587", "32300068", "600", "39906", "3/28/2022", ],
#         ["M0006212203587", "38300033", "1200", "39906", "3/28/2022", ],
#         ["M0006212203587", "32300064", "600", "39906", "3/28/2022", ],
#         ["M0006212203587", "32000042", "300", "39906", "3/28/2022", ],
#         ["M0006212203587", "33000060", "800", "39906", "3/28/2022", ],
#         ["M0006212203587", "38300026", "300", "39906", "3/28/2022", ],
#         ["M0006212203592", "31100036", "650", "39984", "3/28/2022", ],
#         ["M0006212203598", "31100047", "1000", "40089", "3/29/2022", ],
#         ["M0006212203598", "31100044", "500", "40089", "3/29/2022", ],
#         ["M00092122002085", "31000100", "200", "39772", "3/25/2022", ],
#         ["M00092122002085", "31100260", "300", "39772", "3/25/2022", ],
#         ["M00092122002085", "38300017", "1200", "39772", "3/25/2022", ],
#         ["M00092122002085", "38300014", "1500", "39772", "3/25/2022", ],
#         ["M00092122002085", "38300010", "2000", "39772", "3/25/2022", ],
#         ["M0009212202091", "38300018", "1000", "39961", "3/28/2022", ],
#         ["M0009212202091", "31000387", "400", "39961", "3/28/2022", ],
#         ["M0009212202091", "31000412", "500", "39961", "3/28/2022", ],
#         ["M0009212202091", "31000385", "900", "39961", "3/28/2022", ],
#         ["M00472122001363", "32000045", "200", "39996", "3/29/2022", ],
#         ["M00472122001363", "38300046", "800", "39996", "3/29/2022", ],
#         ["N0016212204120", "35000005", "250", "40299", "3/31/2022", ],
#         ["N0016212204120", "35000070", "250", "40299", "3/31/2022", ],
#         ["N0016212204120", "35000007", "250", "40299", "3/31/2022", ],
#         ["N0016212204120", "35000014", "200", "40299", "3/31/2022", ],
#         ["N0016212204120", "35000003", "200", "40299", "3/31/2022", ],
#         ["N0016212204123", "35000070", "500", "40300", "3/31/2022", ],
#         ["N0016212204123", "35000014", "600", "40300", "3/31/2022", ],
#     ]
#     for grn in grns:
#         print(grn[0])
#         doc = frappe.get_doc('TSAI Invoice', grn[0])
#         for d in doc.invoice_items:
#             print(d.mat_no)
#             print(grn[1])
#             print('---------')
#             if int(d.mat_no) == int(grn[1]):
#                 print('hi')
#                 # print(grn[2])
#                 date = pd.to_datetime(grn[4]).date()
#                 print(date)
#                 d.grn = 1
#                 d.grn_qty = grn[2]
#                 d.grn_date = date
#                 d.grn_no = grn[3]
#         doc.save(ignore_permissions=True)
#         frappe.db.commit()
