from __future__ import unicode_literals

import frappe, os, json
from frappe import _

from frappe.utils.pdf import get_pdf,cleanup
from frappe.core.doctype.access_log.access_log import make_access_log
from frappe.utils import now_datetime, formatdate,random_string

from PyPDF2 import PdfFileWriter
from frappe.utils.background_jobs import enqueue

no_cache = 1

base_template_path = "templates/www/printview.html"
standard_format = "templates/print_formats/standard.html"

from frappe.www.printview import validate_print_permission


@frappe.whitelist()
def enqueue_download_multi_pdf(start_date,employee_type):
	frappe.errprint(start_date)
	frappe.errprint(employee_type)
	result = frappe.db.sql("SELECT name FROM `tabSalary Slip` WHERE start_date = '%s' AND employee_type = '%s'" % (start_date, employee_type), as_dict=True)
	salary_slips = [row.name for row in result]
	# result = frappe.db.sql("Select name from `tabSalary Slip` where start_date = '%s' and employee_type = '%s'" % (start_date,employee_type),as_list=1)
	# salary_slips = []
	# for i in result:
	# 	salary_slips = i.name
	# frappe.errprint(salary_slips)
	enqueue(download_multi_pdf, queue='default', timeout=15000, event='download_multi_pdf',doctype="Salary Slip", name=json.dumps(salary_slips), format='Salary Slip New')
	frappe.msgprint("Bulk Salary Slip Download is successsfully Initiated. Kindly wait for sometime and refresh the page.")


@frappe.whitelist()
def download_multi_pdf(doctype, name, format=None, no_letterhead=0,letterhead=None, options=None):
	"""
	Concatenate multiple docs as PDF .

	Returns a PDF compiled by concatenating multiple documents. The documents
	can be from a single DocType or multiple DocTypes

	Note: The design may seem a little weird, but it exists exists to
		ensure backward compatibility. The correct way to use this function is to
		pass a dict to doctype as described below

	NEW FUNCTIONALITY
	=================
	Parameters:
	doctype (dict):
		key (string): DocType name
		value (list): of strings of doc names which need to be concatenated and printed
	name (string):
		name of the pdf which is generated
	format:
		Print Format to be used

	Returns:
	PDF: A PDF generated by the concatenation of the mentioned input docs

	OLD FUNCTIONALITY - soon to be deprecated
	=========================================
	Parameters:
	doctype (string):
		name of the DocType to which the docs belong which need to be printed
	name (string or list):
		If string the name of the doc which needs to be printed
		If list the list of strings of doc names which needs to be printed
	format:
		Print Format to be used

	Returns:
	PDF: A PDF generated by the concatenation of the mentioned input docs
	"""

	import json
	output = PdfFileWriter()

	if not isinstance(doctype, dict):
		result = json.loads(name)

		# Concatenating pdf files
		for i, ss in enumerate(result):
			output = frappe.get_print(doctype, ss, format, as_pdf = True, output = output, no_letterhead=no_letterhead)
		filename = "{doctype}.pdf".format(doctype=doctype.replace(" ", "-").replace("/", "-"))
	else:
		for doctype_name in doctype:
			for doc_name in doctype[doctype_name]:
				try:
					output = frappe.get_print(doctype_name, doc_name, format, as_pdf = True, output = output, no_letterhead=no_letterhead)
				except Exception:
					frappe.log_error("Permission Error on doc {} of doctype {}".format(doc_name, doctype_name))
		filename = "{}.pdf".format(name)

	ret = frappe.get_doc({
			"doctype": "File",
			"attached_to_name": 'Download Bulk Salary Slip',
			"attached_to_doctype": 'Download Bulk Salary Slip',
			"attached_to_field": 'salary_slip',
			"file_name": filename,
			"is_private": 0,
			"content": read_multi_pdf(output),
			"decode": False
		})
	ret.save(ignore_permissions=True)
	frappe.db.commit()
	attached_file = frappe.get_doc("File", ret.name)
	frappe.db.set_value('Download Bulk Salary Slip',None,'salary_slip',attached_file.file_url)
	frappe.db.set_value('Download Bulk Salary Slip',None,'last_download_on',now_datetime())
	frappe.local.response.filecontent = read_multi_pdf(output)
	frappe.local.response.type = "download"

def read_multi_pdf(output):
	# Get the content of the merged pdf files
	fname = os.path.join("/tmp", "frappe-pdf-{0}.pdf".format(frappe.generate_hash()))
	output.write(open(fname,"wb"))

	with open(fname, "rb") as fileobj:
		filedata = fileobj.read()
	return filedata