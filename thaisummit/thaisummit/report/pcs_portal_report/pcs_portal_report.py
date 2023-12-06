# Copyright (c) 2013, TEAMPRO and contributors
# For license information, please see license.txt

from frappe.model.document import Document
import datetime
import frappe
from frappe.model.document import Document
import math
import frappe
import json
import requests
import pandas as pd
import openpyxl
from six import BytesIO
from frappe.utils import (
    flt,
    cint,
    cstr,
    get_html_format,
    get_url_to_form,
    gzip_decompress,
    format_duration,
    today
)
from datetime import timedelta, datetime
# from __future__ import unicode_literals
from six.moves import range
from six import string_types
import frappe
import json
from frappe.utils import getdate,get_time, cint, add_months, date_diff, add_days, nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime
from datetime import datetime
from calendar import monthrange

from frappe import _, msgprint
from frappe.utils import flt
from frappe.utils import cstr, cint, getdate
import pandas as pd 
# from __future__ import unicode_literals
from functools import total_ordering
from itertools import count,groupby
# import more_itertools
import frappe
from frappe import permissions
from frappe.utils import cstr, cint, getdate, get_last_day, get_first_day, add_days
from frappe.utils import cstr, add_days, date_diff, getdate, format_date,now
from math import floor
from frappe import msgprint, _
from calendar import month, monthrange
from datetime import date, timedelta, datetime,time
from numpy import true_divide 
from six.moves import range
from six import string_types
import frappe
import json
from frappe.utils import getdate, cint, add_months, date_diff, add_days, nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime
from datetime import datetime
from calendar import monthrange
from frappe import _, msgprint
from frappe.utils import flt
from frappe.utils import cstr, cint, getdate
import pandas as pd
from datetime import datetime, timedelta
from datetime import datetime, timedelta
# from __future__ import unicode_literals
from functools import total_ordering
from itertools import count
import frappe
from frappe import permissions
from frappe.utils import cstr, cint, getdate, get_last_day, get_first_day, add_days
from frappe.utils import cstr, add_days, date_diff, getdate, format_date
from math import floor
from frappe import msgprint, _
from calendar import month, monthrange
from datetime import date, timedelta, datetime,time
from numpy import true_divide
import pandas as pd
import datetime as dt


def execute(filters=None):
    columns, data = [], []
    columns = get_columns(filters)
    data = get_data(filters)
    return columns, data

def get_columns(filters):
    columns = [
    _('Customer') + ':Data:180',
    _('Vendor Code') + ':Data:180',
    _('Vendor Name') + ':Data:180',
    _('Item Code') + ':Data:180',
    _('Part No') + ':Data:180',
    _('Item Description') + ':Data:180',
    _('Model') + ':Data:180',
    _('Grade') + ':Data:180',
    _('MAT Type') + ':Data:180',
    _('Size Type') + ':Data:180',
    _('RM Length') + ':Data:180',
    _('RM Width') + ':Data:180',
    _('RM Thick') + ':Data:180',
    _('Strip Qty') + ':Data:180',
    _('Gross Weight') + ':Data:180',
    _('Net Weight') + ':Data:180',
    _('Scrap Weight') + ':Data:180',
    _('RM Price') + ':Data:180',
    _('Gross WT Cost') + ':Data:180',
    _('Scrap Cost/kg') + ':Data:180',
    _('Scrap Cost') + ':Data:180',
    _('RM Cost') + ':Data:180',
    _('Process Cost') + ':Data:180',
    _('Admin Cost') + ':Data:180',
    _('Transport Cost') + ':Data:180',
    _('Final Part Cost') + ':Data:180',
    ]
    return columns

