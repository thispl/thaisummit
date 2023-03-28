frappe.ui.form.on('Bus Arrival Form', {
	time(frm) {
		frappe.call({
			method: 'thaisummit.thaisummit.doctype.bus_arrival_form.bus_arrival_form.get_bus_arrival_shift',
			args: {
				time_apply: frm.doc.time,
			},
			callback(r) {
				frm.set_value('shift', r.message[0])
				if(r.message[0] == '3'){
					var previous_day = frappe.datetime.add_days(frm.doc.date,-1)
					frm.set_value('date',previous_day)
					frm.set_value('status', r.message[1])
					frm.set_value('late_minutes', r.message[2])
				}
				else{
					frm.set_value('status', r.message[1])
					frm.set_value('late_minutes', r.message[2])
				}
				
			}
		})
	},
	bus_number(frm) {
		if (frm.doc.bus_number) {
			var vehcile_number = frm.doc.bus_number;
			var change_upper_case = vehcile_number.toUpperCase();
			frm.set_value('bus_number', change_upper_case);
		}
	},
	// time(frm){
	// 	console.log('hi')
		// if(frm.doc.shift == '3'){
		// 	var previous_day = frappe.datetime.add_days(frm.doc.date,-1)
		// 	frm.set_value(frm.doc.date,previous_day)
		// }
	// }
})