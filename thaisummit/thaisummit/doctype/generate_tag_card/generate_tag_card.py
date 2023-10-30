# Copyright (c) 2023, TEAMPRO and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import frappe
from frappe.model.document import Document
import math
import frappe
import json
import requests
import pandas as pd
import openpyxl
from frappe import _
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
from datetime import timedelta, datetime
# from __future__ import unicode_literals
from six.moves import range
from six import string_types
import frappe
import json
from frappe.utils import getdate,get_time, cint, add_months, date_diff, add_days, nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime
from datetime import datetime
from calendar import monthrange

from frappe import _, msgprint
from frappe.utils import flt
from frappe.utils import cstr, cint, getdate
import pandas as pd 
# from __future__ import unicode_literals
from functools import total_ordering
from itertools import count,groupby
# import more_itertools
import frappe
from frappe import permissions
from frappe.utils import cstr, cint, getdate, get_last_day, get_first_day, add_days
from frappe.utils import cstr, add_days, date_diff, getdate, format_date,now
from math import floor
from frappe import msgprint, _
from calendar import month, monthrange
from datetime import date, timedelta, datetime,time
from numpy import true_divide 
from operator import itemgetter


class GenerateTagCard(Document):

	# def on_update(self):
	# 	table = self.table_9
	# 	for t in table:
	# 		tab = frappe.get_doc("Tag Card",t.item_card_no)
	# 		tab.link_document = self.name
	# 		tab.save(ignore_permissions=True)
	# 		frappe.db.commit	

	def validate(self):
		prod_line_emp = []
		user = frappe.session.user
		if user not in ['Administrator','gururaja528@gmail.com']:
			emp_details = frappe.db.sql("""select name from `tabEmployee Production Line Details` where user_id ='%s' """%(user),as_dict=1)[0]
			emp_name = emp_details['name']
			emp_doc = frappe.get_doc('Employee Production Line Details', emp_name)
			emp_prod_line = emp_doc.get('production_line')
			for e in emp_prod_line:
				prod_line_emp.append(e.production_line_no)
			tag_production_line = self.production_line or 0
			if tag_production_line in prod_line_emp:
				# Production Order not Released
				if self.production_order_qty == 0:
					child_mat = self.child_parts
					for m in child_mat:
						tce = frappe.new_doc("Tag Card Errors")
						tce.error_name = "Production Order not Released"
						tce.mat_numbers = self.mat_number
						tce.production_order_qty = self.production_order_qty
						tce.user_id = self.user_name
						tce.tag_card_qty = self.quantity
						tce.date = self.date
						tce.time = self.time 
						tce.child_mat_number = m.child_part
						tce.warehouse_qty = m.warehouse_qty
						tce.shortage_qty = m.shortage 
						tce.save(ignore_permissions=True)
						frappe.db.commit()
					frappe.throw(_('Production Order not Released'))
				# Quantity is greater than Production Order Quantity
				if cint(self.production_order_qty) < self.quantity:
					child_mat = self.child_parts
					for m in child_mat:
						tce = frappe.new_doc("Tag Card Errors")
						tce.error_name = "Quantity is greater than Production Order Quantity"
						tce.mat_numbers = self.mat_number
						tce.production_order_qty = self.production_order_qty
						tce.user_id = self.user_name
						tce.tag_card_qty = self.quantity
						tce.date = self.date
						tce.time = self.time 
						tce.child_mat_number = m.child_part
						tce.warehouse_qty = m.warehouse_qty
						tce.shortage_qty = m.shortage 
						tce.save(ignore_permissions=True)
						frappe.db.commit()
					frappe.throw(_("Quantity is greater than Production Order Quantity"))

				

				# Enter the Quantity according to packing standard
				q_ty = float(self.quantity)
				pack_std = float(self.packing_std)
				check_qty = round(q_ty / pack_std ) * pack_std
				if self.quantity != check_qty:
					child_mat = self.child_parts
					for m in child_mat:
						tce = frappe.new_doc("Tag Card Errors")
						tce.error_name = "Enter the Quantity according to packing standard"
						tce.mat_numbers = self.mat_number
						tce.production_order_qty = self.production_order_qty
						tce.user_id = self.user_name
						tce.tag_card_qty = self.quantity
						tce.date = self.date
						tce.time = self.time 
						tce.child_mat_number = m.child_part
						tce.warehouse_qty = m.warehouse_qty
						tce.shortage_qty = m.shortage 
						tce.save(ignore_permissions=True)
						frappe.db.commit()
					frappe.throw(_("Enter the Quantity according to packing standard"))
				# Child Parts Quantity Shortage	
				bom_list = frappe.db.sql("""select * from `tabTSAI BOM` where fm ='%s' and depth = '2' and uom != '' """%(self.mat_number),as_dict=1)
				for c in bom_list:
					warehouse_qty = get_live_stock(c.item,self.mat_number)
					qty_short = c.item_quantity * self.quantity
					if warehouse_qty < qty_short:
						short_qty = warehouse_qty - qty_short
						child_mat = self.child_parts
						for m in child_mat:
							tce = frappe.new_doc("Tag Card Errors")
							tce.error_name = "Child Parts Quantity Shortage"
							tce.mat_numbers = self.mat_number
							tce.production_order_qty = self.production_order_qty
							tce.user_id = self.user_name
							tce.tag_card_qty = self.quantity
							tce.date = self.date
							tce.time = self.time 
							tce.child_mat_number = m.child_part
							tce.warehouse_qty = m.warehouse_qty
							tce.shortage_qty = m.shortage 
							tce.save(ignore_permissions=True)
							frappe.db.commit()
						frappe.throw(_('Child Parts Quantity Shortage'))

				part_master = frappe.db.sql("""select tag_card_flow_master as tc from `tabTSAI Part Master` where mat_no ='%s' """%(self.mat_number),as_dict=1)[0]
				name_f = part_master['tc']
				if name_f:
					doc = frappe.get_doc('Tag Card Flow Master', name_f)
					children = doc.get('tag_card_workflow_table')
					self.set('workflow_table', [])
					for child_row in children:
						workflow_name = child_row.workflow
						role_name = child_row.role_name
						allowed_for = child_row.allowed_for
						frappe.errprint(workflow_name)
						self.append('workflow_table',{
							'workflow':workflow_name,
							'role_name':role_name,
							'allowed_for':allowed_for
						})
				else:
					frappe.msgprint("Kindly set the workflow for this mat number")
					
				self.shift = get_shift_type()
				self.date = date.today()
				self.time = datetime.now().strftime('%H:%M:%S')
				u_name = frappe.db.sql("""select username from `tabUser` where name='%s' """%(frappe.session.user),as_dict=1)[0]
				self.user_name = u_name['username']

				self.set('table_9', [])
				q_ty = float(self.quantity)
				pack_std = float(self.packing_std)
				qty_clac =  q_ty / pack_std
				q_clac = int(qty_clac)
				qr_list = []
				for i in range(1,q_clac+1):
					new_string = "{}-{}".format(self.name, i)			
					self.append('table_9',{
						'item_card_no':new_string,
						'mat_no':self.mat_number,
						'packing_standard':self.packing_std,
						'production_order':self.production_order_qty,
						'qty':self.packing_std
					})
					qr_list.append(new_string)
				my_string = ','.join(qr_list)
				self.qr_code = my_string
			else:
				frappe.throw(_('This Mat Number doesnt belongs to your production line'))
		else:
			# Production Order not Released
			if self.production_order_qty == 0:
				child_mat = self.child_parts
				for m in child_mat:
					tce = frappe.new_doc("Tag Card Errors")
					tce.error_name = "Production Order not Released"
					tce.mat_numbers = self.mat_number
					tce.production_order_qty = self.production_order_qty
					tce.user_id = self.user_name
					tce.tag_card_qty = self.quantity
					tce.date = self.date
					tce.time = self.time 
					tce.child_mat_number = m.child_part
					tce.warehouse_qty = m.warehouse_qty
					tce.shortage_qty = m.shortage 
					tce.save(ignore_permissions=True)
					frappe.db.commit()
				frappe.throw(_('Production Order not Released'))
			# Quantity is greater than Production Order Quantity
			if cint(self.production_order_qty) < self.quantity:
				child_mat = self.child_parts
				for m in child_mat:
					tce = frappe.new_doc("Tag Card Errors")
					tce.error_name = "Quantity is greater than Production Order Quantity"
					tce.mat_numbers = self.mat_number
					tce.production_order_qty = self.production_order_qty
					tce.user_id = self.user_name
					tce.tag_card_qty = self.quantity
					tce.date = self.date
					tce.time = self.time 
					tce.child_mat_number = m.child_part
					tce.warehouse_qty = m.warehouse_qty
					tce.shortage_qty = m.shortage 
					tce.save(ignore_permissions=True)
					frappe.db.commit()
				frappe.throw(_("Quantity is greater than Production Order Quantity"))

			

			# Enter the Quantity according to packing standard
			q_ty = float(self.quantity)
			pack_std = float(self.packing_std)
			check_qty = round(q_ty / pack_std ) * pack_std
			if self.quantity != check_qty:
				child_mat = self.child_parts
				for m in child_mat:
					tce = frappe.new_doc("Tag Card Errors")
					tce.error_name = "Enter the Quantity according to packing standard"
					tce.mat_numbers = self.mat_number
					tce.production_order_qty = self.production_order_qty
					tce.user_id = self.user_name
					tce.tag_card_qty = self.quantity
					tce.date = self.date
					tce.time = self.time 
					tce.child_mat_number = m.child_part
					tce.warehouse_qty = m.warehouse_qty
					tce.shortage_qty = m.shortage 
					tce.save(ignore_permissions=True)
					frappe.db.commit()
				frappe.throw(_("Enter the Quantity according to packing standard"))
			# Child Parts Quantity Shortage	
			bom_list = frappe.db.sql("""select * from `tabTSAI BOM` where fm ='%s' and depth = '2' and uom != '' """%(self.mat_number),as_dict=1)
			for c in bom_list:
				warehouse_qty = get_live_stock(c.item,self.mat_number)
				qty_short = c.item_quantity * self.quantity
				if warehouse_qty < qty_short:
					short_qty = warehouse_qty - qty_short
					child_mat = self.child_parts
					for m in child_mat:
						tce = frappe.new_doc("Tag Card Errors")
						tce.error_name = "Child Parts Quantity Shortage"
						tce.mat_numbers = self.mat_number
						tce.production_order_qty = self.production_order_qty
						tce.user_id = self.user_name
						tce.tag_card_qty = self.quantity
						tce.date = self.date
						tce.time = self.time 
						tce.child_mat_number = m.child_part
						tce.warehouse_qty = m.warehouse_qty
						tce.shortage_qty = m.shortage 
						tce.save(ignore_permissions=True)
						frappe.db.commit()
					frappe.throw(_('Child Parts Quantity Shortage'))

			part_master = frappe.db.sql("""select tag_card_flow_master as tc from `tabTSAI Part Master` where mat_no ='%s' """%(self.mat_number),as_dict=1)[0]
			name_f = part_master['tc']
			if name_f:
				doc = frappe.get_doc('Tag Card Flow Master', name_f)
				children = doc.get('tag_card_workflow_table')
				self.set('workflow_table', [])
				for child_row in children:
					workflow_name = child_row.workflow
					role_name = child_row.role_name
					allowed_for = child_row.allowed_for
					frappe.errprint(workflow_name)
					self.append('workflow_table',{
						'workflow':workflow_name,
						'role_name':role_name,
						'allowed_for':allowed_for
					})
			else:
				frappe.msgprint("Kindly set the workflow for this mat number")
				
			self.shift = get_shift_type()
			self.date = date.today()
			self.time = datetime.now().strftime('%H:%M:%S')
			u_name = frappe.db.sql("""select username from `tabUser` where name='%s' """%(frappe.session.user),as_dict=1)[0]
			self.user_name = u_name['username']

			self.set('table_9', [])
			q_ty = float(self.quantity)
			pack_std = float(self.packing_std)
			qty_clac =  q_ty / pack_std
			q_clac = int(qty_clac)
			qr_list = []
			for i in range(1,q_clac+1):
				new_string = "{}-{}".format(self.name, i)			
				self.append('table_9',{
					'item_card_no':new_string,
					'mat_no':self.mat_number,
					'packing_standard':self.packing_std,
					'production_order':self.production_order_qty,
					'qty':self.packing_std
				})
				qr_list.append(new_string)
			my_string = ','.join(qr_list)
			self.qr_code = my_string

		# this function actually happend during on_submit

		part_master = frappe.db.sql("""select tag_card_flow_master as tc from `tabTSAI Part Master` where mat_no ='%s' """%(self.mat_number),as_dict=1)[0]
		name_f = part_master['tc']
		doc = frappe.get_doc('Tag Card Flow Master', name_f)
		children = doc.get('tag_card_workflow_table')
		table = self.table_9
		for t in table:
			tab = frappe.new_doc("Tag Card")
			tab.item_card_no = t.item_card_no
			tab.production_order_qty = t.production_order
			tab.mat_number = self.mat_number
			tab.mat_name = self.mat_name
			tab.part_number = self.part_number
			tab.packing_std = t.packing_standard
			tab.quantity = t.qty
			tab.supcode = self.supcode
			tab.user_code = self.user_code
			tab.user_name = self.user_name
			tab.date = self.date
			tab.time = self.time
			tab.shift = self.shift
			tab.current_workflow = children[0].workflow
			tab.previous_workflow = children[0].workflow
			tab.workflow = 1
			tab.roleflow = 1
			tab.production_line = self.production_line
			tab.allowed_role = children[0].allowed_for
			url = "http://apioso.thaisummit.co.th:10401/api/ProductionReceiptTagCard"
			payload = json.dumps({
			"receiptdate": self.date.strftime("%d-%m-%Y"),
			"fgqty": t.qty,
			"itemno": self.mat_number,
			"tagcardno": t.item_card_no
			})
			headers = {
			'API_KEY': '/1^i[#fhSSDnC8mHNTbg;h^uR7uZe#ninearin!g9D:pos+&terpTpdaJ$|7/QYups;==~w~!AWwb&DU',
			'Content-Type': 'application/json'
			}
			response = requests.request("POST", url, headers=headers, data=payload)
			res = json.loads(response.text)
			frappe.log_error(res['Status'])
			tab.status = res['Status']
			tab.append('workflow_tracker_table',{
				'flow_name': children[0].workflow,
				'time':datetime.now().strftime('%H:%M:%S'),
				'date':date.today(),
				'user_name':self.user_name
			})
			frappe.log_error(title="generate_tag_card",message=payload)
			u_name = frappe.db.sql("""select username from `tabUser` where name='%s' """%(frappe.session.user),as_dict=1)[0]
			frappe.log_error(title="generate_tag_card",message=u_name['username'])
			tab.save(ignore_permissions=True)
			frappe.db.commit()


	@frappe.whitelist()
	def get_child_mat(self):
		self.date = date.today()
		self.time = datetime.now().strftime('%H:%M:%S')
		u_name = frappe.db.sql("""select username from `tabUser` where name='%s' """%(frappe.session.user),as_dict=1)[0]
		self.user_name = u_name['username']
		self.set('child_parts', [])
		bom_list = frappe.db.sql("""select * from `tabTSAI BOM` where fm ='%s' and depth = '2' and uom != '' """%(self.mat_number),as_dict=1)
		for c in bom_list:
			warehouse_qty = get_live_stock(c.item,self.mat_number)
			qty_short = c.item_quantity * self.quantity
			if warehouse_qty < qty_short:
				short_qty = warehouse_qty - qty_short
			else:
				short_qty = 0
			self.append('child_parts',{
				'child_part':c.item,
				'warehouse_qty':warehouse_qty,
				'tag_card_qty':self.quantity,
				'shortage':short_qty,
			})
		# Production Order not Released
		if self.production_order_qty == 0:
			child_mat = self.child_parts
			for m in child_mat:
				tce = frappe.new_doc("Tag Card Errors")
				tce.error_name = "Production Order not Released"
				tce.mat_numbers = self.mat_number
				tce.production_order_qty = self.production_order_qty
				tce.user_id = self.user_name
				tce.tag_card_qty = self.quantity
				tce.date = self.date
				tce.time = self.time 
				tce.child_mat_number = m.child_part
				tce.warehouse_qty = m.warehouse_qty
				tce.shortage_qty = m.shortage 
				tce.save(ignore_permissions=True)
				frappe.db.commit()
			frappe.throw(_('Production Order not Released'))
		# Quantity is greater than Production Order Quantity
		if cint(self.production_order_qty) < self.quantity:
			child_mat = self.child_parts
			for m in child_mat:
				tce = frappe.new_doc("Tag Card Errors")
				tce.error_name = "Quantity is greater than Production Order Quantity"
				tce.mat_numbers = self.mat_number
				tce.production_order_qty = self.production_order_qty
				tce.user_id = self.user_name
				tce.tag_card_qty = self.quantity
				tce.date = self.date
				tce.time = self.time 
				tce.child_mat_number = m.child_part
				tce.warehouse_qty = m.warehouse_qty
				tce.shortage_qty = m.shortage 
				tce.save(ignore_permissions=True)
				frappe.db.commit()
			frappe.throw(_("Quantity is greater than Production Order Quantity"))

		

		# Enter the Quantity according to packing standard
		q_ty = float(self.quantity)
		pack_std = float(self.packing_std)
		check_qty = round(q_ty / pack_std ) * pack_std
		if self.quantity != check_qty:
			child_mat = self.child_parts
			for m in child_mat:
				tce = frappe.new_doc("Tag Card Errors")
				tce.error_name = "Enter the Quantity according to packing standard"
				tce.mat_numbers = self.mat_number
				tce.production_order_qty = self.production_order_qty
				tce.user_id = self.user_name
				tce.tag_card_qty = self.quantity
				tce.date = self.date
				tce.time = self.time 
				tce.child_mat_number = m.child_part
				tce.warehouse_qty = m.warehouse_qty
				tce.shortage_qty = m.shortage 
				tce.save(ignore_permissions=True)
				frappe.db.commit()
			frappe.throw(_("Enter the Quantity according to packing standard"))

		
	
	@frappe.whitelist()
	def get_data(self):
		self.date = date.today()
		self.time = datetime.now().strftime('%H:%M:%S')
		u_name = frappe.db.sql("""select username from `tabUser` where name='%s' """%(frappe.session.user),as_dict=1)[0]
		self.user_name = u_name['username']
		self.set('child_parts', [])
		bom_list = frappe.db.sql("""select * from `tabTSAI BOM` where fm ='%s' and depth = '2' and uom != '' """%(self.mat_number),as_dict=1)
		for c in bom_list:
			warehouse_qty = get_live_stock(c.item,self.mat_number)
			qty_short = c.item_quantity * self.quantity
			if warehouse_qty < qty_short:
				short_qty = warehouse_qty - qty_short
			else:
				short_qty = 0
			self.append('child_parts',{
				'child_part':c.item,
				'warehouse_qty':warehouse_qty,
				'tag_card_qty':self.quantity,
				'shortage':short_qty,
			})
		
		bom_list = frappe.db.sql("""select * from `tabTSAI BOM` where fm ='%s' and depth = '2' and uom != '' """%(self.mat_number),as_dict=1)
				
		data = ''
		data += '<table class="table table-bordered" style="width:100%"><tr><td style="padding:1px;border: 1px solid black;background-color:#7CFC00;"><center><b>Mat Number</b></center></td><td style="padding:1px;border: 1px solid black;background-color:#7CFC00;"><center><b>Item Description</b></center></td><td style="padding:1px;border: 1px solid black;background-color:#7CFC00;"><center><b>UOM</b></center></td><td style="padding:1px;border: 1px solid black;background-color:#7CFC00;"><center><b>Quantity</b></center></td><td style="padding:1px;border: 1px solid black;background-color:#7CFC00;"><center><b>Warehouse</b></center></td><td style="padding:1px;border: 1px solid black;background-color:#7CFC00;"><center><b>Depth</b></center></td><td style="padding:1px;border: 1px solid black;background-color:#7CFC00;"><center><b>Bom Type</b></center></td><td style="padding:1px;border: 1px solid black;background-color:#7CFC00;"><center><b>Warehouse Qty</b></center></td><td style="padding:1px;border: 1px solid black;background-color:#7CFC00;"><center><b>Print Qty</b></center></td><td style="padding:1px;border: 1px solid black;background-color:#7CFC00;"><center><b>Shortage Qty</b></center></td><td style="padding:1px;border: 1px solid black;background-color:#7CFC00;"><center><b>Status</b></center></td></tr>'
		item_name = None
		for b in bom_list:
			warehouse_qty = get_live_stock(b.item,self.mat_number)
			part_name = frappe.db.sql("""select parts_name from `tabTSAI Part Master` where name ='%s' """%(b.item),as_dict=1)[0]
			if part_name['parts_name']:
				item_name = part_name['parts_name']
			data += '<tr><td style="text-align:center;padding:1px;border: 1px solid black;">%s</td><td style="text-align:center;padding:1px;border: 1px solid black;">%s</td><td style="text-align:center;padding:1px;border: 1px solid black;">%s</td><td style="text-align:center;text-align:center;padding:1px;border: 1px solid black;">%s</td><td style="text-align:center;padding:1px;border: 1px solid black;">%s</td><td style="text-align:center;padding:1px;border: 1px solid black;">%s</td><td style="text-align:center;padding:1px;border: 1px solid black;">%s</td><td style="text-align:center;padding:1px;border: 1px solid black;">%s</td><td style="text-align:center;padding:1px;border: 1px solid black;">%s</td>'%(b.item,item_name,b.uom,b.item_quantity,b.whse,b.depth,b.bom_type,warehouse_qty,self.quantity)
			qty_short = b.item_quantity * self.quantity
			if warehouse_qty < qty_short:
				short_qty = warehouse_qty - qty_short
				status = 'shortage'
				data += '<td style="padding:1px;text-align:center;background-color:#FF0000;border: 1px solid black;"><b>%s</b></td><td style="padding:1px;text-align:center;background-color:#FF0000;border: 1px solid black;"><b>%s</b></td></tr>'%(short_qty,status)
			else:
				short_qty = '-'
				status = 'ok'
				data += '<td style="padding:1px;border: 1px solid black;text-align:center;">%s</td><td style="text-align:center;padding:1px;border: 1px solid black;">%s</td></tr>'%(short_qty,status)
			
		return data

