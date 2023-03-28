// Copyright (c) 2023, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Test doc', {
	// 20th ques
	pincode(frm){
		frappe.call({
			method: "thaisummit.thaisummit.doctype.test_doc.get_location",
			args: {
				'pincode': frm.doc.pincode,
			},
			callback(r) {
				if (r.message) {
					frm.set_value('pincode', r.message);
				}
	
			}
		})
	},
	// 27th ques
	onload(frm){
		if (frappe.user.has_role('Hod')){
			frm.set_value("field_name",0)
		}
	},
	// 24 th ques
	delivery_option(frm){
		if (frm.doc.delivery_option == 'pick up in-store'){
		frm.toggle_display('shipping_address', false);
	}

	},
	refresh: function(frm) {
		// 4th ques
		if (!frappe.user.has_role('System Manager')) {
			frm.toggle_display('field_name', false);
		}

	},
	
	validate(frm){
		// 17th ques
		frappe.call({
            method: 'haisummit.thaisummit.doctype.test_doc.validate_positive_integer',
            args: {
				 'value': frm.doc.value 
				},
            callback: function(r) {
                if (r.message) {
                }
            }
        });
		// 14th ques
		frappe.call({
			method: "thaisummit.thaisummit.doctype.test_doc.hide_field",
			args: {
				'emp': frm.doc.employee,
			},
			callback(r) {
				if (r.message == test_department) {
					frm.toggle_display('field_name', false);
				}
	
			}
		})
		// 13th ques
		var entered_date = frm.doc.date;
		var current_date = frappe.datetime.get_today();

		if (entered_date < current_date) {
			frappe.msgprint('Date must be a Current date!');
			validated = false;
		}
		// 9th ques
		var email = frm.doc.supcode;
		if (!frappe.utils.validate_email(email)) {
			frappe.msgprint('Invalid email address!');
			validated = false;
		}
		// 8th ques
		if (!frm.doc.__islocal) {
			var current_user = frappe.session.user;
			frm.set_value('current_user',current_user)

		}
		// 1st ques
		frappe.call({
			method: "thaisummit.thaisummit.doctype.test_doc.sale_order",
			args: {
				'total': frm.doc.total_amount,
			},
			callback(r) {
				if (r.message) {
					
				}
	
			}
		})
		// 3rd ques
		var phone_number = frm.doc.phone_number;
		var phone_number_regex = /^\d{10}$/; // regular expression to match 10-digit phone numbers

		if (!phone_number_regex.test(phone_number)) {
			frappe.msgprint('Invalid phone number! Please enter a 10-digit phone number.');
			validated = false;
		}
	}
	
});
