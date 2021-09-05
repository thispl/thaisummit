// Copyright (c) 2021, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Attendance Dashboard', {
	refresh: function (frm) {
		var $breadcrumbs = $("#navbar-breadcrumbs").empty().html('<li><a href="/app/home">Home</a></li>');
		// frm.$.attendance.css({ 'border-color':'#00FF00' });
		frm.disable_save()
		frm.trigger('display_data')
	},
	month(frm) {
		frm.trigger('display_data')
	},
	display_data(frm) {
		console.log(frappe.session.user)
		frappe.db.get_value('Employee', { "user_id": frappe.session.user }, 'employee', (r) => {
			console.log(r)
			if (r.employee) {
				frappe.call({
					method: "thaisummit.thaisummit.doctype.attendance_dashboard.attendance_dashboard.get_shift",
					args: {
						emp: r.employee,
						month: frm.doc.month,
						year: frm.doc.year
					},
					callback: function (r) {
						frm.fields_dict.attendance.$wrapper.empty().append(r.message)
					}
				})
				frappe.call({
					method: "thaisummit.thaisummit.doctype.attendance_dashboard.attendance_dashboard.get_ot",
					args: {
						emp: r.employee,
						month: frm.doc.month,
						year: frm.doc.year
					},
					callback: function (r) {
						frm.fields_dict.ot.$wrapper.empty().append(r.message)
					}
				})
			}
			else {
				frm.fields_dict.attendance.$wrapper.empty().append("<center><h2>Attendance Not Found</h2></center>")
			}
		})
	}
});
