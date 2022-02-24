// Copyright (c) 2021, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Part Master Data', {
	refresh: function(frm) {
		frappe.breadcrumbs.add("Home","E-KANBAN");
		frm.disable_save()
		frm.call('get_data').then(r=>{
			if (r.message) {
				frm.fields_dict.html.$wrapper.empty().append(r.message)
			}
		})
	},
	download: function (frm) {
		window.location.href = repl(frappe.request.url +
			'?cmd=%(cmd)s', {
			cmd: "thaisummit.thaisummit.doctype.part_master_data.part_master_data.download",
		});
	},
	upload(frm){
		if(frm.doc.attach){
			frappe.call({
				method : 'thaisummit.thaisummit.doctype.part_master_data.part_master_data.upload',
				args: {
					file: frm.doc.attach
				},
				freeze: true,
				freeze_message: 'Updating Master Data....',
				callback(r){
					if(r.message){
						frappe.show_alert({
							message:__('Master Data Updated Successfully'),
							indicator:'green'
						}, 5);
						frm.set_value('attach','')
						frm.save()
						frm.trigger('refresh')
					}
				}
			})
		}
		else{
			frappe.msgprint('Please Attach the Excel')
		}
	}
});