def get_data(filters):
    data = []
    scrap_weight = 0
    scrap_cost = 0
    final_part_cost = 0
    price = 0
    rm_cost = 0
    gross_wt_cost = 0
    cus = 0
    pcs_part_master = frappe.db.sql("""select * from `tabPCS Part Master` where customer ='%s' """%(filters.customer),as_dict=1)
    u_name = frappe.db.sql("""select username from `tabUser` where name='%s' """%(frappe.session.user),as_dict=1)[0]
    user_name = u_name['username']
    track = frappe.new_doc("PCS Report History")
    track.employee_id = user_name
    track.time = datetime.now().strftime('%H:%M:%S')
    track.date = date.today()
    track.customer = filters.customer
    track.save(ignore_permissions=True)
    frappe.db.commit()
    for p in pcs_part_master:
        if filters.customer == "IYM":
            if p.customer == "IYM":
                if p.mat_type == "TUBE":
                    tube_iym = frappe.get_single('RM Input').iym_tube
                    for iy in tube_iym:
                        if p.grade == iy.grade and p.rm_length == iy.rm_length:
                            # and p.rm__width == iy.rm_width and p.rm_thick == iy.rm_thick
                            frappe.errprint("yes")
                            if p.mat_type == "TUBE":
                                price = float(iy.new)
                            else:
                                price = 0
                            
                        scrap_master = frappe.get_doc('PCS Scrap Master','PCS Scrap Master')
                        frappe.errprint("hlo")
                        for s in scrap_master.scrap_master:
                            if p.vendor_name == s.vendor_name:
                                cus = s.iym
                            gross_weight = float(p.gross_weight)
                            net_weight = float(p.net_weight)
                            gross_wt_cost = round((gross_weight * price),3)
                            scrap_weight = round((gross_weight - net_weight),3)
                            scrap_cost = round((scrap_weight * float(s.iym)),2)
                            # rm_cost = round((gross_wt_cost - scrap_cost),3)
                            rm_cost = round((price * gross_weight),2)
                            frappe.errprint(rm_cost)
                            frappe.errprint("no")
                            # final_part_cost = round((float(p.process_cost) + float(p.admin_cost) + float(rm_cost) + float(p.transport_cost)),3)
                            final_part_cost = round(((float(p.process_cost) + float(p.admin_cost) + float(rm_cost) + float(p.transport_cost)) - float(p.reduction_cost)),2)
                               
                elif p.mat_type == "MACHINING/WIRE" or p.mat_type == "MACHINING/WIRE/COATING/PLATING":
                    price = 0
                    gross_weight = 0
                    net_weight = 0
                    gross_wt_cost = 0
                    final_part_cost = round((p.final_amount),2)
                    rm_cost = 0
                    scrap_weight = 0
                    scrap_cost = 0
                    cus = 0
                else:
                    rm_price_iym = frappe.get_single('RM Input').rm_input_table1
                    for r in rm_price_iym:
                        if p.grade == r.grade:
                            if p.size_type == ">100":
                                price = r.new1
                            elif p.size_type == "<100":
                                price = r.new2
                            elif p.size_type == "STD SHEET":
                                price = r.std_new
                            else:
                                price = 0
                                   
                        scrap_master = frappe.get_doc('PCS Scrap Master','PCS Scrap Master')
                        frappe.errprint("hi")
                        for s in scrap_master.scrap_master:
                            if p.vendor_name == s.vendor_name:
                                cus = s.iym
                            gross_weight = float(p.gross_weight)
                            net_weight = float(p.net_weight)
                            gross_wt_cost = (gross_weight * price)
                            scrap_weight = (gross_weight - net_weight)
                            scrap_cost = (scrap_weight * float(cus))
                            rm_cost = (gross_wt_cost - scrap_cost)
                            # final_part_cost = round((float(p.process_cost) + float(p.admin_cost) + float(rm_cost) + float(p.transport_cost)),3)
                            final_part_cost = round((float(p.process_cost) + float(p.admin_cost) + float(rm_cost) + float(p.transport_cost) - float(p.reduction_cost)),2)

        elif filters.customer == "RE":
            if p.customer == "RE":
                if p.mat_type == "MACHINING/WIRE/COATING/PLATING":
                    price = 0
                    gross_weight = 0
                    net_weight = 0
                    gross_wt_cost = 0
                    final_part_cost = round((p.final_amount),2)
                    rm_cost = 0
                    scrap_weight = 0
                    scrap_cost = 0
                    cus = 0
                elif p.mat_type == 'STRIP' or p.mat_type == 'COIL':
                    rm_price_re = frappe.get_single('RM Input').rm_input_table2
                    for r in rm_price_re:
                        if p.grade == r.grade:
                            if p.mat_type == 'STRIP':
                                if p.size_type == ">100":
                                    price = r.new1
                                elif p.size_type == "<100":
                                    price = r.new2
                                else:
                                    price = 0
                            elif p.mat_type == 'COIL':
                                if p.size_type == ">100": 
                                    price = r.coil_new
                                elif p.size_type == "<100":
                                    price = r.coil_new1
                                else:
                                    price = 0
                            scrap_master = frappe.get_doc('PCS Scrap Master','PCS Scrap Master')
                            for s in scrap_master.scrap_master:
                                if p.vendor_name == s.vendor_name:
                                    cus = s.re
                                gross_weight = float(p.gross_weight)
                                net_weight = float(p.net_weight)
                                gross_wt_cost = (gross_weight * price)
                                scrap_weight = (gross_weight - net_weight)
                                scrap_cost = (scrap_weight * float(cus))
                                rm_cost = (gross_wt_cost - scrap_cost)
                                # rm_cost = round((price * gross_weight),3)
                                # final_part_cost = round((float(p.process_cost) + float(p.admin_cost) + float(rm_cost) + float(p.transport_cost)),3)
                                final_part_cost = round(((float(p.process_cost) + float(p.admin_cost) + float(rm_cost) + float(p.transport_cost)) - float(p.reduction_cost)),2)

                elif p.mat_type == "TUBE":
                    tube_re = frappe.get_single('RM Input').re_tube
                    for t in tube_re:
                        if p.grade == t.grade and p.rm_length == t.rm_length and p.rm__width == t.rm_width and p.rm_thick == t.rm_thick:
                            if p.mat_type == "TUBE":
                                price = t.new
                            else:
                                price = 0
                            scrap_master = frappe.get_doc('PCS Scrap Master','PCS Scrap Master')
                            for s in scrap_master.scrap_master:
                                if p.vendor_name == s.vendor_name:
                                    cus = s.re
                            gross_weight = float(p.gross_weight)
                            net_weight = float(p.net_weight)
                            gross_wt_cost = round((gross_weight * price),3)
                            scrap_weight = round((gross_weight - net_weight),3)
                            scrap_cost = round((scrap_weight * float(s.re)),2)
                            # rm_cost = round((gross_wt_cost - scrap_cost),3)
                            rm_cost = round((price * gross_weight),2)
                            final_part_cost = round(((float(p.process_cost) + float(p.admin_cost) + float(rm_cost) + float(p.transport_cost)) - float(p.reduction_cost)),2)
        
        row =[p.customer,p.vendor_code,p.vendor_name,p.item_code,p.part_no,p.parts_name,p.model,p.grade,p.mat_type,p.size_type,p.rm_length,p.rm__width,p.rm_thick,p.strip_qty,p.gross_weight,p.net_weight,scrap_weight,price,gross_wt_cost,cus,scrap_cost,rm_cost,(float(p.process_cost)),(float(p.admin_cost)),(float(p.transport_cost)),(final_part_cost)]
        data.append(row)
    return data

