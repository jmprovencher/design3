# import the necessary packages
import sys
from stationbase.interface.StationBase import StationBase
from stationbase.interface.ImageReelle import ImageReelle
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSlot

import ConfigPath


class Interface(QtGui.QWidget):
    def __init__(self):
        super(Interface, self).__init__()
        self.setGeometry(1280, 1280, 1280, 700)
        self.setWindowTitle('Interface')
        self.btnDemarrer = QtGui.QPushButton('Demarrer', self)
        self.btnDemarrer.resize(120, 46)
        self.btnDemarrer.move(200, 200)
        self.demarre = False


    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.afficherInformations(qp)
        self.executerDemarage(qp)
        qp.end()

    def executerDemarage(self, qp):
        self.btnDemarrer.clicked.connect(self.estDemarrer)
        if(self.demarre == True):
            ImageReelle(qp)
            StationBase(qp)
            self.afficherImages(qp)

    def estDemarrer(self):
        self.demarre = True

    def afficherInformations(self, qp):
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

    def afficherImages(self, qp):
        self.dessinerOrange(qp)
        qp.drawRect(450, 348, 830, 5)
        qp.drawRect(638, 0, 5, 700)

    def dessinerOrange(self, qp):
        qp.setBrush(QtGui.QColor(252, 100, 0, 250))
        qp.setPen(QtGui.QColor(252, 100, 0))

    def dessinerNoir(self, qp):
        qp.setBrush(QtGui.QColor(0, 0, 0, 250))
        qp.setPen(QtGui.QColor(0, 0, 0))

    def formatContours(self, qp):
        qp.setBrush(QtGui.QColor(250, 250, 250, 250))
        qp.setPen(QtGui.QColor(0, 0, 250))

def main():
    app = QtGui.QApplication(sys.argv)
    interface = Interface()
    interface.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
