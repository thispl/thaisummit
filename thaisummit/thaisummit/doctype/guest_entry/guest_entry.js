// Copyright (c) 2022, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Guest Entry', {
	//this is the type field by clicking to change the type_id of four naming_series
	onload(frm) {
		if(frm.doc.docstatus != 1){
        var time = new Date().toLocaleTimeString();
        var time_format = moment(time, "h:mm:ss A").format("HH:mm");
        frm.set_value('time', time_format)
		}
	},
	type(frm){
		if(frm.doc.type == 'Customer'){
			frm.set_value('naming_series','CUS.####')
		}
		else if(frm.doc.type == 'Vendor'){
			frm.set_value('naming_series','VEN.####')
		}
		else if (frm.doc.type == 'Government Officers'){
			frm.set_value('naming_series','GOV.####')
		}
		else if(frm.doc.type == 'Others'){
			frm.set_value('naming_series','OTS.####')
		}
		else{
			frm.set_value('naming_series','CUS.####')
		}
	},
	to(frm){
		var date_diff = frappe.datetime.get_diff(frm.doc.to,frm.doc.from)
		if (date_diff < 90){
		}
		else{
			frappe.throw(__('You Cannot apply beyond 90 Days'))
			frm.set_value('to','')
		}
	},
	break_fast(frm){
		if(frm.doc.break_fast == 1){
			var date_diff = frappe.datetime.get_diff(frm.doc.to,frm.doc.from)
			frm.set_value('bf_no_of_days',date_diff + 1)
			var price_amount = frappe.db.get_value('Food Menu',{'menu':'Break Fast'},'price',(r) => {
				if(r){
					frm.set_value('bf_price',r.price)
					var days_to_price = frm.doc.bf_no_of_days * frm.doc.bf_price
					frm.set_value('bf_amount',days_to_price)
					frm.trigger('get_total_amount_food')
				}
			})
		}
		else{
			frm.set_value('bf_no_of_days',0)
			frm.set_value('bf_price',0)
			frm.set_value('bf_amount',0)
			frm.set_value('total_amount',0)
		}
	},
	lunch(frm){
		if(frm.doc.lunch == 1){
			var date_diff = frappe.datetime.get_diff(frm.doc.to,frm.doc.from)
			frm.set_value('lu_no_of_days',date_diff + 1)
			var price_amount = frappe.db.get_value('Food Menu',{'menu':'Lunch'},'price',(r) => {
				if(r){
					frm.set_value('lu_price',r.price)
					var days_to_price = frm.doc.bf_no_of_days * frm.doc.bf_price
					frm.set_value('lu_amount',days_to_price)
					frm.trigger('get_total_amount_food')
				}
			})
		}
		else{
			frm.set_value('lu_no_of_days',0)
			frm.set_value('lu_price',0)
			frm.set_value('lu_amount',0)
			frm.set_value('total_amount',0)
		}

	},
	lunch_briyani_veg(frm){
		if(frm.doc.lunch_briyani_veg == 1){
			var date_diff = frappe.datetime.get_diff(frm.doc.to,frm.doc.from)
			frm.set_value('lbv_no_of_days',date_diff + 1)
			var price_amount = frappe.db.get_value('Food Menu',{'menu':'Lunch Briyani Veg'},'price',(r) => {
				if(r){
					frm.set_value('lbv_price',r.price)
					var days_to_price = frm.doc.lbv_no_of_days * frm.doc.lbv_price
					frm.set_value('lbv_amount',days_to_price)
				}
			})
		}
		else{
			frm.set_value('lbv_no_of_days',0)
			frm.set_value('lbv_price',0)
			frm.set_value('lbv_amount',0)
			frm.set_value('total_amount',0)
		}
	},
	lunch_briyani_non_veg(frm){
		if(frm.doc.lunch_briyani_non_veg == 1){
			var date_diff = frappe.datetime.get_diff(frm.doc.to,frm.doc.from)
			frm.set_value('lbnv_no_of_days',date_diff + 1)
			var price_amount = frappe.db.get_value('Food Menu',{'menu':'Lunch Briyani Non Veg'},'price',(r) => {
				if(r){
					frm.set_value('lbnv_price',r.price)
					var days_to_price = frm.doc.lbnv_no_of_days * frm.doc.lbnv_price
					frm.set_value('lbnv_amount',days_to_price)
				}
			})
		}
		else{
			frm.set_value('lbnv_no_of_days',0)
			frm.set_value('lbnv_price',0)
			frm.set_value('lbnv_amount',0)
			frm.set_value('total_amount',0)
		}
	},
	lunch_special_veg(frm){
		if(frm.doc.lunch_special_veg == 1){
			var date_diff = frappe.datetime.get_diff(frm.doc.to,frm.doc.from)
			frm.set_value('lsv_no_of_days',date_diff + 1)
			var price_amount = frappe.db.get_value('Food Menu',{'menu':'Lunch Special Veg'},'price',(r) => {
				if(r){
					frm.set_value('lsv_price',r.price)
					var days_to_price = frm.doc.lsv_no_of_days * frm.doc.lsv_price
					frm.set_value('lsv_amount',days_to_price)
				}
			})
		}
		else{
			frm.set_value('lsv_no_of_days',0)
			frm.set_value('lsv_price',0)
			frm.set_value('lsv_amount',0)
			frm.set_value('total_amount',0)
		}
	},
	lunch_special_non_veg(frm){
		if(frm.doc.lunch_special_non_veg == 1){
			var date_diff = frappe.datetime.get_diff(frm.doc.to,frm.doc.from)
			frm.set_value('lsnv_no_of_days',date_diff + 1)
			var price_amount = frappe.db.get_value('Food Menu',{'menu':'Lunch Special Non Veg'},'price',(r) => {
				if(r){
					frm.set_value('lsnv_price',r.price)
					var days_to_price = frm.doc.lsnv_no_of_days * frm.doc.lsnv_price
					frm.set_value('lsnv_amount',days_to_price)
				}
			})
		}
		else{
			frm.set_value('lsnv_no_of_days',0)
			frm.set_value('lsnv_price',0)
			frm.set_value('lsnv_amount',0)
			frm.set_value('total_amount',0)
		}
	},
	dinner(frm){
		if(frm.doc.dinner == 1){
			var date_diff = frappe.datetime.get_diff(frm.doc.to,frm.doc.from)
			frm.set_value('dn_no_of_days',date_diff + 1)
			var price_amount = frappe.db.get_value('Food Menu',{'menu':'Dinner'},'price',(r) => {
				if(r){
					frm.set_value('dn_price',r.price)
					var days_to_price = frm.doc.bf_no_of_days * frm.doc.bf_price
					frm.set_value('dn_amount',days_to_price)
					frm.trigger('get_total_amount_food')
				}
			})
		}
		else{
			frm.set_value('dn_no_of_days',0)
			frm.set_value('dn_price',0)
			frm.set_value('dn_amount',0)
			frm.set_value('total_amount',0)
		}

	},
	dinner_briyani_veg(frm){
		if(frm.doc.dinner_briyani_veg == 1){
			var date_diff = frappe.datetime.get_diff(frm.doc.to,frm.doc.from)
			frm.set_value('dbv_no_of_days',date_diff + 1)
			var price_amount = frappe.db.get_value('Food Menu',{'menu':'Dinner Briyani Veg'},'price',(r) => {
				if(r){
					frm.set_value('dbv_price',r.price)
					var days_to_price = frm.doc.dbv_no_of_days * frm.doc.dbv_price
					frm.set_value('dbv_amount',days_to_price)
				}
			})	
		}
		else{
			frm.set_value('dbv_no_of_days',0)
			frm.set_value('dbv_price',0)
			frm.set_value('dbv_amount',0)
			frm.set_value('total_amount',0)
		}
	},
	dinner_briyani_non_veg(frm){
		if(frm.doc.dinner_briyani_non_veg == 1){
			var date_diff = frappe.datetime.get_diff(frm.doc.to,frm.doc.from)
			frm.set_value('dbnv_no_of_days',date_diff + 1)
			var price_amount = frappe.db.get_value('Food Menu',{'menu':'Dinner Briyani Non Veg'},'price',(r) => {
				if(r){
					frm.set_value('dbnv_price',r.price)
					var days_to_price = frm.doc.dbnv_no_of_days * frm.doc.dbnv_price
					frm.set_value('dbnv_amount',days_to_price)
				}
			})	
		}
		else{
			frm.set_value('dbnv_no_of_days',0)
			frm.set_value('dbnv_price',0)
			frm.set_value('dbnv_amount',0)
			frm.set_value('total_amount',0)
		}
	},
	dinner_special_veg(frm){
		if(frm.doc.dinner_special_veg == 1){
			var date_diff = frappe.datetime.get_diff(frm.doc.to,frm.doc.from)
			frm.set_value('dsv_no_of_days',date_diff + 1)
			var price_amount = frappe.db.get_value('Food Menu',{'menu':'Dinner Special Veg'},'price',(r) => {
				if(r){
					frm.set_value('dsv_price',r.price)
					var days_to_price = frm.doc.dsv_no_of_days * frm.doc.dsv_price
					frm.set_value('dsv_amount',days_to_price)
				}
			})	
		}
		else{
			frm.set_value('dsv_no_of_days',0)
			frm.set_value('dsv_price',0)
			frm.set_value('dsv_amount','0')
			frm.set_value('total_amount',0)
		}
	},
	dinner_special_non_veg(frm){
		if(frm.doc.dinner_special_non_veg == 1){
			var date_diff = frappe.datetime.get_diff(frm.doc.to,frm.doc.from)
			frm.set_value('dsnv_no_of_days',date_diff + 1)
			var price_amount = frappe.db.get_value('Food Menu',{'menu':'Dinner Special Non Veg'},'price',(r) => {
				if(r){
					frm.set_value('dsnv_price',r.price)
					var days_to_price = frm.doc.dsnv_no_of_days * frm.doc.dsnv_price
					frm.set_value('dsnv_amount',days_to_price)
				}
			})	
		}
		else{
			frm.set_value('dsnv_no_of_days',0)
			frm.set_value('dsnv_price',0)
			frm.set_value('dsnv_amount',0)
			frm.set_value('total_amount',0)
		}
	},
	supper_dates(frm){
		if(frm.doc.supper_dates == 1){
			var date_diff = frappe.datetime.get_diff(frm.doc.to,frm.doc.from)
			frm.set_value('sd_no_of_days',date_diff + 1)
			var price_amount = frappe.db.get_value('Food Menu',{'menu':'Supper Dates'},'price',(r) => {
				if(r){
					frm.set_value('sd_price',r.price)
					var days_to_price = frm.doc.sd_no_of_days * frm.doc.sd_price
					frm.set_value('sd_amount',days_to_price)
				}
			})	
		}
		else{
			frm.set_value('sd_no_of_days',0)
			frm.set_value('sd_price',0)
			frm.set_value('sd_amount',0)
			frm.set_value('total_amount',0)
		}
	},
	supper_special_food(frm){
		if(frm.doc.supper_special_food == 1){
			var date_diff = frappe.datetime.get_diff(frm.doc.to,frm.doc.from)
			frm.set_value('ssf_no_of_days',date_diff + 1)
			var price_amount = frappe.db.get_value('Food Menu',{'menu':'Supper Special Food'},'price',(r) => {
				if(r){
					frm.set_value('ssf_price',r.price)
					var days_to_price = frm.doc.ssf_no_of_days * frm.doc.ssf_price
					frm.set_value('ssf_amount',days_to_price)
				}
			})	
		}
		else{
			frm.set_value('ssf_no_of_days',0)
			frm.set_value('ssf_price',0)
			frm.set_value('ssf_amount',0)
			frm.set_value('total_amount',0)
		}
	},
	refresh(frm){
		if(frm.doc.workflow_state == 'Approved'){
			frm.add_custom_button(__('QR PRINT'), function () {
				var f_name = frm.doc.name
				var print_format = "Guest Entry QR Generate";
				window.open(frappe.urllib.get_full_url("/api/method/frappe.utils.print_format.download_pdf?"
					+ "doctype=" + encodeURIComponent(frm.doc.doctype)
					+ "&name=" + encodeURIComponent(f_name)
					+ "&trigger_print=1"
					+ "&format=" + print_format
					+ "&no_letterhead=0"
				));
			})
		}
	}
});
