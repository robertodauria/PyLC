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
from threading import Thread

DEBUG = 1 # Attiva/disattiva i messaggi di debug
VERSION = "0.1a" # Versione del server

class PyLCServer():
	def __init__(self, port):
		self.port = port
		self.eh_thread = EchoHandler(50000)
		self.eh_thread.setDaemon(True)
		self.eh_thread.start()
	
class EchoHandler(Thread): # Gestisce le echo request inviate dai client
	def __init__(self, port):
		Thread.__init__(self)
		self.port = port	
		
	def run(self):
		self.hsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.hsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.hsocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		self.hsocket.bind(('', self.port))
		if DEBUG:
			print "[EchoHandler] Socket inizializzato sulla porta", self.port
		while 1:
			data, source = self.hsocket.recvfrom(8192)
			
			if data == "+00": # Se e' una echo request
				if DEBUG:
					print "[EchoHandler] Ricevuta echo request da", source
					
				# Invia acknowledgement e versione server
				self.hsocket.sendto("+01 " + VERSION, source)

if __name__ == "__main__":
	server = PyLCServer(50100)
	while 1:
		pass
