import nxppy
import time

mifare=nxppy.Mifare()

while True:
	try:
		uid=mifare.select()
		print "Read uid: ",uid
	
	except nxppy.SelectError:
		pass

	time.sleep(1)
