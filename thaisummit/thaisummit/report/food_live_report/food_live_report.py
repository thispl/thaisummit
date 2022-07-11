# Copyright (c) 2013, TEAMPRO and contributors
# For license information, please see license.txt

from datetime import datetime
import frappe
from frappe import _, msgprint
from frappe.utils import cstr, cint, getdate, get_last_day, get_first_day, add_days
from frappe.utils import cstr, add_days, date_diff, getdate, format_date


def execute(filters=None):
	columns = get_columns()
	data = []
	food_plan = get_data(filters)
	for food in food_plan:
		data.append(food)
	return columns, data

def get_columns():
	columns = [
		_('Date') +':Data:100',_('Type') +':Data:200',_('Plan') +':Data:100',_('Actual') +':Data:100',_('Paid') +':Data:100',_('Rate') +':Data:100',_('Amount') +':Data:100'
	]
	return columns

def get_data(filters):
	food_menu = frappe.db.get_all('Food Menu',['*'])
	data = []
	dates = get_dates(filters.from_date,filters.to_date)
	for date in dates:
		food_menu = frappe.db.get_value('Food Menu',['*'])
		for food in food_menu:
			if food.name == 'Break Fast':
				food_plan = frappe.db.get_value('Food Plan',{'date':date},['bf_head_count'])
				actual_food = frappe.db.count('Food Scan',{'date':date,'food':food.name})
				if actual_food > food_plan:
					paid = actual_food
					amount = actual_food * food.price
				else:
					paid = food_plan
					amount = food_plan * food.price	
				row1 = [date,food.name,food_plan,actual_food,paid,food.price,amount]
				data.append(row1)
	return data	
	# for food in food_menu:
		
		# for date in dates:
		# 	# date_format = datetime.strptime(str(date),'%Y-%m-%d').strftime('%d-%m-%Y')
		# 	if food.name == 'Break Fast':
		# 		food_plan = frappe.db.get_value('Food Plan',{'date':date},['bf_head_count'])
		# 		actual_food = frappe.db.count('Food Scan',{'date':date,'food':food.name})
		# 		if actual_food > food_plan:
		# 			paid = actual_food
		# 			amount = actual_food * food.price
		# 		else:
		# 			paid = food_plan
		# 			amount = food_plan * food.price	
		# 		row1 = [date,food.name,food_plan,actual_food,paid,food.price,amount]
		# 		data.append(row1)
		# return data		

			# if food.name == 'Lunch':
			# 	food_plan = frappe.db.get_value('Food Plan',{'date':filters.from_date},['lu_head_count'])
			# 	actual_food = frappe.db.count('Food Scan',{'date':filters.from_date,'food':food.name})
			# 	if actual_food > food_plan:
			# 		paid = actual_food
			# 		amount = actual_food * food.price
			# 	else:
			# 		paid = food_plan
			# 		amount = food_plan * food.price	
			# 	row2 = [date_format,food.name,food_plan,actual_food,paid,food.price,amount]
			# 	data.append(row2)

			# if food.name == 'Lunch Briyani Veg':
			# 	food_plan = frappe.db.get_value('Food Plan',{'date':filters.from_date},['lbv_head_count'])
			# 	actual_food = frappe.db.count('Food Scan',{'date':filters.from_date,'food':food.name})
			# 	if actual_food > food_plan:
			# 		paid = actual_food
			# 		amount = actual_food * food.price
			# 	else:
			# 		paid = food_plan
			# 		amount = food_plan * food.price	
			# 	row3 = [date_format,food.name,food_plan,actual_food,paid,food.price,amount]
			# 	data.append(row3)

			# if food.name == 'Lunch Briyani Non Veg':
			# 	food_plan = frappe.db.get_value('Food Plan',{'date':filters.from_date},['lbnv_head_count'])
			# 	actual_food = frappe.db.count('Food Scan',{'date':filters.from_date,'food':food.name})
			# 	if actual_food > food_plan:
			# 		paid = actual_food
			# 		amount = actual_food * food.price
			# 	else:
			# 		paid = food_plan
			# 		amount = food_plan * food.price	
			# 	row4 = [date_format,food.name,food_plan,actual_food,paid,food.price,amount]
			# 	data.append(row4)

			# if food.name == 'Lunch Special Veg':
			# 	food_plan = frappe.db.get_value('Food Plan',{'date':filters.from_date},['lsv_head_count'])
			# 	actual_food = frappe.db.count('Food Scan',{'date':filters.from_date,'food':food.name})
			# 	if actual_food > food_plan:
			# 		paid = actual_food
			# 		amount = actual_food * food.price
			# 	else:
			# 		paid = food_plan
			# 		amount = food_plan * food.price	
			# 	row5 = [date_format,food.name,food_plan,actual_food,paid,food.price,amount]
			# 	data.append(row5)

			# if food.name == 'Lunch Special Non Veg':
			# 	food_plan = frappe.db.get_value('Food Plan',{'date':filters.from_date},['lsnv_head_count'])
			# 	actual_food = frappe.db.count('Food Scan',{'date':filters.from_date,'food':food.name})
			# 	if actual_food > food_plan:
			# 		paid = actual_food
			# 		amount = actual_food * food.price
			# 	else:
			# 		paid = food_plan
			# 		amount = food_plan * food.price	
			# 	row6 = [date_format,food.name,food_plan,actual_food,paid,food.price,amount]
			# 	data.append(row6)

			# if food.name == 'Dinner':
			# 	food_plan = frappe.db.get_value('Food Plan',{'date':filters.from_date},['dn_head_count'])
			# 	actual_food = frappe.db.count('Food Scan',{'date':filters.from_date,'food':food.name})
			# 	if actual_food > food_plan:
			# 		paid = actual_food
			# 		amount = actual_food * food.price
			# 	else:
			# 		paid = food_plan
			# 		amount = food_plan * food.price	
			# 	row7 = [date_format,food.name,food_plan,actual_food,paid,food.price,amount]
			# 	data.append(row7)

			# if food.name == 'Dinner Briyani Veg':
			# 	food_plan = frappe.db.get_value('Food Plan',{'date':filters.from_date},['dbv_head_count'])
			# 	actual_food = frappe.db.count('Food Scan',{'date':filters.from_date,'food':food.name})
			# 	if actual_food > food_plan:
			# 		paid = actual_food
			# 		amount = actual_food * food.price
			# 	else:
			# 		paid = food_plan
			# 		amount = food_plan * food.price	
			# 	row8 = [date_format,food.name,food_plan,actual_food,paid,food.price,amount]
			# 	data.append(row8)

			# if food.name == 'Dinner Briyani Non Veg':
			# 	food_plan = frappe.db.get_value('Food Plan',{'date':filters.from_date},['dbnv_head_count'])
			# 	actual_food = frappe.db.count('Food Scan',{'date':filters.from_date,'food':food.name})
			# 	if actual_food > food_plan:
			# 		paid = actual_food
			# 		amount = actual_food * food.price
			# 	else:
			# 		paid = food_plan
			# 		amount = food_plan * food.price	
			# 	row9 = [date_format,food.name,food_plan,actual_food,paid,food.price,amount]
			# 	data.append(row9)

			# if food.name == 'Dinner Special Veg':
			# 	food_plan = frappe.db.get_value('Food Plan',{'date':filters.from_date},['dsv_head_count'])
			# 	actual_food = frappe.db.count('Food Scan',{'date':filters.from_date,'food':food.name})
			# 	if actual_food > food_plan:
			# 		paid = actual_food
			# 		amount = actual_food * food.price
			# 	else:
			# 		paid = food_plan
			# 		amount = food_plan * food.price	
			# 	row10 = [date_format,food.name,food_plan,actual_food,paid,food.price,amount]
			# 	data.append(row10)

			# if food.name == 'Dinner Special Non Veg':
			# 	food_plan = frappe.db.get_value('Food Plan',{'date':filters.from_date},['dsnv_head_count'])
			# 	actual_food = frappe.db.count('Food Scan',{'date':filters.from_date,'food':food.name})
			# 	if actual_food > food_plan:
			# 		paid = actual_food
			# 		amount = actual_food * food.price
			# 	else:
			# 		paid = food_plan
			# 		amount = food_plan * food.price	
			# 	row11 = [date_format,food.name,food_plan,actual_food,paid,food.price,amount]
			# 	data.append(row11)

			# if food.name == 'Supper':
			# 	food_plan = frappe.db.get_value('Food Plan',{'date':filters.from_date},['sp_head_count'])
			# 	actual_food = frappe.db.count('Food Scan',{'date':filters.from_date,'food':food.name})
			# 	if actual_food > food_plan:
			# 		paid = actual_food
			# 		amount = actual_food * food.price
			# 	else:
			# 		paid = food_plan
			# 		amount = food_plan * food.price	
			# 	row12 = [date_format,food.name,food_plan,actual_food,paid,food.price,amount]
			# 	data.append(row12)

			# if food.name == 'Supper Dates':
			# 	food_plan = frappe.db.get_value('Food Plan',{'date':filters.from_date},['sd_head_count'])
			# 	actual_food = frappe.db.count('Food Scan',{'date':filters.from_date,'food':food.name})
			# 	if actual_food > food_plan:
			# 		paid = actual_food
			# 		amount = actual_food * food.price
			# 	else:
			# 		paid = food_plan
			# 		amount = food_plan * food.price	
			# 	row13 = [date_format,food.name,food_plan,actual_food,paid,food.price,amount]
			# 	data.append(row13)

			# if food.name == 'Supper Special Food':
			# 	food_plan = frappe.db.get_value('Food Plan',{'date':filters.from_date},['ssf_head_count'])
			# 	actual_food = frappe.db.count('Food Scan',{'date':filters.from_date,'food':food.name})
			# 	if actual_food > food_plan:
			# 		paid = actual_food
			# 		amount = actual_food * food.price
			# 	else:
			# 		paid = food_plan
			# 		amount = food_plan * food.price	
			# 	row14 = [date_format,food.name,food_plan,actual_food,paid,food.price,amount]
			# 	data.append(row14)					

		# return data


def get_dates(from_date,to_date):
    no_of_days = date_diff(add_days(to_date, 1), from_date)
    dates = [add_days(from_date, i) for i in range(0, no_of_days)]
    return dates