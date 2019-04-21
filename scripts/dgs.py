
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
r_constant = 8.3144598
f_constant = 96485.33289
getcontext().prec = 9999
accuracy_count = 0

# Set up logging module, system log and DG log

dglog = logging.getLogger("DG")
dglogHandler = logging.FileHandler(globals.systemLocation + "/logs/dg.log")
dglogFormatter = logging.Formatter('%(message)s')
dglogHandler.setFormatter(dglogFormatter)
dglog.addHandler(dglogHandler)
dglog.setLevel(logging.DEBUG)
syslog = logging.getLogger("ECMS")

# Log successful module start

currentLog = "Imported dgs module from scripts"
syslog.info(currentLog)

# Functions

# Refresh line for <module>Print functions

def restartLine():
    sys.stdout.write('\r')
    sys.stdout.flush()

# Print message in case of error

def errorResponse():
	print("")
	print("")
	print(" SYSTEM FAILED | Check the system log for details (default directory: /logs/sys.log)")

def readRecentLogEvent():

	global dg_currentLog

	log = open(globals.systemLocation + "/logs/dg.log","r")
	data = log.readlines()
	log.close()
	dg_currentLog = data[len(data)-1]
	dg_currentLog = dg_currentLog[:-1]

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
try:
	for parent5 in root1.findall("dg_info"):
		TempRange = parent5.find("data[@key='TempRange']").text
		if TempRange == "None":
			TempRange = ""
except Exception as debug_error:
	syslog.debug(debug_error)
	currentLog = "Could not find a key 'TempRange' at 'dg_info' in application.xml'"
	syslog.error(currentLog)
	time.sleep(1)
	errorResponse()
	os._exit(0)
try:
	for parent6 in root1.findall("dg_info"):
		ChargeAccuracy = parent6.find("data[@key='ChargeAccuracy']").text
		if ChargeAccuracy == "None":
			ChargeAccuracy = ""
except Exception as debug_error:
	syslog.debug(debug_error)
	currentLog = "Could not find a key 'ChargeAccuracy' at 'dg_info' in application.xml'"
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
	cursor.execute("SELECT COUNT(*) FROM ecms_index;")
	indexRowCount =  cursor.fetchone()[0]
	indexRowCount = int(indexRowCount)
except Exception as debug_error:
	syslog.debug(debug_error)
	currentLog = "Failed to count rows of ecms_index table"
	syslog.error(currentLog)
	time.sleep(1)
	errorResponse()
	os._exit(0)

connection.commit()
connection.close()

time.sleep(0.2)

currentLog = "Data generation has been initialised"
syslog.info(currentLog)

time.sleep(1)

print("")
print(Fore.CYAN + Style.BRIGHT + " [ " + db_name + " ] " + Style.RESET_ALL + " TempRange: " + str(TempRange) + " Accuracy: " + str(ChargeAccuracy))
config_start_time = time.clock()

