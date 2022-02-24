
frappe.ui.form.on('test1', {
	refresh(frm){
		frm.disable_save()
		console.log(frappe.session.user)
		frappe.db.get_value("Employee",{'user_id':frappe.session.user},'name', (r) => {
			if (r.message){
				console.log(r.message)
				frm.set_value('employee',r.message)
			}
		})
		frm.disable_save()
			frm.set_value('to_date',frappe.datetime.add_days(frappe.datetime.month_start(), 24))
	
			var d = frappe.datetime.add_months(frappe.datetime.month_start(), -1)
			frm.set_value('from_date',frappe.datetime.add_days(d, 25))
	},
	employee(frm){
		frm.trigger('get_data')
	},
	from_date(frm){
		frm.trigger('get_data')
	},
	to_date(frm){
		frm.trigger('get_data')
	},
	get_data: function (frm) {
		if (frm.doc.from_date && frm.doc.to_date && frm.doc.employee) {
			if (!frappe.is_mobile()) {
				frm.trigger('get_data_system')
			}
			else {
				frm.trigger('get_data_mobile')
			}
		}
	},
	get_data_system(frm) {
		frappe.db.get_value('Employee', { "name": frm.doc.employee }, 'employee', (r) => {
			if (r.employee) {
				frappe.call({
					method: "thaisummit.thaisummit.doctype.attendance_summary.attendance_summary.get_data_system",
					args: {
						emp: r.employee,
						from_date: frm.doc.from_date,
						to_date: frm.doc.to_date
					},
					callback: function (r) {
						frm.fields_dict.html.$wrapper.empty().append(r.message)
					}
				})
			}
			else {
				frm.fields_dict.html.$wrapper.empty().append("<center><h2>Attendance Not Found</h2></center>")
			}
		})
	},
	get_data_mobile(frm) {
		frappe.db.get_value('Employee', { "name": frm.doc.employee }, 'employee', (r) => {
			if (r.employee) {
				frappe.call({
					method: "thaisummit.thaisummit.doctype.attendance_summary.attendance_summary.get_data_mobile",
					args: {
						emp: r.employee,
						from_date: frm.doc.from_date,
						to_date: frm.doc.to_date
					},
					callback: function (r) {
						frm.fields_dict.html.$wrapper.empty().append(r.message)
					}
				})
			}
			else {
				frm.fields_dict.html.$wrapper.empty().append("<center><h2>Attendance Not Found</h2></center>")
			}
		})
	}
});
