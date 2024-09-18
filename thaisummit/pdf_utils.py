import frappe
import os
from PyPDF2 import PdfFileReader, PdfFileWriter

def generate_combined_pdf():
    # Fetch the document and its attachments
    doctype = 'Attendance'
    docname = 'HR-ATT-2024-258618'
    doc = frappe.get_doc(doctype, docname)
    attachments = frappe.get_all('File', filters={'attached_to_name': docname, 'attached_to_doctype': doctype})

    # Generate the PDF
    pdf_content = generate_pdf_from_doctype(doctype, doc)

    # Merge PDFs
    pdf_writer = PdfFileWriter()
    pdf_writer.appendPagesFromReader(PdfFileReader(pdf_content))

    for attachment in attachments:
        attachment_path = frappe.get_site_path('public', attachment.file_url)
        with open(attachment_path, 'rb') as attachment_file:
            pdf_reader = PdfFileReader(attachment_file)
            for page_num in range(pdf_reader.numPages):
                pdf_writer.addPage(pdf_reader.getPage(page_num))

    # Save the merged PDF to a temporary file
    output_pdf_path = os.path.join(frappe.utils.get_temp_dir(), f'{docname}_combined.pdf')
    with open(output_pdf_path, 'wb') as output_pdf_file:
        pdf_writer.write(output_pdf_file)


    with open(output_pdf_path, "rb") as fileobj:
        filedata = fileobj.read()

    # Return the path to the combined PDF
    ret = frappe.get_doc({
            "doctype": "File",
            "attached_to_name": 'Download Bulk Salary Slip',
            "attached_to_doctype": 'Download Bulk Salary Slip',
            "attached_to_field": 'salary_slip',
            "file_name": 'filename',
            "is_private": 0,
            "content": filedata,
            "decode": False
        })
    ret.save(ignore_permissions=True)
    frappe.db.commit()
    attached_file = frappe.get_doc("File", ret.name)
    return attached_file

def generate_pdf_from_doctype(doctype, doc):
    # Implement PDF generation logic for your specific doctype here
    # You can use Frappe's built-in PDF generation utilities
    # For example:
    pdf_content = frappe.get_print(doctype, doc.name)
    return pdf_content
