#!/usr/bin/python3
#
#   Copyright (C) SAGEMCOM. ALL rights reserved
#
#   The information and source code contained herein is the exclusive property
#   of SAGEMCOM and may not be disclosed, examined or reproduced in whole
#   or in part without the explicit written authorization from SAGEMCOM.
#
#-----------------------------------------------------------------------
# Global declarations
#-----------------------------------------------------------------------
#
# pylint: disable=bare-except
# Accept to have except without a code value
#
# pylint: disable=too-many-instance-attributes
# Accept to have Too many instance attributes
#
# pylint: disable=superfluous-parens
# Accept to have Unnecessary parens after 'print' keyword
#
# set noet ci pi sts=0 sw=4 ts=4
"Livebox tools"
import sys
import time
import argparse
import logging

# Windows http lib name is different
import json
try:
	import httplib
	NEWHTTPLIB = False
	http = None
except ImportError:
	try:
		import http.client
		NEWHTTPLIB = True
	except ImportError:
		print('Unable to import http.client')
		sys.exit(2)

ID_VERSION = '5.0.0'

ID_SOFTWARE = 'SoftwareVersion'
ID_SERIAL = 'SerialNumber'
ID_MAC = 'BaseMAC'
ID_HWVER = 'HardwareVersion'
ID_SOFTADD = 'AdditionalSoftwareVersion'
ID_PRODUCT = 'ProductClass'
ID_STATUS = 'status'
ID_CHANNEL = 'channelid'
ID_GUI_UNKNOWN = 'Unknown'
ID_GUI_CONNECTED = 'connected'
ID_ERRORS = 'errors'
ID_STATUS_TRUE = 'True'

ID_DEBUG_LOG = '%(asctime)-15s [%(levelname)s] %(message)s'

ID_WAITINGFOR = 'Caution : Action effect will take some time'

ID_GWTIMEOUT = 'Gateway Timeout'
ID_CONFIRM_PASSWORD = 'Please confirm the password on the product screen when asked'

DEBUG_TAG_URL = '*** url'
DEBUG_TAG_HEADER = '*** Header'
DEBUG_TAG_BODY = '*** Body'
DEBUG_TAG_RECEIVED = '*** Received'
DEBUG_TAG_HTTP_RESPONSE = '*** HTTP response code'
DEBUG_TAG_REC_HEADER = '*** Received header'
DEBUG_TAG_REC_BODY = '*** Received body'

ID_DEFAULT_PASSWD = 'LiveboxV99'

ID_REGLISSE = 'Livebox 7'
ID_URL_DEFAULT = '/ws'
ID_URL_SCREEN = '/sysbus/Screen:setAnonymousDisplay'

ID_SET_COOKIE = 'Set-cookie'
ID_SESSID = '/sessid='
ID_CONTEXTID = 'contextID'
ID_DATA = 'data'