# # Copyright (c) 2013, TEAMPRO and contributors
# # For license information, please see license.txt

# from frappe.model.document import Document
# import datetime
# import frappe
# from frappe.model.document import Document
# import math
# import frappe
# import json
# import requests
# import pandas as pd
# import openpyxl
# from six import BytesIO
# from frappe.utils import (
#     flt,
#     cint,
#     cstr,
#     get_html_format,
#     get_url_to_form,
#     gzip_decompress,
#     format_duration,
#     today
# )
# from datetime import timedelta, datetime
# # from __future__ import unicode_literals
# from six.moves import range
# from six import string_types
# import frappe
# import json
# from frappe.utils import getdate,get_time, cint, add_months, date_diff, add_days, nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime
# from datetime import datetime
# from calendar import monthrange

# from frappe import _, msgprint
# from frappe.utils import flt
# from frappe.utils import cstr, cint, getdate
# import pandas as pd 
# # from __future__ import unicode_literals
# from functools import total_ordering
# from itertools import count,groupby
# # import more_itertools
# import frappe
# from frappe import permissions
# from frappe.utils import cstr, cint, getdate, get_last_day, get_first_day, add_days
# from frappe.utils import cstr, add_days, date_diff, getdate, format_date,now
# from math import floor
# from frappe import msgprint, _
# from calendar import month, monthrange
# from datetime import date, timedelta, datetime,time
# from numpy import true_divide 
# from six.moves import range
# from six import string_types
# import frappe
# import json
# from frappe.utils import getdate, cint, add_months, date_diff, add_days, nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime
# from datetime import datetime
# from calendar import monthrange
# from frappe import _, msgprint
# from frappe.utils import flt
# from frappe.utils import cstr, cint, getdate
# import pandas as pd
# from datetime import datetime, timedelta
# from datetime import datetime, timedelta
# # from __future__ import unicode_literals
# from functools import total_ordering
# from itertools import count
# import frappe
# from frappe import permissions
# from frappe.utils import cstr, cint, getdate, get_last_day, get_first_day, add_days
# from frappe.utils import cstr, add_days, date_diff, getdate, format_date
# from math import floor
# from frappe import msgprint, _
# from calendar import month, monthrange
# from datetime import date, timedelta, datetime,time
# from numpy import true_divide
# import pandas as pd
# import datetime as dt


