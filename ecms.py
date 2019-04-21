
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

start_time = time.clock()
systemLocation = os.path.dirname(__file__)
initStatus = 0
secStatus = 0
dgsStatus = 0

# Set up logging module and system log

syslog = logging.getLogger("ECMS")
syslogHandler = logging.FileHandler(systemLocation + "/logs/sys.log")
syslogFormatter = logging.Formatter('[%(asctime)s %(filename)s %(lineno)d %(process)d] %(levelname)s %(message)s')
syslogHandler.setFormatter(syslogFormatter)
syslog.addHandler(syslogHandler)
syslog.setLevel(logging.DEBUG)

# Log application initialisation

currentLog = "=================== New Initialisation ==================="
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
	print(Fore.RED + Style.BRIGHT + " SYSTEM FAILED " + Style.RESET_ALL + "Check the system log for details (default directory: /logs/sys.log)")

# Get most recent log entry

def readRecentLogEvent():

	global currentLog

	log = open(systemLocation + "/logs/sys.log","r")
	data = log.readlines()
	log.close()
	currentLog = data[len(data)-1]
	currentLog = currentLog[:-1]

	currentLog = re.sub("[\(\[].*?[\)\]]", "", currentLog)
	currentLog = str(currentLog)


# Prepare to execute init module

def initApplication():

	global currentLog

	try:
		Thread(target = initPrint).start()
	except Exception as debug_error:
		syslog.debug(debug_error)
		currentLog = "Could not call initPrint() function within thread"
		syslog.warning(currentLog)

	try:
		Thread(target = initImport).start()
	except Exception as debug_error:
		syslog.debug(debug_error)
		currentLog = "Could not call initImport() function within thread"
		syslog.error(currentLog)
		time.sleep(1)
		errorResponse()
		os._exit(0)

# Import init module

def initImport():

	global initStatus, currentLog

	from scripts import init
	initStatus = init.status
	currentLog = init.currentLog

# Response function for init module

def initPrint():

	global initStatus, currentLog, init_time, sec_time, secStatus

	while (initStatus == 1):
		readRecentLogEvent()
		if(len(currentLog) > 55 ):
			currentLogBuffer = len(currentLog) - 55
			currentLog = currentLog[:-currentLogBuffer]
			currentLog = currentLog + "..."
		sys.stdout.write(Style.BRIGHT + Fore.CYAN + " [ Initialisation ]  \ " + Style.RESET_ALL + currentLog)
		sys.stdout.flush()
		time.sleep(0.1)
		restartLine()
		sys.stdout.write(" "*90)
		sys.stdout.flush()
		restartLine()
		readRecentLogEvent()
		if(len(currentLog) > 55 ):
			currentLogBuffer = len(currentLog) - 55
			currentLog = currentLog[:-currentLogBuffer]
			currentLog = currentLog + "..."
		sys.stdout.write(Style.BRIGHT + Fore.CYAN + " [ Initialisation ]  | " + Style.RESET_ALL + currentLog)
		sys.stdout.flush()
		time.sleep(0.1)
		restartLine()
		sys.stdout.write(" "*90)
		sys.stdout.flush()
		restartLine()
		readRecentLogEvent()
		if(len(currentLog) > 55 ):
			currentLogBuffer = len(currentLog) - 55
			currentLog = currentLog[:-currentLogBuffer]
			currentLog = currentLog + "..."
		sys.stdout.write(Style.BRIGHT + Fore.CYAN + " [ Initialisation ]  / " + Style.RESET_ALL + currentLog)
		sys.stdout.flush()
		time.sleep(0.1)
		restartLine()
		sys.stdout.write(" "*90)
		sys.stdout.flush()
		restartLine()
		readRecentLogEvent()
		if(len(currentLog) > 55 ):
			currentLogBuffer = len(currentLog) - 55
			currentLog = currentLog[:-currentLogBuffer]
			currentLog = currentLog + "..."
		sys.stdout.write(Style.BRIGHT + Fore.CYAN + " [ Initialisation ]  — " + Style.RESET_ALL + currentLog)
		sys.stdout.flush()
		time.sleep(0.1)
		restartLine()
		sys.stdout.write(" "*90)
		sys.stdout.flush()
		restartLine()
		readRecentLogEvent()
		if(len(currentLog) > 55 ):
			currentLogBuffer = len(currentLog) - 55
			currentLog = currentLog[:-currentLogBuffer]
			currentLog = currentLog + "..."
		sys.stdout.write(Style.BRIGHT + Fore.CYAN + " [ Initialisation ]  \ " + Style.RESET_ALL + currentLog)
		sys.stdout.flush()
		time.sleep(0.1)
		restartLine()
		sys.stdout.write(" "*90)
		sys.stdout.flush()
		restartLine()
		readRecentLogEvent()
		if(len(currentLog) > 55 ):
			currentLogBuffer = len(currentLog) - 55
			currentLog = currentLog[:-currentLogBuffer]
			currentLog = currentLog + "..."
		sys.stdout.write(Style.BRIGHT + Fore.CYAN + " [ Initialisation ]  | " + Style.RESET_ALL + currentLog)
		sys.stdout.flush()
		time.sleep(0.1)
		restartLine()
		sys.stdout.write(" "*90)
		sys.stdout.flush()
		restartLine()
		readRecentLogEvent()
		if(len(currentLog) > 55 ):
			currentLogBuffer = len(currentLog) - 55
			currentLog = currentLog[:-currentLogBuffer]
			currentLog = currentLog + "..."
		sys.stdout.write(Style.BRIGHT + Fore.CYAN + " [ Initialisation ]  / " + Style.RESET_ALL + currentLog)
		sys.stdout.flush()
		time.sleep(0.1)
		restartLine()
		sys.stdout.write(" "*90)
		sys.stdout.flush()
		restartLine()
		readRecentLogEvent()
		if(len(currentLog) > 55 ):
			currentLogBuffer = len(currentLog) - 55
			currentLog = currentLog[:-currentLogBuffer]
			currentLog = currentLog + "..."
		sys.stdout.write(Style.BRIGHT + Fore.CYAN + " [ Initialisation ]  — " + Style.RESET_ALL + currentLog)
		sys.stdout.flush()
		time.sleep(0.1)
		restartLine()
		sys.stdout.write(" "*90)
		sys.stdout.flush()
		restartLine()
		readRecentLogEvent()
		if(len(currentLog) > 55 ):
			currentLogBuffer = len(currentLog) - 55
			currentLog = currentLog[:-currentLogBuffer]
			currentLog = currentLog + "..."

	currentLog = "Initialisation completed successfully"
	init_time = time.clock()
	print(Style.BRIGHT + Fore.CYAN + " [ Initialisation ] " + Style.RESET_ALL + "Module completed in " + str(init_time) + " seconds")
	syslog.info(currentLog)
	secStatus = 1
	secApplication()

