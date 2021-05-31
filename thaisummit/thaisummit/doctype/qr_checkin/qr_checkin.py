# -*- coding: utf-8 -*-
# Copyright (c) 2021, TEAMPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import numpy as np
import cv2
import pyzbar.pyzbar as pyzbar

class QRCheckin(Document):
	def scan_qr(self):
		frappe.errprint("hi")
		# cap = cv2.VideoCapture(-1)

		# while True:
		# 	_, frame = cap.read()
		# 	cv2.imshow("Frame",frame)

		# 	key = cv2.waitkey(1)
		# 	if key == 27:
		# 		break


		# cap = cv2.VideoCapture(0)
		# font = cv2.FONT_HERSHEY_PLAIN
		# while True:
		# 	_, frame = cap.read()
		# 	frappe.errprint(frame)
			# decodedObjects = pyzbar.decode(frame)
			# frappe.errprint(decodedObjects)
			# for obj in decodedObjects:
			# 	# frappe.errprint("Data", obj.data)
			# 	cv2.putText(frame, str(obj.data), (50, 50), font, 2,
			# 				(255, 0, 0), 3)