#-----------------------------------------------------------------------
# Class
#-----------------------------------------------------------------------
class CLivebox:
	"Livebox tools class"
	def __init__(self, addr, debug, passwd):
		"Init"
		# Debug mode
		self.verbose = debug
		self.host = addr
		self.passwd = passwd

		# Common header
		self.cook = None
		self.sess = None
		self.ctx = None

		# Get general info
		self.soft = ID_GUI_UNKNOWN
		self.softadd = ID_GUI_UNKNOWN
		self.serial = ID_GUI_UNKNOWN
		self.macaddr = ID_GUI_UNKNOWN
		self.product = ID_GUI_UNKNOWN
		self.get_info()

		# get gui status
		self.guistate = ID_GUI_UNKNOWN
		self.get_gui_state()

	def get_info(self):
		"read product informations"
		mess = "get_info host = " + self.host
		logging.debug(mess)

		# Build params
		header = { \
			"Content-Type" : "application/x-sah-ws-4-call+json;charset=UTF-8", \
			"Referer" : "http://"+self.host+"/ws", \
		}
		body = "{\"service\" : \"DeviceInfo\", \"method\" : \"get\", \"parameters\" : {}}"

		# HTTP session
		data = http_session(self.host, ID_URL_DEFAULT, header, body)

		# Parse received data
		if ID_STATUS in data:
			json_obj = data[ID_STATUS]
			if ID_SOFTWARE in json_obj:
				self.soft = json_obj[ID_SOFTWARE]
			if ID_SOFTADD in json_obj:
				self.softadd = json_obj[ID_SOFTADD]
			if ID_SERIAL in json_obj:
				self.serial = json_obj[ID_SERIAL]
			if ID_MAC in json_obj:
				self.macaddr = json_obj[ID_MAC]
			if ID_PRODUCT in json_obj:
				self.product = json_obj[ID_PRODUCT]
		else:
			print('Error reading informations')

	def get_gui_state(self):
		"read userinfo"
		logging.debug('get_gui_state')

		# Build params
		header = { \
			"Content-Type" : "application/x-sah-ws-4-call+json;charset=UTF-8", \
			"Referer" : "http://"+self.host+"/ws", \
		}
		body = "{\"service\":\"UserInterface\",\"method\":\"getState\", \"parameters\":{}}"

		# HTTP session
		data = http_session(self.host, ID_URL_DEFAULT, header, body)

		# Parse received data
		if ID_STATUS in data:
			self.guistate = data[ID_STATUS]
		else:
			self.guistate = ID_GUI_UNKNOWN

	def set_gui_state(self):
		"Set the GUI state"
		logging.debug("GUI unlock action")
		print('GUI Unlock action .....')

		if self.guistate == ID_GUI_CONNECTED:
			logging.debug("Livebox unlock Already done")
			print("GUI unlock result = Already done")
			return

		# Build params
		header = { \
			"Content-Type" : "application/x-sah-ws-4-call+json;charset=UTF-8", \
			"Referer" : "http://"+self.host+"/ws", \
		}
		body = "{\"service\" : \"UserInterface\", \"method\" : \"setState\", \
\"parameters\" : {\"currentState\":\"connected\"}}"

		# HTTP session
		data = http_session(self.host, ID_URL_DEFAULT, header, body)

		# Parse received data
		if ID_STATUS in data and data[ID_STATUS] is True:
			print("GUI unlock result = success")
		else:
			print("GUI unlock result = Error")

	def set_passwd(self):
		"Set the GUI password"
		logging.debug("Set the sGUI password")
		print('Set password action .....')

		# "method":"getUser"
		header = { \
			"Content-Type" : "application/x-sah-ws-4-call+json;charset=UTF-8", \
			"Referer" : "http://"+self.host+"/ws", \
		}
		body = "{\"service\" : \"UserManagement\", \"method\" : \"getUser\", \
\"parameters\" : {\"name\":\"admin\"}}"
		data = http_session(self.host, ID_URL_DEFAULT, header, body)

		# SIP-Trunk.Line.LINE1.Session.1.X_SOFTATHOME-COM_Conn", "RuleEngine"]}
		print(ID_CONFIRM_PASSWORD)
		header = { \
			"Content-Type" : "application/x-sah-event-4-call+json", \
			"Accept" : "*/*", \
			"Origin" : "http://"+self.host, \
			"Referer" : "http://"+self.host+"/", \
			"X-Sah-Request-Type": "idle", \
		}
		body = "{\"events\":[\"NMC\",\"Scheduler\",\"PnP\",\"ZWave\",\
\"Devices.Device\",\"VoiceService.VoiceApplication.VoiceProfile.\
SIP-Trunk.Line.LINE1.Session.1.X_SOFTATHOME-COM_Conn\",\"RuleEngine\"]}"
		data = http_session(self.host, ID_URL_DEFAULT, header, body)
		channel = None
		if ID_CHANNEL in data:
			channel = str(data[ID_CHANNEL])
			logging.debug(channel)
		if channel is None:
			logging.debug('Error setting passord')
			print('Error setting passord')
			return
		# "method":"start","parameters":{}}
		header = { \
			"Content-Type" : "application/x-sah-ws-4-call+json;charset=UTF-8", \
			"Referer" : "http://"+self.host+"/ws", \
		}
		body = "{\"service\" : \"PasswordRecovery\", \"method\" : \"start\", \
\"parameters\" : {}}"
		data = http_session(self.host, ID_URL_DEFAULT, header, body)

		# SIP-Trunk.Line.LINE1.Session.1.X_SOFTATHOME-COM_Conn","RuleEngine"],"channelid":3}
		header = { \
			"Content-Type" : "application/x-sah-event-4-call+json", \
			"Accept" : "*/*", \
			"Origin" : "http://"+self.host, \
			"Referer" : "http://"+self.host+"/", \
			"X-Sah-Request-Type": "idle", \
		}
		body = "{\"events\" : [\"NMC\", \"Scheduler\",\"PnP\",\"ZWave\",\
\"Devices.Device\",\"VoiceService.VoiceApplication.VoiceProfile.\
SIP-Trunk.Line.LINE1.Session.1.X_SOFTATHOME-COM_Conn\",\"RuleEngine\"],\"channelid\":"+channel+"}"
		data = http_session(self.host, ID_URL_DEFAULT, header, body)

		# "method":"getState","parameters":{}}
		header = { \
			"Content-Type" : "application/x-sah-ws-4-call+json;charset=UTF-8", \
			"Referer" : "http://"+self.host+"/ws", \
		}
		body = "{\"service\":\"UserInterface\",\"method\":\"getState\",\"parameters\":{}}"
		data = http_session(self.host, ID_URL_DEFAULT, header, body)

		# "method":"getUser","parameters":{"name":"admin"}}
		header = { \
			"Content-Type" : "application/x-sah-ws-4-call+json;charset=UTF-8", \
			"Referer" : "http://"+self.host+"/ws", \
		}
		body = "{\"service\" : \"UserManagement\", \"method\" : \"getUser\", \
\"parameters\" : {\"name\":\"admin\"}}"
		data = http_session(self.host, ID_URL_DEFAULT, header, body)

		# "method":"setPassword","parameters":{"password":"PASSWD"}}
		header = { \
			"Content-Type" : "application/x-sah-ws-4-call+json;charset=UTF-8", \
			"Referer" : "http://"+self.host+"/ws", \
		}
		body = "{\"service\" : \"PasswordRecovery\", \"method\" : \"setPassword\", \
\"parameters\" : {\"password\":\""+self.passwd+"\"}}"
		data = http_session(self.host, ID_URL_DEFAULT, header, body)

		if ID_STATUS in data:
			if data[ID_STATUS] is True:
				print('Set password success')
				print('Password is : '+self.passwd)
				logging.debug('Set password success')
			else:
				print('Set password error')
				print(data[ID_STATUS])
				logging.debug(data[ID_STATUS])
		else:
			print('Set password error')
			logging.debug('Set password error')

		# "method":"stop","parameters":{}}