# Prepare to execute sec module

def secApplication():

	global currentLog

	try:
		Thread(target = secPrint).start()
	except Exception as debug_error:
		syslog.debug(debug_error)
		currentLog = "Could not call secPrint() function within thread"
		syslog.warning(currentLog)

	try:
		Thread(target = secImport).start()
	except Exception as debug_error:
		syslog.debug(debug_error)
		currentLog = "Could not call secImport() function within thread"
		syslog.error(currentLog)
		time.sleep(1)
		errorResponse()
		os._exit(0)

# Import sec module

def secImport():

	global secStatus, currentLog

	from scripts import sec
	secStatus = sec.status
	currentLog = sec.currentLog

# Response function for sec module

def secPrint():

	global secStatus, currentLog, init_time, sec_time, dgsStatus

	while (secStatus == 1):
		readRecentLogEvent()
		if(len(currentLog) > 55 ):
			currentLogBuffer = len(currentLog) - 55
			currentLog = currentLog[:-currentLogBuffer]
			currentLog = currentLog + "..."
		sys.stdout.write(Style.BRIGHT + Fore.CYAN + " [ System Environment Configuration ] \ " + Style.RESET_ALL + currentLog)
		sys.stdout.flush()
		time.sleep(0.1)
		restartLine()
		sys.stdout.write(" "*90)
		sys.stdout.flush()
		restartLine()
		readRecentLogEvent()
		if(len(currentLog) > 55 ):
			currentLogBuffer = len(currentLog) - 55
			currentLog = currentLog[:-currentLogBuffer]
			currentLog = currentLog + "..."
		sys.stdout.write(Style.BRIGHT + Fore.CYAN + " [ System Environment Configuration ] | " + Style.RESET_ALL + currentLog)
		sys.stdout.flush()
		time.sleep(0.1)
		restartLine()
		sys.stdout.write(" "*90)
		sys.stdout.flush()
		restartLine()
		readRecentLogEvent()
		if(len(currentLog) > 55 ):
			currentLogBuffer = len(currentLog) - 55
			currentLog = currentLog[:-currentLogBuffer]
			currentLog = currentLog + "..."
		sys.stdout.write(Style.BRIGHT + Fore.CYAN + " [ System Environment Configuration ] / " + Style.RESET_ALL + currentLog)
		sys.stdout.flush()
		time.sleep(0.1)
		restartLine()
		sys.stdout.write(" "*90)
		sys.stdout.flush()
		restartLine()
		readRecentLogEvent()
		if(len(currentLog) > 55 ):
			currentLogBuffer = len(currentLog) - 55
			currentLog = currentLog[:-currentLogBuffer]
			currentLog = currentLog + "..."
		sys.stdout.write(Style.BRIGHT + Fore.CYAN + " [ System Environment Configuration ] — " + Style.RESET_ALL + currentLog)
		sys.stdout.flush()
		time.sleep(0.1)
		restartLine()
		sys.stdout.write(" "*90)
		sys.stdout.flush()
		restartLine()
		readRecentLogEvent()
		if(len(currentLog) > 55 ):
			currentLogBuffer = len(currentLog) - 55
			currentLog = currentLog[:-currentLogBuffer]
			currentLog = currentLog + "..."
		sys.stdout.write(Style.BRIGHT + Fore.CYAN + " [ System Environment Configuration ] \ " + Style.RESET_ALL + currentLog)
		sys.stdout.flush()
		time.sleep(0.1)
		restartLine()
		sys.stdout.write(" "*90)
		sys.stdout.flush()
		restartLine()
		readRecentLogEvent()
		if(len(currentLog) > 55 ):
			currentLogBuffer = len(currentLog) - 55
			currentLog = currentLog[:-currentLogBuffer]
			currentLog = currentLog + "..."
		sys.stdout.write(Style.BRIGHT + Fore.CYAN + " [ System Environment Configuration ] | " + Style.RESET_ALL + currentLog)
		sys.stdout.flush()
		time.sleep(0.1)
		restartLine()
		sys.stdout.write(" "*90)
		sys.stdout.flush()
		restartLine()
		readRecentLogEvent()
		if(len(currentLog) > 55 ):
			currentLogBuffer = len(currentLog) - 55
			currentLog = currentLog[:-currentLogBuffer]
			currentLog = currentLog + "..."
		sys.stdout.write(Style.BRIGHT + Fore.CYAN + " [ System Environment Configuration ] / " + Style.RESET_ALL + currentLog)
		sys.stdout.flush()
		time.sleep(0.1)
		restartLine()
		sys.stdout.write(" "*90)
		sys.stdout.flush()
		restartLine()
		readRecentLogEvent()
		if(len(currentLog) > 55 ):
			currentLogBuffer = len(currentLog) - 55
			currentLog = currentLog[:-currentLogBuffer]
			currentLog = currentLog + "..."
		sys.stdout.write(Style.BRIGHT + Fore.CYAN + " [ System Environment Configuration ] — " + Style.RESET_ALL + currentLog)
		sys.stdout.flush()
		time.sleep(0.1)
		restartLine()
		sys.stdout.write(" "*90)
		sys.stdout.flush()
		restartLine()
		readRecentLogEvent()
		if(len(currentLog) > 55 ):
			currentLogBuffer = len(currentLog) - 55
			currentLog = currentLog[:-currentLogBuffer]
			currentLog = currentLog + "..."

	currentLog = "System Environment Configuration completed successfully"
	sec_time = time.clock() - init_time
	print(Style.BRIGHT + Fore.CYAN + " [ System Environment Configuration ] " + Style.RESET_ALL + "Module completed in " + str(sec_time) + " seconds")
	syslog.info(currentLog)
	time.sleep(0.5)
	print("")
	print(Style.BRIGHT + Fore.MAGENTA + " Data Generation " + Style.RESET_ALL)
	time.sleep(1.5)
	dgsApplication()

