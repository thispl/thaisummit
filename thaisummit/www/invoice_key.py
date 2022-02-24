from __future__ import unicode_literals
from ast import get_source_segment
from doctest import DocTestFailure
from email import message
import math
import frappe
from frappe.utils import today, flt, cint, getdate, get_datetime
from datetime import timedelta, datetime
from frappe.utils import cstr, add_days, date_diff, getdate, today
import json
import requests
import pandas as pd
import openpyxl
from six import BytesIO
from frappe.utils import (
    flt,
    cint,
    cstr,
    get_html_format,
    get_url_to_form,
    gzip_decompress,
    format_duration,
)


@frappe.whitelist()
def get_data():
    # if 'System Manager' not in frappe.get_roles(frappe.session.user):
    #     if 'Supplier' in frappe.get_roles(frappe.session.user):
    # supplier_code = ''
    # if 'System Manager' not in frappe.get_roles(frappe.session.user):
    supplier_code = frappe.db.get_value(
        'TSAI Supplier', {'user': frappe.session.user}, 'user_name')
    if supplier_code:
        url = "http://182.156.241.14/StockDetail/Service1.svc/GetPOLineDetails"
        date = datetime.strptime(today(), '%Y-%m-%d')
        date = datetime.strftime(date, "%Y%m%d")
        payload = json.dumps({
            "Fromdate": "",
            "Todate": "",
            "SupplierCode": supplier_code,
            "DeliveryDate": date
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        pos = json.loads(response.text)
        data = []
        for po in pos:
            if frappe.db.exists('TSAI Part Master', po['Mat_No']):
                pr_name = frappe.db.get_value(
                    'Prepared Report', {'report_name': 'Daily Order'}, 'name')
                attached_file_name = frappe.db.get_value(
                    "File",
                    {"attached_to_doctype": 'Prepared Report',
                        "attached_to_name": pr_name},
                    "name",
                )
                attached_file = frappe.get_doc("File", attached_file_name)
                compressed_content = attached_file.get_content()
                uncompressed_content = gzip_decompress(compressed_content)
                dos = json.loads(uncompressed_content.decode("utf-8"))

                daily_order = 0
                min_qty = 0
                max_qty = 0
                for do in dos:
                    if do['item'] == po['Mat_No']:
                        daily_order = do['daily_order']
                        min_qty = do['min_qty']
                        max_qty = do['max_qty']

                in_transit_qty = 0

                url = "http://182.156.241.14/StockDetail/Service1.svc/GetItemInventory"
                payload = json.dumps({
                    "ItemCode": po['Mat_No']
                })
                headers = {
                    'Content-Type': 'application/json'
                }
                response = requests.request(
                    "POST", url, headers=headers, data=payload)
                stock = 0
                if response:
                    stocks = json.loads(response.text)
                    ica = frappe.db.sql(
                        "select warehouse from `tabInventory Control Area` where invoice_key = 'Y' ", as_dict=True)

                    wh_list = [d['warehouse'] for d in ica if 'warehouse' in d]

                    df = pd.DataFrame(stocks)
                    df = df[df['Warehouse'].isin(wh_list)]
                    stock = pd.to_numeric(df["Qty"]).sum()

                t_qty = stock+in_transit_qty
                req_qty = 0
                open_qty = float(po['Open_Qty'])
                packing_std = frappe.db.get_value(
                    "TSAI Part Master", po['Mat_No'], 'packing_std')
                po_date = pd.to_datetime(po['Po_Date']).date()
                delivery_date = pd.to_datetime(po['Delivery_Date']).date()
                if open_qty > 0:
                    if t_qty < max_qty:
                        grn_qty = frappe.db.sql("""select sum(`tabInvoice Items`.key_qty) as key_qty from `tabTSAI Invoice`
                        left join `tabInvoice Items` on `tabTSAI Invoice`.name = `tabInvoice Items`.parent
                        where `tabTSAI Invoice`.po_no = '%s' and `tabInvoice Items`.mat_no = '%s' """ % (po['PoNo'], po['Mat_No']), as_dict=True)[0].key_qty or 0
                        req_qty = math.floor((max_qty - t_qty - grn_qty)/packing_std)*packing_std
                data.append([po['Mat_No'], po['Part_No'], po['Part_Name'], po['PoNo'], po_date, delivery_date, po['Supplier_name'], po['Uom'], round(float(po['Unit_Pice']), 2), round(float(po['Po_Qty'])), open_qty, round(
                    (open_qty/float(po['Po_Qty']))*100), packing_std, daily_order, max_qty, min_qty, stock, in_transit_qty, t_qty, req_qty, '', '', float(po['GSTPercentage']), '', ''])
    return data

# @frappe.whitelist()
# def validate_data(table):
#     table = json.loads(table)
#     errlist = ''
#     for row in table:
#         if float(row[21]['content'] or 0) > float(row[20]['content']):
#             errlist += "Key Qty cannot be greater than Req Qty in row no. %s \n"%row[0]['content']
#         if not (float(row[21]['content'] or 0) / float(row[13]['content'])).is_integer():
#             errlist += "Key Qty of row no. %s is not in Packing Standard \n"%row[0]['content']
#     if errlist:
#         return errlist, 'err'

#     res = []
#     for row in table:
#         up = 0
#         key_qty = 0
#         if row[9]['content'] and row[21]['content']:
#             up = float(row[9]['content'])
#             key_qty = float(row[21]['content'])
#         basic_amount = round(up * key_qty,2)
#         gst_amount = 0
#         invoice_amount = basic_amount + gst_amount
#         res.append([row[1]['content'],row[2]['content'],row[3]['content'],row[4]['content'],row[5]['content'],row[6]['content'],row[7]['content'],row[8]['content'],row[9]['content'],row[10]['content'],row[11]['content'],row[12]['content'],row[13]['content'],row[14]['content'],row[15]['content'],row[16]['content'],row[17]['content'],row[18]['content'],row[19]['content'],row[20]['content'],row[21]['content'],basic_amount,gst_amount,invoice_amount,row[25]['content']])
#     return res, 'ok'


@frappe.whitelist()
def submit_po(table, qr_code, irn_no, invoice_no):
    table = json.loads(table)
    supplier_code = frappe.db.get_value(
        'TSAI Supplier', {'user': frappe.session.user}, 'user_name')

    inv = frappe.new_doc('TSAI Invoice')
    inv.po_no = table[0][4]['content']
    inv.po_date = table[0][5]['content']
    inv.qr_code = qr_code
    inv.irn_no = irn_no
    inv.invoice_no = invoice_no
    inv.invoice_date = today()
    inv.supplier_code = supplier_code
    total_qty = 0
    total_basic = 0
    total_gst_amount = 0
    total_invoice_amount = 0
    for row in table:
        if row[21]['content'] and row[22]['content']:
            total_qty += int(row[21]['content'])
            total_basic += int(row[22]['content'])
            total_gst_amount += int(row[24]['content'])
            total_invoice_amount += int(row[25]['content'])
            inv.append('invoice_items', {
                'mat_no': row[1]['content'],
                'parts_no': row[2]['content'],
                'parts_name': row[3]['content'],
                'uom': row[8]['content'],
                'unit_price': row[9]['content'],
                'hsc_sac': '',
                'packing_standard': row[13]['content'],
                'key_qty': row[21]['content'],
                'basic_amount': row[22]['content'],
                'gst_percent': row[23]['content'],
                'gst_amount': row[24]['content'],
                'invoice_amount': row[25]['content']
            })
    inv.total_qty = total_qty
    inv.total_basic_amount = total_basic
    inv.gst_percentage = table[0][23]['content']
    inv.total_gst_amount = total_gst_amount
    inv.total_invoice_amount = total_invoice_amount
    inv.save(ignore_permissions=True)
    frappe.db.commit()
    return 'ok'


def get_dates(from_date, to_date):
    no_of_days = date_diff(add_days(to_date, 1), from_date)
    dates = [add_days(from_date, i) for i in range(0, no_of_days)]
    return dates


@frappe.whitelist()
def get_invoice_no():
    supplier_code = frappe.db.get_value(
        'TSAI Supplier', {'user': frappe.session.user}, 'user_name')
    inv_no = frappe.db.sql("select max(creation),name from `tabTSAI Invoice` where supplier_code = '%s' " %
                           supplier_code, as_dict=True)[0].name
    invoice_no = str(supplier_code) + "21220000" + str(int(inv_no[-5:])+1)
    return invoice_no


@frappe.whitelist()
def download_excel():
    supplier_code = frappe.db.get_value(
        'TSAI Supplier', {'user': frappe.session.user}, 'user_name')
    if supplier_code:
        url = "http://182.156.241.14/StockDetail/Service1.svc/GetPOLineDetails"
        date = datetime.strptime(today(), '%Y-%m-%d')
        date = datetime.strftime(date, "%Y%m%d")
        payload = json.dumps({
            "Fromdate": "",
            "Todate": "",
            "SupplierCode": supplier_code,
            "DeliveryDate": date
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        pos = json.loads(response.text)
        data = []
        for po in pos:
            if frappe.db.exists('TSAI Part Master', po['Mat_No']):
                pr_name = frappe.db.get_value(
                    'Prepared Report', {'report_name': 'Daily Order'}, 'name')
                attached_file_name = frappe.db.get_value(
                    "File",
                    {"attached_to_doctype": 'Prepared Report',
                        "attached_to_name": pr_name},
                    "name",
                )
                attached_file = frappe.get_doc("File", attached_file_name)
                compressed_content = attached_file.get_content()
                uncompressed_content = gzip_decompress(compressed_content)
                dos = json.loads(uncompressed_content.decode("utf-8"))

                daily_order = 0
                min_qty = 0
                max_qty = 0
                for do in dos:
                    if do['item'] == po['Mat_No']:
                        daily_order = do['daily_order']
                        min_qty = do['min_qty']
                        max_qty = do['max_qty']

                in_transit_qty = 0

                url = "http://182.156.241.14/StockDetail/Service1.svc/GetItemInventory"
                payload = json.dumps({
                    "ItemCode": po['Mat_No']
                })
                headers = {
                    'Content-Type': 'application/json'
                }
                response = requests.request(
                    "POST", url, headers=headers, data=payload)
                stock = 0
                if response:
                    stocks = json.loads(response.text)
                    ica = frappe.db.sql(
                        "select warehouse from `tabInventory Control Area` where invoice_key = 'Y' ", as_dict=True)

                    wh_list = [d['warehouse'] for d in ica if 'warehouse' in d]

                    df = pd.DataFrame(stocks)
                    df = df[df['Warehouse'].isin(wh_list)]
                    stock = pd.to_numeric(df["Qty"]).sum()

                t_qty = stock+in_transit_qty
                req_qty = 0
                open_qty = float(po['Open_Qty'])
                packing_std = frappe.db.get_value(
                    "TSAI Part Master", po['Mat_No'], 'packing_std')
                po_date = pd.to_datetime(po['Po_Date']).date()
                delivery_date = pd.to_datetime(po['Delivery_Date']).date()
                if open_qty > 0:
                    if t_qty < max_qty:
                        req_qty = math.floor(
                            (max_qty - t_qty)/packing_std)*packing_std
                data.append([po['Mat_No'], po['Part_No'], po['Part_Name'], po['PoNo'], po_date, delivery_date, po['Supplier_name'], po['Uom'], round(float(po['Unit_Pice']), 2), round(float(po['Po_Qty'])), open_qty, round(
                    (open_qty/float(po['Po_Qty']))*100), packing_std, daily_order, max_qty, min_qty, stock, in_transit_qty, t_qty, req_qty, '', '', float(po['GSTPercentage']), '', ''])

    xlsx_file = make_xlsx(data)
    frappe.response['filename'] = 'Invoice_Key.xlsx'
    frappe.response['filecontent'] = xlsx_file.getvalue()
    frappe.response['type'] = 'binary'


def make_xlsx(data, sheet_name=None, wb=None, column_widths=None):
    # args = frappe.local.form_dict
    column_widths = column_widths or []
    if wb is None:
        wb = openpyxl.Workbook()

    ws = wb.create_sheet(sheet_name, 0)

    cols = ["MAT No", "Parts No", "Parts Name", "PO No", "PO Date", "Delivery date", "Supplier Name", "UOM", "Unit Price", "PO Qty", "Open Qty", "%", "Packing",
            "Daily Order", "Max Qty", "Min Qty", "Stock Qty", "In transit Qty", "Total Qty", "Req Qty", "Key Qty", "Basic Amount", "GST %", "GST Amount", "Invoice Amount"]
    ws.append(cols)

    for row in data:
        ws.append(row)

    ws.sheet_view.zoomScale = 80

    xlsx_file = BytesIO()
    wb.save(xlsx_file)
    return xlsx_file


def get_stock(mat_no):
    url = "http://182.156.241.14/StockDetail/Service1.svc/GetItemInventory"
    payload = json.dumps({
        "ItemCode": mat_no
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    stocks = json.loads(response.text)
    ica = frappe.db.sql(
        "select warehouse from `tabInventory Control Area` where invoice_key = 'Y' ", as_dict=True)

    wh_list = [d['warehouse'] for d in ica if 'warehouse' in d]

    df = pd.DataFrame(stocks)
    df = df[df['Warehouse'].isin(wh_list)]
    stock = pd.to_numeric(df["Qty"]).sum()
    return stock


def test_do():
    pr_name = frappe.db.get_value(
        'Prepared Report', {'report_name': 'Daily Order'}, 'name')
    attached_file_name = frappe.db.get_value(
        "File",
        {"attached_to_doctype": 'Prepared Report', "attached_to_name": pr_name},
        "name",
    )
    attached_file = frappe.get_doc("File", attached_file_name)
    compressed_content = attached_file.get_content()
    uncompressed_content = gzip_decompress(compressed_content)
    dos = json.loads(uncompressed_content.decode("utf-8"))
    for do in dos:
        if do['item'] == '91100080':
            print(do)


def test_po():
    url = "http://182.156.241.14/StockDetail/Service1.svc/GetPOLineDetails"
    date = str(today()).replace('-', '')
    payload = json.dumps({
        "Fromdate": "",
        "Todate": "",
        "SupplierCode": "",
        "DeliveryDate": date
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    pos = json.loads(response.text)
    print(len(pos))
    # if pos:
    #     frappe.db.sql("delete from `tabTSAI PO`")
    #     for p in pos:
    #         po_date = pd.to_datetime(p['Po_Date']).date()
    #         delivery_date = pd.to_datetime(p['Delivery_Date']).date()
    #         po = frappe.new_doc("TSAI PO")
    #         po.update({
    #         "mat_no" : p['Mat_No'],
    #         "parts_no" : p['Part_No'],
    #         "parts_name" : p['Part_Name'],
    #         "po_no" : p['PoNo'],
    #         "po_date" : po_date,
    #         "delivery_date" : delivery_date,
    #         "supplier_name" : p['Supplier_name'],
    #         "po_qty" : p['Po_Qty'],
    #         "po_status" : p['Po_Status'],
    #         "uom" : p['Uom'],
    #         "unit_price" : p['Unit_Pice'],
    #         })
    #         po.save(ignore_permissions=True)
    #         frappe.db.commit()
