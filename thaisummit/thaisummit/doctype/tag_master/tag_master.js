// Copyright (c) 2021, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('TAG Master', {
    refresh: function(frm) {
        // frm.set_value("item_delivered" ,0)
        if(frappe.user.has_role('Tag Manager')){
        if (!frm.doc.item_delivered){
        frm.add_custom_button(__("Delivered"), function(){
            frm.set_value("item_delivered" ,1)
            frm.call('get_delay')
            .then(r =>{
                console.log(r.message[0]);
                frm.set_value('sent',r.message[0]);
                frm.set_value('delay_duration',r.message[1])
            })  
        })
    } 
}
        // var qr_code = "[)>069KY0BP2GSWF211000080V3G563L3G56KJ0777Q00015910KY0B3G56100014544Z1237315"
        // console.log(qr_code.length)
        // // frm.call('parts')
        // .then(r =>{
        // })
    },
    qr:function(frm){
        frm.call('parts')
        .then(r =>{
            console.log("Parts")
            console.log(r.message)
            // frm.set_value("parts_no",r.message[0])
        })
        
        
    }

});