# Prepare to execute ddgs module

def dgsApplication():

	global currentLog

	try:
		Thread(target = dgsImport).start()
	except Exception as debug_error:
		syslog.debug(debug_error)
		currentLog = "Could not call secImport() function within thread"
		syslog.error(currentLog)
		time.sleep(1)
		errorResponse()
		os._exit(0)

# Import dgs module

def dgsImport():

	global dgsStatus, currentLog, accuracy_count, TempRange, ChargeAccuracy, indexRowCount

	from scripts import dgs
	dgsStatus = dgs.status
	currentLog = dgs.currentLog
	accuracy_count = dgs.accuracy_count
	TempRange = dgs.TempRange
	ChargeAccuracy = dgs.ChargeAccuracy
	indexRowCount = dgs.indexRowCount

	systemReport()

# System Report

def systemReport():

	global sec_time, init_time, accuracy_count, TempRange, ChargeAccuracy, indexRowCount

	init_m, init_s = divmod(init_time, 60)
	init_h, init_m = divmod(init_m, 60)

	sec_m, sec_s = divmod(sec_time, 60)
	sec_h, sec_m = divmod(sec_m, 60)

	dgs_time = time.clock()
	dgs_time = dgs_time - sec_time
	dgs_time = dgs_time - init_time
	dgs_m, dgs_s = divmod(dgs_time, 60)
	dgs_h, dgs_m = divmod(dgs_m, 60)

	system_time = time.clock()
	system_m, system_s = divmod(system_time, 60)
	system_h, system_m = divmod(system_m, 60)

	time.sleep(0.5)
	print("")
	print(Style.BRIGHT + Fore.MAGENTA + " System Report " + Style.RESET_ALL)
	print("")
	print(Style.BRIGHT + Fore.RED + " init module execution time		" + Style.RESET_ALL + str(int(init_h)) + ":" + str(int(init_m)) + ":" + str(int(init_s)))
	print(Style.BRIGHT + Fore.RED + " sec module execution time		" + Style.RESET_ALL + str(int(sec_h)) + ":" + str(int(sec_m)) + ":" + str(int(sec_s)))
	print(Style.BRIGHT + Fore.RED + " dgs module execution time		" + Style.RESET_ALL + str(int(dgs_h)) + ":" + str(int(dgs_m)) + ":" + str(int(dgs_s)))
	print(Style.BRIGHT + Fore.RED + " System execution time			" + Style.RESET_ALL + str(int(system_h)) + ":" + str(int(system_m)) + ":" + str(int(system_s)))
	print("")
	print(Style.BRIGHT + Fore.RED + " Flagged Configurations			" + Style.RESET_ALL + str(indexRowCount - accuracy_count))
	print(Style.BRIGHT + Fore.RED + " Temperature Range			" + Style.RESET_ALL + str(TempRange))
	print(Style.BRIGHT + Fore.RED + " Accuracy Level				" + Style.RESET_ALL + str(ChargeAccuracy))
	print("")
	currentLog = "System completed with " + str(indexRowCount - accuracy_count) + "flagged configuration(s)"
	syslog.info(currentLog)
	time.sleep(1.5)

