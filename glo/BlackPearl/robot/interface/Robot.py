from robot.communication.RobotClient import RobotClient
from robot.vision.AnalyseImageEmbarquee import AnalyseImageEmbarquee
from robot.interface.FeedVideoRobot import FeedVideoRobot
from robot.communication.LectureUART import LectureUART
from threading import Thread
import time
from robot.interface.RobotService import RobotService

COMMANDE_ILE = 'alignement_ile'
COMMANDE_TRESOR = 'alignement_tresor'
COMMANDE_STATION = 'alignement_station'
COMMANDE_MANCHESTER = "decoderManchester"
MAX_TENSION_CONDENSATEUR = 4.60

class Robot(Thread):
    def __init__(self, uartDriver):
        Thread.__init__(self)
        self.uartDriver = uartDriver
        self.service = RobotService()
        self.instructions = []

        self.alignementEnCours = False
        self.positionTresor = False
        self.positionDepot = False
        self.tacheTerminee = False
        self.commandeTerminee = False
        self.pretEnvoyerLettre = False
        self.tresorCapturer = False
        self.tresorNonCapturer = False

        self.lettreObtenue = None
        self.indiceObtenu = None
        self.adresseIP = '192.168.0.45'

        self.tensionCondensateur = 0
        self._demarrerFeedVideo()
        self._demarrerConnectionTCP()

    def run(self):
        print("Run")
        self._demarrerLectureUART()
        time.sleep(2)
        self.uartDriver.phaseInitialisation()
        self.robotClient.demarrageTermine = True

    def demarrerAlignementStation(self):
        print("Demarre phase alignement station")
        self.alignementEnCours = True
        self.uartDriver.cameraPositionFace()
        self.uartDriver.sendCommand('forward', 4)
        time.sleep(1)
        self._demarrerAnalyseVideo('station_final')
        time.sleep(1)
        self.uartDriver.preAlignementStation()
        self._executerAlignement()
        self._attendreChargeComplete()
        print("Charge complete")
        self.uartDriver.stopCondensateur()
        print("CONDENSATEUR OFF")
        self.uartDriver.sendCommand('backward', 10)
        time.sleep(5)
        self._decoderManchester()
        self.uartDriver.postAlignementStation()
        self.alignementEnCours = False

    def _attendreManchester(self):
        while self.lettreObtenue is None:
            print("Attente decodage lettre")
            time.sleep(0.5)
        time.sleep(0.1)


    def demarrerAlignementTresor(self):
        print("Demarre phase alignement tresor")
        self.alignementEnCours = True
        self.uartDriver.cameraPositionDepot()
        self._demarrerAnalyseVideo('tresor')

        if (self.tresorCapturer):
            self.uartDriver.preAlignementTresor()
            self.uartDriver.cameraPositionFace()
            self._executerAlignement()
            self.uartDriver.postAlignementTresor()

        self.alignementEnCours = False

    def demarrerAlignementIle(self, parametre):
        print("Demarre phase alignement ile")
        self.alignementEnCours = True
        self.uartDriver.cameraPositionDepot()
        self._demarrerAnalyseVideo(parametre)
        self._executerAlignement()
        time.sleep(0.2)
        self.uartDriver.postAlignementIle()
        self.alignementEnCours = False

    def ajouterDirectives(self, instructions):
        self.instructions.append(instructions)

    def traiterCommande(self, commande, parametre):
        if commande == COMMANDE_ILE:
            self.demarrerAlignementIle(parametre)
        elif commande == COMMANDE_TRESOR:
            self.demarrerAlignementTresor()
        elif commande == COMMANDE_STATION:
            self.demarrerAlignementStation()
        elif commande == COMMANDE_MANCHESTER:
            self._decoderManchester()
        else:
            self.commandeTerminee = False
            self.uartDriver.sendCommand(commande, parametre)
            self.attendreCommandeTerminee()

    def _executerAlignement(self):
        print 'nb de correction'
        print len(self.instructions)
        for inst in self.instructions:
            commande, parametre = inst
            parametre = int(parametre)
            self.commandeTerminee = False
            print("Envoie commande a traiter commande")
            print commande, parametre
            self.traiterCommande(commande, parametre)
            print("Commande envoyee a traiter commande")
            time.sleep(1)
        self.instructions = []

    def attendreCommandeTerminee(self):
        while not self.commandeTerminee:
            print("Attente commande terminee")
            time.sleep(0.5)
        print 'commande fini.'

    def _decoderManchester(self):
        self.uartDriver.lireManchester()
        self._attendreManchester()
        self.indiceObtenu = self.service.obtenirCible(self.lettreObtenue)
        self.pretEnvoyerLettre = True

    def _attendreChargeComplete(self):
        while (float(self.tensionCondensateur) < MAX_TENSION_CONDENSATEUR ):
            print(self.tensionCondensateur)
            self.robotClient.envoyerTension()
            time.sleep(0.5)

    def _demarrerFeedVideo(self):
        self.threadVideo = FeedVideoRobot()
        self.threadVideo.initialiserVideo()
        self.threadVideo.start()

    def _demarrerConnectionTCP(self):
        self.robotClient = RobotClient(self, self.adresseIP)
        time.sleep(2)
        self.robotClient.start()

    def _demarrerLectureUART(self):
        self.threadLecture = LectureUART(self)
        self.flushUART()
        self.threadLecture.start()

    def flushUART(self):
        self.uartDriver.UART.flushInput()
        time.sleep(1)

    def _demarrerAnalyseVideo(self, type):
        print("Demarrage analyse %s", type)
        self.analyseImageEmbarquee = AnalyseImageEmbarquee(self)
        self.analyseImageEmbarquee.definirType(type)
        self.analyseImageEmbarquee.start()
        self.analyseImageEmbarquee.join()

