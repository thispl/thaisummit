// Copyright (c) 2021, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('TAG OUT', {
	submit:function(frm){
        cur_frm.set_df_property("submit", "hidden", true);
        var today = new Date();

        var date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();

        var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
        var datetime = date+' '+time
        frm.set_value("submit_time",datetime)
            frm.call('make_as_delivery',{
				receipt_entry:frm.doc.receipt_entry_table
			})
            .then(r =>{
                frappe.msgprint(__(r.message))
            })
    },
    refresh: function(frm) {
        frm.disable_save()
        $("input[data-fieldname='qr']").focus()
        
    },

    qr:function(frm){
        var today = new Date();

        var date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();

        var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
        var datetime = date+' '+time
            var qr_length = (frm.doc.qr).length
            console.log(qr_length)
            if (qr_length == 68){
            var part_no = frm.doc.qr.substring(11, 25)
            var qty = frm.doc.qr.substring(38,43)
            frappe.db.get_doc('Part Master',part_no)
                .then(doc => {
                frm.add_child("receipt_entry_table",{
                    parts_no :part_no,
                    quantity :parseInt(qty, 10),
                    card_type:doc.tag_type,
                    parts_name:doc.parts_name,
                    mat_no:doc.mat_no,
                    model:doc.model_no,
                    date_and_time:datetime,
                    qr :frm.doc.qr,
                    date :date,
                    sp_purchase_price:doc.sp_purchase_price
                    
                })
                frm.refresh_field("receipt_entry_table")
                frm.set_value("qr","")
                })
            }
            else if(qr_length == 49){
            var part_no = frm.doc.qr.substring(11, 25)
            var qty = frm.doc.qr.substring(44,49)
            frappe.db.get_doc('Part Master',part_no)
                .then(doc => {
                frm.add_child("receipt_entry_table",{
                    parts_no :part_no,
                    quantity :parseInt(qty, 10),
                    card_type:doc.tag_type,
                    parts_name:doc.parts_name,
                    mat_no:doc.mat_no,
                    model:doc.model_no,
                    date_and_time:datetime,
                    qr :frm.doc.qr,
                    date :date,
                    sp_purchase_price:doc.sp_purchase_price
            });
            frm.refresh_field("receipt_entry_table")
            frm.set_value("qr","")
        })
            }
		}
});