# Establish XML connections

try:
	tree1 = ET.parse(systemLocation + "/xml/application.xml")
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
	tree2 = ET.parse(systemLocation + "/xml/epdb.xml")
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

# Get variables from application.xml

try:
	for parent1 in root1.findall("release_info"):
		DisplayNameFull = parent1.find("data[@key='DisplayNameFull']").text
		if DisplayNameFull == "None":
			DisplayNameFull = ""
except Exception as debug_error:
	syslog.debug(debug_error)
	currentLog = "Could not find a key 'DisplayNameFull' at 'release_info' in application.xml'"
	syslog.error(currentLog)
	time.sleep(1)
	errorResponse()
	os._exit(0)
try:
	for parent2 in root1.findall("release_info"):
		ReleaseVersion = parent2.find("data[@key='ReleaseVersion']").text
		if ReleaseVersion == "None":
			ReleaseVersion = ""
except Exception as debug_error:
	syslog.debug(debug_error)
	currentLog = "Could not find a key 'ReleaseVersion' at 'release_info' in application.xml"
	syslog.error(currentLog)
	time.sleep(1)
	errorResponse()
	os._exit(0)
try:
	for parent3 in root1.findall("release_info"):
		ReleaseDate = parent3.find("data[@key='ReleaseDate']").text
		if ReleaseDate == "None":
			ReleaseDate = ""
except Exception as debug_error:
	syslog.debug(debug_error)
	currentLog = "Could not find a key 'ReleaseDate' at 'release_info' in application.xml"
	syslog.error(currentLog)
	time.sleep(1)
	errorResponse()
	os._exit(0)
try:
	for parent3 in root1.findall("dev_info"):
		DeveloperName = parent3.find("data[@key='DeveloperName']").text
		if DeveloperName == "None":
			DeveloperName = ""
except Exception as debug_error:
	syslog.debug(debug_error)
	currentLog = "Could not find a key 'DeveloperName' at 'dev_info' in application.xml"
	syslog.error(currentLog)
	time.sleep(1)
	errorResponse()
	os._exit(0)

# UI Start response

print("")
print(Style.DIM + " " + DisplayNameFull)
print(" Version " + ReleaseVersion + " | Released " + ReleaseDate)
print(" Developed by " + DeveloperName + Style.RESET_ALL)
print("")
time.sleep(0.5)
print(Style.BRIGHT + Fore.MAGENTA + " Create and configure system environment " + Style.RESET_ALL)
print("")
time.sleep(1.5)

currentLog = "UI start response successful"
syslog.info(currentLog)

# Begin application initialisation

initStatus = 1
initApplication()
