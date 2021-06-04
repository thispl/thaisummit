# -*- coding: utf-8 -*-
# Copyright (c) 2021, TEAMPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import cstr, add_days, date_diff, getdate
from frappe import _
from frappe.utils.csvutils import UnicodeWriter, read_csv_content
from frappe.utils.file_manager import get_file
from frappe.model.document import Document

class ShiftSchedule(Document):
	def date_diff(self):
		if self.from_date and self.to_date:
			diff = date_diff(self.to_date,self.from_date)
			if diff > 5:
				frappe.throw("Shift Schedule can't be raised for more than 6 days")

	def on_submit(self):
		sas = frappe.get_all("Shift Assignment",{'shift_schedule':self.name,'docstatus':'0'})
		for sa in sas:
			doc = frappe.get_doc('Shift Assignment',sa.name)
			doc.submit()
			frappe.db.commit()
		frappe.msgprint('Shift Schedule Approved Successfully')

	def validate_employees(self):
		filepath = get_file(self.upload)
		pps = read_csv_content(filepath[1])
		dates = self.get_dates()
		err_list = ""
		for pp in pps:
			if pp[0] != 'ID':
				if pp[0]:
					if not pp[1]:
						err_list +='<li>Employe Name should not be Empty. </li>'
					if not pp[2]:
						err_list +='<li>Department should not be Empty. </li>'
					if not pp[3]:
						err_list +='<li>Department Code should not be Empty. </li>'
					if not pp[4]:
						err_list +='<li>Employee Type should not be Empty. </li>'
					# if not pp[5]:
					# 	err_list +='<li>Shift should not be Empty. </li>'
					if not pp[6]:
						err_list +='<li>Route should not be Empty. </li>'
					if not pp[7]:
						err_list +='<li>Boarding Point should not be Empty. </li>'
					if not frappe.db.exists("Employee",{'name':pp[0],'status':'Active'}):
						err_list +='<li><font color="red"><b>%s</b></font> is not an Active Employee. </li>'%(pp[0])
					else:
						if self.department != frappe.db.get_value("Employee",pp[0],"department"):
							err_list += '<li><font color="red"><b>%s</b></font> doesnot belongs to <b>%s</b> department. </li>'%(pp[0],self.department)
						else:
							if pp[5]:
								for date in dates:
									sa = frappe.db.exists('Shift Assignment',{'employee':pp[0],'start_date':date,'docstatus':['!=','2']})
									if sa:
										err_list += '<li>%s department have already allocated shift for <font color="red"><b>%s</b></font> for the date %s </li>'%(frappe.db.get_value("Shift Assignment",sa,"department"),pp[0],date)
							else:
								err_list += '<li>Shift value missing for <font color="red"><b>%s</b></font> in the upload sheet.</li>'%(pp[0])
				else:
					li = [pp[1],pp[2],pp[3],pp[4],pp[5],pp[6],pp[7]]
					if len(li) != 8:
						err_list += '<li>ID should not be Empty.</li>'

		return err_list

	def get_dates(self):
		"""get list of dates in between from date and to date"""
		no_of_days = date_diff(add_days(self.to_date, 1), self.from_date)
		dates = [add_days(self.from_date, i) for i in range(0, no_of_days)]
		return dates

	def show_csv_data(self):
		filepath = get_file(self.upload)
		pps = read_csv_content(filepath[1])
		data_list = ''
		for pp in pps:
			if pp[0] == 'ID':
				data_list += "<tr><td style='background-color:#f0b27a; border: 1px solid black'>%s</td><td style='background-color:#f0b27a; border: 1px solid black'>%s</td><td style='background-color:#f0b27a; border: 1px solid black'>%s</td><td style='background-color:#f0b27a; border: 1px solid black'>%s</td><td style='background-color:#f0b27a; border: 1px solid black'>%s</td><td style='background-color:#f0b27a; border: 1px solid black'>%s</td><td style='background-color:#f0b27a; border: 1px solid black'>%s</td><td style='background-color:#f0b27a; border: 1px solid black'>%s</td></tr>"%(pp[0],pp[1],pp[2],pp[3],pp[4],pp[5],pp[6],pp[7])
			else:
				data_list += "<tr><td style = 'border: 1px solid black'>%s</td><td style = 'border: 1px solid black'>%s</td><td style = 'border: 1px solid black'>%s</td><td style = 'border: 1px solid black'>%s</td><td style = 'border: 1px solid black'>%s</td><td style = 'border: 1px solid black'>%s</td><td style = 'border: 1px solid black'>%s</td><td style = 'border: 1px solid black'>%s</td></tr>"%(pp[0],pp[1],pp[2],pp[3],pp[4],pp[5],pp[6],pp[7])

		return data_list

	def show_summary(self):
		filepath = get_file(self.upload)
		pps = read_csv_content(filepath[1])
		data = ''
		# wc1,wc2,wc3,wcpp1,wcpp2,bc1,bc2,bc3,bcpp1,bcpp2,ft1,ft2,ft3,ftpp1,ftpp2,nt1,nt2,nt3,ntpp1,ntpp2,cl1,cl2,cl3,clpp1,clpp2 =0
		wc1 = 0
		wc2 = 0
		wc3 = 0
		wcpp1 = 0
		wcpp2 = 0
		bc1 = 0
		bc2 = 0
		bc3 = 0
		bcpp1 = 0
		bcpp2 = 0
		ft1 = 0
		ft2 = 0
		ft3 = 0
		ftpp1 = 0
		ftpp2 = 0
		nt1 = 0
		nt2 = 0
		nt3 = 0
		ntpp1 = 0
		ntpp2 = 0
		cl1 = 0
		cl2 = 0
		cl3 = 0
		clpp1 = 0
		clpp2 =0
		for pp in pps:
			if pp[4] == 'WC':
				if pp[5] == "1":
					wc1 +=1
				elif pp[5] == "2":
					wc2 +=1
				elif pp[5] == "3":
					wc3 +=1
				elif pp[5] == "PP1":
					wcpp1 +=1
				elif pp[5] == "PP2":
					wcpp2 +=1
			if pp[4] == 'BC':
				if pp[5] == "1":
					bc1 +=1
				elif pp[5] == "2":
					bc2 +=1
				elif pp[5] == "3":
					wc3 +=1
				elif pp[5] == "PP1":
					bcpp1 +=1
				elif pp[5] == "PP2":
					bcpp2 +=1
			if pp[4] == 'FT':
				if pp[5] == "1":
					ft1 +=1
				elif pp[5] == "2":
					ft2 +=1
				elif pp[5] == "3":
					wc3 +=1
				elif pp[5] == "PP1":
					ftpp1 +=1
				elif pp[5] == "PP2":
					ftpp2 +=1
			if pp[4] == 'nt':
				if pp[5] == "1":
					nt1 +=1
				elif pp[5] == "2":
					nt2 +=1
				elif pp[5] == "3":
					wc3 +=1
				elif pp[5] == "PP1":
					ntpp1 +=1
				elif pp[5] == "PP2":
					ntpp2 +=1
			if pp[4] == 'CL':
				if pp[5] == "1":
					cl1 +=1
				elif pp[5] == "2":
					cl2 +=1
				elif pp[5] == "3":
					wc3 +=1
				elif pp[5] == "PP1":
					clpp1 +=1
				elif pp[5] == "PP2":
					clpp2 +=1
		total = wc1+wc2+wc3+wcpp1+wcpp2+bc1+bc2+bc3+bcpp1+bcpp2+ft1+ft2+ft3+ftpp1+ftpp2+nt1+nt2+nt3+ntpp1+ntpp2+cl1+cl2+cl3+clpp1+clpp2
		data += """
			<td style="background-color:#f0b27a; border: 1px solid black">Shift</td><td style="background-color:#f0b27a ; border: 1px solid black">1</td><td style="background-color:#f0b27a; border: 1px solid black">2</td><td style="background-color:#f0b27a; border: 1px solid black">3</td><td style="background-color:#f0b27a; border: 1px solid black">PP1</td><td style="background-color:#f0b27a; border: 1px solid black">PP2</td><td style="background-color:#f0b27a ; border: 1px solid black">Total</td>
			</tr>
			<tr>
				<th style = 'border: 1px solid black'>WC</th><td style = 'border: 1px solid black'>%s</td><td style = 'border: 1px solid black'>%s</td><td style = 'border: 1px solid black'>%s</td><td style = 'border: 1px solid black'>%s</td><td style = 'border: 1px solid black'>%s</td><td style="background-color:#58d68d ; border: 1px solid black">%s</td>
			</tr>
			<tr>
				<th style = 'border: 1px solid black'>BC</th><td style = 'border: 1px solid black'>%s</td><td style = 'border: 1px solid black'>%s</td><td style = 'border: 1px solid black'>%s</td><td style = 'border: 1px solid black'>%s</td><td style = 'border: 1px solid black'>%s</td><td style="background-color:#58d68d ; border: 1px solid black">%s</td>
			</tr>
			<tr>
				<th style = 'border: 1px solid black'>FT</th><td style = 'border: 1px solid black'>%s</td><td style = 'border: 1px solid black'>%s</td><td style = 'border: 1px solid black'>%s</td><td style = 'border: 1px solid black'>%s</td><td style = 'border: 1px solid black'>%s</td><td style="background-color:#58d68d; border: 1px solid black">%s</td>
			</tr>
			<tr>
				<th style = 'border: 1px solid black'>NT</th><td style = 'border: 1px solid black'>%s</td><td style = 'border: 1px solid black'>%s</td><td style = 'border: 1px solid black'>%s</td><td style = 'border: 1px solid black'>%s</td><td style = 'border: 1px solid black'>%s</td><td style="background-color:#58d68d; border: 1px solid black">%s</td>
			</tr>
			<tr>
				<th style = 'border: 1px solid black'>CL</th><td style = 'border: 1px solid black'>%s</td><td style = 'border: 1px solid black'>%s</td><td style = 'border: 1px solid black'>%s</td><td style = 'border: 1px solid black'>%s</td><td style = 'border: 1px solid black'>%s</td><td style="background-color:#58d68d; border: 1px solid black">%s</td>
			</tr>
			<tr>
				<td style="background-color:#58d68d; border: 1px solid black">Total</td><td style="background-color:#58d68d; border: 1px solid black">%s</td><td style="background-color:#58d68d; border: 1px solid black">%s</td><td style="background-color:#58d68d; border: 1px solid black">%s</td><td style="background-color:#58d68d; border: 1px solid black">%s</td><td style="background-color:#58d68d; border: 1px solid black">%s</td><td style="background-color:#58d68d; border: 1px solid black">%s</td>
			</tr>"""%(wc1,wc2,wc3,wcpp1,wcpp2,(wc1+wc2+wc3+wcpp1+wcpp2),bc1,bc2,bc3,bcpp1,bcpp2,(bc1+bc2+bc3+bcpp1+bcpp2),ft1,ft2,ft3,ftpp1,ftpp2,(ft1+ft2+ft3+ftpp1+ftpp2),nt1,nt2,nt3,ntpp1,ntpp2,(nt1+nt2+nt3+ntpp1+ntpp2),cl1,cl2,cl3,clpp1,clpp2,(cl1+cl2+cl3+clpp1+clpp2),(wc1+bc1+ft1+nt1+cl1),(wc2+bc2+ft2+nt2+cl2),(wc3+bc3+ft3+nt3+cl3),(wcpp1+bcpp1+ftpp1+ntpp1+clpp1),(wcpp2+bcpp2+ftpp2+ntpp2+clpp2),total)

		return data


