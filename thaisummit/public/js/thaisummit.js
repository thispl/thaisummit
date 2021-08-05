// dom ready
document.addEventListener("DOMContentLoaded", (event)=>{
    // navbar and anchor element
    let page_actions = document.querySelector(".page-actions");
    if (page_actions){
        let anc = document.createElement('a');
    anc.href = "/app/attendance-dashboard/Attendance%20Dashboard"
    anc.innerHTML = '<div><i class="fa fa-address-card"></i> &nbsp;<b>Attendance Dashboard</b></div>'
    page_actions.prepend(anc)

    }

    let std_actions = document.querySelector(".standard-actions");
    std_actions.classList.add('hide');
    

    let container = document.querySelector(".container");
    let para = document.createElement('p');
    let role = 'Employee'
    if(frappe.user.has_role('CEO')){
        role = 'CEO'
    }
    else if(frappe.user.has_role('HR GM')){
        role = 'HR GM'
    }
    else if(frappe.user.has_role('HOD')){
        role = 'HOD'
    }
    para.innerHTML = '<div style="text-align:center;"> &nbsp; &nbsp;<i class="fa fa-user"></i> &nbsp;'+ role +'</div>'
    container.appendChild(para)
  })