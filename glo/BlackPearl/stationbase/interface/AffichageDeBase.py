from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QPainter

class AffichageDeBase():
    def __init__(self, qp):
        self.dessinerNoir(qp)
        qp.drawText(50, 400 + 50, QtCore.QString('Trajectoire :'))
        qp.drawText(50, 450 + 50, QtCore.QString('Tension condensateur :'))
        qp.drawText(50, 500 + 50, QtCore.QString('Position et Orientation du Robot :'))
        qp.drawText(50, 550 + 50, QtCore.QString('Ile cible :'))
        self.formatContours(qp)
        qp.drawRect(260, 385 + 50, 120, 20)
        qp.drawRect(260, 435 + 50, 80, 20)
        qp.drawRect(260, 485 + 50, 300, 20)
        qp.drawRect(260, 535 + 50, 100, 20)
        self.dessinerNoir(qp)
        qp.drawText(275, 400 + 50, QtCore.QString('88.95''N  15.10''O '))
        qp.drawText(275, 450 + 50, QtCore.QString('1.23 V '))
        qp.drawText(275, 500 + 50, QtCore.QString('0.8245m, 0.23421m     68.35''S  1.36''O '))
        qp.drawText(275, 550 + 50, QtCore.QString('Cercle rouge'))
        self.dessinerOrange(qp)
        qp.drawText(450, 338, QtCore.QString('Carte reelle'))
        qp.drawText(450, 378, QtCore.QString('Carte virtuelle'))
        qp.drawRect(450, 348, 830, 5)
        qp.drawRect(638, 0, 5, 700)
        self.dessinerNoir(qp)
        qp.drawText(80, 80, QtCore.QString('Robot connecter?'))
        qp.drawEllipse(200, 50, 50, 50)
        self.dessinerRouge(qp)
        qp.drawEllipse(205, 55, 40, 40)

    def dessinerOrange(self, qp):
        qp.setBrush(QtGui.QColor(252, 100, 0, 250))
        qp.setPen(QtGui.QColor(252, 100, 0))

    def dessinerNoir(self, qp):
        qp.setBrush(QtGui.QColor(0, 0, 0, 250))
        qp.setPen(QtGui.QColor(0, 0, 0))

    def formatContours(self, qp):
        qp.setBrush(QtGui.QColor(250, 250, 250, 250))
        qp.setPen(QtGui.QColor(0, 0, 250))

    def dessinerRouge(self, qp):
        qp.setBrush(QtGui.QColor(240, 0, 0, 250))
        qp.setPen(QtGui.QColor(140, 0, 0))