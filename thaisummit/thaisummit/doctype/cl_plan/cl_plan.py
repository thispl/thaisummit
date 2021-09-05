# Copyright (c) 2021, TEAMPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import cstr, add_days, date_diff, getdate
from frappe import _
from frappe.utils.csvutils import UnicodeWriter, read_csv_content
from frappe.utils.file_manager import get_file
from frappe.model.document import Document
from frappe.utils.background_jobs import enqueue
from datetime import datetime,timedelta,date,time
from frappe.utils import format_date

class CLPlan(Document):
	pass


@frappe.whitelist()
def validate_csv(from_date,to_date,file):
	cl_plan = frappe.db.sql("""select name from `tabCL Head Count Plan` where date between '%s' and '%s' """%(from_date,to_date),as_dict=True)
	if cl_plan:
		frappe.throw('CL Plan already submitted for the selected date')
	filepath = get_file(file)
	pps = read_csv_content(filepath[1])

	for pp in pps:
		if pp[0] != 'Date':
			if pp[0]:
				if not frappe.db.exists("Contractor",{'name':pp[1]}):
					err_list ='<li><font color="red">Contractor<b>%s</b></font> not Found. </li>'%(pp[1])
					frappe.throw(err_list)


@frappe.whitelist()
def create_cl_head_count_plan(file):
	filepath = get_file(file)
	pps = read_csv_content(filepath[1])
	for pp in pps:
		if pp[0] != 'Date':
			date = datetime.strptime(pp[0], '%d-%m-%Y').date()
			frappe.errprint(date)
			doc = frappe.new_doc('CL Head Count Plan')
			doc.date = date
			doc.contractor = pp[1]
			doc.shift_1 = pp[2]
			doc.shift_2 = pp[3]
			doc.shift_3 = pp[4]
			doc.shift_pp1 = pp[5]
			doc.shift_pp2 = pp[6]
			doc.save(ignore_permissions=True)
			frappe.db.commit()
	frappe.msgprint('CL Plan Submitted Successfully')


@frappe.whitelist()
def get_template():
	args = frappe.local.form_dict

	if getdate(args.from_date) > getdate(args.to_date):
		frappe.throw(_("To Date should be greater than From Date"))

	w = UnicodeWriter()
	w = add_header(w)

	w = add_data(w, args)
	# write out response as a type csv
	frappe.response['result'] = cstr(w.getvalue())
	frappe.response['type'] = 'csv'
	frappe.response['doctype'] = "CL Plan"

@frappe.whitelist()
def add_header(w):
	w.writerow(["Date","Contractor","1","2","3","PP1","PP2"])
	return w

@frappe.whitelist()
def add_data(w, args):
	data = get_data(args)
	writedata(w, data)
	return w

@frappe.whitelist()
def get_data(args):
	dates = get_dates(args)
	data = []
	for date in dates:
		contractors = frappe.get_all('Contractor')
		for contractor in contractors:
			row = [format_date(date),contractor.name]
			data.append(row)
	return data


@frappe.whitelist()
def writedata(w, data):
	for row in data:
		w.writerow(row)

def get_dates(args):
	no_of_days = date_diff(add_days(args.to_date, 1), args.from_date)
	dates = [add_days(args.from_date, i) for i in range(0, no_of_days)]
	return dates
