# Copyright (c) 2021, TEAMPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import cstr, add_days, date_diff, getdate, format_date
from datetime import datetime

class DailySalesReport(Document):
	@frappe.whitelist()
	def get_data(self):
		columns = 0
		group_header = """<tr><td rowspan=2 style="background-color:#fafa13; border: 1px solid black; font-size:9px; padding:1px;"><b><center>Date</center></b></td><td rowspan=2 style="background-color:#fafa13; border: 1px solid black; font-size:9px; padding:1px;">Day</td>
		<td style="background-color:#fafa13; border: 1px solid black; font-size:9px; padding:1px;">IYM</td>"""
		customer_header = '<tr><td style="background-color:#fafa13; border: 1px solid black; font-size:9px; padding:1px;">HPS</td>'
		groups = ['IYM','RE','FORD']
		for g in groups:
			customer = frappe.db.sql("""select short_name from `tabTSAI Customer` where running is not null and customer_group = '%s' order by running """%(g),as_dict=True)
			for c in customer:
				group_header += '<td style="background-color:#fafa13; border: 1px solid black; font-size:9px; padding:1px;"><center><b>%s</b><center></td>'%g
				customer_header += '<td style="background-color:#fafa13; border: 1px solid black; font-size:9px; padding:1px;"><center><b>%s</b></center></td>'%c.short_name
				columns += 1
			group_header += '<td rowspan=2 style="background-color:#FFBF00; border: 1px solid black; font-size:9px; padding:1px;"><center><b>TOTAL \n%s</b></center></td>'% str(g)
		group_header += '<td rowspan=2 style="background-color:#7dcea0; border: 1px solid black; font-size:9px; padding:1px;"><center><b>TOTAL</b></center></td>'
		data = """<table><tr><td colspan=%s style="background-color:#fafa13; border: 1px solid black; font-size:15px; padding:1px;"><center><b>DAILY SALES REPORT</b></center></td></tr>"""%(columns+7)
		data += group_header + '</tr>'
		data += customer_header + '</tr>'

		hps_parts = ('10000289','10000290','10000291','10000335','10000336','10000337','10000338')
		dates = get_dates(self)
		hps_total = 0
		for date in dates:
			row = '<tr>'
			row_total = 0
			dt = datetime.strptime(date,'%Y-%m-%d')
			d = dt.strftime('%d-%b-%Y')
			day = datetime.date(dt).strftime('%a')
			hps_out = frappe.db.sql(""" select sum(sales_value) as sales_value from `tabSAP Outgoing Report` where ar_invoice_date = '%s' and part_no in %s and customer_ref_no not like '_________/O/%%' """%(date,hps_parts),as_dict=True)
			if hps_out[0].sales_value is not None:
				hps_total += hps_out[0].sales_value
				hps_out = hps_out[0].sales_value
				row += '<td style="border: 1px solid black; font-size:9px; padding:1px;" nowrap>%s</td><td style="border: 1px solid black; font-size:9px; padding:1px;">%s</td><td style="border: 1px solid black; font-size:9px; padding:1px;">%s</td>'%(d,day,'{:,}'.format(round(hps_out)))
			else:
				hps_out = 0
				row += '<td style="border: 1px solid black; font-size:9px; padding:1px;">%s</td><td style="border: 1px solid black; font-size:9px; padding:1px;">%s</td><td style="border: 1px solid black; font-size:9px; padding:1px;">-</td>'%(d,day)
			for g in groups:
				customer = frappe.db.sql("""select short_name from `tabTSAI Customer` where running is not null and customer_group = '%s' order by running """%(g),as_dict=True)
				sap_total = 0
				for c in customer:
					sap_out = frappe.db.sql("""select sum(sales_value) as sales_value from `tabSAP Outgoing Report` where ar_invoice_date = '%s' and short_name = '%s' and customer_ref_no not like '_________/O/%%' """%(date,c.short_name),as_dict=True)
					if sap_out[0].sales_value is not None:
						row += '<td style="border: 1px solid black; font-size:9px; padding:1px;">%s</td>'%'{:,}'.format((round(sap_out[0].sales_value)))
						sap_total += sap_out[0].sales_value + hps_out
						row_total += sap_out[0].sales_value + hps_out
					else:
						row += '<td style="border: 1px solid black; font-size:9px; padding:1px;">-</td>'
					hps_out = 0
				if sap_total == 0:
					row += '<td style="background-color:#FFBF00;border: 1px solid black; font-size:9px; padding:1px;">-</td>'
				else:
					row += '<td style="background-color:#FFBF00;border: 1px solid black; font-size:9px; padding:1px;">%s</td>'%'{:,}'.format(round(sap_total))
			if row_total == 0:
				row += '<td style="background-color:#7dcea0;border: 1px solid black; font-size:9px; padding:1px;">-</td>'
			else:
				row += '<td style="background-color:#7dcea0;border: 1px solid black; font-size:9px; padding:1px;">%s</td>'%'{:,}'.format(round(row_total))

			data += row
		total = '</tr><tr><td colspan=2 style="background-color:#fafa13; border: 1px solid black; font-size:9px; padding:1px;">TOTAL</td><td style="background-color:#fafa13; border: 1px solid black; font-size:9px; padding:1px;">%s</td>'%'{:,}'.format(round(hps_total))
		overall_total = 0
		for g in groups:
			customer = frappe.db.sql("""select short_name from `tabTSAI Customer` where running is not null and customer_group = '%s' order by running """%(g),as_dict=True)
			sap_total = 0
			for c in customer:
				sap_out = frappe.db.sql(""" select sum(sales_value) as sales_value from `tabSAP Outgoing Report` where ar_invoice_date in %s and short_name = '%s' and customer_ref_no not like '_________/O/%%' """%(tuple(dates),c.short_name),as_dict=True)
				if sap_out[0].sales_value is not None:
					total += '<td style="background-color:#fafa13; border: 1px solid black; font-size:9px; padding:1px;">%s</td>'%'{:,}'.format(round(sap_out[0].sales_value))
					sap_total += sap_out[0].sales_value + hps_total
					overall_total += sap_out[0].sales_value + hps_total
				else:
					total += '<td style="background-color:#fafa13; border: 1px solid black; font-size:9px; padding:1px;">-</td>'
				hps_total = 0
			if sap_total == 0:
				total += '<td style="background-color:#fafa13; border: 1px solid black; font-size:9px; padding:1px;">-</td>'
			else:
				total += '<td style="background-color:#fafa13; border: 1px solid black; font-size:9px; padding:1px;">%s</td>'%'{:,}'.format(round(sap_total))
		if overall_total == 0:
			total += '<td style="background-color:#fafa13; border: 1px solid black; font-size:9px; padding:1px;">-</td>'
		else:
			total += '<td style="background-color:#fafa13; border: 1px solid black; font-size:9px; padding:1px;">%s</td>'%'{:,}'.format(round(overall_total))
		data += total + '</tr></table>'
			
		return data

def get_dates(self):
	no_of_days = date_diff(add_days(self.to_date, 1), self.from_date)
	dates = [add_days(self.from_date, i) for i in range(0, no_of_days)]
	return dates