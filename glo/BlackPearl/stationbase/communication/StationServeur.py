import socket
from threading import Thread, RLock
import time
from stationbase.communication.TCPServer import TCPServer

verrou = RLock()

class StationServeur(Thread):
    def __init__(self, stationBase):
        Thread.__init__(self)
        self.stationBase = stationBase
        self.monServeur = TCPServer()

    def run(self):
        while 1:
            if (self.doitEnvoyerFichier()):
                try:
                    self.sendFile('data.json')
                    self.stationBase.envoyerFichier = False
                except:
                    #still not working, getting socket error : only one usage of each socket adress
                    print "Connection with the remote host lost, Trying to reconnect"
                    self.monServer.closeConnection()
                    self.monServer = TCPServer()
                    print self.monServer.connectionEstablished
            time.sleep(0.01)

    def doitEnvoyerFichier(self):
        return self.stationBase.envoyerFichier



