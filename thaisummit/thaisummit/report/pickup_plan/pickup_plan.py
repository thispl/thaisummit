# Copyright (c) 2013, TEAMPRO and contributors
# For license information, please see license.txt

from calendar import month
import frappe
# from datetime import date, timedelta
from frappe import msgprint, _
from warnings import  filters
from frappe.utils import cstr, cint, getdate
from frappe.utils import cstr, add_days, date_diff, getdate,today
from datetime import date, timedelta, datetime
import pandas as pd
import requests
import json
from frappe.utils import (
	flt,
	cint,
	cstr,
	get_html_format,
	get_url_to_form,
	gzip_decompress,
	format_duration,
)


def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    data = get_data()
    return columns, data


def get_columns():
    columns = [
        _('Mat No') + ':Data/:100',
        _('Part No') + ':Data/:150',
        _('Part Name') + ':Data/:200',
        _('Packing') + ':Data/:80',
        ]
    for i in range(8):
        dt = datetime.strptime(add_days(today(),i),'%Y-%m-%d')
        columns.append(_('%s'%datetime.strftime(dt,'%d-%b')) + ':Data/:80')
    return columns

def get_data():
    supplier_condition = ''
    if 'Supplier' in frappe.get_roles(frappe.session.user):
        if 'System Manager' not in frappe.get_roles(frappe.session.user):
            supplier = frappe.db.get_value('User',frappe.session.user,'full_name')
            supplier_condition = "and `tabTSAI PO`.supplier_name = '%s' "%supplier
    pos = frappe.db.sql("""select `tabTSAI PO`.name, `tabTSAI PO`.mat_no,`tabTSAI Part Master`.parts_no,`tabTSAI Part Master`.parts_name,`tabTSAI PO`.po_no,`tabTSAI PO`.po_date,`tabTSAI PO`.delivery_date,`tabTSAI PO`.supplier_name,`tabTSAI PO`.uom,`tabTSAI PO`.unit_price,`tabTSAI PO`.po_qty,`tabTSAI Part Master`.packing_std from `tabTSAI PO` 
    left join `tabTSAI Part Master` on `tabTSAI PO`.mat_no = `tabTSAI Part Master`.name
    where `tabTSAI PO`.po_status = 'O' and `tabTSAI PO`.delivery_date >= '%s' and left(`tabTSAI PO`.mat_no,1) in ('1','2','3','4','5') %s order by `tabTSAI PO`.creation """%(today(),supplier_condition),as_dict=True)
    data = []
    for po in pos:
        if frappe.db.exists('TSAI Part Master',po.mat_no):
            pr_name = frappe.db.get_value('Prepared Report',{'report_name':'Daily Order'},'name')
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
                if do['item'] == po.mat_no:
                    daily_order = do['daily_order']
                    min_qty = do['min_qty']
                    max_qty = do['max_qty']

            pol_qty = frappe.db.get_value('PO Ledger',{'tsai_po':po.name},['sum(key_qty)']) or 0
            open_qty = po.po_qty - pol_qty
            in_transit_qty = 0

            url = "http://182.156.241.14/StockDetail/Service1.svc/GetItemInventory"
            payload = json.dumps({
            "ItemCode":po.mat_no
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
            if open_qty > 0:
                if t_qty < max_qty:
                    req_qty = round(((max_qty - t_qty)/po.packing_std)*po.packing_std)
            
            row = [po.mat_no,po.parts_no,po.parts_name,po.packing_std,req_qty]
            for do in dos:
                if do['item'] == po.mat_no:
                    tomorrow = add_days(today(),1)
                    for i in range(7):
                        dt = datetime.strptime(add_days(tomorrow,i),'%Y-%m-%d')
                        day = datetime.strftime(dt,'%d')
                        month = datetime.strftime(dt,'%b')
                        qty = do[day+'_'+month.lower()]
                        row.append(qty)
            data.append(row)
    return data