try:

	for primary_config_id in range(indexRowCount):

		# Define initial loop variables

		accuracy = 0

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

		try:
			cursor = connection.cursor ()
		except Exception as debug_error:
			syslog.debug(debug_error)
			currentLog = "Failed to create MySQL cursor object"
			syslog.error(currentLog)
			time.sleep(1)
			errorResponse()
			os._exit(0)

		# Retrieve AID and CID of current configuration

		cursor.execute("SELECT CID FROM `ecms_index` WHERE id=" + str(primary_config_id + 1)+ ";")
		cid = cursor.fetchone()[0]
		cursor.execute("SELECT AID FROM `ecms_index` WHERE id=" + str(primary_config_id + 1)+ ";")
		aid = cursor.fetchone()[0]

		# Retrieve electrodes

		cursor.execute("SELECT CATHODE FROM `ecms_index` WHERE id=" + str(primary_config_id + 1)+ ";")
		cathode = cursor.fetchone()[0]
		cursor.execute("SELECT ANODE FROM `ecms_index` WHERE id=" + str(primary_config_id + 1)+ ";")
		anode = cursor.fetchone()[0]

		# Calculate SSVP

		cursor.execute("SELECT SSVP FROM `ept` WHERE id=" + str(cid)+ ";")
		c_ssvp = cursor.fetchone()[0]
		cursor.execute("SELECT SSVP FROM `ept` WHERE id=" + str(aid)+ ";")
		a_ssvp = -1 * float(cursor.fetchone()[0])
		ssvp = float(c_ssvp) + float(a_ssvp)

		# Retrieve MTE and Redox Code

		cursor.execute("SELECT MTE FROM `ecms_index` WHERE id=" + str(primary_config_id + 1)+ ";")
		mte = cursor.fetchone()[0]
		cursor.execute("SELECT REDOX FROM `ecms_index` WHERE id=" + str(primary_config_id + 1)+ ";")
		redox = cursor.fetchone()[0]

		# Calculate the Quotient

		for temperature in range(int(TempRange)):

			vp = 0

			for charge_id in range(int(ChargeAccuracy)):

				reactant_code = redox.split("=")[0]
				product_code = redox.split("=")[1]
				charge_change = ((int(ChargeAccuracy) - 1) - charge_id) / int(ChargeAccuracy)

				# Handle Reactants

				reactant_data = ecms_decoder.decodeObject(reactant_code)
				reactant_count = reactant_data[0]
				reactants = 0

				for reactant_id in range(reactant_count):
					if reactants == 0:
						reactants = (reactant_data[reactant_id + 1],)
					else:
						reactants = reactants + (reactant_data[reactant_id + 1],)

				q_reactants = 1

				for reactant_object_id in range(reactant_count):
					reactant_subscript_sum = 0
					reactant_state = ecms_decoder.checkObjectState(reactants[reactant_object_id])
					if reactant_state == "aq" or reactant_state == "g":
						reactant_subscript = ecms_decoder.decodeSubscript(reactants[reactant_object_id])
						reactant_object_coefficient = ecms_decoder.decodeObjectCoefficient(reactants[reactant_object_id])
						for reactant_subscript_id in range(len(reactant_subscript)):
							reactant_subscript_sum = Decimal(reactant_subscript_sum) + Decimal(reactant_subscript[reactant_subscript_id])
						q_reactants = Decimal(q_reactants) * ((Decimal(reactant_subscript_sum) * Decimal(1 - Decimal(charge_change))) ** Decimal(reactant_object_coefficient))

				# Handle Products

				product_data = ecms_decoder.decodeObject(product_code)
				product_count = product_data[0]
				products = 0

				for product_id in range(product_count):
					if products == 0:
						products = (product_data[product_id + 1],)
					else:
						products = products + (product_data[product_id + 1],)

				q_products = 1


				for product_object_id in range(product_count):
					product_subscript_sum = 0
					product_state = ecms_decoder.checkObjectState(products[product_object_id])
					if product_state == "aq" or product_state == "g":
						product_subscript = ecms_decoder.decodeSubscript(products[product_object_id])
						product_object_coefficient = ecms_decoder.decodeObjectCoefficient(products[product_object_id])
						for product_subscript_id in range(len(product_subscript)):
							product_subscript_sum = Decimal(product_subscript_sum) + Decimal(product_subscript[product_subscript_id])

						q_products = Decimal(q_products) * ((Decimal(product_subscript_sum) * (Decimal(1 / Decimal(ChargeAccuracy)) + Decimal(charge_change))) ** Decimal(product_object_coefficient))

				# Calculate the Quotient and electrical potential

				quotient = Decimal(q_products) / Decimal(q_reactants)
				e = Decimal(ssvp) - (Decimal(Decimal(r_constant * (temperature + 1))/Decimal(mte * f_constant)) * Decimal(math.log(quotient)))
				e = float(str(e)[:15])

				if Decimal(e) > 0:
					if str(ssvp)[:5] == str(e)[:5]:
						if accuracy != 1:
							accuracy = 1
							accuracy_count = accuracy_count + 1
						else:
							accuracy = 1
						accuracy = 1

				if vp == 0:
					vp = (e,)
				else:
					vp = vp + (e,)

			# Update ecms_index SSVP

			cursor.execute("INSERT INTO `" + str(primary_config_id + 1) + "` (`vp`) VALUES ('" + str(vp) + "');")

		# Calculate theoretical capacity of cell

		cpg_mw = Decimal(0)

		for reactant_cpg_id in range(reactant_count):
			for element_cpg_id in range(len(ecms_decoder.decodeObjectElements(reactants[reactant_cpg_id]))):
				element_atomic_id = ecms_decoder.decodeObjectElements(reactants[reactant_cpg_id])[element_cpg_id]
				if element_atomic_id == "e":
					element_cpg_subscript = 1
				else:
					element_cpg_subscript = ecms_decoder.decodeSubscript(reactants[reactant_cpg_id])[element_cpg_id]
				cursor.execute("SELECT MASS FROM `pte` WHERE id='" + str(element_atomic_id) + "';")
				element_id_mass = cursor.fetchone()[0]
				cpg_mw = cpg_mw + Decimal(Decimal(element_cpg_subscript) * Decimal(element_id_mass))

		tcpg = ((Decimal(f_constant) * Decimal(mte)) / Decimal(cpg_mw)) * Decimal(Decimal(1000) / Decimal(3600))

		# Calculate Theoretical Energy Density

		tedpg = Decimal(tcpg) * Decimal(ssvp)

		# Update Index Table

		cursor.execute("UPDATE `ecms_index` SET `SSVP` = " + str(ssvp) + " WHERE id = " + str(primary_config_id + 1) + ";")
		cursor.execute("UPDATE `ecms_index` SET `TCPG` = " + str(tcpg)[:30] + " WHERE id = " + str(primary_config_id + 1) + ";")
		cursor.execute("UPDATE `ecms_index` SET `TEDPG` = " + str(tedpg)[:30] + " WHERE id = " + str(primary_config_id + 1) + ";")
		cursor.execute("UPDATE `ecms_index` SET `CMW` = " + str(cpg_mw)[:30] + " WHERE id = " + str(primary_config_id + 1) + ";")
		connection.commit()
		connection.close()

		config_end_time = time.clock()
		config_time = (config_end_time - config_start_time) / (primary_config_id + 1)
		config_time = str(int(((indexRowCount - (primary_config_id + 1)) * config_time) / 60))
		if int(config_time) <= 1:
			config_time_text = "< 1 minute left"
		else:
			config_time_text = config_time + " minutes left"

		if primary_config_id != 0:
			restartLine()
			sys.stdout.write(" "*90)
			sys.stdout.flush()
			restartLine()

			if accuracy == 1:
				sys.stdout.write(" " + Fore.GREEN + Style.BRIGHT + dg_currentLog_1 + Style.RESET_ALL + dg_currentLog_2)
			else:
				sys.stdout.write(" " + Fore.YELLOW + Style.BRIGHT + dg_currentLog_1 + Style.RESET_ALL + dg_currentLog_2)

		dg_currentLog_1 = "[Config " + str(primary_config_id + 1) + "]"
		dg_currentLog_2 = " CID: " + str(cid) + " AID: " + str(aid) + " SSVP: " + str(ssvp)
		dg_currentLog = dg_currentLog_1 + dg_currentLog_2
		dglog.info(dg_currentLog)
		print("")

		if accuracy == 1:
			sys.stdout.write(" " + Fore.GREEN + Style.BRIGHT + dg_currentLog_1 + Style.RESET_ALL + dg_currentLog_2 + "   " + str(int(((primary_config_id + 1) / indexRowCount) * 100)) + "% ( " + config_time_text + " )")
			sys.stdout.flush()
		else:
			sys.stdout.write(" " + Fore.YELLOW + Style.BRIGHT + dg_currentLog_1 + Style.RESET_ALL + dg_currentLog_2 + "   |   " + str(int(((primary_config_id + 1) / indexRowCount) * 100)) + "% ( " + config_time_text + ")")
			sys.stdout.flush()

except Exception as debug_error:
	syslog.debug(debug_error)
	currentLog = "Failed while calculating configuration SSVPs"
	syslog.error(currentLog)
	time.sleep(1)
	errorResponse()
	os._exit(0)

# Prepare for module end

restartLine()
sys.stdout.write(" "*90)
sys.stdout.flush()
restartLine()

if accuracy == 1:
	sys.stdout.write(" " + Fore.GREEN + Style.BRIGHT + dg_currentLog_1 + Style.RESET_ALL + dg_currentLog_2)
else:
	sys.stdout.write(" " + Fore.YELLOW + Style.BRIGHT + dg_currentLog_1 + Style.RESET_ALL + dg_currentLog_2)
print("")

currentLog = "dgs module complete"
syslog.info(currentLog)

time.sleep(1)
status = 0
