import socket
from threading import Thread, RLock
import time
from stationbase.communication.TCPServer import TCPServer
import  ConfigPath

verrou = RLock()

class StationServeur(Thread):
    def __init__(self, stationBase):
        Thread.__init__(self)
        self.stationBase = stationBase
        self.monServeur = TCPServer()

    def run(self):
        self.attendreWakeUpRobot()
        while 1:
            if (self.stationBase.envoyerCommande):
                self.envoyerCommande()
            elif (self.stationBase.attenteDuRobot):
                data = self.attendreInfoRobot()
                self.traiterInfoRobot(data)
            else:
                time.sleep(0.1)

    def envoyerCommande(self):
        while 1:
            try:
                self.monServeur.sendFile(self.stationBase.myRequest)
                self.stationBase.envoyerCommande = False
            except:
                #still not working, getting socket error : only one usage of each socket adress
                print "Connection with the remote host lost, Trying to reconnect"
                self.monServeur.closeConnection()
                self.monServeur = TCPServer()
                print self.monServeur.connectionEstablished

    def attendreInfoRobot(self):
        while 1:
            try:
                data = self.monServeur.receiveFile()
            except Exception as e:
                print e
                #still not working, getting socket error : only one usage of each socket adress
                print "Connection with the remote host lost, Trying to reconnect"
                self.monServeur.closeConnection()
                self.monServeur = TCPServer()
                print self.monServeur.connectionEstablished

            if data == -1:
                print('Error while receiving file')

            return data

    def traiterInfoRobot(self, data):
        print data
        commande = data['commande']
        parametre = data['parametre']
        if (commande == "tension"):
            self.stationBase.tensionCondensateur = parametre
        elif (commande == "robotPret"):
            self.stationBase.robotEstPret = True
        elif (commande == "termine"):
            self.stationBase.commandeTermine = True
            self.stationBase.attenteDuRobot = False

    def attendreWakeUpRobot(self):
        while 1:
            try:
                data = self.monServeur.receiveFile()
                commande = data['commande']
                if (commande == "robotPret"):
                    self.stationBase.robotEstPret = True
                    break
            except Exception as e:
                print e
                #still not working, getting socket error : only one usage of each socket adress
                print "Connection with the remote host lost, Trying to reconnect"
                self.monServeur.closeConnection()
                self.monServeur = TCPServer()
                print self.monServeur.connectionEstablished

            if data == -1:
                print('Error while receiving file')