@frappe.whitelist()
def get_live_stock(mat_no,fm):
	whse = frappe.db.sql("""select whse from `tabTSAI BOM` where item ='%s' and fm = '%s' """%(mat_no,fm),as_dict=1)[0]
	whse_name = whse['whse']
	url = "http://apioso.thaisummit.co.th:10401/api/GetItemInventory"
	payload = json.dumps({
		"ItemCode": mat_no,
	})
	headers = {
		'Content-Type': 'application/json',
		'API_KEY': '/1^i[#fhSSDnC8mHNTbg;h^uR7uZe#ninearin!g9D:pos+&terpTpdaJ$|7/QYups;==~w~!AWwb&DU',
	}
	response = requests.request(
		"POST", url, headers=headers, data=payload)
	stock = 0  # set default value to 0
	if response:
		stocks = json.loads(response.text)
		if stocks:
			filtered_stocks = [d for d in stocks if d["Warehouse"] == whse_name]
			stock = [float(d["Qty"]) for d in filtered_stocks]
	return stock[0] if stock else 0  # return 0 if stock is empty


@frappe.whitelist()
def get_shift_type():
	nowtime = datetime.now()
	shift_date = date.today()
	shift = frappe.db.get_value('Shift Type',{'name':'1'},['qr_start_time','qr_end_time'])
	# shift1_time = [time(hour=shift[0].seconds//3600,minute=((shift[0].seconds//60)%60),second=0),time(hour=shift[1].seconds//3600,minute=((shift[1].seconds//60)%60),second=0)]
	# frappe.errprint(shift1_time)
	shift1_time = [time(hour=8, minute=0, second=1),time(hour=16, minute=30, second=0)]
	shift2_time = [time(hour=16, minute=30, second=0),time(hour=1, minute=00, second=0)]
	shift3_time = [time(hour=1, minute=0, second=1),time(hour=8, minute=0, second=0)]
	# shiftpp2_time = [time(hour=23, minute=32, second=0),time(hour=23, minute=59, second=0)]
	# shiftpp1_time = [time(hour=7, minute=0, second=0),time(hour=10, minute=0, second=0)]
	# shift2_cont_time = [time(hour=22, minute=1, second=0),time(hour=22, minute=59, second=0)]
	curtime = time(hour=nowtime.hour, minute=nowtime.minute, second=nowtime.second)
	shift_type = 'NA'
	if is_between(curtime,shift1_time):
		shift_type = '1'
	if is_between(curtime,shift2_time):
		shift_type = '2'
	# if is_between(curtime,shift2_cont_time):
	#     shift_type = '2'
	if is_between(curtime,shift3_time):
		shift_type = '3'
		shift_date = shift_date + timedelta(days=-1)
	# if is_between(curtime,shiftpp2_time):
	# 	shift_type = 'PP2'
	
	return shift_type