#		header = { \
#			"Content-Type" : "application/x-sah-ws-4-call+json;charset=UTF-8", \
#			"Referer" : "http://"+self.host+"/ws", \
#		}
#		body = "{\"service\" : \"PasswordRecovery\", \"method\" : \"stop\", \
#\"parameters\" : \"password\":{}}"
#		data = http_session(self.host, ID_URL_DEFAULT, header, body)

	def set_screen_state(self):
		"Set the screen state"
		logging.debug("Set the screen state")
		print('Clear screen action .....')

		# API spec : Screen.setAnonymousDisplay("ecranUsine")
		header = { \
			"Content-Type" : "application/x-sah-ws-4-call+json;charset=UTF-8", \
			"Referer" : "http://"+self.host+"/ws", \
		}
		body = "{\"parameters\":{\"name\":\"ecranUsine\"}}"

		# Open HTTP session
		data = http_session(self.host, ID_URL_SCREEN, header, body)

		# Display result
		if ID_ERRORS in data:
			# if "errors" in data
			logging.debug("Livebox answer is error")
			print("Clear screen result = error")
		else:
			logging.debug("Livebox answer is success")
			print("Clear screen result = success")
			print(ID_WAITINGFOR)

	def reboot(self):
		"Send reboot command"
		logging.debug("Call of reboot")
		print('Reboot action .....')
		if self.passwd is None:
			print('Password is mandatory to call Reboot .....')
			return

		# Get ctx ID
		self.ctx, self.sess, self.cook = http_session_with_password(self.host, self.passwd)

		# Build header using context, session and cookie
		header = { \
			"Content-Type" : "application/x-sah-ws-4-call+json;charset=UTF-8", \
			"Authorization" : "X-Sah "+self.ctx, \
			"Referer" : "http://"+self.host+"/ws", \
			"Cookie" : self.cook+"/sessid="+self.sess+"; "+self.cook+ \
			"/context="+self.ctx+"; "+self.cook+"/login=admin" \
		}
		body = "{\"service\" : \"NMC\", \"method\" : \"reboot\", \"parameters\":{}}"
		data = http_session(self.host, ID_URL_DEFAULT, header, body)

		if ID_STATUS in data and data[ID_STATUS] is True:
			print("Reboot result = success")
			print(ID_WAITINGFOR)
		else:
			print("Reboot result = Error")

	def reset(self):
		"Send reset command"
		logging.debug("Call factory reset")
		print('Reboot action .....')
		if self.passwd is None:
			print('Password is mandatory to call Reset .....')
			return

		# Get ctx ID
		self.ctx, self.sess, self.cook = http_session_with_password(self.host, self.passwd)

		# Build header using context, session and cookie
		header = { \
			"Content-Type" : "application/x-sah-ws-4-call+json;charset=UTF-8", \
			"Authorization" : "X-Sah "+self.ctx, \
			"Referer" : "http://"+self.host+"/ws", \
			"Cookie" : self.cook+"/sessid="+self.sess+"; "+self.cook+ \
			"/context="+self.ctx+"; "+self.cook+"/login=admin" \
		}
		body = "{\"service\" : \"NMC\", \"method\" : \"reset\", \"parameters\":{}}"
		data = http_session(self.host, ID_URL_DEFAULT, header, body)

		if ID_STATUS in data and data[ID_STATUS] is True:
			print("Reset result = success")
			print(ID_WAITINGFOR)
		else:
			print("Reset result = Error")

	def set_wifi6_on(self):
		"Set the WIFI6 on"
		logging.debug("Set the WIFI6 on")
		print('Set Wifi6 on action .....')
		if ID_REGLISSE in self.product:
			logging.debug('Product is REGLISSE')
			print('Product is REGLISSE')
			wifiid = 'vap6g0priv0'
		else:
			logging.debug('Product is SAFRAN')
			print('Product is SAFRAN')
			wifiid = 'vap6g0priv'

		if self.passwd is None:
			print('Password is mandatory to call wifi6 on.....')
			return

		# Get ctx ID
		self.ctx, self.sess, self.cook = http_session_with_password(self.host, self.passwd)

		# Build header using context, session and cookie
		header = { \
			"Content-Type" : "application/x-sah-ws-4-call+json;charset=UTF-8", \
			"Authorization" : "X-Sah "+self.ctx, \
			"Referer" : "http://"+self.host+"/ws", \
			"Cookie" : self.cook+"/sessid="+self.sess+"; "+self.cook+ \
			"/context="+self.ctx+"; "+self.cook+"/login=admin" \
		}
		body = "{\"service\":\"NeMo.Intf.lan\",\"method\":\"setWLANConfig\", \
\"parameters\":{\"mibs\":{\"penable\":{\"rad6g0\": {\"Enable\": \"true\"}}}}}"
		data = http_session(self.host, ID_URL_DEFAULT, header, body)

		body = "{\"service\":\"NeMo.Intf.lan\",\"method\":\"setWLANConfig\", \
\"parameters\":{\"mibs\":{\"penable\":{\""+wifiid+"\": {\"Enable\": \"true\"}}}}}"
		data = http_session(self.host, ID_URL_DEFAULT, header, body)

		if ID_ERRORS in data:
			print("wifi6 result = error")
		else:
			print("wifi6 on result = success")
			print(ID_WAITINGFOR)
			return