# def execute(filters=None):
#     columns, data = [], []
#     columns = get_columns(filters)
#     data = get_data(filters)
#     return columns, data

# def get_columns(filters):
#     columns = [
#     _('Customer') + ':Data:180',
#     _('Vendor Code') + ':Data:180',
#     _('Vendor Name') + ':Data:180',
#     _('Item Code') + ':Data:180',
#     _('Part No') + ':Data:180',
#     _('Item Description') + ':Data:180',
#     _('Model') + ':Data:180',
#     _('Grade') + ':Data:180',
#     _('MAT Type') + ':Data:180',
#     _('Size Type') + ':Data:180',
#     _('RM Length') + ':Data:180',
#     _('RM Width') + ':Data:180',
#     _('RM Thick') + ':Data:180',
#     _('Strip Qty') + ':Data:180',
#     _('Gross Weight') + ':Data:180',
#     _('Net Weight') + ':Data:180',
#     _('Scrap Weight') + ':Data:180',
#     _('RM Price') + ':Data:180',
#     _('Gross WT Cost') + ':Data:180',
#     _('Scrap Cost/kg') + ':Data:180',
#     _('Scrap Cost') + ':Data:180',
#     _('RM Cost') + ':Data:180',
#     _('Process Cost') + ':Data:180',
#     _('Admin Cost') + ':Data:180',
#     _('Transport Cost') + ':Data:180',
#     _('Final Part Cost') + ':Data:180',
#     ]
#     return columns

# def get_data(filters):
#     data = []
#     scrap_weight = 0
#     scrap_cost = 0
#     final_part_cost = 0
#     price = 0
#     rm_cost = 0
#     gross_wt_cost = 0
#     cus = 0
#     pcs_part_master = frappe.db.sql("""select * from `tabPCS Part Master` where customer ='%s' """%(filters.customer),as_dict=1)
#     u_name = frappe.db.sql("""select username from `tabUser` where name='%s' """%(frappe.session.user),as_dict=1)[0]
#     user_name = u_name['username']
#     track = frappe.new_doc("PCS Report History")
#     track.employee_id = user_name
#     track.time = datetime.now().strftime('%H:%M:%S')
#     track.date = date.today()
#     track.customer = filters.customer
#     track.save(ignore_permissions=True)
#     frappe.db.commit()
#     for p in pcs_part_master:
#         if filters.customer == "IYM":
#             if p.customer == "IYM":
#                 if p.mat_type == "TUBE":
#                     tube_iym = frappe.get_single('RM Input').iym_tube
#                     for iy in tube_iym:
#                         if p.grade == iy.grade and p.rm_length == iy.rm_length:
#                             # and p.rm__width == iy.rm_width and p.rm_thick == iy.rm_thick
#                             frappe.errprint("yes")
#                             if p.mat_type == "TUBE":
#                                 price = float(iy.new)
#                             else:
#                                 price = 0
                            
#                             scrap_master = frappe.get_doc('PCS Scrap Master','PCS Scrap Master')
#                             frappe.errprint("hlo")
#                             for s in scrap_master.scrap_master:
#                                 if p.vendor_name == s.vendor_name:
#                                     cus = s.iym
#                                 gross_weight = float(p.gross_weight)
#                                 net_weight = float(p.net_weight)
#                                 gross_wt_cost = float(gross_weight * price)
#                                 scrap_weight = float(gross_weight - net_weight)
#                                 scrap_cost = float(scrap_weight * float(s.iym))
#                                 # rm_cost = (gross_wt_cost - scrap_cost)
#                                 rm_cost = float(price * gross_weight)
#                                 frappe.errprint(rm_cost)
#                                 frappe.errprint("no")
#                                 final_part_cost = float(float(p.process_cost) + float(p.admin_cost) + float(rm_cost) + float(p.transport_cost))
                        
                                
#                 elif p.mat_type == "MACHINING/WIRE" or p.mat_type == "MACHINING/WIRE/COATING/PLATING":
#                     price = 0
#                     gross_weight = 0
#                     net_weight = 0
#                     gross_wt_cost = 0
#                     final_part_cost = p.final
#                     rm_cost = 0
#                     scrap_weight = 0
#                     scrap_cost = 0
#                     cus = 0
#                 else:
#                     rm_price_iym = frappe.get_single('RM Input').rm_input_table1
#                     for r in rm_price_iym:
#                         if p.grade == r.grade:
#                             if p.size_type == ">100":
#                                 price = r.new1
#                             elif p.size_type == "<100":
#                                 price = r.new2
#                             elif p.size_type == "STD SHEET":
#                                 price = r.std_new
#                             else:
#                                 price = 0
                                   
