
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

# Get system log

syslog = logging.getLogger("ECMS")

# Log successful module start

currentLog = "Imported init module from scripts"
syslog.info(currentLog)
time.sleep(0.5)

# Functions

# Print message in case of error

def errorResponse():
	print("")
	print("")
	print(" SYSTEM FAILED | Check the system log for details (default directory: /logs/sys.log)")

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

try:
	tree3 = ET.parse(globals.systemLocation + "/xml/pte.xml")
	root3 = tree3.getroot()
except Exception as debug_error:
	syslog.debug(debug_error)
	currentLog = "Could not connect to pte.xml"
	syslog.error(currentLog)
	time.sleep(1)
	errorResponse()
	os._exit(0)

currentLog = "Connected to pte.xml"
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

# Establish MySQL Server connection and create cursor object

try:
	connection = MySQLdb.connect (host = str(ServerHostName), user = str(ServerUser), passwd = str(ServerPassword))
except Exception as debug_error:
	syslog.debug(debug_error)
	currentLog = "Failed to connect " + ServerUser + "@" + ServerHostName + " to MySQL server with password"
	syslog.error(currentLog)
	time.sleep(1)
	errorResponse()
	os._exit(0)

currentLog = "MySQL server connection created"
syslog.info(currentLog)
time.sleep(0.5)

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

# Create system DB

try:
	cursor.execute ("CREATE DATABASE `" + db_name + "` /*!40100 DEFAULT CHARACTER SET latin1 */")
except Exception as debug_error:
	syslog.debug(debug_error)
	currentLog = "Failed to create system DB"
	syslog.error(currentLog)
	time.sleep(1)
	errorResponse()
	os._exit(0)

currentLog = "Created system DB: " + db_name
syslog.info(currentLog)
time.sleep(0.5)

try:
	cursor.close()
except Exception as debug_error:
	syslog.debug(debug_error)
	currentLog = "Failed to close MySQL cursor object"
	syslog.warning(currentLog)
	time.sleep(1)
	errorResponse()
	os._exit(0)

try:
	connection.close()
except Exception as debug_error:
	syslog.debug(debug_error)
	currentLog = "Failed to close MySQL connection object"
	syslog.warning(currentLog)
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

# Create ecms_index table

try:
	cursor.execute("CREATE TABLE `ecms_index` (`id` int(255) AUTO_INCREMENT,`CATHODE` varchar(1000),`ANODE` varchar(1000),`ELYTE` varchar(1000),`MTE` int(255),`CHR` varchar(1000),`AHR` varchar(1000),`CID` int(255),`AID` int(255),`REDOX` varchar(1000),`SSVP` varchar(1000),`TCPG` varchar(1000),`TEDPG` varchar(1000),`CMW` varchar(1000),PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=latin1")
except Exception as debug_error:
	syslog.debug(debug_error)
	currentLog = "Failed to create ecms_index table in System DB"
	syslog.error(currentLog)
	time.sleep(1)
	errorResponse()
	os._exit(0)

currentLog = "Created ecm_index table in System DB"
syslog.info(currentLog)
time.sleep(0.2)

# Create ept table

try:
	cursor.execute("CREATE TABLE `ept` (`id` int(255) NOT NULL AUTO_INCREMENT,`OX` varchar(1000) NOT NULL,`RED` varchar(1000) NOT NULL,`SSVP` varchar(1000) NOT NULL,PRIMARY KEY (`id`)) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1")
except Exception as debug_error:
	syslog.debug(debug_error)
	currentLog = "Failed to create ept table in System DB"
	syslog.error(currentLog)
	time.sleep(1)
	errorResponse()
	os._exit(0)

currentLog = "Created ept table in System DB"
g = syslog.info(currentLog)
time.sleep(0.2)

# Create pte table

try:
	cursor.execute("CREATE TABLE `pte` (`id` varchar(100) NOT NULL,`MASS` varchar(500) NOT NULL,PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=latin1")
except Exception as debug_error:
	syslog.debug(debug_error)
	currentLog = "Failed to create pte table in System DB"
	syslog.error(currentLog)
	time.sleep(1)
	errorResponse()
	os._exit(0)

currentLog = "Created pte table in System DB"
g = syslog.info(currentLog)
time.sleep(0.2)

# Insert data from epdb.xml into MySQL table

try:
	for parent5 in root2.findall("row"):
		id = parent5.get("id")
		ox = parent5.find("ox").text
		red = parent5.find("red").text
		ssvp = parent5.find("ssvp").text
		cursor.execute("INSERT INTO `ept` (`id`, `OX`, `RED`, `SSVP`) VALUES ('" + id + "', '" + ox + "', '" + red + "', '" + ssvp + "');")
except Exception as debug_error:
	syslog.debug(debug_error)
	currentLog = "Failed while inserting data from epdb.xml into ept MySQL table"
	syslog.error(currentLog)
	time.sleep(1)
	errorResponse()
	os._exit(0)

currentLog = "Succesfully inserted data from epdb.xml into ept MySQL table"
syslog.info(currentLog)
time.sleep(0.2)

# Insert data from pte.xml into MySQL table

try:
	for parent6 in root3.findall("ATOM"):
		id = parent6.find("SYMBOL").text
		mass = parent6.find("ATOMIC_WEIGHT").text
		cursor.execute("INSERT INTO `pte` (`id`, `MASS`) VALUES ('" + id + "', '" + mass + "');")
except Exception as debug_error:
	syslog.debug(debug_error)
	currentLog = "Failed while inserting data from pte.xml into pte MySQL table"
	syslog.error(currentLog)
	time.sleep(1)
	errorResponse()
	os._exit(0)

currentLog = "Succesfully inserted data from pte.xml into ept MySQL table"
syslog.info(currentLog)
time.sleep(0.2)

# Prepare for module end

connection.commit()
currentLog = "init module complete"
syslog.info(currentLog)
time.sleep(0.5)
status = 0
