from stationbase.trajectoire.Trajectoire import Trajectoire
from elements.StationRecharge import StationRecharge
from elements.Cible import Cible
import time
import copy


class Carte:
    def __init__(self):
        self.listeIles = []
        self.listeTresors = []
        self.robot = None
        self.cible = Cible([self])
        self.stationRecharge = StationRecharge()
        self.trajectoire = Trajectoire()

    def getIles(self):
        return self.listeIles

    def getIlesCorrespondantes(self, informationIleCible):
        retour = []
        for ile in self.listeIles:
            if ile.couleur == informationIleCible or ile.forme == informationIleCible:
                retour.append(ile)
        return retour

    def setIles(self, listIles):
        self.listeIles = listIles

    def getTresor(self):
        return self.m_tresor

    def setTresors(self, listTresors):
        self.listeTresors = listTresors

    def getRobot(self):
        return self.robot

    def getRobotValide(self):
        while self.robot is None:
            time.sleep(0.01)
        return copy.deepcopy(self.robot)

    def setRobot(self, robot):
        self.robot = robot

    def getTrajectoire(self):
        return self.trajectoire

    def getCible(self):
        return self.cible

    def setCible(self, cible):
        self.cible = cible

    def getStationRecharge(self):
        return self.stationRecharge