#--------------------------------------------------------------------
# Functions
#--------------------------------------------------------------------
def http_session(host, url, header, body):
	'Http session follow up'

	# Debug infos
	http_session_cnx_debug(url, header, body)

	#  HTTP session depending from http library
	if NEWHTTPLIB is False:
		conn = httplib.HTTPConnection(host)
	else:
		conn = http.client.HTTPConnection(host)

	try:
		conn.request("POST", url, body, header)
	except IOError:
		logging.debug('IOError : request 1')
	except:
		print("Livebox not ready")
		sys.exit(1)

	try:
		resp = conn.getresponse()
	except IOError:
		logging.debug('IOError : get response')
		sys.exit(1)
	except:
		logging.debug("Livebox is not responding")
		print("Livebox is not responding")
		sys.exit(1)

	data = resp.read()
	conn.close()

	logging.debug(DEBUG_TAG_HTTP_RESPONSE)
	logging.debug(resp.status)
	logging.debug(resp.reason)

	strdata = {ID_STATUS, False}
	if resp.reason != "OK":
		return strdata

	strdata = json.loads(data)
	if strdata is None:
		strdata = {ID_STATUS, False}
	logging.debug(DEBUG_TAG_RECEIVED)
	logging.debug(strdata)

	return strdata

def http_session_with_password(host, password):
	'extract ID info from http answer'
	logging.debug('http_session_with_password')

	# Build header using context, session and cookie
	header = { \
		"Content-Type" : "application/x-sah-ws-4-call+json;charset=UTF-8", \
		"Authorization" : "X-Sah-Login", \
	}
	body = "{\"service\" : \"sah.Device.Information\", \"method\" : \"createContext\", \
\"parameters\" : {\"applicationName\":\"webui\",\"username\":\"admin\",\"password\": \
\""+password+"\"}}"

	# Debug infos
	http_session_cnx_debug(ID_URL_DEFAULT, header, body)

	# First HTTP session
	if NEWHTTPLIB is False:
		connection = httplib.HTTPConnection(host)
	else:
		connection = http.client.HTTPConnection(host)

	try:
		connection.request("POST", ID_URL_DEFAULT, body, header)
	except:
		print("Livebox not ready")
		sys.exit(1)

	try:
		resp = connection.getresponse()
	except:
		logging.debug("Livebox is not responding")
		print("Livebox is not responding")
		sys.exit(1)

	data = resp.read()
	connection.close()

	logging.debug(DEBUG_TAG_HTTP_RESPONSE)
	logging.debug(resp.status)
	logging.debug(resp.reason)

	cookie = ""
	session = ""
	context = ""
	if resp.reason != "OK":
		return context, session, cookie

	# Get cookie and session in header
	logging.debug(DEBUG_TAG_REC_HEADER)
	value = resp.getheader(ID_SET_COOKIE)
	logging.debug(value)
	lst = value.split(";")
	result = lst[0].split(ID_SESSID)
	cookie = result[0]
	session = result[1]
	logging.debug(cookie)
	logging.debug(session)

	# Get context ID in body
	json_obj = json.loads(data)
	if ID_DATA in json_obj:
		value = json_obj[ID_DATA]
		if ID_CONTEXTID in value:
			context = value[ID_CONTEXTID]
	logging.debug(DEBUG_TAG_REC_BODY)
	logging.debug(context)

	return context, session, cookie

