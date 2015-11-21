#!/usr/bin/env python

import socket, sys, json, random, math
from threading import *
from Queue import *
from time import *

__author__ = "Samuele De Giuseppe"
__license__ = "GPL"
__version__ = "1.0"
__email__ = "samuele.degiuseppe@gmail.com"

class udp_thread (Thread):
	def __init__(self, q):
		super(udp_thread,self).__init__()
		self.q = q

		#create receiving socket
		IP = '127.0.0.1'
		PORT = 13854
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.connect((IP, PORT))

		#autentication
		formatting = "{\"enableRawOutput\":true,\"format\":\"Json\"}"
		self.s.send(formatting)
		authorize = "{\"appName\":\"BrainwaveShooters\",\"appKey\":\"9f54141b4b4c567c558d3a76cb8d715cbde03096\"}"
		self.s.send(authorize)

	def run(self):
		BUFFER = 2048
		#keep on receiving data and put it into the queue
		while 1: 

			data = self.s.recv(BUFFER).split('\r')[:-1]
			self.q.put(data)

			for d in data:
				try: 
					json_data = json.loads(d)
				except: 
					#print 'data was incomplete'
					return


def parse(queue, s_mx):

	#this function send the eSense dict data to desired socket UDP
	#you can retrieve the data as a normal dict with its keys
	if queue.empty(): 
		#print "Queue is empty"
		return

	data = queue.get_nowait()
	for d in data:
		try: 
			json_data = json.loads(d)
		except: 
			#print 'data was incomplete'
			return
	
		if 'poorSignalLevel' in json_data:
			if  json_data['poorSignalLevel'] == 200:
				continue
		
		elif 'eSense' in json_data:
			s_mx.sendto(str(json_data['eSense']),SOCKET_UDP)

	return



if __name__=="__main__":

	print "\nTHE DATA WILL BE SENDED AS DICT WHERE THE MAIN KEY FOR THE RELEVANT DATA IS eSense.",
	print "CHECK FOR THIS KEY AND THEN PARSE ALL THE ELEMENTS, ALL THE OTHER INFORMATIONS ARE RAW DATA\n"

	SEND_IP = '127.0.0.1'
	SEND_PORT = 65000

	if len(sys.argv) > 1:
		if '-h' in sys.argv:
			print "\n\t### USAGE ###"
			print "\tpython Daemind.py -p [port] -a [address]"
			print "\tport default value :- 65000"
			print "\taddress default value :- 127.0.0.1\n"

			sys.exit()

		else:
			if '-p' in sys.argv:
				i = sys.argv.index('-p')
				SEND_PORT = int(sys.argv[i+1])
			if '-a' in sys.argv:
				i = sys.argv.index('-a')
				SEND_IP = str(sys.argv[i+1])

	SOCKET_UDP = (SEND_IP,SEND_PORT)

	print "\n\tCONNECTING\n\tport: ",SEND_PORT,"\n\tIP: ",SEND_IP,'\n'

	s_mx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	queue = Queue()
	t = udp_thread(queue)
	t.daemon = True
	t.start()

	print '\nRUNNING...\n'

	while 1:
		parse(queue, s_mx)








