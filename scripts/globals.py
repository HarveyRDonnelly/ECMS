
# ===================================================== #
#	Electrochemical Modelling System (ECMS)				#
#	Version 1.1.0 | Released 2017/12/28					#
#	Developed by Harvey Donnelly						#
#	http://www.donl.io | harvey@donl.io					#
# ===================================================== #

import time, os

def init():
	global db_name, systemLocation

	time_stamp = time.strftime("%Y%m%d%H%M%S")
	db_name = "ecms_" + time_stamp

	systemLocation = os.path.dirname(__file__)[:-7]

init()
