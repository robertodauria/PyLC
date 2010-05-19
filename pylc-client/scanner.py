import socket, sys
from threading import Thread

DEBUG = 1 # Attiva/disattiva i messaggi di debug

class Scanner():
	def __init__(self, port):
		self.port = port
		self.scanlist = []
		self.results = []
		
		# Acquisizione IP
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		# hack per rilevare l'ip dell'ethernet (non il loopback)
		s.connect(('1.0.0.0', 0))
		self.localip = s.getsockname()[0]
		if DEBUG:
			print "IP rilevato:", self.localip
		
		# Ricerca server nella sottorete di classe C
		self.localip = self.localip.split('.')[:-1]
		
		for IP in range(1, 255):
			to_check = ".".join(self.localip) + "." + str(IP)
			scan = Scan(to_check, port)
			self.scanlist.append(scan)
			scan.start()
		
		for scan in self.scanlist:
			scan.join()
			if scan.server:
				self.results.append(scan.addr)
		

class Scan(Thread): # Thread dello scanner
	def __init__(self, addr, port):
		Thread.__init__(self)
		self.addr = addr
		self.port = port
	def run(self):
		sock = socket.socket()
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
