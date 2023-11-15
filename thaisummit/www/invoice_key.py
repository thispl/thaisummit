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

@frappe.whitelist(allow_guest=True)
def get_test_data():
    supplier_code = frappe.db.get_value(
        'TSAI Supplier', {'email': 'm0006@thaisummit.co.in'}, 'name')
    if supplier_code:
        url = "http://apioso.thaisummit.co.th:10401/api/POLineDetails"
        date = datetime.strptime(today(), '%Y-%m-%d')
        date = datetime.strftime(date, "%Y%m%d")
        payload = json.dumps({
            "Fromdate": "",
            "Todate": "",
            "SupplierCode": supplier_code,
            "DeliveryDate": date,
            # "DeliveryDate": '20220228'
        })
        headers = {
            'Content-Type': 'application/json',
            'API_KEY': '/1^i[#fhSSDnC8mHNTbg;h^uR7uZe#ninearin!g9D:pos+&terpTpdaJ$|7/QYups;==~w~!AWwb&DU'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        try:
            pos = json.loads(response.text)
        except :
            frappe.msgprint("Unable to display Invoice Key due to API Issue")
        data = []

        for po in pos:
            if frappe.db.exists('TSAI Part Master', po['Mat_No']):
                pr_name = frappe.db.get_value(
                    'Prepared Report', {'report_name': 'Supplier Daily Order','status':'Completed'}, 'name')
                attached_file_name = frappe.db.get_value(
                    "File",
                    {"attached_to_doctype": 'Prepared Report',
                        "attached_to_name": pr_name},
                    # {"attached_to_doctype": 'Prepared Report',
                    #     "attached_to_name": pr_name},
                    "name",
                )
                attached_file = frappe.get_doc("File", attached_file_name)
                compressed_content = attached_file.get_content()
                uncompressed_content = gzip_decompress(compressed_content)
                dos = json.loads(uncompressed_content.decode("utf-8"))
                
                daily_order = 0
                min_qty = 0
                max_qty = 0
                # for do in dos:
                #     if str(do['item']) == po['Mat_No']:
                #         daily_order = cint(do['daily_order'])
                #         min_qty = cint(do['min_qty'])
                #         max_qty = cint(do['max_qty'])
                # url = "http://apioso.thaisummit.co.th:10401/api/GetItemInventory"
                # payload = json.dumps({
                #     "ItemCode": po['Mat_No']
                # })
                # headers = {
                #     'Content-Type': 'application/json',
                #     'API_KEY': '/1^i[#fhSSDnC8mHNTbg;h^uR7uZe#ninearin!g9D:pos+&terpTpdaJ$|7/QYups;==~w~!AWwb&DU',
                # }
                # response = requests.request(
                #     "POST", url, headers=headers, data=payload)
                # stock = 0
                # if response:
                #     stocks = json.loads(response.text)
                #     if stocks:
                #         ica = frappe.db.sql(
                #             "select warehouse from `tabInventory Control Area` where invoice_key = 'Y' ", as_dict=True)

                #         wh_list = [d['warehouse'] for d in ica if 'warehouse' in d]
                #         df = pd.DataFrame(stocks)
                #         df = df[df['Warehouse'].isin(wh_list)]
                #         stock = pd.to_numeric(df["Qty"]).sum()

                # in_transit_qty_po = frappe.db.sql("""select sum(`tabInvoice Items`.key_qty) as key_qty from `tabTSAI Invoice`
                #         left join `tabInvoice Items` on `tabTSAI Invoice`.name = `tabInvoice Items`.parent
                #         where `tabTSAI Invoice`.status = 'OPEN' and `tabTSAI Invoice`.po_no = '%s' and `tabInvoice Items`.mat_no = '%s' and `tabTSAI Invoice`.supplier_code = '%s' and `tabInvoice Items`.grn = 0 """ % (po['PoNo'],po['Mat_No'],supplier_code), as_dict=True)[0].key_qty or 0

                # in_transit_qty = frappe.db.sql("""select sum(`tabInvoice Items`.key_qty) as key_qty from `tabTSAI Invoice`
                #         left join `tabInvoice Items` on `tabTSAI Invoice`.name = `tabInvoice Items`.parent
                #         where `tabTSAI Invoice`.status = 'OPEN' and `tabInvoice Items`.mat_no = '%s' and `tabTSAI Invoice`.supplier_code = '%s' and `tabInvoice Items`.grn = 0 """ % (po['Mat_No'],supplier_code), as_dict=True)[0].key_qty or 0
                # t_qty = stock + in_transit_qty
                # req_qty = 0
                # open_qty = float(po['Open_Qty'])
                # if open_qty > 0:
                #     open_percent = round((open_qty/float(po['Po_Qty']))*100)
                # else:
                #     open_percent = 0
                # packing_std = frappe.db.get_value(
                #     "TSAI Part Master", po['Mat_No'], 'packing_std')
                # po_date = pd.to_datetime(po['Po_Date']).date()
                # delivery_date = pd.to_datetime(po['Delivery_Date']).date()
                # share = frappe.db.get_value('Shares of Business Entry',{'supplier_code':supplier_code,'mat_no':po['Mat_No']},'share_of_business') or '-'
                # # if open_qty > 0:
                
                # if t_qty < min_qty:
                #     try:
                #         req_qty = math.ceil((max_qty - t_qty)/packing_std)*packing_std
                #     except:
                #         req_qty = 0
                #     if req_qty < 0:
                #         req_qty = 0
                
                # mrp_daily_order = frappe.db.get_value(
                #     "TSAI Part Master", po['Mat_No'], 'mrp_daily_order')
                # if open_qty > 0:
                #     if daily_order == 0:
                #         if t_qty == 0:
                #             try:
                #                 req_qty = math.ceil((mrp_daily_order * min_qty)/packing_std)*packing_std
                #             except:
                #                 req_qty = 0
                        # if open_qty < req_qty:
                        #     req_qty = math.floor(open_qty/packing_std)*packing_std
                        
                # data.append([po['Mat_No'], po['Part_No'], po['Part_Name'], po['PoNo'], po_date, delivery_date, po['Supplier_name'], po['Uom'], round(float(po['Unit_Pice']), 2), round(float(po['Po_Qty'])), open_qty, round(
                #     (open_qty/float(po['Po_Qty']))*100), packing_std, daily_order, share, max_qty, min_qty, stock, in_transit_qty, t_qty, req_qty, '', '', float(po['GSTPercentage']), '', ''])
                data.append([po['Mat_No'], po['Part_No'], po['Part_Name'],po['PoNo'],po['PoEntry'], po['Uom'],round(float(po['Unit_Pice']), 2),po['HSN_code'],'', '', float(po['CGST']),float(po['SGST']),float(po['IGST']), '', ''])
        return data


@frappe.whitelist()
def get_data():
    supplier_code = frappe.db.get_value(
        'TSAI Supplier', {'email': frappe.session.user}, 'name')
    if supplier_code:
        url = "http://apioso.thaisummit.co.th:10401/api/POLineDetails"
        date = datetime.strptime(today(), '%Y-%m-%d')
        date = datetime.strftime(date, "%Y%m%d")
        payload = json.dumps({
            "Fromdate": "",
            "Todate": "",
            "SupplierCode": supplier_code,
            "DeliveryDate": date,
            # "DeliveryDate": '20220228'
        })
        headers = {
            'Content-Type': 'application/json',
            'API_KEY': '/1^i[#fhSSDnC8mHNTbg;h^uR7uZe#ninearin!g9D:pos+&terpTpdaJ$|7/QYups;==~w~!AWwb&DU'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        pos = ''
        try:
            pos = json.loads(response.text)
        except :
            frappe.msgprint("Unable to display Invoice Key due to API Issue")
        data = []
        if pos:
            for po in pos:
                if frappe.db.exists('TSAI Part Master', po['Mat_No']):
                    pr_name = frappe.db.get_value(
                        'Prepared Report', {'report_name': 'Supplier Daily Order','status':'Completed'}, 'name')
                    attached_file_name = frappe.db.get_value(
                        "File",
                        {"attached_to_doctype": 'Prepared Report',
                            "attached_to_name": pr_name},
                        # {"attached_to_doctype": 'Prepared Report',
                        #     "attached_to_name": pr_name},
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
                        if str(do['item']) == po['Mat_No']:
                            daily_order = cint(do['daily_order'])
                            min_qty = cint(do['min_qty'])
                            max_qty = cint(do['max_qty'])
                    url = "http://apioso.thaisummit.co.th:10401/api/GetItemInventory"
                    payload = json.dumps({
                        "ItemCode": po['Mat_No']
                    })
                    headers = {
                        'Content-Type': 'application/json',
                        'API_KEY': '/1^i[#fhSSDnC8mHNTbg;h^uR7uZe#ninearin!g9D:pos+&terpTpdaJ$|7/QYups;==~w~!AWwb&DU',
                    }
                    response = requests.request(
                        "POST", url, headers=headers, data=payload)
                    stock = 0
                    if response:
                        stocks = json.loads(response.text)
                        if stocks:
                            ica = frappe.db.sql(
                                "select warehouse from `tabInventory Control Area` where invoice_key = 'Y' ", as_dict=True)

                            wh_list = [d['warehouse'] for d in ica if 'warehouse' in d]
                            df = pd.DataFrame(stocks)
                            df = df[df['Warehouse'].isin(wh_list)]
                            stock = pd.to_numeric(df["Qty"]).sum()

                    in_transit_qty_po = frappe.db.sql("""select sum(`tabInvoice Items`.key_qty) as key_qty from `tabTSAI Invoice`
                            left join `tabInvoice Items` on `tabTSAI Invoice`.name = `tabInvoice Items`.parent
                            where `tabTSAI Invoice`.status = 'OPEN' and `tabTSAI Invoice`.po_no = '%s' and `tabInvoice Items`.mat_no = '%s' and `tabTSAI Invoice`.supplier_code = '%s' and `tabInvoice Items`.grn = 0 """ % (po['PoNo'],po['Mat_No'],supplier_code), as_dict=True)[0].key_qty or 0

                    in_transit_qty = frappe.db.sql("""select sum(`tabInvoice Items`.key_qty) as key_qty from `tabTSAI Invoice`
                            left join `tabInvoice Items` on `tabTSAI Invoice`.name = `tabInvoice Items`.parent
                            where `tabTSAI Invoice`.status = 'OPEN' and `tabInvoice Items`.mat_no = '%s' and `tabTSAI Invoice`.supplier_code = '%s' and `tabInvoice Items`.grn = 0 """ % (po['Mat_No'],supplier_code), as_dict=True)[0].key_qty or 0
                    t_qty = stock + in_transit_qty
                    req_qty = 0
                    open_qty = float(po['Open_Qty'])
                    if open_qty > 0:
                        open_percent = round((open_qty/float(po['Po_Qty']))*100)
                    else:
                        open_percent = 0
                    packing_std = frappe.db.get_value(
                        "TSAI Part Master", po['Mat_No'], 'packing_std')
                    po_date = pd.to_datetime(po['Po_Date']).date()
                    delivery_date = pd.to_datetime(po['Delivery_Date']).date()
                    share = frappe.db.get_value('Shares of Business Entry',{'supplier_code':supplier_code,'mat_no':po['Mat_No']},'share_of_business') or '-'
                    # if open_qty > 0:
                    
                    if t_qty < min_qty:
                        try:
                            req_qty = math.ceil((max_qty - t_qty)/packing_std)*packing_std
                        except:
                            req_qty = 0
                        if req_qty < 0:
                            req_qty = 0
                    
                    mrp_daily_order = frappe.db.get_value(
                        "TSAI Part Master", po['Mat_No'], 'mrp_daily_order')
                    if open_qty > 0:
                        if daily_order == 0:
                            if t_qty == 0:
                                try:
                                    req_qty = math.ceil((mrp_daily_order * min_qty)/packing_std)*packing_std
                                except:
                                    req_qty = 0
                            # if open_qty < req_qty:
                            #     req_qty = math.floor(open_qty/packing_std)*packing_std
                            
                    # data.append([po['Mat_No'], po['Part_No'], po['Part_Name'], po['PoNo'], po_date, delivery_date, po['Supplier_name'], po['Uom'], round(float(po['Unit_Pice']), 2), round(float(po['Po_Qty'])), open_qty, round(
                    #     (open_qty/float(po['Po_Qty']))*100), packing_std, daily_order, share, max_qty, min_qty, stock, in_transit_qty, t_qty, req_qty, '', '', float(po['GSTPercentage']), '', ''])
                    data.append([po['Mat_No'], po['Part_No'], po['Part_Name'],po['PoNo'],po['PoEntry'], po_date, po['Uom'],round(float(po['Unit_Pice']), 2),po['HSN_code'], open_qty, open_percent, packing_std, req_qty, '', '', float(po['CGST']),float(po['SGST']),float(po['IGST']), '', ''])
        return data


@frappe.whitelist()
def submit_po(table, qr_code, irn_no, invoice_no):
    table = json.loads(table)
    supplier_code = frappe.db.get_value(
        'TSAI Supplier', {'email': frappe.session.user}, 'name')
    inv = frappe.new_doc('TSAI Invoice')
    inv.qr_code = qr_code
    inv.irn_no = irn_no
    inv.invoice_no = invoice_no
    inv.invoice_date = today()
    inv.supplier_code = supplier_code
    total_qty = 0
    total_basic = 0
    total_gst_amount = 0
    total_invoice_amount = 0
    total_bin = 0
    for row in table:
        if row[14]['content'] and row[15]['content']:
            po_no = row[4]['content']
            po_entry = row[5]['content']
            po_date = row[6]['content']
            total_qty += int(row[14]['content'])
            total_basic += float(row[15]['content'])
            total_gst_amount += float(row[20]['content'])
            total_invoice_amount += float(row[21]['content'])
            total_bin += float(row[14]['content'])/row[12]['content']
            inv.append('invoice_items', {
                'mat_no': row[1]['content'],
                'parts_no': row[2]['content'],
                'parts_name': row[3]['content'],
                'uom': row[7]['content'],
                'unit_price': row[8]['content'],
                'hsn_code': row[9]['content'],
                'packing_standard': row[12]['content'],
                'po_qty' : row[10]['content'],
                'key_qty': row[14]['content'],
                'basic_amount': row[15]['content'],
                'cgst': row[16]['content'],
                'sgst': row[17]['content'],
                'igst': row[18]['content'],
                'tcs' : row[19]['content'],
                'gst_amount': row[20]['content'],
                'invoice_amount': row[21]['content']
            })
    inv.po_no = po_no
    inv.po_entry = po_entry
    inv.po_date = po_date
    inv.total_qty = total_qty
    inv.total_basic_amount = total_basic
    inv.cgst = table[0][16]['content']
    inv.sgst = table[0][17]['content']
    inv.igst = table[0][18]['content']
    inv.tcs = table[0][19]['content']
    inv.total_gst_amount = total_gst_amount
    inv.total_invoice_amount = total_invoice_amount
    inv.total_bin = total_bin
    inv.save(ignore_permissions=True)
    frappe.db.commit()
    invoice_no_type = frappe.db.get_value(
        'TSAI Supplier', {'email': frappe.session.user}, 'invoice_no_type')
    if invoice_no_type == 'Automatic':
        frappe.db.set_value('TSAI Supplier',supplier_code,'current_running_no',invoice_no[-6:])
    return 'ok'


def get_dates(from_date, to_date):
    no_of_days = date_diff(add_days(to_date, 1), from_date)
    dates = [add_days(from_date, i) for i in range(0, no_of_days)]
    return dates


@frappe.whitelist()
def get_invoice_no():
    invoice_no_type = frappe.db.get_value(
        'TSAI Supplier', {'email': frappe.session.user}, 'invoice_no_type')
    if invoice_no_type == 'Automatic':
        supplier_code = frappe.db.get_value(
            'TSAI Supplier', {'email': frappe.session.user}, 'name')
        cur_no = frappe.db.get_value("TSAI Supplier",{'name':supplier_code},'current_running_no')
        
        no = "0000" + str(int(cur_no) + 1)
        date = datetime.strptime(today(), '%Y-%m-%d')
        month = datetime.strftime(date, "%m")
        year = datetime.strftime(date, "%Y")
        if int(month) <= 3 :
            invoice_no = str(supplier_code) + str(int(year[-2:])-1)+str(year[-2:]) + no[-5:]
        else:
            invoice_no = str(supplier_code) + str(year[-2:])+str(int(year[-2:])+1) + no[-5:]
        return invoice_no
    else:
        return ''


@frappe.whitelist()
def download_excel():
    supplier_code = frappe.db.get_value(
        'TSAI Supplier', {'email': frappe.session.user}, 'name')
    if supplier_code:
        url = "http://apioso.thaisummit.co.th:10401/api/POLineDetails"
        date = datetime.strptime(today(), '%Y-%m-%d')
        date = datetime.strftime(date, "%Y%m%d")
        payload = json.dumps({
            "Fromdate": "",
            "Todate": "",
            "SupplierCode": supplier_code,
            "DeliveryDate": date
        })
        headers = {
            'Content-Type': 'application/json',
            'API_KEY': '/1^i[#fhSSDnC8mHNTbg;h^uR7uZe#ninearin!g9D:pos+&terpTpdaJ$|7/QYups;==~w~!AWwb&DU',
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        pos = json.loads(response.text)
        data = []
        for po in pos:
            if frappe.db.exists('TSAI Part Master', po['Mat_No']):
                pr_name = frappe.db.get_value(
                    'Prepared Report', {'report_name': 'Supplier Daily Order','status':'Completed'}, 'name')
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
                    if cstr(do['item']) == po['Mat_No']:
                        daily_order = cint(do['daily_order'])
                        min_qty = do['min_qty']
                        max_qty = do['max_qty']                
                url = "http://apioso.thaisummit.co.th:10401/api/GetItemInventory"
                payload = json.dumps({
                    "ItemCode": po['Mat_No']
                })
                headers = {
                    'Content-Type': 'application/json',
                    'API_KEY': '/1^i[#fhSSDnC8mHNTbg;h^uR7uZe#ninearin!g9D:pos+&terpTpdaJ$|7/QYups;==~w~!AWwb&DU',
                }
                response = requests.request(
                    "POST", url, headers=headers, data=payload)
                stock = 0
                if response:
                    stocks = json.loads(response.text)
                    if stocks:
                        ica = frappe.db.sql(
                            "select warehouse from `tabInventory Control Area` where invoice_key = 'Y' ", as_dict=True)

                        wh_list = [d['warehouse'] for d in ica if 'warehouse' in d]

                        df = pd.DataFrame(stocks)
                        df = df[df['Warehouse'].isin(wh_list)]
                        stock = pd.to_numeric(df["Qty"]).sum()
                
                in_transit_qty_po = frappe.db.sql("""select sum(`tabInvoice Items`.key_qty) as key_qty from `tabTSAI Invoice`
                        left join `tabInvoice Items` on `tabTSAI Invoice`.name = `tabInvoice Items`.parent
                        where `tabTSAI Invoice`.status = 'OPEN' and `tabTSAI Invoice`.po_no = '%s' and `tabInvoice Items`.mat_no = '%s' and `tabTSAI Invoice`.supplier_code = '%s' and `tabInvoice Items`.grn = 0 """ % (po['PoNo'],po['Mat_No'],supplier_code), as_dict=True)[0].key_qty or 0

                in_transit_qty = frappe.db.sql("""select sum(`tabInvoice Items`.key_qty) as key_qty from `tabTSAI Invoice`
                        left join `tabInvoice Items` on `tabTSAI Invoice`.name = `tabInvoice Items`.parent
                        where `tabTSAI Invoice`.status = 'OPEN' and `tabInvoice Items`.mat_no = '%s' and `tabTSAI Invoice`.supplier_code = '%s' and `tabInvoice Items`.grn = 0 """ % (po['Mat_No'],supplier_code), as_dict=True)[0].key_qty or 0
                frappe.errprint(stock)
                t_qty = stock + in_transit_qty
                req_qty = 0
                open_qty = float(po['Open_Qty'])
                if open_qty > 0:
                    open_percent = round((open_qty/float(po['Po_Qty']))*100)
                else:
                    open_percent = 0
                packing_std = frappe.db.get_value(
                    "TSAI Part Master", po['Mat_No'], 'packing_std')
                mrp_daily_order = frappe.db.get_value(
                    "TSAI Part Master", po['Mat_No'], 'mrp_daily_order')
                po_date = pd.to_datetime(po['Po_Date']).date()
                delivery_date = pd.to_datetime(po['Delivery_Date']).date()
                share = frappe.db.get_value('Shares of Business Entry',{'supplier_code':supplier_code,'mat_no':po['Mat_No']},'share_of_business') or '-'
                # if open_qty > 0:
                if t_qty < min_qty:
                    try:
                        req_qty = math.ceil((max_qty - t_qty)/packing_std)*packing_std
                    except:
                        req_qty = 0
                    if req_qty < 0:
                        req_qty = 0
                    
                mrp_daily_order = frappe.db.get_value(
                    "TSAI Part Master", po['Mat_No'], 'mrp_daily_order')
                if open_qty > 0:
                    if daily_order == 0:
                        if t_qty == 0:
                            try:
                                req_qty = math.ceil((mrp_daily_order * min_qty)/packing_std)*packing_std
                            except:
                                req_qty = 0
                    # if open_qty < req_qty:
                    #     req_qty = math.floor(open_qty/packing_std)*packing_std
                        
                data.append([po['Mat_No'], po['Part_No'], po['Part_Name'], po['PoNo'], po['PoEntry'], po_date, delivery_date, po['Supplier_name'], po['Uom'], round(float(po['Unit_Pice']), 2), po['HSN_code'], round(float(po['Po_Qty'])), open_qty,open_percent, packing_std, daily_order,share, max_qty, min_qty, in_transit_qty_po, t_qty, req_qty, '', '',float(po['CGST']),float(po['SGST']),float(po['IGST']),float(po['TCS']), '', ''])

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

    cols = ["MAT No", "Parts No", "Parts Name", "PO No", "PO Entry", "PO Date", "Delivery date", "Supplier Name", "UOM", "Unit Price", "HSN Code","PO Qty", "Open Qty", "%", "Packing",
            "Daily Order","Share %" ,"Max Qty", "Min Qty", "In transit Qty", "Total Qty", "Req Qty", "Key Qty", "Basic Amount", "CGST %","SGST %","IGST %", "TCS %", "GST Amount", "Invoice Amount"]
    ws.append(cols)

    for row in data:
        ws.append(row)

    ws.sheet_view.zoomScale = 80

    xlsx_file = BytesIO()
    wb.save(xlsx_file)
    return xlsx_file


def get_stock(mat_no):
    url = "http://apioso.thaisummit.co.th:10401/api/GetItemInventory"
    payload = json.dumps({
        "ItemCode": mat_no
    })
    headers = {
        'Content-Type': 'application/json',
        'API_KEY': '/1^i[#fhSSDnC8mHNTbg;h^uR7uZe#ninearin!g9D:pos+&terpTpdaJ$|7/QYups;==~w~!AWwb&DU',
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

@frappe.whitelist()
def get_transit_qty(po_no,mat_no):
    supplier_code = frappe.db.get_value(
            'TSAI Supplier', {'email': frappe.session.user}, 'name')
    transit_qty = frappe.db.sql("""select sum(`tabInvoice Items`.key_qty) as key_qty from `tabTSAI Invoice`
    left join `tabInvoice Items` on `tabTSAI Invoice`.name = `tabInvoice Items`.parent
    where `tabTSAI Invoice`.status = 'OPEN' and `tabTSAI Invoice`.po_no = '%s'and `tabInvoice Items`.mat_no = '%s' and `tabTSAI Invoice`.supplier_code = '%s' and `tabInvoice Items`.grn = 0 """ % (po_no,mat_no,supplier_code), as_dict=True)[0].key_qty or 0
    return transit_qty


# def test_do():
#     pr_name = frappe.db.get_value(
#         'Prepared Report', {'report_name': 'Supplier Daily Order','status':'Completed'}, 'name')
#     attached_file_name = frappe.db.get_value(
#         "File",
#         {"attached_to_doctype": 'Prepared Report', "attached_to_name": pr_name},
#         "name",
#     )
#     attached_file = frappe.get_doc("File", attached_file_name)
#     compressed_content = attached_file.get_content()
#     uncompressed_content = gzip_decompress(compressed_content)
#     dos = json.loads(uncompressed_content.decode("utf-8"))
#     for do in dos:
#         if do['item'] == '91100080':
#             print(do)


def test_po():
    url = "http://apioso.thaisummit.co.th:10401/api/POLineDetails"
    date = str(today()).replace('-', '')
    payload = json.dumps({
        "Fromdate": "",
        "Todate": "",
        "SupplierCode": "",
        "DeliveryDate": date
    })
    headers = {
        'Content-Type': 'application/json',
        'API_KEY': '/1^i[#fhSSDnC8mHNTbg;h^uR7uZe#ninearin!g9D:pos+&terpTpdaJ$|7/QYups;==~w~!AWwb&DU',
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

