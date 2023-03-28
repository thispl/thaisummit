// Copyright (c) 2022, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Food Entry Scan', {
	
	
	employee_guest(frm){
		var emp = frm.doc.employee_guest
		if(frm.doc.employee_guest){
			frappe.call({
				method:'thaisummit.thaisummit.doctype.food_entry_scan.food_entry_scan.get_canteen_user_id',
				args:{
					user:frm.doc.employee_guest,
				},
				freeze:true,
				freeze_message:('food Scan'),
				callback(r){
					if(r.message == 'Completed'){	
						frm.set_value('employee_guest','')
						$("input[data-fieldname='employee_guest']").focus()
						frm.trigger('get_live_screen')
					}
					// else{
					// 	// frm.set_value('employee_guest','')	
					// 	frm.trigger('get_live_screen')
					// }
					
					// setTimeout(function(){
						
					// 	frm.get_field("output").$wrapper.html('');
					//  }, 5000);
				}
			})	
		}
		
	},
	
	get_live_screen(frm){
		frappe.call({
			method:'thaisummit.www.canteen_live_screen.get_live_screen_data',
			args:{
			},
			callback(r){
				var data = r.message;
				if(r.message.food_type == 'Break Fast'){
					frm.fields_dict.output.$wrapper.empty().append(frappe.render_template('canteen_live_screen_bf_data',r.message))
					frm.fields_dict.employee_list.$wrapper.empty().append(frappe.render_template('employee_display_bf',r.message))	
				}
				else if(r.message.food_type == 'Lunch' ){
					frm.fields_dict.output.$wrapper.empty().append(frappe.render_template('canteen_live_screen_lu_data',r.message))
					frm.fields_dict.employee_list.$wrapper.empty().append(frappe.render_template('employee_display_lu',r.message))
				}
				else if (r.message.food_type == 'Dinner'){
					frm.fields_dict.output.$wrapper.empty().append(frappe.render_template('canteen_live_screen_dn_data',r.message))
					frm.fields_dict.employee_list.$wrapper.empty().append(frappe.render_template('employee_display_dn',r.message))
				}
				else if (r.message.food_type == 'NA'){
					frm.fields_dict.output.$wrapper.empty().append(frappe.render_template('canteen_live_screen_dn_data',r.message))
					frm.fields_dict.employee_list.$wrapper.empty().append(frappe.render_template('employee_display_dn',''))
				}
				else{
					// frm.fields_dict.output.$wrapper.empty().append(frappe.render_template('canteen_live_screen_su_data',r.message))
					frm.fields_dict.output.$wrapper.empty().append(frappe.render_template('canteen_live_screen_sp_data',r.message))
					// frm.fields_dict.output.$wrapper.empty().append(frappe.render_template('canteen_live_screen_sd_data',r.message))
					frm.fields_dict.employee_list.$wrapper.empty().append(frappe.render_template('employee_display_sp',r.message))
				} 
				
			}
			
		})
	},
	refresh(frm){
		$("input[data-fieldname='employee_guest']").focus()
		frm.disable_save()
		if (frm.trigger("get_live_screen")){
		// 	frm.trigger("get_live_screen")
		}
		// else{
		// 	frappe.throw(__('Today Food Plan was not Entry'))
		// }
		
	}
});
