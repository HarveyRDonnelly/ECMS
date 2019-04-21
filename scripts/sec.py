
# ===================================================== #
#	Electrochemical Modelling System (ECMS)				#
#	Version 1.1.0 | Released 2017/12/28					#
#	Developed by Harvey Donnelly						#
#	http://www.donl.io | harvey@donl.io					#
# ===================================================== #

# Import initial modules

import MySQLdb, sys, time, os, re, math
import xml.etree.ElementTree as ET
import threading
from threading import Thread
import logging
from scripts import globals, ecms_decoder
from decimal import *
from colorama import *

# Initialise any neccessary modules

init()

# Define any initial variables

status = 1
systemLocation = os.path.dirname(__file__)
db_name = globals.db_name
config_id = 0

# Get system log

syslog = logging.getLogger("ECMS")

# Log successful module start

currentLog = "Imported sec module from scripts"
syslog.info(currentLog)

# Functions

# Print message in case of error

def errorResponse():
	print("")
	print("")
	print(" SYSTEM FAILED | Check the system log for details (default directory: /logs/sys.log)")

# Calculate LCM of two integers

def calcLCM(x, y):
	if x > y:
		greater = x
	else:
		greater = y

	while(True):
		if((greater % x == 0) and (greater % y == 0)):
			lcm = greater
			break
		greater += 1

	return lcm

# Establish XML connections

try:
	tree1 = ET.parse(globals.systemLocation + "/xml/application.xml")
	root1 = tree1.getroot()
except Exception as debug_error:
	syslog.debug(debug_error)
	currentLog = "Could not connect to application.xml"
	syslog.error(currentLog)
	time.sleep(1)
	errorResponse()
	os._exit(0)

currentLog = "Connected to application.xml"
syslog.info(currentLog)

try:
	tree2 = ET.parse(globals.systemLocation + "/xml/epdb.xml")
	root2 = tree2.getroot()
except Exception as debug_error:
	syslog.debug(debug_error)
	currentLog = "Could not connect to epdb.xml"
	syslog.error(currentLog)
	time.sleep(1)
	errorResponse()
	os._exit(0)

currentLog = "Connected to epdb.xml"
syslog.info(currentLog)

currentLog = "Established XML connections"
syslog.info(currentLog)
time.sleep(0.5)

# Get variables from application.xml

try:
	for parent1 in root1.findall("release_info"):
		DisplayNameShort = parent1.find("data[@key='DisplayNameShort']").text
		if DisplayNameShort == "None":
			DisplayNameShort = ""
except Exception as debug_error:
	syslog.debug(debug_error)
	currentLog = "Could not find DisplayNameShort at release_info in application.xml"
	syslog.error(currentLog)
	time.sleep(1)
	errorResponse()
	os._exit(0)
try:
	for parent2 in root1.findall("mysql_info"):
		ServerHostName = parent2.find("data[@key='ServerHostname']").text
		if ServerHostName == "None":
			ServerHostName = ""
except Exception as debug_error:
	syslog.debug(debug_error)
	currentLog = "Could not find ServerHostName at mysql_info in application.xml"
	syslog.error(currentLog)
	time.sleep(1)
	errorResponse()
	os._exit(0)
try:
	for parent3 in root1.findall("mysql_info"):
		ServerUser = parent3.find("data[@key='ServerUser']").text
		if ServerUser == "None":
			ServerUser = ""
except Exception as debug_error:
	syslog.debug(debug_error)
	currentLog = "Could not find ServerUser at mysql_info in application.xml"
	syslog.error(currentLog)
	time.sleep(1)
	errorResponse()
	os._exit(0)
try:
	for parent4 in root1.findall("mysql_info"):
		ServerPassword = parent4.find("data[@key='ServerPassword']").text
		if str(ServerPassword) == "None":
			ServerPassword = ""
except Exception as debug_error:
	syslog.debug(debug_error)
	currentLog = "Could not find ServerPassword at mysql_info in application.xml"
	syslog.error(currentLog)
	time.sleep(1)
	errorResponse()
	os._exit(0)

