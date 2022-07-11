frappe.ui.form.on('Bus Arrival Form', 
{
    //onload(frm) 
    //{ 		
        //var time = new Date().toLocaleTimeString();
	    //var time_format = moment(time, "h:mm:ss A").format("HH:mm");  
	    //frm.set_value('time',time_format);
 		//frappe.call({
 		  //  'method':'thaisummit.utils.get_bus_arrival_shift',
 		    //'args':
 		      //     {
 		        //   },
 		     //callback(r)
 		     //{
 		       // frm.set_value('shift',r.message[0]);
				//frm.set_value('status',r.message[1]);
				//frm.set_value('late_minutes',r.message[2]);
				//  console.log(r.message)
		    // },
 	      //})
    //},

    bus_number(frm)
	{
	    if(frm.doc.bus_number)
	    {
	        var vehcile_number = frm.doc.bus_number;
	        var change_upper_case = vehcile_number.toUpperCase();
	        frm.set_value('bus_number',change_upper_case);
	    }
	    
	    
	}
})