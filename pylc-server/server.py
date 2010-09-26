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
import select
from threading import Thread

DEBUG = 1 # Attiva/disattiva i messaggi di debug
VERSION = "0.1a" # Versione del server

class PyLCServer():
    def __init__(self, port):
        self.port = port
        self.eh_thread = EchoHandler(50001)
        self.ch_thread = ConnectionHandler(50000)
        self.eh_thread.setDaemon(True)
        self.ch_thread.setDaemon(True)
        self.eh_thread.start()
        self.ch_thread.start()

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

class ConnectionHandler(Thread):
    def __init__(self, port):
        Thread.__init__(self)
        self.port = port
        
        self.sockets = {}
        self.currentID = 0
    
    def broadcast(self, message, sender): # TODO
        for sock in self.sockets.keys():
            if sock is not sender:
                sock.send(message)
        
    def run(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('', self.port))
        self.s.listen(1)
        
        while(1): # Ciclo principale del server
            self.sockList = [self.s.fileno()]
            for sock in self.sockets.keys():
                # Creazione lista socket aperti
                self.sockList.append(sock.fileno())
            
            self.toRead, self.toWrite, self.onError = select.select(
                self.sockList, [], [], None)
            
            for sockToRead in self.toRead:
                if sockToRead == self.s.fileno(): 
                    # Nuova connessione
                    # Accetto la connessione e assegno un ID progressivo
                    newsock, addr = self.s.accept() 
                    self.sockets[newsock] = self.currentID
                    self.currentID += 1
                    if DEBUG:
                        print "[ConnectionHandler] Nuova connessione"
                        print "[ConnectionHandler] Indirizzo origine:", addr
                else:
                    # Messaggio su connessione esistente
                    for sock in self.sockets.keys():
                        if sock.fileno() == sockToRead: break
                    sockID = self.sockets[sock]
                    
                    message, source = sock.recvfrom(2048)
                    print "[ConnectionHandler] Messaggio ricevuto da ID", sockID, ":", message
        
if __name__ == "__main__":
    server = PyLCServer(50100)
    while(1):
        pass