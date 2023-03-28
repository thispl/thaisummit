import frappe

@frappe.whitelist()
def get_employee():
    emp_details = frappe.db.get_value('Employee',{'user_id':frappe.session.user},['employee','employee_name',])
    # employee = frappe.db.sql(""" select employee,employee_name from `tabEmployee` where user_id = '%s' """%(frappe.session.user),as_dict=True)
    # frappe.errprint(employee)
    return emp_details