#                     scrap_master = frappe.get_doc('PCS Scrap Master','PCS Scrap Master')
#                     frappe.errprint("hi")
#                     for s in scrap_master.scrap_master:
#                         if p.vendor_name == s.vendor_name:
#                             cus = s.iym
#                         gross_weight = float(p.gross_weight)
#                         net_weight = float(p.net_weight)
#                         gross_wt_cost = float(gross_weight * price),
#                         scrap_weight = float(gross_weight - net_weight),
#                         scrap_cost = float(scrap_weight * float(s.iym)),
#                         rm_cost = float(gross_wt_cost - scrap_cost),
#                         final_part_cost = float(float(p.process_cost) + float(p.admin_cost) + float(rm_cost) + float(p.transport_cost)),
                                        
#         elif filters.customer == "RE":
#             if p.customer == "RE":
#                 if p.mat_type == "MACHINING/WIRE/COATING/PLATING":
#                     price = 0
#                     gross_weight = 0
#                     net_weight = 0
#                     gross_wt_cost = 0
#                     final_part_cost = p.final
#                     rm_cost = 0
#                     scrap_weight = 0
#                     scrap_cost = 0
#                     cus = 0
#                 elif p.mat_type == 'STRIP' or p.mat_type == 'COIL':
#                     rm_price_re = frappe.get_single('RM Input').rm_input_table2
#                     for r in rm_price_re:
#                         if p.grade == r.grade:
#                             if p.mat_type == 'STRIP':
#                                 if p.size_type == ">100":
#                                     price = r.new1
#                                 elif p.size_type == "<100":
#                                     price = r.new2
#                                 else:
#                                     price = 0
#                             elif p.mat_type == 'COIL':
#                                 if p.size_type == ">100": 
#                                     price = r.coil_new
#                                 elif p.size_type == "<100":
#                                     price = r.coil_new1
#                                 else:
#                                     price = 0
#                             scrap_master = frappe.get_doc('PCS Scrap Master','PCS Scrap Master')
#                             for s in scrap_master.scrap_master:
#                                 if p.vendor_name == s.vendor_name:
#                                     cus = s.re
#                                 gross_weight = float(p.gross_weight)
#                                 net_weight = float(p.net_weight)
#                                 gross_wt_cost = float(gross_weight * price)
#                                 scrap_weight = float(gross_weight - net_weight)
#                                 scrap_cost = float(scrap_weight * float(s.re))
#                                 rm_cost = float(gross_wt_cost - scrap_cost)
#                                 # rm_cost = (price * gross_weight)
#                                 final_part_cost = float(float(p.process_cost) + float(p.admin_cost) + float(rm_cost) + float(p.transport_cost))
                    
#                 elif p.mat_type == "TUBE":
#                     tube_re = frappe.get_single('RM Input').re_tube
#                     for t in tube_re:
#                         if p.grade == t.grade and p.rm_length == t.rm_length and p.rm__width == t.rm_width and p.rm_thick == t.rm_thick:
#                             if p.mat_type == "TUBE":
#                                 price = t.new
#                             else:
#                                 price = 0
#                             scrap_master = frappe.get_doc('PCS Scrap Master','PCS Scrap Master')
#                             for s in scrap_master.scrap_master:
#                                 if p.vendor_name == s.vendor_name:
#                                     cus = s.re
#                             gross_weight = float(p.gross_weight)
#                             net_weight = float(p.net_weight)
#                             gross_wt_cost = float(gross_weight * price)
#                             scrap_weight = float(gross_weight - net_weight)
#                             scrap_cost = float(scrap_weight * float(s.re))
#                             # rm_cost = (gross_wt_cost - scrap_cost)
#                             rm_cost = float(price * gross_weight)
#                             final_part_cost = float(float(p.process_cost) + float(p.admin_cost) + float(rm_cost) + float(p.transport_cost))
        
#         row =[p.customer,p.vendor_code,p.vendor_name,p.item_code,p.part_no,p.parts_name,p.model,p.grade,p.mat_type,p.size_type,p.rm_length,p.rm__width,p.rm_thick,p.strip_qty,(p.gross_weight),p.net_weight,scrap_weight,price,gross_wt_cost,cus,scrap_cost,rm_cost,float(p.process_cost),round(float(p.admin_cost),3),round(float(p.transport_cost),3),final_part_cost]
#         data.append(row)
#     return data