# Establish MySQL DB connection and create cursor object

try:
	connection = MySQLdb.connect (host = str(ServerHostName), user = str(ServerUser), passwd = str(ServerPassword), db = str(db_name))
except Exception as debug_error:
	syslog.debug(debug_error)
	currentLog = "Failed to connect " + ServerUser + "@" + ServerHostName + " to the System DB"
	syslog.error(currentLog)
	time.sleep(1)
	errorResponse()
	os._exit(0)

currentLog = "MySQL System DB connection created"
syslog.info(currentLog)
time.sleep(0.3)

try:
	cursor = connection.cursor ()
except Exception as debug_error:
	syslog.debug(debug_error)
	currentLog = "Failed to create MySQL cursor object"
	syslog.error(currentLog)
	time.sleep(1)
	errorResponse()
	os._exit(0)

currentLog = "Created MySQL cursor object"
syslog.info(currentLog)

# Count rows in ept table

try:
	cursor.execute("SELECT COUNT(*) FROM ept;")
	cursor.execute("SELECT COUNT(*) FROM ept;")
	eptRowCount =  cursor.fetchone()[0]
	eptRowCount = int(eptRowCount)
except Exception as debug_error:
	syslog.debug(debug_error)
	currentLog = "Failed to count rows of ept table"
	syslog.error(currentLog)
	time.sleep(1)
	errorResponse()
	os._exit(0)

# Set up environment for every configuration