def http_session_cnx_debug(url, header, body):
	'http_session_send_debug'
	logging.debug('http_session_send_debug')

	# Debug infos
	logging.debug(DEBUG_TAG_URL)
	logging.debug(url)
	logging.debug(DEBUG_TAG_HEADER)
	logging.debug(header)
	logging.debug(DEBUG_TAG_BODY)
	logging.debug(body)



#--------------------------------------------------------------------
#  main
#--------------------------------------------------------------------
if __name__ == '__main__':

	# Check options
	PARSER = argparse.ArgumentParser()
	PARSER.add_argument('-a', '--addr', help='IP address (default 192.168.1.1)', default='192.168.1.1')
	PARSER.add_argument('-b', '--reboot', action='store_true', help='Reboot the product')
	PARSER.add_argument('-s', '--clear_screen', action='store_true', help='Turn the screen off (LB6)')
	PARSER.add_argument('-l', '--logs', action='store_true', help='Write result in local log file')
	PARSER.add_argument('-f', '--file', help='Set log file name', default=None)
	PARSER.add_argument('-n', '--serial', help='Serial number to check', default='')
	PARSER.add_argument('-P', '--passwd', help='Product GUI password', default=None)
	PARSER.add_argument('-q', '--quiet', action='store_true', help='Don\'t display collected infos')
	PARSER.add_argument('-r', '--reset', action='store_true', help='Factory reset of the product')
	PARSER.add_argument('-c', '--set_passwd', action='store_true', \
		help='Set GUI password (default=LiveboxV99)')
	PARSER.add_argument('-t', '--unlock', action='store_true', help='Unlock Livebox GUI access')
	PARSER.add_argument('-v', '--debug', action='store_true', help='Debug verbose mode on')
	PARSER.add_argument('-w', '--wifi6', action='store_true', help='Turn WIFI6 on')
	ARGS = PARSER.parse_args()

	if ARGS.debug:
		logging.basicConfig(level=logging.DEBUG, format=ID_DEBUG_LOG,)
		print("System is         : " + sys.platform)
		print("Script version is : " + ID_VERSION)

	PASSWORD = ARGS.passwd
	if ARGS.set_passwd:
		if PASSWORD is None:
			PASSWORD = ID_DEFAULT_PASSWD

	# Open Livebox context and display infos
	print("Get informations using IP addr " + ARGS.addr)
	MY_LIVEBOX = CLivebox(ARGS.addr, ARGS.debug, PASSWORD)

	# Run actions if needed
	if ARGS.serial:
		print("Serial number to check is  " + ARGS.serial)
		if ARGS.serial != MY_LIVEBOX.serial:
			print("CAUTION !!!")
			print("The serial number " + MY_LIVEBOX.serial + " doesn't match")
			sys.exit(0)

	if not ARGS.quiet:
		print("Product        = " + MY_LIVEBOX.product)
		print("Serial number  = " + MY_LIVEBOX.serial)
		print("MAC address    = " + MY_LIVEBOX.macaddr)
		print("Soft version   = " + MY_LIVEBOX.soft)
		print("Soft Ver. add. = " + MY_LIVEBOX.softadd)
		print("User info      = " + MY_LIVEBOX.guistate)

	if ARGS.logs or ARGS.file:
		if ARGS.file:
			FILENAME = ARGS.file
		else:
			# Build default file name
			FILENAME = MY_LIVEBOX.serial + "_info.log"

		print("Log file name is [" + FILENAME + "]")
		with open(FILENAME, "w", encoding="utf-8") as fout:
			fout.write("Product        = " + MY_LIVEBOX.product + "\n")
			fout.write("Serial number  = " + MY_LIVEBOX.serial + "\n")
			fout.write("MAC address    = " + MY_LIVEBOX.macaddr + "\n")
			fout.write("Soft version   = " + MY_LIVEBOX.soft + "\n")
			fout.write("Soft Ver. add. = " + MY_LIVEBOX.softadd + "\n")
			fout.write("User info      = " + MY_LIVEBOX.guistate + "\n")
			fout.close()

	if ARGS.unlock:
		MY_LIVEBOX.set_gui_state()

	if ARGS.set_passwd:
		MY_LIVEBOX.set_gui_state()
		MY_LIVEBOX.set_passwd()

	if ARGS.clear_screen:
		MY_LIVEBOX.set_screen_state()

	if ARGS.reboot:
		MY_LIVEBOX.reboot()

	if ARGS.reset:
		MY_LIVEBOX.reset()

	if ARGS.wifi6:
		MY_LIVEBOX.set_wifi6_on()

	if sys.platform != "linux":
		time.sleep(10)

	sys.exit(0)
