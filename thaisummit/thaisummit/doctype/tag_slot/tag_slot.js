// Copyright (c) 2021, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('TAG Slot', {
	refresh: function (frm) {
		var parts_list = []
		if(frm.doc.docstatus == 0){
			frm.add_custom_button(__("Call SAP"), function () {
				frm.call('calculate_quantity')
					.then(r => {
						if(r.message[0] == 'Quantity Updated') {
							frm.set_value('last_updated_on',r.message[1])
							frm.save()
							}
					})
			})

		}
		
	
	},
	download:function(frm) {
		console.log(frappe.request.url)
		window.location.href = repl(frappe.request.url +
			'?cmd=%(cmd)s&name=%(name)s', {
			cmd: "thaisummit.thaisummit.doctype.tag_slot.tag_slot.download_excel",
			name: frm.doc.name
		});
	},
	// onload:function(frm){
	// 	console.log("hi")
	// 	cur_frm.fields_dict["tag_wise_list"].$wrapper.find('.grid-body .rows').find(".grid-row").each(function(i, item) {
	// 		let d = locals[cur_frm.fields_dict["tag_wise_list"].grid.doctype][$(item).attr('data-name')];
	// 		if(d["difference"] < 0){
	// 			$(item).find('.grid-static-col').css({'background-color': '#FF0000'});
	// 		}
	// 	});				
	// },

	on_submit: function(frm){
		frm.call('create_tag_master')
				.then(r => {
					frappe.msgprint(__(r.message))
				})
	}

});
// frappe.ui.form.on('Tag Wise List', onload ,function(frm,cdt,cdn) {
// 	var child = locals[cdt][cdn];
//     cur_frm.doc.tag_wise_list.forEach(function(child){
// 			console.log("hi")

// 	var sel = format('div[data-fieldname="tag_wise_list"] > div.grid-row[data-idx="{0}"]', [child.idx]);
// 		if(child.difference < 0){
// 			console.log("hi")

// 			$(sel).css('background-color', "#ff5858");
// 		}
	
// })
// frappe.ui.form.on("Shipping List", "one1", function(frm, cdt, cdn){
//     var child = locals[cdt][cdn];
//     cur_frm.doc.shipping_list.forEach(function(child){
//     var sel = format('div[data-fieldname="shipping_list"] > div.grid-row[data-idx="{0}"]', [child.idx]);
//         if (child.one1 > 0){
//         $(sel).css('background-color', "#ff5858");
//         } else {
//             $(sel).css('background-color', 'transparent');
//         }
//     });
// });
	