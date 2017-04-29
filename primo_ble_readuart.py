#!/usr/bin/env python

import datetime
import time
import os
import sys
import subprocess
import pexpect
#import signal

#DEBUG SWITCH
DEBUG=0

def debugPrint(msg):
	global DEBUG
	if DEBUG:
		print "[DEBUG]"+msg

#start Demon and device
def envInit():
	debugPrint("Initial the environment...")
	os.system("/etc/init.d/bluetoothd restart")
	os.system("hciconfig hci0 reset")

#Scan the BLE device
def scanBLEDevice():
	debugPrint("Scan the BLE device ...")
	subprocess.Popen("hcitool lescan > blescan.txt & && sleep 3",shell=True).kill()

#Get the BLE address of the test board
def getBLEAddress():
	STATUS=True
	BLEAddress = None
	debugPrint("Get the BLE Address...")
	f1 = open("blescan.txt","r")
	while STATUS:
		line = f1.readline()
		if len(line) < 2:
			STATUS = False
		else:
			if (line.split(' ')[1] == "BLE") and (line.split(' ')[2] == "NFC"):
				BLEAddress = line.split(" ")[0]
				STATUS = False
		pass
	f1.close()
	return BLEAddress


def enableUARTRead(bleAddress):
	global DEBUG
	debugPrint("Read UART values...")
	try:
		child = pexpect.spawn("gatttool -b %s -t random -I" % (bleAddress))
		#log = file('pexpect.log', 'w')
		#child.logfile = log
		if DEBUG:
			child.logfile = sys.stdout
		child.expect(">")

		child.sendline("connect")
		child.expect("successful")
		child.expect(">")

		#Enable notifications
		child.sendline("char-write-req 0x0012 01")
		#Disable notifications
		#child.sendline("char-write-req 0x0012 00")
		child.expect("successfully")
		child.expect(">")

		readValue(child)

		child.sendline("disconnect")
		child.expect(">")

		child.sendline("exit")
		child.close(force=True)
	except pexpect.TIMEOUT:
		return False
	
	#child.sendcontrol('c')  CTRL+C
	return True

#Read and decode the value read from the notification
def readValue(child):
	while True:
	    if not child.isalive():
		print "connection not alive"
		return None

	    try:
		index = child.expect('Notification handle = .*? \r\n', timeout=30)

	    except pexpect.TIMEOUT:
		#
		# The gatttool does not report link-lost directly.
		# The only way found to detect it is monitoring the prompt '[CON]'
		# and if it goes to '[   ]' this indicates the connection has
		# been broken.
		# In order to get a updated prompt string, issue an empty
		# sendline('').  If it contains the '[   ]' string, then
		# raise an exception. Otherwise, if not a link-lost condition,
		# continue to wait.
		#
		child.sendline('')
		string = child.before
		if '[   ]' in string:
		    print 'Connection lost! '
		    raise Exception('Connection Lost')
		return None
	    
	    if index == 0:
		after = child.after
		debugPrint("After:" + str(after))
		hxstr = after.split()[3:]
		handle = long(float.fromhex(hxstr[0]))
		debugPrint("Handle:" + str(handle))
		debugPrint(str(hxstr[2:]))
		L=hxstr[2:]
		string=""
		for i in L: string+=i
		ret=string.decode("hex").rstrip()
		if ret!="": print "Ret:" + ret

	    else:
		print "unexpeced index: {0}".format(index)
		return None

#main
def main():
	#envInit()
	#scanBLEDevice()
	#address = getBLEAddress()
	#address= "E8:EC:B8:30:AB:B4"
	if len(sys.argv[1:])==0:
		print "Missing BLE address. You need the pass the BLE address as argument."	
		return

	address=sys.argv[1:][0]
	if address is None:
		print ("Failed to find the BLE device " + address)
		return False
	else:
		ret = enableUARTRead(address)
		if ret is False:
			return False
		ret = checkNFCResult()
		return ret	

if __name__ == '__main__':
	main()
