# Copyright (c) 2022, TEAMPRO and contributors
# For license information, please see license.txt

from email import message
from select import select
import frappe
from frappe.model.document import Document
import json
from frappe.utils.background_jobs import enqueue
from frappe.utils import now_datetime, formatdate,random_string
import frappe
from frappe import throw, _
from frappe.model.document import Document
import time
from datetime import timedelta
from frappe.utils.file_manager import get_file
from frappe.utils.csvutils import UnicodeWriter, read_csv_content
from email.utils import formatdate 
import frappe
from frappe.utils.data import cstr
from frappe.utils import date_diff, add_months,today,add_days,nowdate,flt,getdate
import calendar
from frappe.utils.file_manager import get_file
from frappe.utils.csvutils import UnicodeWriter, read_csv_content
from datetime import date, datetime, timedelta
from frappe import _, get_file_items
from frappe.utils import get_first_day, today, get_last_day, format_datetime, add_years, date_diff, add_days, getdate, cint, format_date,get_url_to_form
from frappe.utils import add_months, add_days, format_time, today, nowdate, getdate, format_date
import calendar
from frappe.utils import get_first_day, today, get_last_day, format_datetime, add_years, date_diff, add_days, getdate, cint, format_date,get_url_to_form
from frappe.utils.background_jobs import enqueue

from frappe.desk.query_report import background_enqueue_run
import frappe
from frappe.utils import cstr
from datetime import datetime
from datetime import date,timedelta
import calendar
from dateutil import relativedelta
import time
from frappe.utils import add_to_date, formatdate, get_link_to_form, getdate, nowdate
from frappe.utils import (
	add_days,
	add_months,
	cint,
	date_diff,
	flt,
	get_first_day,
	get_last_day,
	get_link_to_form,
	getdate,
	rounded,
	today,
)

from frappe.utils import nowdate, get_last_day, getdate, add_days, add_years, today
from frappe.model.document import Document


import datetime
from datetime import datetime
import requests
import math
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
	today
)

class EkanbanSettings(Document):
	pass

	
@frappe.whitelist()
def enqueue_update_bom(file):
	enqueue(update_bom, queue='default', timeout=6000, event='update_bom',file=file)
	return 'Succuss'

@frappe.whitelist()
def update_bom(file):
	frappe.db.sql("""delete from `tabTSAI BOM`""")
	frappe.log_error(title="BOM Delete",message="BOM Deleted By %s" % frappe.session.user)
	filepath = get_file(file)
	pps = read_csv_content(filepath[1])
	for p in pps[1:]:
		bom = frappe.new_doc("TSAI BOM")
		bom.item = p[0]
		bom.item_descripition = p[1]
		bom.uom = p[2]
		bom.item_quantity = p[3]
		bom.whse = p[4]
		bom.depth = p[6]
		bom.price = p[5]
		bom.bom_type = p[7]
		bom.fm = p[8]
		bom.save(ignore_permissions=True)
		bom.submit()
		frappe.db.commit()

@frappe.whitelist()
def enqueue_grn_details():
	enqueue(fetch_grn_details, queue='default', timeout=60000, event='fetch_grn_details')
	return 'Succuss'

@frappe.whitelist()
def fetch_grn_details():
	invs = frappe.db.sql("""select name from `tabTSAI Invoice` where sync_grn = 0 """,as_dict=True)
	for inv in invs:
		url = "http://apioso.thaisummit.co.th:10401/api/GRNData"
		payload = json.dumps({
			"InvNo": inv.name
		})
		headers = {
			'Content-Type': 'application/json',
			'API_KEY': '/1^i[#fhSSDnC8mHNTbg;h^uR7uZe#ninearin!g9D:pos+&terpTpdaJ$|7/QYups;==~w~!AWwb&DU'
		}
		response = requests.request(
			"POST", url, headers=headers, data=payload)
		if response.text:  
			grns = json.loads(response.text)
			for grn in grns:
				if grn['InvNo'] == inv.name:
					doc = frappe.get_doc('TSAI Invoice',inv.name)
					for d in doc.invoice_items:
						if grn['MatNo'] == str(d.mat_no):
							d.grn = 1
							d.grn_qty = str(grn["GRNQty"])
							d.grn_date = pd.to_datetime(grn["GRNDate"]).date()
							d.grn_no = grn["GRNNo"]
					doc.save(ignore_permissions=True)
					frappe.db.commit()
		inv_grn = frappe.get_doc('TSAI Invoice',inv.name)
		sum_key = 0  
		sum_grn_qty = 0 
		for i in inv_grn.invoice_items:
			sum_key += i.key_qty
			sum_grn_qty += i.grn_qty
		if sum_key == sum_grn_qty:
			inv_grn.sync_grn = 1
		else:
			inv_grn.sync_grn = 0
		inv_grn.save(ignore_permissions=True)
		frappe.db.commit()

	return 'ok'

