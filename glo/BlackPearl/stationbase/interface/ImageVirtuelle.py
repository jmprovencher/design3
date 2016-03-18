from PyQt4 import QtGui, QtCore

import ConfigPath
import math


class ImageVirtuelle():
    def __init__(self, qp, listeIles, listeTresors, trajectoire):
        qp.drawPixmap(640, 350, QtGui.QPixmap(ConfigPath.Config().appendToProjectPath('images/test_image_vide.png')), 0, 90, 640, 480)
        print("PAINT EVEN ###################")
        self.dessinerIles(qp, listeIles)
        self.dessinerTresors(qp, listeTresors)
        listeDePoint = []
        self.dessinerTrajectoire(qp, trajectoire)
        self.dessinerConnecter(qp)

    def dessinerConnecter(self, qp):
        qp.setBrush(QtGui.QColor(0, 110, 60, 250))
        qp.setPen(QtGui.QColor(0, 110, 60))
        qp.drawEllipse(205, 55, 40, 40)

    def dessinerTresors(self, qp, listeTresors):
        for tresor in listeTresors:
            print("DESSINE TRESOR")
            position = tresor.centre_x * 0.4 + 618, tresor.centre_y * 0.4 + 355
            self.dessinerTresor(qp, position)

    def dessinerIles(self, qp, listeIles):
        for ile in listeIles:
            print("DESSINE ILES: ", ile.forme, ile.couleur)
            position = (ile.centre_x * 0.4 + 618, ile.centre_y * 0.4 + 355)
            couleur = ile.couleur
            forme = ile.forme
            self.dessiner(qp, forme, couleur, position)


    def definirCouleur(self, qp, couleur):
        if (couleur == "Jaune"):
            qp.setBrush(QtGui.QColor(205, 175, 0, 250))
            qp.setPen(QtGui.QColor(205, 175, 0))
        elif (couleur == "Rouge"):
            qp.setBrush(QtGui.QColor(140, 0, 30, 250))
            qp.setPen(QtGui.QColor(140, 0, 30))
        elif (couleur == "Vert"):
            qp.setBrush(QtGui.QColor(0, 110, 60, 250))
            qp.setPen(QtGui.QColor(0, 110, 60))
        elif (couleur == "Bleu"):
            qp.setBrush(QtGui.QColor(0, 140, 190, 250))
            qp.setPen(QtGui.QColor(0, 140, 190))

    def dessinerTresor(self, qp, position):
        centre_x, centre_y = position
        qp.setBrush(QtGui.QColor(205, 175, 0, 250))
        qp.setPen(QtGui.QColor(205, 175, 0))
        qp.drawRect(centre_x, centre_y, 10, 4)


    def dessiner(self, qp, forme, couleur, position):
        centre_x, centre_y = position
        if (couleur == "Jaune"):
            qp.setBrush(QtGui.QColor(205, 175, 0, 250))
            qp.setPen(QtGui.QColor(205, 175, 0))
        elif (couleur == "Rouge"):
            qp.setBrush(QtGui.QColor(140, 0, 30, 250))
            qp.setPen(QtGui.QColor(140, 0, 30))
        elif (couleur == "Vert"):
            qp.setBrush(QtGui.QColor(0, 110, 60, 250))
            qp.setPen(QtGui.QColor(0, 110, 60))
        elif (couleur == "Bleu"):
            qp.setBrush(QtGui.QColor(0, 140, 190, 250))
            qp.setPen(QtGui.QColor(0, 140, 190))
        if (forme == "Carre"):
            qp.drawRect(centre_x - 15, centre_y -15, 30, 30)
        elif (forme == "Cercle"):
            qp.drawEllipse(centre_x - 16, centre_y - 16, 32, 32)
        elif (forme == "Triangle"):
            polygone = QtGui.QPolygon([
                QtCore.QPoint(centre_x - 18, centre_y + 12),
                QtCore.QPoint(centre_x, centre_y - 24),
                QtCore.QPoint(centre_x + 18, centre_y + 12)
            ])
            qp.drawConvexPolygon(polygone)

        elif (forme == "Pentagone"):
            polygone = QtGui.QPolygon([
                QtCore.QPoint(centre_x - 18, centre_y),
                QtCore.QPoint(centre_x, centre_y - 18),
                QtCore.QPoint(centre_x + 18, centre_y),
                QtCore.QPoint(centre_x + 9, centre_y + 18),
                QtCore.QPoint(centre_x - 9, centre_y + 18),
                QtCore.QPoint(centre_x - 18, centre_y)
            ])
            qp.drawConvexPolygon(polygone)

    def dessinerTrajectoire(self, qp, listeDePoint):
        if(listeDePoint):
            qp.setBrush(QtGui.QColor(0, 140, 190, 250))
            qp.setPen(QtGui.QColor(0, 140, 190))
            qp.setPen(QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine))
            point1 = (listeDePoint[0][0] * 0.4 + 618, listeDePoint[0][1] * 0.4 + 355)
            point2 = (listeDePoint[1][0] * 0.4 + 618, listeDePoint[1][1] * 0.4 + 355)
            qp.drawLine(point1[0], point1[1], point2[0],point2[1] )
            if (len(listeDePoint) > 2):
                self.dessinerTrajectoire(qp, listeDePoint[1::1])
            if (len(listeDePoint) == 2):
                self.dessinerFlecheBout(qp, point1, point2)

    def dessinerFlecheBout(self, qp, pointAvantDernier, pointN):
        vecteurBout = ((pointAvantDernier[0] - pointN[0]) , (pointAvantDernier[1] - pointN[1]))
        distanceBout = (math.sqrt(((vecteurBout[0])**2) + ((vecteurBout[1])**2)))/15
        vecUnitaireBout = (vecteurBout[0]/distanceBout, vecteurBout[1]/distanceBout)
        flecheGauche = ((vecUnitaireBout[0] * math.cos(math.pi/4)) + (vecUnitaireBout[1] * math.sin(math.pi/4)), (- vecUnitaireBout[0] * math.sin(math.pi/4)) + (vecUnitaireBout[1] * math.cos(math.pi/4)))
        flecheDroite = ((vecUnitaireBout[0] * math.cos(- math.pi/4)) + (vecUnitaireBout[1] * math.sin(- math.pi/4)), (- vecUnitaireBout[0] * math.sin(- math.pi/4)) + (vecUnitaireBout[1] * math.cos(- math.pi/4)))
        qp.drawLine(pointN[0], pointN[1], pointN[0] + flecheGauche[0], pointN[1] + flecheGauche[1])
        qp.drawLine(pointN[0], pointN[1], pointN[0] + flecheDroite[0], pointN[1] + flecheDroite[1])