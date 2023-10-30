// Copyright (c) 2023, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Generate Tag Card', {
	refresh(frm) {
		if(!frm.doc.__islocal ){
			frm.disable_save()
		}
		if (frm.doc.production_line){
			frappe.call({
				method: "thaisummit.custom.update_list",
				args: {
					'production_line': frm.doc.production_line,
				},
				callback(r) {
					if (r.message) {
							frm.add_custom_button(__("Print Tag Card"), function () {
								var f_name = frm.doc.name
								var print_format = "Tag Card";


								window.open(frappe.urllib.get_full_url("/api/method/frappe.utils.print_format.download_pdf?"
									+ "doctype=" + encodeURIComponent("Generate Tag Card")
									+ "&name=" + encodeURIComponent(f_name)
									+ "&trigger_print=1"
									+ "&format=" + print_format
									+ "&no_letterhead=0"
								));
							});
						

					}

				}
			})
		
	}
		$("button[data-original-title=Print]").hide();
	},

	mat_number(frm) {
		if(frm.doc.mat_number){
			frappe.call({
				method: "thaisummit.custom.tag_mat_name",
				args: {
					'mat_number': frm.doc.mat_number,
				},
				freeze:true,
				freeze_message: 'Checking....',
				callback(r) {
					if (r.message) {
						frm.set_value("mat_name", r.message[0]);
						frm.set_value("part_number", r.message[1]);
						frm.set_value("packing_std", r.message[2]);
						frm.set_value("production_line", r.message[3])
					}
	
				}
			})
			frappe.call({
				method: "thaisummit.custom.get_opq",
				args: {
					'mat_number': frm.doc.mat_number,
				},
				callback(r) {
					if (r.message) {
						frm.set_value("production_order_qty", r.message);
					}
					else {
						frm.set_value("production_order_qty", '0');
					}
	
				}
			})
		}
		
	},
	onload: function (frm) {
		if(frm.doc.quantity){
		frm.fields_dict.html.$wrapper.empty().append('')
		if (frm.doc.docstatus == 0) {
			frm.call('get_data').then(r => {
				if (r.message) {
					frm.fields_dict.html.$wrapper.empty().append(r.message)
				}
			})

		}
	}

	},

	quantity(frm) {
		if(frm.doc.quantity){
			frm.call('get_child_mat').then(r => {

			})
			frm.call('get_data').then(r => {
				if (r.message) {
					frm.fields_dict.html.$wrapper.empty().append(r.message)
				}
			})
	
		}
		



	},
});
