// Copyright (c) 2016, TEAMPRO and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.ui.form.on('First Aid',{
    onload(frm) {
        
        var time = new Date().toLocaleTimeString();
        var time_format = moment(time, "h:mm:ss A").format("HH:mm");
        frm.set_value('time', time_format)
    },
    
    date_of_birth: function (frm) {
        frm.trigger("age_calculation");
    },
    age_calculation: function (frm) {
        var dob = frm.doc.date_of_birth;
        var birthDate = new Date(dob);
        var difference = Date.now() - birthDate.getTime();
        var ageDate = new Date(difference);
        var calculatedAge = Math.abs(ageDate.getUTCFullYear() - 1970);
        frm.set_value("age", calculatedAge);
        if (calculatedAge < 18) {
            frappe.msgprint("Employee lesser than age 18 will not be allowed");
            frappe.validated = false;
        }

    },
    refresh(frm){
		frappe.db.get_value("Employee",{'id_no':frappe.session.user},['employee','employee_name'], (r) => {
			if (r){
				frm.set_value('employee',r.employee)
				frm.set_value('employee_name',r.employee_name)
			}
		})
    },
    id_no(frm){
		frappe.call({
            method:'thaisummit.thaisummit.doctype.first_aid.first_aid.get_previous_entry',
            args:{
                emp:frm.doc.id_no,
                name:frm.doc.name,
            },
            callback(r){
                frm.fields_dict.previous_entry.$wrapper.empty().append(r.message)
            }
        })
    },

    refresh(frm) {
        if(frm.doc.docstatus == 0){
            frm.add_custom_button(__('Print First Aid'),function(){
                window.open(
                    frappe.urllib.get_full_url(`/api/method/frappe.utils.print_format.download_pdf?
					doctype=${encodeURIComponent("First Aid")}
					&name=${encodeURIComponent(frm.doc.name)}
					&format=${encodeURIComponent('First Aid')}`)
                )
            })
        }
    },
})