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

import socket
import time
import select

DEBUG = 1 # Attiva/disattiva i messaggi di debug
VERSION = "0.1a" # Versione del client

class Radar():
	
	def __init__(self):
		self.replies = []
		self.starttime = 0
		self.ready_to_read = [] 
		self.ready_to_write = [] 
		self.on_error = []
		self.timeout = 1   # Tempo di attesa per la risposta, in secondi
		
		# Inizializzazione socket UDP per il broadcast
		self.rsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.rsocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	
	def sendecho(self, port): # Invia una echo request sulla rete
		
		self.rsocket.sendto("+00", ('<broadcast>', port))
		
		self.starttime = time.time()
		while (time.time() - self.starttime) <= self.timeout:
			
			self.ready_to_read, self.ready_to_write, self.on_error = \
					select.select([self.rsocket], [], [], self.timeout)
			
			for s in self.ready_to_read:
				data, source = s.recvfrom(2048)
				
				if DEBUG:
					print "[Radar] Echo reply:", source
				
				if data == ("+01 " + VERSION):
					if DEBUG:
						print "[Radar] Trovato server valido:", source
					self.replies.append(source)
					
				else:
					if DEBUG:
						print "[Radar] Versione server non corrispondente"
		return self.replies
	
	
if __name__ == "__main__":
	radar = Radar()
	replies = radar.sendecho(50000)
	print "Server trovati:"
	for s in replies: print s
