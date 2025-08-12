// Copyright (c) 2021, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Delete Shift Schedule', {
	refresh: function (frm) {
		frm.disable_save()
		frappe.breadcrumbs.add("Home","Shift Schedule");
	},
	delete_shift(frm) {
		if (frm.doc.department != 'All Departments') {
			frappe.call({
				method: "thaisummit.thaisummit.doctype.delete_shift_schedule.delete_shift_schedule.enqueue_delete_shift",
				args: {
					department: frm.doc.department,
					from_date: frm.doc.from_date,
				},
				freeze: true,
				freeze_message: "Deleting Shift Schedule"
			});
			frappe.msgprint('Deleting Shift Schedule. Please check after few mins.')
		}
		else{
			frappe.call({
				method: "thaisummit.thaisummit.doctype.delete_shift_schedule.delete_shift_schedule.enqueue_delete_all_shift",
				args: {
					from_date: frm.doc.from_date,
				},
				freeze: true,
				freeze_message: "Deleting Shift Schedule"
			});
			frappe.msgprint('Deleting Shift Schedule. Please check after few mins.')
		}
	},
	// to_date(frm) {
	// 	if (frm.doc.to_date) {
	// 		if (frm.doc.to_date < frappe.datetime.now_date()) {
	// 			frappe.msgprint("To Date should not be a Past Date")
	// 			frm.set_value('to_date', '')
	// 		}
	// 		else if (frm.doc.to_date < frm.doc.from_date) {
	// 			frappe.msgprint("To Date should not be greater than From Date")
	// 			frm.set_value('to_date', '')
	// 		}

	// 	}
	// },
	// from_date(frm) {
	// 	if (frm.doc.from_date) {
	// 		if (frm.doc.from_date < frappe.datetime.now_date()) {
	// 			frappe.msgprint("Date should not be a Past Date")
	// 			frm.set_value('from_date', '')
	// 		}
	// 	}
	// }
});