@frappe.whitelist()
def create_shift_assignment(file,from_date,to_date,name):
	filepath = get_file(file)
	pps = read_csv_content(filepath[1])
	no_of_days = date_diff(add_days(to_date, 1), from_date)
	dates = [add_days(from_date, i) for i in range(0, no_of_days)]
	for pp in pps:
		if pp[5] != 'Shift':
			if pp[5]:
				for date in dates:
					if not frappe.db.exists("Shift Assignment",{'employee':pp[0],'start_date':date,'end_date':date,'docstatus':['in',[0,1]]}):
						doc = frappe.new_doc("Shift Assignment")
						doc.employee = pp[0]
						doc.shift_type = pp[5]
						doc.start_date = date
						doc.end_date = date
						doc.route_no = pp[6]
						doc.boarding_point = pp[7]
						doc.shift_schedule = name
						doc.save(ignore_permissions=True)
						frappe.db.commit()
				frappe.db.set_value('Employee',pp[0],"default_shift",pp[5])
	frappe.msgprint('Shift Schedule uploaded successfully')
	

@frappe.whitelist()
def get_template():
	args = frappe.local.form_dict

	if getdate(args.from_date) > getdate(args.to_date):
		frappe.throw(_("To Date should be greater than From Date"))

	w = UnicodeWriter()
	w = add_header(w)

	w = add_data(w, args)
	

	# write out response as a type csv
	frappe.response['result'] = cstr(w.getvalue())
	frappe.response['type'] = 'csv'
	frappe.response['doctype'] = "Shift Assignment"

