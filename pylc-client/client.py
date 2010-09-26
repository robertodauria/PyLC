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
import sys
import select

import radar
VERSION = "0.1a"
SERVERPORT = 50000
DEBUG = 1

class PyLCClient():
    def __init__(self, server, port):
        self.server = server
        self.port = port
    
    def start(self):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((self.server, self.port))
            if DEBUG:
                print "[PyLCClient] Connesso a", self.server, "porta", self.port
        except socket.error, e:
            print "Impossibile connettersi al server. Esco."
            exit()
        while(1):
            sys.stdout.write('>')
            sys.stdout.flush()
            
            self.toRead, self.ToWrite, self.onError = select.select(
                [0, self.s], [], [], None)
            
            for sock in self.toRead:
                if sock == 0: # Input da STDIN
                    data = sys.stdin.readline().strip()
                    if data: self.s.send(data)
                elif sock == self.s:
                    data = receive(self.s)
                    sys.stdout.write(data + '\n')
                    sys.stdout.flush()
            

print "PyLC Test CLI - Versione", VERSION
print "Cerco server sulla porta", str(SERVERPORT + 1) + "..."
myRadar = radar.Radar()
replies = myRadar.sendecho(SERVERPORT + 1)

if len(replies) != 0: # Lista server trovati
    print "Server trovati:"
    
    i = 0
    for s in replies: 
        print str(i) + ": " + s[0]
        i += 1
else:
    print "Nessun server trovato. Esco."
    exit()
    
if len(replies) == 1: # Seleziono l'unico server presente
    server = replies[0][0]
    port = replies[0][1] - 1
else: # Scelta del server
    print "Seleziona numero server da utilizzare:"
    nserver = input()
    if nserver <= len(replies) - 1:
        server = replies[nserver][0]
        port = replies[nserver][1] - 1
    else:
        print "Numero server non valido. Esco."
        exit()
    
print
print "Utilizzo", server + ", porta", port
myServer = PyLCClient(server, port)
myServer.start()

