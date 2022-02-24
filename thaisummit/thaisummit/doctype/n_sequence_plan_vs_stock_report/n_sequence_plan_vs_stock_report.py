# Copyright (c) 2021, TEAMPRO and contributors
# For license information, please see license.txt

from typing import DefaultDict
import frappe
from frappe.utils import cstr, add_days, date_diff, format_datetime, format_date
from frappe import _
from frappe.utils.csvutils import UnicodeWriter, read_csv_content
from frappe.utils.file_manager import get_file
from frappe.model.document import Document
from frappe.utils.background_jobs import enqueue
from frappe.utils import today
import datetime
from datetime import datetime

class NSequencePlanvsStockReport(Document):
    @frappe.whitelist()
    def get_html_data(self):
        if self.date:
            from_date = self.date
        else:
            from_date = today()

        to_date = from_date

        no_of_days = date_diff(add_days(to_date, 1), from_date)
        dates = [add_days(from_date, i) for i in range(0, no_of_days)]

        header = "<table class='table tabe-bordered'><tr><td colspan='4' style='background-color:#FEF701;border: 1px solid black;font-size:18px;padding:0px'><center><b>N SEQUENCE PLAN VS STOCK REPORT</b></center></td><td style='background-color:#FA8072;border: 1px solid black;font-size:18px;padding:0px'><center><b>DELIVERY PLAN</b></center></td><td colspan='5' style='background-color:#52c132;border: 1px solid black;font-size:18px;padding:0px'><center><b>STOCK</b></center></td><td colspan='3' style='border: 1px solid black;font-size:18px;padding:0px'><center><b>%s</b></center></td></tr>"%today()

        d1 = datetime.strptime(dates[0],'%Y-%m-%d')
        d1 = d1.strftime('%d/%m')
        header += "<tr><td style='border: 1px solid black;padding:1px;text-align: center;'><b style='text-align: center;'>MAT NO</b></td><td style='border: 1px solid black;padding:1px;text-align: center;'><b>PART NO</b></td><td style='border: 1px solid black;padding:1px;text-align: center;'><b>PART NAME</b></td><td style='border: 1px solid black;padding:1px;text-align: center;'><b>DAILY ORDER</b></td><td style='border: 1px solid black;padding:1px;text-align: center;'><b>%s</b></td><td style='border: 1px solid black;padding:1px';text-align: center;><b>FG</b></td><td style='border: 1px solid black;padding:1px;text-align: center;'><b>WELD</b></td><td style='border: 1px solid black;padding:1px;text-align: center;'><b>HPS</b></td><td style='border: 1px solid black;padding:1px;text-align: center;'><b>TOTAL STOCK</b></td><td style='border: 1px solid black;padding:1px;text-align: center;'><b>COVERAGE</b></td><td style='border: 1px solid black;padding:1px;text-align: center;'><b>SHORT</b></td><td style='border: 1px solid black;padding:1px;text-align: center;'><b>PROD PLAN</b></td><td style='border: 1px solid black;padding:1px;text-align: center;'><b>STATUS</b></td></tr>"%(d1)

        data = get_data(from_date,to_date)

        html = header + data + "</table>"

        return html

def get_data(from_date,to_date):
    data = ''
    no_of_days = date_diff(add_days(to_date, 1), from_date)
    dates = [add_days(from_date, i) for i in range(0, no_of_days)]
    master = frappe.db.sql("""select DISTINCT mat_no, part_no,part_name from `tabTSA Master` where date between '%s' and '%s' and mat_no is not null """%(from_date,to_date),as_dict=True)
    for m in master:
        daily_order = frappe.db.sql("""select sum(quantity) as total from `tabTSA Master` where mat_no = '%s' and date between '%s' and '%s' """%(m.mat_no,from_date,to_date),as_dict=True)[0].total or 0
        row = "<tr><td style='border: 1px solid black;padding:2px;'>%s</td><td style='border: 1px solid black;padding:2px;'>%s</td><td style='border: 1px solid black;padding:2px;'>%s</td>"%(m.mat_no,m.part_no,m.part_name)
        days = 0
        qty_list = ''
        for date in dates:
            qty = frappe.db.get_value('TSA Master',{'mat_no':m.mat_no,'date':date},'quantity') or '-'
            if qty != '-':
                days += 1
            qty_list += "<td style='border: 1px solid black;padding:2px;'>%s</td>"%(qty)
        row += qty_list
        row += "<td style='border: 1px solid black;padding:2px;'>%s</td>"%daily_order
        # fg = frappe.db.get_value('SAP Outgoing Report',{'part_no':m.mat_no,'wh':'FG'},'quantity') or '-'
        # weld = frappe.db.get_value('SAP Outgoing Report',{'part_no':m.mat_no,'wh':'Weld'},'quantity') or '-'
        # hps = frappe.db.get_value('SAP Outgoing Report',{'part_no':m.mat_no,'wh':'HPS'},'quantity') or '-'
        fg = frappe.db.get_value('TSAI Stock',{'item_no':m.mat_no,'wh':'FG'},'qty') or '-'
        weld = frappe.db.get_value('TSAI Stock',{'item_no':m.mat_no,'wh':'Weld'},'qty') or '-'
        hps = frappe.db.get_value('TSAI Stock',{'item_no':m.mat_no,'wh':'HPS'},'qty') or '-'
        total_stock = 0
        fg_stock = 0
        if type(fg) == int:
            total_stock += fg
            fg_stock += fg
        if type(weld) == int:
            total_stock += weld
        if type(hps) == int:
            total_stock += hps
        if daily_order > 0:
            coverage = round(fg_stock/(daily_order/days),1)
        else:
            coverage = 0
        short = daily_order - total_stock
        if short < 0:
            short = 0
        prod_plan = frappe.db.get_value('SAP Production Plan',{'product_no':m.mat_no,'order_date':today()},'planned_quantity') or '-'
        status = ''
        if type(prod_plan) == int:
            if prod_plan < int(daily_order):
                status = 'Check'
                check_clr = '#FF0000'
            else:
                status = 'OK'
                check_clr = '#FFFFFF'
        else:
            status = 'Check'
            check_clr = '#FF0000'
        row += "<td style='border: 1px solid black;padding:2px;'>%s</td><td style='border: 1px solid black;padding:2px;'>%s</td><td style='border: 1px solid black;padding:2px;'>%s</td><td style='border: 1px solid black;padding:2px;'>%s</td><td style='border: 1px solid black;padding:2px;'>%s</td><td style='border: 1px solid black;padding:2px;'>%s</td><td style='border: 1px solid black;padding:2px;'>%s</td><td style='border: 1px solid black;padding:2px;background-color:%s'>%s</td>"%(fg,weld,hps,total_stock,coverage,short,prod_plan,check_clr,status)
        # upcoming_qty1 = frappe.db.get_value('TSA Master',{'mat_no':m.mat_no,'date':add_days(to_date,1)},'quantity') or '-'
        # upcoming_qty2 = frappe.db.get_value('TSA Master',{'mat_no':m.mat_no,'date':add_days(to_date,2)},'quantity') or '-'
        # row += "<td style='border: 1px solid black;padding:2px;'>%s</td><td style='border: 1px solid black;padding:2px;'>%s</td>"%(upcoming_qty1,upcoming_qty2)
        data += row + "</tr>"
    return data