def add_header(w):
	w.writerow(["ID", "Name", "Department", "Department Code", "Type", "Shift","Route No","Boarding Point"])
	return w

def add_data(w, args):
	data = get_data(args)
	writedata(w, data)
	return w

def get_data(args):
	employees = get_active_employees(args)
	data = []
	for employee in employees:
		row = [
			employee.name, employee.employee_name, employee.department,frappe.db.get_value("Department",employee.department,"department_code"),employee.employee_type,employee.default_shift,employee.route_no or 'NB',employee.boarding_point or 'NB'
		]
		data.append(row)
	return data



def writedata(w, data):
	for row in data:
		w.writerow(row)


def get_active_employees(args):
	employees = frappe.db.get_all('Employee',
		fields=['name', 'employee_name', 'department', 'date_of_joining', 'company', 'relieving_date','employee_type','boarding_point','default_shift','route_no'],
		filters={
			'docstatus': ['<', 2],
			'status': 'Active',
			'department': (args["department"]).replace("1","&")
		}
	)
	return employees


@frappe.whitelist()
def shift_wise_count(doc):
	employee_type = ["BC","WC","CL","NT","FT"]
	data = "<table class='table table-bordered'><tr><td colspan='2' style='background-color:#f0b27a'><center>Shift 1</center></td><td colspan='2' style='background-color:#f0b27a'><center>Shift 2</center></td><td colspan='2' style='background-color:#f0b27a'><center>Shift 3</center></td><td colspan='2' style='background-color:#f0b27a'><center>Shift PP1</center></td><td colspan='2' style='background-color:#f0b27a'><center>Shift PP2</center></td><td colspan='2' style='background-color:#f0b27a'><center>Total Head Count</center></td></tr>"
	for emp_type in employee_type:
		s1 = 0
		s2 = 0
		s3 = 0
		spp1 = 0
		spp2 = 0
		shift1 = frappe.db.sql("select count(*) as count from `tabShift Assignment` where shift_type = '1' and docstatus != 2 and start_date = '%s' and employee_type = '%s' "%(doc.from_date,emp_type),as_dict=True)
		shift2 = frappe.db.sql("select count(*) as count from `tabShift Assignment` where shift_type = '2' and docstatus != 2 and start_date = '%s' and employee_type = '%s' "%(doc.from_date,emp_type),as_dict=True)
		shift3 = frappe.db.sql("select count(*) as count from `tabShift Assignment` where shift_type = '3' and docstatus != 2 and start_date = '%s' and employee_type = '%s' "%(doc.from_date,emp_type),as_dict=True)
		shiftpp1 = frappe.db.sql("select count(*) as count from `tabShift Assignment` where shift_type = 'PP1' and docstatus != 2 and start_date = '%s' and employee_type = '%s' "%(doc.from_date,emp_type),as_dict=True)
		shiftpp2 = frappe.db.sql("select count(*) as count from `tabShift Assignment` where shift_type = 'PP2' and docstatus != 2 and start_date = '%s' and employee_type = '%s' "%(doc.from_date,emp_type),as_dict=True)
		if shift1:
			s1 = shift1[0].count
		if shift2:
			s2 = shift2[0].count
		if shift3:
			s3 = shift3[0].count
		if shiftpp1:
			spp1 = shiftpp1[0].count
		if shiftpp2:
			spp2 = shiftpp2[0].count
		total = s1+s2+s3+spp1+spp2
		data += '<tr><td style="background-color:#58d68d">%s</td><td>%s</td><td style="background-color:#58d68d">%s</td><td>%s</td><td style="background-color:#58d68d">%s</td><td>%s</td><td style="background-color:#58d68d">%s</td><td>%s</td><td style="background-color:#58d68d">%s</td><td>%s</td><td style="background-color:#58d68d">%s</td><td>%s</td></tr>'%(emp_type,s1,emp_type,s2,emp_type,s3,emp_type,spp1,emp_type,spp2,emp_type,total)
	sf1 = frappe.db.sql("select count(*) as count from `tabShift Assignment` where shift_type = '1' and docstatus != 2 and start_date = '%s' "%(doc.from_date),as_dict=True)
	sf2 = frappe.db.sql("select count(*) as count from `tabShift Assignment` where shift_type = '2' and docstatus != 2 and start_date = '%s' "%(doc.from_date),as_dict=True)
	sf3 = frappe.db.sql("select count(*) as count from `tabShift Assignment` where shift_type = '3' and docstatus != 2 and start_date = '%s' "%(doc.from_date),as_dict=True)
	sfpp1 = frappe.db.sql("select count(*) as count from `tabShift Assignment` where shift_type = 'PP1' and docstatus != 2 and start_date = '%s' "%(doc.from_date),as_dict=True)
	sfpp2 = frappe.db.sql("select count(*) as count from `tabShift Assignment` where shift_type = 'PP2' and docstatus != 2 and start_date = '%s' "%(doc.from_date),as_dict=True)

	data += '<tr><td style="background-color:#f0b27a">Total</td><td>%s</td><td style="background-color:#f0b27a">Total</td><td>%s</td><td style="background-color:#f0b27a">Total</td><td>%s</td><td style="background-color:#f0b27a">Total</td><td>%s</td><td style="background-color:#f0b27a">Total</td><td>%s</td><td style="background-color:#f0b27a">Total</td><td>%s</td></tr>'%(sf1[0].count,sf2[0].count,sf3[0].count,sfpp1[0].count,sfpp2[0].count,sf1[0].count+sf2[0].count+sf3[0].count+sfpp1[0].count+sfpp2[0].count)
	data = data + '</table>' 
	return data


@frappe.whitelist()
def shift_employees(doc,shift):
	shift_emp = frappe.db.sql("select employee,employee_name from `tabShift Assignment` where shift_type = '%s' and docstatus != 2 and start_date = '%s' "%(shift,doc.from_date),as_dict=True)
	data = "<table class='table table-bordered'><tr><td style='background-color:#f0b27a'><center>S.No</center></td><td colspan='2' style='background-color:#f0b27a'><center>Shift %s</center></td></tr>"%(shift)
	if shift_emp:
		i = 1
		for s in shift_emp:
			data += '<tr><td style="background-color:#f0b27a">%s</td><td style="background-color:#58d68d">%s</td><td>%s</td></tr>'%(i,s.employee,s.employee_name)
			i += 1
	else:
		data += '<tr><td></td><td></td></tr>'
	data = data + '</table>'
	return data

