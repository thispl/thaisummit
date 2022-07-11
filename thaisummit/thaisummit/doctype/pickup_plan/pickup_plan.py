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
from frappe.model.document import Document
from frappe.utils import (
    flt,
    cint,
    cstr,
    get_html_format,
    get_url_to_form,
    gzip_decompress,
    format_duration,
)

class PickupPlan(Document):
    @frappe.whitelist()
    def get_pickup_plan(self):
        table = """<table class='table table-bordered=1'>
        <tr>
            <td style="background-color:#ffedcc; padding:2px; border: 1px solid black; font-size:15px;">
                <center><b>S.No</b></center>
            </td>
            <td style="background-color:#ffedcc; padding:2px; border: 1px solid black; font-size:15px;">
                <center><b>Mat No</b></center>
            </td>
            <td style="background-color:#ffedcc; padding:2px; border: 1px solid black; font-size:15px;">
                <center><b>Part No</b></center>
            </td>
            <td style="background-color:#ffedcc; padding:2px; border: 1px solid black; font-size:15px;">
                <center><b>Part Name</b></center>
            </td>
            <td style="background-color:#ffedcc; padding:2px; border: 1px solid black; font-size:15px;">
                <center><b>Model</b></center>
            </td>
            <td style="background-color:#ffedcc; padding:2px; border: 1px solid black; font-size:15px;">
                <center><b>Packing Std</b></center>
            </td>
        """
        for i in range(8):
            dt = datetime.strptime(add_days(today(),i),'%Y-%m-%d')
            table += """ <td style="background-color:#ffedcc; padding:2px; border: 1px solid black; font-size:15px;" nowrap>
                <center><b>%s</b></center>
            </td> """%(datetime.strftime(dt,'%d-%b'))
        table += "</tr>"

        supplier_code = frappe.db.get_value(
        'TSAI Supplier', {'email': frappe.session.user}, 'name')
        if supplier_code:
            url = "http://172.16.1.18/StockDetail/Service1.svc/GetPOLineDetails"
            date = datetime.strptime(today(), '%Y-%m-%d')
            date = datetime.strftime(date, "%Y%m%d")
            payload = json.dumps({
                "Fromdate": "",
                "Todate": "",
                "SupplierCode": supplier_code,
                "DeliveryDate": date,
            })
            headers = {
                'Content-Type': 'application/json'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            try:
                pos = json.loads(response.text)
            except:
                frappe.msgprint("Unable to display Pickup Plan due to API Issue")

        x = 1
        if pos:
            for po in pos:
                if po['Po_Status'] == 'O':
                    if frappe.db.exists('TSAI Part Master',po['Mat_No']):
                        pr_name = frappe.db.get_value('Prepared Report',{'report_name':'Supplier Daily Order','status':'Completed'},'name')
                        attached_file_name = frappe.db.get_value(
                            "File",
                            {"attached_to_doctype": 'Prepared Report', "attached_to_name": pr_name},
                            "name",
                        )
                        attached_file = frappe.get_doc("File", attached_file_name)
                        compressed_content = attached_file.get_content()
                        uncompressed_content = gzip_decompress(compressed_content)
                        dos = json.loads(uncompressed_content.decode("utf-8"))

                        max_qty = 0
                        for do in dos:
                            if do['item'] == po['Mat_No']:
                                max_qty = do['max_qty']

                        open_qty = float(po['Open_Qty'])
                        in_transit_qty = 0

                        url = "http://172.16.1.18/StockDetail/Service1.svc/GetItemInventory"
                        payload = json.dumps({
                        "ItemCode": po['Mat_No']
                        })
                        headers = {
                        'Content-Type': 'application/json'
                        }
                        response = requests.request("POST", url, headers=headers, data=payload)
                        stock = 0
                        if response:
                            stocks = json.loads(response.text)
                            if stocks:
                                ica = frappe.db.sql("select warehouse from `tabInventory Control Area` where invoice_key = 'Y' ",as_dict=True)

                                wh_list = [d['warehouse'] for d in ica if 'warehouse' in d]

                                df = pd.DataFrame(stocks)
                                df = df[df['Warehouse'].isin(wh_list)]
                                stock = pd.to_numeric(df["Qty"]).sum()

                        t_qty = stock+in_transit_qty
                        req_qty = '-'
                        packing_std = frappe.db.get_value(
                            "TSAI Part Master", po['Mat_No'], 'packing_std')
                        model = frappe.db.get_value(
                            "TSAI Part Master", po['Mat_No'], 'model')
                        share = frappe.db.get_value('Shares of Business Entry',{'supplier_code':supplier_code,'mat_no':po['Mat_No']},'share_of_business') or '-'
                        if open_qty > 0:
                            if t_qty < max_qty:
                                if share != '-' :
                                    req_qty = ((math.floor(
                                    (max_qty - t_qty)/packing_std)*packing_std)*share)/100
                                else:
                                    try:
                                        req_qty = math.floor(
                                        (max_qty - t_qty)/packing_std)*packing_std
                                    except:
                                        req_qty = 0
                                if req_qty == 0:
                                    req_qty = '-'
                        
                        row = """<tr>
                                <td style="border: 1px solid black; font-size:13px;">%s</td>
                                <td style="border: 1px solid black; font-size:13px;">%s</td>
                                <td style="border: 1px solid black; font-size:13px;">%s</td>
                                <td style="border: 1px solid black; font-size:13px;">%s</td>
                                <td style="border: 1px solid black; font-size:13px;">%s</td>
                                <td style="border: 1px solid black; font-size:13px;"><center>%s</center></td>
                                <td style="border: 1px solid black; font-size:13px;"><center>%s</center></td>
                        """%(x,po['Mat_No'],po['Part_No'],po['Part_Name'],model,packing_std,req_qty)
                        x += 1
                        for do in dos:
                            if do['item'] == po['Mat_No']:
                                tomorrow = add_days(today(),1)
                                for i in range(7):
                                    dt = datetime.strptime(add_days(tomorrow,i),'%Y-%m-%d')
                                    day = datetime.strftime(dt,'%d')
                                    month = datetime.strftime(dt,'%b')
                                    qty = do[day+'_'+month.lower()]
                                    if qty == 0:
                                        qty = '-'
                                    row += '<td style="border: 1px solid black; font-size:13px;"><center>%s</center></td>'%qty
                        row += '</tr>'
                        table += row
            table += '</table>'
            return table




@frappe.whitelist()
def download_excel():
    data = []
    supplier_code = frappe.db.get_value(
        'TSAI Supplier', {'email': frappe.session.user}, 'name')
    if supplier_code:
        url = "http://172.16.1.18/StockDetail/Service1.svc/GetPOLineDetails"
        date = datetime.strptime(today(), '%Y-%m-%d')
        date = datetime.strftime(date, "%Y%m%d")
        payload = json.dumps({
            "Fromdate": "",
            "Todate": "",
            "SupplierCode": supplier_code,
            "DeliveryDate": date,
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        pos = json.loads(response.text)

    x = 0
    for po in pos:
        if po['Po_Status'] == 'O':
            x += 1
            if frappe.db.exists('TSAI Part Master',po['Mat_No']):
                pr_name = frappe.db.get_value('Prepared Report',{'report_name':'Supplier Daily Order','status':'Completed'},'name')
                attached_file_name = frappe.db.get_value(
                    "File",
                    {"attached_to_doctype": 'Prepared Report', "attached_to_name": pr_name},
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

                # pol_qty = frappe.db.get_value('PO Ledger',{'tsai_po':po.name},['sum(key_qty)']) or 0
                # open_qty = po.po_qty - pol_qty
                open_qty = float(po['Open_Qty'])
                in_transit_qty = 0

                url = "http://172.16.1.18/StockDetail/Service1.svc/GetItemInventory"
                payload = json.dumps({
                "ItemCode": po['Mat_No']
                })
                headers = {
                'Content-Type': 'application/json'
                }
                response = requests.request("POST", url, headers=headers, data=payload)
                stock = 0
                if response:
                    stocks = json.loads(response.text)
                    ica = frappe.db.sql("select warehouse from `tabInventory Control Area` where invoice_key = 'Y' ",as_dict=True)

                    wh_list = [d['warehouse'] for d in ica if 'warehouse' in d]

                    df = pd.DataFrame(stocks)
                    df = df[df['Warehouse'].isin(wh_list)]
                    stock = pd.to_numeric(df["Qty"]).sum()

                t_qty = stock+in_transit_qty
                req_qty = 0
                packing_std = frappe.db.get_value(
                    "TSAI Part Master", po['Mat_No'], 'packing_std')
                model = frappe.db.get_value(
                    "TSAI Part Master", po['Mat_No'], 'model')
                share = frappe.db.get_value('Shares of Business Entry',{'supplier_code':supplier_code,'mat_no':po['Mat_No']},'share_of_business') or '-'
                if open_qty > 0:
                    if t_qty < max_qty:
                        if share != '-' :
                            req_qty = ((math.floor(
                            (max_qty - t_qty)/packing_std)*packing_std)*share)/100
                        else:
                            try:
                                req_qty = math.floor(
                                (max_qty - t_qty)/packing_std)*packing_std
                            except:
                                req_qty = 0
                
                row = [po['Mat_No'],po['Part_No'],po['Part_Name'],model,packing_std,req_qty]
                for do in dos:
                    if do['item'] == po['Mat_No']:
                        tomorrow = add_days(today(),1)
                        for i in range(7):
                            dt = datetime.strptime(add_days(tomorrow,i),'%Y-%m-%d')
                            day = datetime.strftime(dt,'%d')
                            month = datetime.strftime(dt,'%b')
                            qty = do[day+'_'+month.lower()]
                            row.append(qty)
                data.append(row)

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

    cols = ["MAT No", "Part No", "Part Name", "Model","Packing Std"]
    for i in range(8):
            dt = datetime.strptime(add_days(today(),i),'%Y-%m-%d')
            cols.append(datetime.strftime(dt,'%d-%b'))
    ws.append(cols)

    for row in data:
        ws.append(row)

    ws.sheet_view.zoomScale = 80

    xlsx_file = BytesIO()
    wb.save(xlsx_file)
    return xlsx_file