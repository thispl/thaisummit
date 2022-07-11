# Copyright (c) 2022, TEAMPRO and contributors
# For license information, please see license.txt

import frappe,json
from frappe.utils import cint
from frappe.model.document import Document

class FoodPlanEntry(Document):
	pass

@frappe.whitelist()
def get_food_plan(date):
	food_plans = frappe.get_all('Food Plan',filters={'date':date},fields=['*'])
	return food_plans

@frappe.whitelist()
def update_food_plan(food_plan_child,date):
	food_plan_child = json.loads(food_plan_child)
	fpcid = frappe.db.exists("Food Plan",{'date':date})
	if fpcid:
		fp = frappe.get_doc("Food Plan",fpcid)
	else:
		fp = frappe.new_doc("Food Plan")
		fp.date = date

	fp.bf_head_count = cint(food_plan_child[0]['head_count'])
	fp.bf_price = cint(food_plan_child[0]['price'])
	fp.bf_amount = cint(food_plan_child[0]['amount'])

	fp.lu_head_count = cint(food_plan_child[1]['head_count'])
	fp.lu_price = cint(food_plan_child[1]['price'])
	fp.lu_amount = cint(food_plan_child[1]['amount'])

	fp.lbv_head_count = cint(food_plan_child[2]['head_count'])
	fp.lbv_price = cint(food_plan_child[2]['price'])
	fp.lbv_amount = cint(food_plan_child[2]['amount'])

	fp.lbnv_head_count = cint(food_plan_child[3]['head_count'])
	fp.lbnv_price = cint(food_plan_child[3]['price'])
	fp.lbnv_amount = cint(food_plan_child[3]['amount'])

	fp.lsv_head_count = cint(food_plan_child[4]['head_count'])
	fp.lsv_price = cint(food_plan_child[4]['price'])
	fp.lsv_amount = cint(food_plan_child[4]['amount'])

	fp.lsnv_head_count = cint(food_plan_child[5]['head_count'])
	fp.lsnv_price = cint(food_plan_child[5]['price'])
	fp.lsnv_amount = cint(food_plan_child[5]['amount'])

	fp.dn_head_count = cint(food_plan_child[6]['head_count'])
	fp.dn_price = cint(food_plan_child[6]['price'])
	fp.dn_amount = cint(food_plan_child[6]['amount'])

	fp.dbv_head_count = cint(food_plan_child[7]['head_count'])
	fp.dbv_price = cint(food_plan_child[7]['price'])
	fp.dbv_amount = cint(food_plan_child[7]['amount'])
		
	fp.dbnv_head_count = cint(food_plan_child[8]['head_count'])
	fp.dbnv_price = cint(food_plan_child[8]['price'])
	fp.dbnv_amount = cint(food_plan_child[8]['amount'])

	fp.dsv_head_count = cint(food_plan_child[9]['head_count'])
	fp.dsv_price = cint(food_plan_child[9]['price'])
	fp.dsv_amount = cint(food_plan_child[9]['amount'])
    
	fp.dsnv_head_count = cint(food_plan_child[10]['head_count'])
	fp.dsnv_price = cint(food_plan_child[10]['price'])
	fp.dsnv_amount = cint(food_plan_child[10]['amount'])

	fp.sp_head_count = cint(food_plan_child[11]['head_count'])
	fp.sp_price = cint(food_plan_child[11]['price'])
	fp.sp_amount = cint(food_plan_child[11]['amount'])

	fp.sd_head_count = cint(food_plan_child[12]['head_count'])
	fp.sd_price = cint(food_plan_child[12]['price'])
	fp.sd_amount = cint(food_plan_child[12]['amount'])

	fp.ssf_head_count = cint(food_plan_child[13]['head_count'])
	fp.ssf_price = cint(food_plan_child[13]['price'])
	fp.ssf_amount = cint(food_plan_child[13]['amount'])


	fp.save(ignore_permissions=True)
	frappe.db.commit()
	return "Updated"		

    

	