@frappe.whitelist()
def enqueue_invoice_key_date_wise(invoice_key_date):
	if not frappe.db.exists("Enqueue Methods",{'method':'Invoice Key Date Wise','status':'Queued'}):
		doc = frappe.new_doc("Enqueue Methods")
		doc.method = "Invoice Key Date Wise"
		doc.status = "Queued"
		doc.save(ignore_permissions=True)
		frappe.db.commit()
		enqueue(download_invoice_key_date_wise, queue='default', timeout=6000, event='build_xlsx_response',invoice_key_date=invoice_key_date,enqueue_id=doc.name)
		frappe.msgprint("Invoice Key Download is successsfully Initiated. Kindly wait for sometime and refresh the page.")
	else:
		frappe.msgprint("Invoice Key Download is already in Progress. Please wait for sometime and refresh the page. ")

@frappe.whitelist()
def download_invoice_key_date_wise(invoice_key_date,enqueue_id):
	# args = frappe.local.form_dict
	pos = frappe.get_all("TSAI PO",{'plan_date':invoice_key_date},['*'])
	data = []
	for po in pos:
		if frappe.db.exists('TSAI Part Master', po.mat_no):
			# pr_name = frappe.db.get_value(
			#     'Prepared Report', {'report_name': 'Supplier Daily Order','status':'Completed'}, 'name')
			pr_name = frappe.db.sql("""select name from `tabPrepared Report` where report_name = 'Supplier Daily Order' and status = 'Completed' and date(creation) = '%s' order by creation """%(invoice_key_date),as_dict=True)[0].name
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
				if str(do['item']) == po.mat_no:
					daily_order = cint(do['daily_order'])
					min_qty = cint(do['min_qty'])
					max_qty = cint(do['max_qty'])


			url = "http://apioso.thaisummit.co.th:10401/api/GetItemInventory"
			payload = json.dumps({
				"ItemCode": po.mat_no
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
						where `tabTSAI Invoice`.status = 'OPEN' and `tabTSAI Invoice`.po_no = '%s' and `tabInvoice Items`.mat_no = '%s' and `tabInvoice Items`.grn = 0 """ % (po.po_no,po.mat_no), as_dict=True)[0].key_qty or 0

			in_transit_qty = frappe.db.sql("""select sum(`tabInvoice Items`.key_qty) as key_qty from `tabTSAI Invoice`
					left join `tabInvoice Items` on `tabTSAI Invoice`.name = `tabInvoice Items`.parent
					where `tabTSAI Invoice`.status = 'OPEN' and `tabInvoice Items`.mat_no = '%s' and `tabInvoice Items`.grn = 0 """ % (po.mat_no), as_dict=True)[0].key_qty or 0
			# in_transit_qty = frappe.db.sql("""select sum(`tabInvoice Items`.key_qty) as key_qty from `tabTSAI Invoice`
			#         left join `tabInvoice Items` on `tabTSAI Invoice`.name = `tabInvoice Items`.parent
			#         where `tabTSAI Invoice`.status = 'OPEN' and `tabTSAI Invoice`.po_no = '%s' and `tabInvoice Items`.mat_no = '%s' and `tabInvoice Items`.grn = 0 """ % (po['PoNo'], po['Mat_No']), as_dict=True)[0].key_qty or 0
			t_qty = stock + in_transit_qty
			req_qty = 0
			open_qty = float(po.open_qty)
			if open_qty > 0:
				open_percent = round((open_qty/float(po.po_qty))*100)
			else:
				open_percent = 0
			packing_std = frappe.db.get_value(
				"TSAI Part Master", po.mat_no, 'packing_std')
			po_date = pd.to_datetime(po.po_date).date()
			delivery_date = pd.to_datetime(po.delivery_date).date()
			# share = frappe.db.get_value('Shares of Business Entry',{'supplier_code':supplier_code,'mat_no':po['Mat_No']},'share_of_business') or '-'
			# if open_qty > 0:
			if t_qty < min_qty:
				# frappe.log_error(title='inv',message = [po['Mat_No'],po['Supplier_name'],max_qty,t_qty,packing_std])
				try:
					req_qty = math.ceil((max_qty - t_qty)/packing_std)*packing_std
				except:
					req_qty = 0
				if req_qty < 0:
					req_qty = 0
				
			mrp_daily_order = frappe.db.get_value(
					"TSAI Part Master", po.mat_no, 'mrp_daily_order')
			if open_qty > 0:
				if daily_order == 0:
					if t_qty == 0:
						try:
							req_qty = math.ceil((mrp_daily_order * min_qty)/packing_std)*packing_std
						except:
							req_qty = 0
			data.append([po.mat_no, po.parts_no, po.parts_name, po.po_no, po_date, delivery_date, po.supplier_name, po.uom, round(float(po.unit_price), 2), po.hsn_code, round(float(po.po_qty)), open_qty, open_percent, packing_std, daily_order, max_qty, min_qty, stock , in_transit_qty_po, t_qty, req_qty, '', '',float(po.cgst),float(po.sgst),float(po.igst), '', ''])

	xlsx_file = make_xlsx(data)
	# frappe.response['filename'] = 'Invoice_Key.xlsx'
	# frappe.response['filecontent'] = xlsx_file.getvalue()
	# frappe.response['type'] = 'binary'
	ret = frappe.get_doc({
			"doctype": "File",
			"attached_to_name": '',
			"attached_to_doctype": 'Ekanban Settings',
			"attached_to_field": 'invoice_key_date_wise',
			"file_name": 'invoice_key ' + str(formatdate(invoice_key_date)) +'.xlsx',
			"is_private": 0,
			"content": xlsx_file.getvalue(),
			"decode": False
		})
	ret.save(ignore_permissions=True)
	frappe.db.commit()
	attached_file = frappe.get_doc("File", ret.name)
	frappe.db.set_value('Ekanban Settings',None,'invoice_key_date_wise',attached_file.file_url)
	frappe.db.set_value('Ekanban Settings',None,'date_wise_last_download_on',now_datetime())
	frappe.db.set_value('Enqueue Methods',enqueue_id,'status','Completed')


def make_xlsx(data, sheet_name=None, wb=None, column_widths=None):
	# args = frappe.local.form_dict
	column_widths = column_widths or []
	if wb is None:
		wb = openpyxl.Workbook()

	ws = wb.create_sheet(sheet_name, 0)

	cols = ["MAT No", "Parts No", "Parts Name", "PO No", "PO Entry","PO Date", "Delivery date", "Supplier Name", "UOM", "Unit Price", "HSN Code","PO Qty", "Open Qty", "%", "Packing",
			"Daily Order" ,"Max Qty", "Min Qty", "Stock" ,"In transit Qty", "Total Qty", "Req Qty", "Key Qty", "Basic Amount", "CGST %","SGST %","IGST %", "TCS %", "GST Amount", "Invoice Amount"]
	ws.append(cols)

	for row in data:
		ws.append(row)

	ws.sheet_view.zoomScale = 80

	xlsx_file = BytesIO()
	wb.save(xlsx_file)
	return xlsx_file

@frappe.whitelist()
def enqueue_overall_invoice_key():
	if not frappe.db.exists("Enqueue Methods",{'method':'Overall Invoice Key','status':'Queued'}):
		doc = frappe.new_doc("Enqueue Methods")
		doc.method = "Overall Invoice Key"
		doc.status = "Queued"
		doc.save(ignore_permissions=True)
		frappe.db.commit()
		enqueue(download_invoice_key, queue='default', timeout=6000, event='build_xlsx_response',enqueue_id=doc.name)
		frappe.msgprint("Overall Invoice Key Download is successsfully Initiated. Kindly wait for sometime and refresh the page.")
	else:
		frappe.msgprint("Overall Invoice Key Download is already in Progress. Please wait for sometime and refresh the page. ")

@frappe.whitelist()
def enqueue_overall_invoice_key_cron_145am():
	enqueue(download_invoice_key, queue='default', timeout=6000, event='build_xlsx_response',enqueue_id=random_string(5))
	frappe.log_error(title="overall_invoice_key_cron",message="Overall Invoice Key Download is successsfully Initiated. Kindly wait for sometime and refresh the page.")

@frappe.whitelist()
def enqueue_overall_invoice_key_cron_930pm():
	enqueue(download_invoice_key, queue='default', timeout=6000, event='build_xlsx_response',enqueue_id=random_string(5))
	frappe.log_error(title="overall_invoice_key_cron",message="Overall Invoice Key Download is successsfully Initiated. Kindly wait for sometime and refresh the page.")

@frappe.whitelist()
def fetch_ekanban_bom():
	frappe.db.sql("delete from `tabTest BOM`")
	frappe.log_error(title="BOM Delete",message="BOM Deleted By %s" % frappe.session.user)


@frappe.whitelist()
def enqueue_overall_invoice_key_cron_930am():
	enqueue(download_invoice_key, queue='default', timeout=6000, event='build_xlsx_response',enqueue_id=random_string(5))
	frappe.log_error(title="overall_invoice_key_cron",message="Overall Invoice Key Download is successsfully Initiated. Kindly wait for sometime and refresh the page.")

@frappe.whitelist()
def enqueue_overall_invoice_key_cron():
	enqueue(download_invoice_key, queue='default', timeout=6000, event='build_xlsx_response',enqueue_id=random_string(5))
	frappe.log_error(title="overall_invoice_key_cron",message="Overall Invoice Key Download is successsfully Initiated. Kindly wait for sometime and refresh the page.")

@frappe.whitelist()
def download_invoice_key(enqueue_id):
	url = "http://apioso.thaisummit.co.th:10401/api/POLineDetails"
	date = datetime.strptime(today(), '%Y-%m-%d')
	date = datetime.strftime(date, "%Y%m%d")
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
	# pos = json.loads(response.text)
	try:
		pos = json.loads(response.text)
	except:
		frappe.msgprint("Unable to display Pickup Plan due to API Issue")
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
						where `tabTSAI Invoice`.status = 'OPEN' and `tabTSAI Invoice`.po_no = '%s' and `tabInvoice Items`.mat_no = '%s' and `tabInvoice Items`.grn = 0 """ % (po['PoNo'],po['Mat_No']), as_dict=True)[0].key_qty or 0

			in_transit_qty = frappe.db.sql("""select sum(`tabInvoice Items`.key_qty) as key_qty from `tabTSAI Invoice`
					left join `tabInvoice Items` on `tabTSAI Invoice`.name = `tabInvoice Items`.parent
					where `tabTSAI Invoice`.status = 'OPEN' and `tabInvoice Items`.mat_no = '%s' and `tabInvoice Items`.grn = 0 """ % (po['Mat_No']), as_dict=True)[0].key_qty or 0
			# in_transit_qty = frappe.db.sql("""select sum(`tabInvoice Items`.key_qty) as key_qty from `tabTSAI Invoice`
			#         left join `tabInvoice Items` on `tabTSAI Invoice`.name = `tabInvoice Items`.parent
			#         where `tabTSAI Invoice`.status = 'OPEN' and `tabTSAI Invoice`.po_no = '%s' and `tabInvoice Items`.mat_no = '%s' and `tabInvoice Items`.grn = 0 """ % (po['PoNo'], po['Mat_No']), as_dict=True)[0].key_qty or 0
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
			# share = frappe.db.get_value('Shares of Business Entry',{'supplier_code':supplier_code,'mat_no':po['Mat_No']},'share_of_business') or '-'
			# if open_qty > 0:
			if t_qty < min_qty:
				# frappe.log_error(title='inv',message = [po['Mat_No'],po['Supplier_name'],max_qty,t_qty,packing_std])
				try:
					req_qty = math.ceil((max_qty - t_qty)/packing_std)*packing_std
				except:
					req_qty = 0
				if req_qty < 0:
					req_qty = 0
			mrp_daily_order = frappe.db.get_value(
					"TSAI Part Master", po["Mat_No"], 'mrp_daily_order')
			if open_qty > 0:
				if daily_order == 0:
					if t_qty == 0:
						try:
							req_qty = math.ceil((mrp_daily_order * min_qty)/packing_std)*packing_std
						except : 
							req_qty = 0
			data.append([po['Mat_No'], po['Part_No'], po['Part_Name'], po['PoNo'], po['PoEntry'], po_date, delivery_date, po['Supplier_name'], po['Uom'], round(float(po['Unit_Pice']), 2), po['HSN_code'], round(float(po['Po_Qty'])), open_qty, open_percent, packing_std, daily_order, max_qty, min_qty, stock , in_transit_qty_po, t_qty, req_qty, '', '',float(po['CGST']),float(po['SGST']),float(po['IGST']),float(po['TCS']), '', ''])

	xlsx_file = make_xlsx(data)
	# frappe.response['filename'] = 'Invoice_Key.xlsx'
	# frappe.response['filecontent'] = xlsx_file.getvalue()
	# frappe.response['type'] = 'binary'
	ret = frappe.get_doc({
			"doctype": "File",
			"attached_to_name": '',
			"attached_to_doctype": 'Ekanban Settings',
			"attached_to_field": 'attach',
			"file_name": 'Overall_Invoice_Key.xlsx',
			"is_private": 0,
			"content": xlsx_file.getvalue(),
			"decode": False
		})
	ret.save(ignore_permissions=True)
	frappe.db.commit()
	attached_file = frappe.get_doc("File", ret.name)
	frappe.db.set_value('Ekanban Settings',None,'invoice_key',attached_file.file_url)
	frappe.db.set_value('Ekanban Settings',None,'overall_last_download_on',now_datetime())
	frappe.db.set_value('Enqueue Methods',enqueue_id,'status','Completed')

