##
# This file is part of PyLC - Python LAN Chat
#
# (c) Copyright 2010 PyLC Development Team
#
# PyLC is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published 
# by the Free Software Foundation; either version 3 of the License,
# or (at your option) any later version.
#
# PyLC is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# Please refer to the GNU Public License for more details.
#
# You should have received a copy of the GNU Public License along with
# this program; if not, write to:
# Free Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
##

import socket, sys
from threading import Thread

DEBUG = 0 # Attiva/disattiva i messaggi di debug

class Scanner():
	
	def __init__(self, port):
		self.port = port
		self.scanlist = []
		self.results = []
	
	def run(self):
		# Acquisizione IP
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		
		# hack per rilevare l'ip dell'ethernet (non il loopback)
		s.connect(('1.0.0.0', 0))
		self.localip = s.getsockname()[0]
		
		if DEBUG:
			print "IP locale:", self.localip

		# Ricerca server nella sottorete
		self.localip = self.localip.split('.')[:-1]
		
		if DEBUG:
			print "Sottorete:", ".".join(self.localip) + ".0"
		
		for IP in range(1, 255): # Avvio di un thread per ogni IP
			to_check = ".".join(self.localip) + "." + str(IP)
			scan = Scan(to_check, self.port)
			self.scanlist.append(scan)
			scan.start()
		
		for scan in self.scanlist: # Lettura risultati da ogni thread
			scan.join()
			if scan.server:
				self.results.append(scan.addr)
		
		return self.results
		

class Scan(Thread): # Thread dello scanner
	
	def __init__(self, addr, port):
		Thread.__init__(self)
		self.addr = addr
		self.port = port
	
	def run(self):
		sock = socket.socket()
		sock.settimeout(0.01)
		try:
			sock.connect((self.addr, self.port))
			if DEBUG:
				print "Server trovato:", self.addr
			self.server = True
		except socket.error, e:
			if DEBUG:
				print "Provato %s, errore: %s" %(self.addr, e)
			self.server = False

	
if __name__ == "__main__":
	myScan = Scanner(80)
	res = myScan.run()
	print "Possibili server trovati:"
	for server in res:
		print server
