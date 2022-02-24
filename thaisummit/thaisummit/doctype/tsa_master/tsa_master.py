# Copyright (c) 2021, TEAMPRO and contributors
# For license information, please see license.txt

from statistics import mode
import frappe
from frappe.model.document import Document
from frappe.utils.background_jobs import enqueue


class TSAMaster(Document):
    pass


@frappe.whitelist()
def enqueue_master_creation(self,method):
    enqueue(master_creation, queue='default', timeout=6000, event='master_creation')

@frappe.whitelist()
def master_creation():
    data = frappe.db.sql(""" SELECT * FROM `tabIYM Sequence Plan` WHERE 'Pending' IN 
    (weld_recv_status,aced_recv_status,fuel_recv_status,assy_recv_status)
    """, as_dict=True)

    for d in data:
        date = d.date
        model = d.model_code
        q = d.parts_qty
        weld = d.weld_recv_status
        aced = d.aced_recv_status
        fuel = d.fuel_recv_status
        assy = d.assy_recv_status
        
        
        if weld == "Pending":
            part_data = frappe.get_all("Part Master",{'model_number':('like',model+'%'),'tag_type':'WELD'},['name','mat_no','parts_no','parts_name','usage','tag_type'])
            create_tsa_master(part_data,date,model)

        if aced == "Pending":
            # if d.assy_line == 'BDY3':
            part_data = frappe.get_all("Part Master",{'model_number':('like',model+'%'),'tag_type':'ACED'},['name','mat_no','parts_no','parts_name','usage','tag_type','model_number'])
            create_tsa_master(part_data,date,model)
        
        if fuel == "Pending":
            part_data = frappe.get_all("Part Master",{'model_number':('like',model+'%'),'tag_type':'FT'},['name','mat_no','parts_no','parts_name','usage','tag_type'])
            create_tsa_master(part_data,date,model)

        if assy == "Pending":
            # if model == 'BCT5':
            part_data = frappe.get_all("Part Master",{'model_number':('like',model+'%'),'tag_type':('in',('ASSY','WELD-CKD'))},['name','mat_no','parts_no','parts_name','usage','tag_type'])
            create_tsa_master(part_data,date,model)
            

def create_tsa_master(part_data,date,model):
    for p in part_data:
        frappe.db.sql(""" DELETE FROM `tabTSA Master` WHERE iym_model_code='%s' AND date='%s' AND section='%s' 
        AND part_no='%s' """% (model,date,p.tag_type,p.parts_no) ,as_dict=True)
        if p.tag_type == 'WELD':
            plan_type = 'weld_plan_qty'
            plan_status = 'weld_recv_status'
        elif p.tag_type == 'ACED':
            plan_type = 'aced_plan_qty'
            plan_status = 'aced_recv_status'
        elif p.tag_type == 'FT':
            plan_type = 'fuel_plan_qty'
            plan_status = 'fuel_recv_status'
        elif p.tag_type in ('ASSY','WELD-CKD'):
            plan_type = 'assy_plan_qty'
            plan_status = 'assy_recv_status'
        quantity = frappe.db.sql("""select sum(%s) as qty from `tabIYM Sequence Plan` where model_code = '%s' and %s = 'Pending' and date = '%s' """%(plan_type,model,plan_status,date),as_dict=True)[0].qty or 0
        # quantity = frappe.db.sql("""select sum(%s) from `tabIYM Sequence Plan` where model_code = '%s' and date = '%s' and %s = 'Pending' """%(plan_type,model,date,plan_status),as_dict=True)
        # print(p.mat_no)
        # print(model)
        print(plan_status)
        print(quantity)
        print(date)
        usage = int(p.usage)
        total_quantity = usage * quantity
        tsa = frappe.new_doc("TSA Master")
        tsa.iym_model_code = model
        tsa.section = p.tag_type
        tsa.mat_no = p.mat_no
        tsa.part_no = p.parts_no
        tsa.part_name = p.parts_name
        tsa.usage = usage
        tsa.quantity = total_quantity
        tsa.date = date
        tsa.save(ignore_permissions=True)
        frappe.db.commit()