try:

	# Loop for every reduction half-reaction

	for primary_config_id in range(eptRowCount):

		# Decode and store details of CHR

		cursor.execute("SELECT RED FROM `ept` WHERE id=" + str(primary_config_id + 1)+ ";")
		r_red_code = cursor.fetchone()

		r_red_data = ecms_decoder.decodeObject(r_red_code[0])
		r_red_element_count = r_red_data[0]
		r_red_elements = 0
		for r_red_element_id in range(r_red_element_count):
			if r_red_elements == 0:
				r_red_elements = (r_red_data[r_red_element_id + 1],)
			else:
				r_red_elements = r_red_elements + (r_red_data[r_red_element_id + 1],)

		cursor.execute("SELECT OX FROM `ept` WHERE id=" + str(primary_config_id + 1)+ ";")
		r_ox_code = cursor.fetchone()

		r_ox_data = ecms_decoder.decodeObject(r_ox_code[0])
		r_ox_element_count = r_ox_data[0]
		r_ox_elements = 0
		for r_ox_element_id in range(r_ox_element_count):
			if r_ox_elements == 0:
				r_ox_elements = (r_ox_data[r_ox_element_id + 1],)
			else:
				r_ox_elements = r_ox_elements + (r_ox_data[r_ox_element_id + 1],)

		# Loop for every potential oxidation half-reaction with a given reduction reaction

		for secondary_config_id in range(eptRowCount):

			cursor.execute("SELECT SSVP FROM `ept` WHERE id=" + str(primary_config_id + 1)+ ";")
			r_ssvp = Decimal(cursor.fetchone()[0])

			cursor.execute("SELECT SSVP FROM `ept` WHERE id=" + str(secondary_config_id + 1)+ ";")
			o_ssvp = Decimal(cursor.fetchone()[0])

			pc_1 = r_ssvp + (o_ssvp * -1)
			pc_2 = o_ssvp + (r_ssvp * -1)

			if pc_1 > pc_2:

				if secondary_config_id != primary_config_id:

					# Decode and store details of AHR

					cursor.execute("SELECT RED FROM `ept` WHERE id=" + str(secondary_config_id + 1)+ ";")
					o_red_code = cursor.fetchone()

					o_red_data = ecms_decoder.decodeObject(o_red_code[0])
					o_red_element_count = o_red_data[0]
					o_red_elements = 0
					for o_red_element_id in range(o_red_element_count):
						if o_red_elements == 0:
							o_red_elements = (o_red_data[o_red_element_id + 1],)
						else:
							o_red_elements = o_red_elements + (o_red_data[o_red_element_id + 1],)


					cursor.execute("SELECT OX FROM `ept` WHERE id=" + str(secondary_config_id + 1)+ ";")
					o_ox_code = cursor.fetchone()

					o_ox_data = ecms_decoder.decodeObject(o_ox_code[0])
					o_ox_element_count = o_ox_data[0]
					o_ox_elements = 0
					for o_ox_element_id in range(o_ox_element_count):
						if o_ox_elements == 0:
							o_ox_elements = (o_ox_data[o_ox_element_id + 1],)
						else:
							o_ox_elements = o_ox_elements + (o_ox_data[o_ox_element_id + 1],)

					# Find MTE for each HR

					r_mte = re.findall("\((.*?)\)", r_red_elements[r_red_element_count - 1])[0]
					o_mte = re.findall("\((.*?)\)", o_red_elements[o_red_element_count - 1])[0]

					# Balance CHR and AHR if neccessary

					if r_mte != o_mte:

						# Calculate Balance Multipliers

						mte = calcLCM(int(r_mte), int(o_mte))
						r_multiplier = int(mte) / int(r_mte)
						o_multiplier = int(mte) / int(o_mte)

						# Balance CHR Reactants

						for r_red_unbalanced_element_id in range(r_red_element_count):
							if r_red_unbalanced_element_id == 0:
								unbalanced_coefficient = ecms_decoder.decodeObjectCoefficient(r_red_elements[r_red_unbalanced_element_id])
								balanced_coefficient = int(unbalanced_coefficient) * int(r_multiplier)
								r_red_balanced_elements = (ecms_decoder.replaceObjectCoefficient(r_red_elements[r_red_unbalanced_element_id], balanced_coefficient, unbalanced_coefficient),)
							else:
								unbalanced_coefficient = ecms_decoder.decodeObjectCoefficient(r_red_elements[r_red_unbalanced_element_id])
								balanced_coefficient = int(unbalanced_coefficient) * int(r_multiplier)
								r_red_balanced_elements = r_red_balanced_elements + (ecms_decoder.replaceObjectCoefficient(r_red_elements[r_red_unbalanced_element_id], balanced_coefficient, unbalanced_coefficient),)

						# Balance CHR Products

						for r_ox_unbalanced_element_id in range(r_ox_element_count):
							if r_ox_unbalanced_element_id == 0:
								unbalanced_coefficient = ecms_decoder.decodeObjectCoefficient(r_ox_elements[r_ox_unbalanced_element_id])
								balanced_coefficient = int(unbalanced_coefficient) * int(r_multiplier)
								r_ox_balanced_elements = (ecms_decoder.replaceObjectCoefficient(r_ox_elements[r_ox_unbalanced_element_id], balanced_coefficient, unbalanced_coefficient),)
							else:
								unbalanced_coefficient = ecms_decoder.decodeObjectCoefficient(r_ox_elements[r_ox_unbalanced_element_id])
								balanced_coefficient = int(unbalanced_coefficient) * int(r_multiplier)
								r_ox_balanced_elements = r_ox_balanced_elements + (ecms_decoder.replaceObjectCoefficient(r_ox_elements[r_ox_unbalanced_element_id], balanced_coefficient, unbalanced_coefficient),)

						# Balance AHR Reactants

						for o_ox_unbalanced_element_id in range(o_ox_element_count):
							if o_ox_unbalanced_element_id == 0:
								unbalanced_coefficient = ecms_decoder.decodeObjectCoefficient(o_ox_elements[o_ox_unbalanced_element_id])
								balanced_coefficient = int(unbalanced_coefficient) * int(o_multiplier)
								o_ox_balanced_elements = (ecms_decoder.replaceObjectCoefficient(o_ox_elements[o_ox_unbalanced_element_id], balanced_coefficient, unbalanced_coefficient),)
							else:
								unbalanced_coefficient = ecms_decoder.decodeObjectCoefficient(o_ox_elements[o_ox_unbalanced_element_id])
								balanced_coefficient = int(unbalanced_coefficient) * int(o_multiplier)
								o_ox_balanced_elements = o_ox_balanced_elements + (ecms_decoder.replaceObjectCoefficient(o_ox_elements[o_ox_unbalanced_element_id], balanced_coefficient, unbalanced_coefficient),)

						# Balance AHR Products

						for o_red_unbalanced_element_id in range(o_red_element_count):
							if o_red_unbalanced_element_id == 0:
								unbalanced_coefficient = ecms_decoder.decodeObjectCoefficient(o_red_elements[o_red_unbalanced_element_id])
								balanced_coefficient = int(unbalanced_coefficient) * int(o_multiplier)
								o_red_balanced_elements = (ecms_decoder.replaceObjectCoefficient(o_red_elements[o_red_unbalanced_element_id], balanced_coefficient, unbalanced_coefficient),)
							else:
								unbalanced_coefficient = ecms_decoder.decodeObjectCoefficient(o_red_elements[o_red_unbalanced_element_id])
								balanced_coefficient = int(unbalanced_coefficient) * int(o_multiplier)
								o_red_balanced_elements = o_red_balanced_elements + (ecms_decoder.replaceObjectCoefficient(o_red_elements[o_red_unbalanced_element_id], balanced_coefficient, unbalanced_coefficient),)

					else:
						mte = r_mte
						r_red_balanced_elements = r_red_elements
						r_ox_balanced_elements = r_ox_elements
						o_ox_balanced_elements = o_ox_elements
						o_red_balanced_elements = o_red_elements

					chr = ""
					ahr = ""

					# Encode CHR as a string

					for r_red_element_count_id in range(r_red_element_count):
						chr = chr + "[" + r_red_balanced_elements[r_red_element_count_id] + "]"

					chr = chr + "="

					for r_ox_element_count_id in range(r_ox_element_count):
						chr = chr + "[" + r_ox_balanced_elements[r_ox_element_count_id] + "]"

					# Encode AHR as a string

					for o_ox_element_count_id in range(o_ox_element_count):
						ahr = ahr + "[" + o_ox_balanced_elements[o_ox_element_count_id] + "]"

					ahr = ahr + "="

					for o_red_element_count_id in range(o_red_element_count):
						ahr = ahr + "[" + o_red_balanced_elements[o_red_element_count_id] + "]"

					# Encode HRs as full Redox code

					chr_reactants = chr.split("=")[0]
					chr_products = chr.split("=")[1]

					ahr_reactants = ahr.split("=")[0]
					ahr_products = ahr.split("=")[1]

					redox = str(chr_reactants) + str(ahr_reactants) + "=" + str(chr_products) + str(ahr_products)

					# Retrieve the Cathode Notation

					cathode = ecms_decoder.removeObjectCoefficient(r_red_elements[0])
					anode = ecms_decoder.removeObjectCoefficient(o_ox_elements[0])

					# Increment Configuration ID

					config_id = config_id + 1

					# Execute MySQL Scripts

					cursor.execute("INSERT INTO `ecms_index` (`ANODE`, `CATHODE`, `MTE`, `CHR`, `AHR`, `REDOX`) VALUES ('" + str(anode) + "', '" + str(cathode) + "', '" + str(mte) + "', '" + str(chr) + "', '" + str(ahr) + "', '" + str(redox) + "');")

					cursor.execute("UPDATE `ecms_index` SET `CID` = " + str(primary_config_id + 1) +", `AID` = " + str(secondary_config_id + 1) + " WHERE id = " + str(config_id) + ";")

					cursor.execute("CREATE TABLE `" + str(config_id) + "` (`id` int(255) AUTO_INCREMENT,`vp` TEXT(1000000),PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=latin1;")

except Exception as debug_error:
	syslog.debug(debug_error)
	currentLog = "Failed while creating config tables"
	syslog.error(currentLog)
	time.sleep(1)
	errorResponse()
	os._exit(0)

currentLog = "Created and indexed all configuration tables"
syslog.info(currentLog)

# Prepare for module end

connection.commit()
time.sleep(1)
status = 0
