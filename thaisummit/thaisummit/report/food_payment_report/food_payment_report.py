from datetime import datetime
import frappe
from frappe import _, msgprint
from frappe.utils import cstr, cint, getdate, get_last_day, get_first_day, add_days
from frappe.utils import cstr, add_days, date_diff, getdate, format_date


def execute(filters=None):
    columns,data = [],[]
    columns = get_columns(filters)
    data = get_data(filters)
    return columns, data

def get_columns(filters):
	columns = [
		_('Date') +':Data:100',_('Type') +':Data:200',_('Plan') +':Data:100',_('Actual') +':Data:100',_('Paid') +':Data:100',_('Rate') +':Data:100',_('Amount') +':Data:100'
	]
	return columns

def get_data(filters):
	data = []
	dates = get_dates(filters.from_date,filters.to_date)
	for date in dates:
		if filters.menu:
			food_menu = frappe.db.get_all('Food Menu',{'name':filters.menu},['*'])
		if not filters.menu:
			food_menu = frappe.db.get_all('Food Menu',['*'])
		for food in food_menu:
			if food.name == 'Break Fast':
				bf = frappe.db.exists('Food Plan',{'date':date})
				if bf:
					bf_count = frappe.db.get_value('Food Plan',{'date':date},['bf_head_count'])
					actual_food = frappe.db.count('Food Scan',{'date':date,'food':food.name})
					if actual_food > bf_count:
						paid = actual_food
						amount = actual_food * food.price
					else:
						paid = bf_count
						amount = bf_count * food.price
					row1 = [format_date(date),food.name,bf_count,actual_food,paid,food.price,amount]		
					data.append(row1)

			if food.name == 'Lunch':
				lu = frappe.db.exists('Food Plan',{'date':date})
				if lu:
					lu_count = frappe.db.get_value('Food Plan',{'date':date},['lu_head_count'])
					actual_food = frappe.db.count('Food Scan',{'date':date,'food':food.name})
					if actual_food > lu_count:
						paid = actual_food
						amount = actual_food * food.price
					else:
						paid = lu_count
						amount = lu_count * food.price
					row2 = [format_date(date),food.name,lu_count,actual_food,paid,food.price,amount]		
					data.append(row2)

			
			if food.name == 'Lunch Briyani Veg':
				lbv = frappe.db.exists('Food Plan',{'date':date})
				if lbv:
					lbv_count = frappe.db.get_value('Food Plan',{'date':date},['lbv_head_count'])
					actual_food = frappe.db.count('Food Scan',{'date':date,'food':food.name})
					if actual_food > lbv_count:
						paid = actual_food
						amount = actual_food * food.price
					else:
						paid = lbv_count
						amount = lbv_count * food.price
					row3 = [format_date(date),food.name,lbv_count,actual_food,paid,food.price,amount]		
					data.append(row3)

			if food.name == 'Lunch Briyani Non Veg':
				lbnv = frappe.db.exists('Food Plan',{'date':date})
				if lbnv:
					lbnv_count = frappe.db.get_value('Food Plan',{'date':date},['lbnv_head_count'])
					actual_food = frappe.db.count('Food Scan',{'date':date,'food':food.name})
					if actual_food > lbnv_count:
						paid = actual_food
						amount = actual_food * food.price
					else:
						paid = lbnv_count
						amount = lbnv_count * food.price
					row4 = [format_date(date),food.name,lbnv_count,actual_food,paid,food.price,amount]		
					data.append(row4)

			if food.name == 'Lunch Special Veg':
				lsv = frappe.db.exists('Food Plan',{'date':date})
				if lsv:
					lsv_count = frappe.db.get_value('Food Plan',{'date':date},['lsv_head_count'])
					actual_food = frappe.db.count('Food Scan',{'date':date,'food':food.name})
					if actual_food > lsv_count:
						paid = actual_food
						amount = actual_food * food.price
					else:
						paid = lsv_count
						amount = lsv_count * food.price
					row5 = [format_date(date),food.name,lsv_count,actual_food,paid,food.price,amount]		
					data.append(row5)

			if food.name == 'Lunch Special Non Veg':
				lsnv = frappe.db.exists('Food Plan',{'date':date})
				if lsnv:
					lsnv_count = frappe.db.get_value('Food Plan',{'date':date},['lsnv_head_count'])
					actual_food = frappe.db.count('Food Scan',{'date':date,'food':food.name})
					if actual_food > lsnv_count:
						paid = actual_food
						amount = actual_food * food.price
					else:
						paid = lsnv_count
						amount = lsnv_count * food.price
					row6 = [format_date(date),food.name,lsnv_count,actual_food,paid,food.price,amount]		
					data.append(row6)

			if food.name == 'Dinner':
				dn = frappe.db.exists('Food Plan',{'date':date})
				if dn:
					dn_count = frappe.db.get_value('Food Plan',{'date':date},['dn_head_count'])
					actual_food = frappe.db.count('Food Scan',{'date':date,'food':food.name})
					if actual_food > dn_count:
						paid = actual_food
						amount = actual_food * food.price
					else:
						paid = dn_count
						amount = dn_count * food.price
					row7 = [format_date(date),food.name,dn_count,actual_food,paid,food.price,amount]		
					data.append(row7)

			if food.name == 'Dinner Briyani Veg':
				dbv = frappe.db.exists('Food Plan',{'date':date})
				if dbv:
					dbv_count = frappe.db.get_value('Food Plan',{'date':date},['dbv_head_count'])
					actual_food = frappe.db.count('Food Scan',{'date':date,'food':food.name})
					if actual_food > dbv_count:
						paid = actual_food
						amount = actual_food * food.price
					else:
						paid = dbv_count
						amount = dbv_count * food.price
					row8 = [format_date(date),food.name,dbv_count,actual_food,paid,food.price,amount]		
					data.append(row8)

			if food.name == 'Dinner Briyani Non Veg':
				dbnv = frappe.db.exists('Food Plan',{'date':date})
				if dbnv:
					dbnv_count = frappe.db.get_value('Food Plan',{'date':date},['dbnv_head_count'])
					actual_food = frappe.db.count('Food Scan',{'date':date,'food':food.name})
					if actual_food > dbnv_count:
						paid = actual_food
						amount = actual_food * food.price
					else:
						paid = dbnv_count
						amount = dbnv_count * food.price
					row9 = [format_date(date),food.name,dbnv_count,actual_food,paid,food.price,amount]		
					data.append(row9)

			if food.name == 'Dinner Special Veg':
				dsv = frappe.db.exists('Food Plan',{'date':date})
				if dsv:
					dsv_count = frappe.db.get_value('Food Plan',{'date':date},['dsv_head_count'])
					actual_food = frappe.db.count('Food Scan',{'date':date,'food':food.name})
					if actual_food > dsv_count:
						paid = actual_food
						amount = actual_food * food.price
					else:
						paid = dsv_count
						amount = dsv_count * food.price
					row10 = [format_date(date),food.name,dsv_count,actual_food,paid,food.price,amount]		
					data.append(row10)

			if food.name == 'Dinner Special Non Veg':
				dsnv = frappe.db.exists('Food Plan',{'date':date})
				if dsnv:
					dsnv_count = frappe.db.get_value('Food Plan',{'date':date},['dsnv_head_count'])
					actual_food = frappe.db.count('Food Scan',{'date':date,'food':food.name})
					if actual_food > dsnv_count:
						paid = actual_food
						amount = actual_food * food.price
					else:
						paid = dsnv_count
						amount = dsnv_count * food.price
					row11 = [format_date(date),food.name,dsnv_count,actual_food,paid,food.price,amount]		
					data.append(row11)

			if food.name == 'Supper':
				sp = frappe.db.exists('Food Plan',{'date':date})
				if sp:
					sp_count = frappe.db.get_value('Food Plan',{'date':date},['sp_head_count'])
					actual_food = frappe.db.count('Food Scan',{'date':date,'food':food.name})
					if actual_food > sp_count:
						paid = actual_food
						amount = actual_food * food.price
					else:
						paid = sp_count
						amount = sp_count * food.price
					row12 = [format_date(date),food.name,sp_count,actual_food,paid,food.price,amount]		
					data.append(row12)

			if food.name == 'Supper Dates':
				sd = frappe.db.exists('Food Plan',{'date':date})
				if sd:
					sd_count = frappe.db.get_value('Food Plan',{'date':date},['sd_head_count'])
					actual_food = frappe.db.count('Food Scan',{'date':date,'food':food.name})
					if actual_food > sd_count:
						paid = actual_food
						amount = actual_food * food.price
					else:
						paid = sd_count
						amount = sd_count * food.price
					row13 = [format_date(date),food.name,sd_count,actual_food,paid,food.price,amount]		
					data.append(row13)

			if food.name == 'Supper Special Food':
				ssf = frappe.db.exists('Food Plan',{'date':date})
				if ssf:
					ssf_count = frappe.db.get_value('Food Plan',{'date':date},['ssf_head_count'])
					actual_food = frappe.db.count('Food Scan',{'date':date,'food':food.name})
					if actual_food > ssf_count:
						paid = actual_food
						amount = actual_food * food.price
					else:
						paid = ssf_count
						amount = ssf_count * food.price
					row14 = [format_date(date),food.name,ssf_count,actual_food,paid,food.price,amount]		
					data.append(row14)						

																										


	return data			
			


def get_dates(from_date,to_date):
    no_of_days = date_diff(add_days(to_date, 1), from_date)
    dates = [add_days(from_date, i) for i in range(0, no_of_days)]
    return dates
