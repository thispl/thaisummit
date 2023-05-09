# Copyright (c) 2022, TEAMPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class BulkSalarySlipDownload(Document):
	pass

# @frappe.whitelist()
# def get_slip(start_date,employee_type):
# 	data = []
# 	slip = frappe.db.get_list('Salary Slip',{'start_date':start_date,'employee_type':employee_type,'docstatus':('!=','2')},['name'])
# 	return slip

# @frappe.whitelist()
# def get_pdf_link(start_date,employee_type,doctype='Salary Slip', print_format='Salary Slip New', no_letterhead=0):
# 	list_url =[]
# 	slip = frappe.db.sql("""select name from `tabSalary Slip` where start_date='%s' and employee_type = '%s' and docstatus != '2' """%(start_date,employee_type),as_dict=1)
# 	for s in slip:
# 		frappe.errprint(s.name)
# 		list_url.append('https://182.156.241.11/api/method/frappe.utils.print_format.download_pdf?doctype={doctype}&name={docname}&format={print_format}&no_letterhead={no_letterhead}'.format(
# 			doctype = doctype,
# 			docname = s.name,
# 			print_format = print_format,
# 			no_letterhead = no_letterhead
# 		))
# 	return list_url

# import requests
# @frappe.whitelist()
# def download_pdfs(start_date, employee_type):
#     urls = get_pdf_link(start_date, employee_type)
#     for url in urls:
#         response = requests.get(url, verify=False)
#         filename = url.split("=")[-1] + ".pdf"
#         with open(filename, "wb") as file:
#             file.write(response.content)



