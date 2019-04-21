
# ===================================================== #
#	Electrochemical Modelling System (ECMS)				#
#	Version 1.1.0 | Released 2017/12/28					#
#	Developed by Harvey Donnelly						#
#	http://www.donl.io | harvey@donl.io					#
# ===================================================== #

# Import initial modules

import MySQLdb, sys, time, os, re
import xml.etree.ElementTree as ET
import threading
from threading import Thread
import logging
from scripts import globals

# Code Management Functions

def decodeObject(hr_code):
	element_count = len(re.findall("\[(.*?)\]", hr_code))
	output = (element_count,)
	for element_id in range(element_count):
		output = output + (re.findall("\[(.*?)\]", hr_code)[element_id],)
	return output

def decodeObjectCoefficient(object):
	result = re.findall("(?<=\()\w+(?=\))|\w", object)
	return result[0]

def replaceObjectCoefficient(object, new_coefficient, old_coefficient):
	new_object = object.replace(str(old_coefficient), str(new_coefficient), 1)
	return new_object

def decodeObjectElements(object):
	result = re.findall("\{(.*?)\}", object)
	return result

def removeObjectCoefficient(object):
	end_location = object.find(")")
	result = object[end_location + 1:]
	return result

def checkObjectState(object):
	query = re.findall("\(\(\([^()]*\)\)\)", object)
	query_count = len(query)
	if query_count == 2:
		raw_result= query[1]
		result = raw_result[3:-3]
	elif query_count == 1:
		raw_result= query[0]
		if int(raw_result[3:-3]) != 0:
			result = "aq"
		else:
			result  = "s"
	elif query_count == 0:
		result = "e"
	return result

def decodeSubscript(object):

	nonsubscript_query = re.findall("\(\(\([^()]*\)\)\)", object)
	nonsubscript_query_count = len(nonsubscript_query)

	query = re.findall("\(\([^()]*\)\)", object)
	query_count = len(query)
	result = 0

	for subscript_id in range(query_count - nonsubscript_query_count):
		query_object = query[subscript_id]
		query_object = query_object[2:-2]
		if result == 0:
			result = (query_object,)
		else:
			result = result + (query_object,)

	return result