def is_between(time, time_range):
	if time_range[1] < time_range[0]:
		return time >= time_range[0] or time <= time_range[1]
	return time_range[0] <= time <= time_range[1]

	




	# def on_submit(self):
		
	# 	part_master = frappe.db.sql("""select tag_card_flow_master as tc from `tabTSAI Part Master` where mat_no ='%s' """%(self.mat_number),as_dict=1)[0]
	# 	name_f = part_master['tc']
	# 	doc = frappe.get_doc('Tag Card Flow Master', name_f)
	# 	children = doc.get('tag_card_workflow_table')
	# 	table = self.table_9
	# 	for t in table:
	# 		tab = frappe.new_doc("Tag Card")
	# 		tab.item_card_no = t.item_card_no
	# 		tab.production_order_qty = t.production_order
	# 		tab.mat_number = self.mat_number
	# 		tab.mat_name = self.mat_name
	# 		tab.part_number = self.part_number
	# 		tab.packing_std = t.packing_standard
	# 		tab.quantity = t.qty
	# 		tab.link_document = self.name
	# 		tab.supcode = self.supcode
	# 		tab.user_code = self.user_code
	# 		tab.user_name = self.user_name
	# 		tab.date = self.date
	# 		tab.time = self.time
	# 		tab.shift = self.shift
	# 		tab.current_workflow = children[0].workflow
	# 		tab.previous_workflow = children[0].workflow
	# 		tab.workflow = 1
	# 		tab.roleflow = 1
	# 		tab.production_line = self.production_line
	# 		tab.allowed_role = children[0].allowed_for
	# 		url = "http://apioso.thaisummit.co.th:10401/api/ProductionReceiptTagCard"
	# 		payload = json.dumps({
	# 		"receiptdate": self.date.strftime("%d-%m-%Y"),
	# 		"fgqty": t.qty,
	# 		"itemno": self.mat_number,
	# 		"tagcardno": t.item_card_no
	# 		})
	# 		headers = {
	# 		'API_KEY': '/1^i[#fhSSDnC8mHNTbg;h^uR7uZe#ninearin!g9D:pos+&terpTpdaJ$|7/QYups;==~w~!AWwb&DU',
	# 		'Content-Type': 'application/json'
	# 		}
	# 		response = requests.request("POST", url, headers=headers, data=payload)
	# 		res = json.loads(response.text)
	# 		frappe.log_error(res['Status'])
	# 		tab.status = res['Status']
	# 		tab.append('workflow_tracker_table',{
	# 			'flow_name': children[0].workflow,
	# 			'time':datetime.now().strftime('%H:%M:%S'),
	# 			'date':date.today(),
	# 			'user_name':self.user_name
	# 		})
	# 		tab.save(ignore_permissions=True)
	# 		frappe.db.commit()