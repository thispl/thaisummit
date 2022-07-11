from xxlimited import foo
import frappe
from frappe import _, msgprint
from frappe.utils import cstr, add_days, date_diff, getdate, format_date
from frappe.utils.data import filter_strip_join
from numpy import format_float_positional
from thaisummit.thaisummit.doctype.food_plan.food_plan import FoodPlan

def execute(filters=None):
	columns = get_columns()
	data = []
	food_plan = get_data(filters)
	for food in food_plan:
		data.append(food)
	return columns, data
	
def get_columns():
	columns  = [
		_('Date') +':Date:100',_('Type') +':Data:100',_('Plan(count)') +':Data:100',_('Actual(count)') +':Data:100',_('Paid(count)') +':Data:100',_('Rate') +':Currency:100',_('Amount') +':Currency:100'
	]
	return columns

def get_data(filters):
	data = []
	meal_type = ['Break Fast','Lunch','Special(Veg)','Special(Non Veg)','Dinner','Supper']
	food_plan = frappe.db.get_all('Food Plan',{'date':('between',(filters.date,filters.to_date))},['*'],order_by='date asc')
	# frappe.errprint(food_plan)
	for fp in food_plan:
		price_plan = frappe.get_list("Price Plan",{'date':fp.date},['*'])
		#Break Fast
		breakfast_rate = price_plan[0]['break_fast']
		bf_actual_count = frappe.db.count("Food Scan",{'date':fp.date,'type':meal_type[0]})
		bf_payable_count = max(fp.break_fast,bf_actual_count)
		bf_amount = bf_payable_count * breakfast_rate
		#Lunch
		lunch_rate = price_plan[0]['lunch']
		lunch_actual_count = frappe.db.count("Food Scan",{'date':fp.date,'type':meal_type[1]})
		lunch_payable_count = max(fp.lunch,lunch_actual_count)
		lunch_amount = lunch_payable_count * lunch_rate
		#Special(Veg)
		special_veg_rate = price_plan[0]['special_veg']
		special_veg_actual_count = frappe.db.count("Food Scan",{'date':fp.date,'type':meal_type[2]})
		special_veg_payable_count = max(fp.special_veg,special_veg_actual_count)
		special_veg_amount = special_veg_payable_count * special_veg_rate
		#Special(Non Veg)
		special_nonveg_rate = price_plan[0]['special_nonveg']
		special_nonveg_actual_count = frappe.db.count("Food Scan",{'date':fp.date,'type':meal_type[3]})
		special_nonveg_payable_count = max(fp.special_nonveg,special_nonveg_actual_count)
		special_nonveg_amount = bf_payable_count * special_nonveg_rate
		#Dinner
		dinner_rate = price_plan[0]['dinner']
		dinner_actual_count = frappe.db.count("Food Scan",{'date':fp.date,'type':meal_type[4]})
		dinner_payable_count = max(fp.dinner,dinner_actual_count)
		dinner_amount = dinner_payable_count * dinner_rate
		#Supper
		supper_rate = price_plan[0]['supper']
		supper_actual_count = frappe.db.count("Food Scan",{'date':fp.date,'type':meal_type[5]})
		supper_payable_count = max(fp.supper,supper_actual_count)
		supper_amount = supper_payable_count * supper_rate
		# frappe.errprint(amount)
		# frappe.errprint(price_plan)
		row1 = [fp.date,meal_type[0],fp.break_fast,bf_actual_count,bf_payable_count,price_plan[0]['break_fast'],bf_amount]
		row2 = [fp.date,meal_type[1],fp.lunch,lunch_actual_count,lunch_payable_count,price_plan[0]['lunch'],lunch_amount]
		row3 = [fp.date,meal_type[2],fp.special_veg,special_veg_actual_count,special_veg_payable_count,price_plan[0]['special_veg'],special_veg_amount]
		row4 = [fp.date,meal_type[3],fp.special_nonveg,special_nonveg_actual_count,special_nonveg_payable_count,price_plan[0]['special_nonveg'],special_nonveg_amount] 
		row5 = [fp.date,meal_type[4],fp.dinner,dinner_actual_count,dinner_payable_count,price_plan[0]['dinner'],dinner_amount]
		row6 = [fp.date,meal_type[5],fp.supper,supper_actual_count,supper_payable_count,price_plan[0]['supper'],supper_amount]

		data.append(row1)	
		data.append(row2)
		data.append(row3)
		data.append(row4)
		data.append(row5)
		data.append(row6)
	return data

