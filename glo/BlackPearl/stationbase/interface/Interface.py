# import the necessary packages
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QPainter
from stationbase.interface.StationBase import StationBase
from stationbase.interface.AfficherImageVirtuelle import AfficherImageVirtuelle
from stationbase.interface.AffichageDeBase import AffichageDeBase
from Tkinter import *
from stationbase.interface.RedirigeurTexte import RedirigeurTexte

class Interface(QtGui.QWidget):
    def __init__(self):
        super(Interface, self).__init__()
        self.threadAfficherImageVirtuelle = AfficherImageVirtuelle(self)
        self.initUI()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        #self.affichageDeBase = AffichageDeBase(qp)
        #if(self.threadStationBase.threadCommunication.robotEstPret):
            #self.dessinerRobotActive(qp)
        qp.end()


    def initUI(self):
        self.setWindowTitle('Interface')
        screenShape = QtGui.QDesktopWidget().screenGeometry()
        self.largeur = screenShape.width()
        self.hauteur = screenShape.height()
        self.resize(self.largeur, self.hauteur)
        self.setAutoFillBackground(False)
        self.feed = QLabel(self)
        self.buffer = 25
        self.feed.setGeometry(5, self.hauteur-(600+self.buffer+5), 800, 600)
        self.feed.setPixmap(self.threadAfficherImageVirtuelle.imageConvertie)
        #self.orientation = QLabel(self)
        #self.orientation.setGeometry(380, 22, 440, 50)
        #self.direction = QLabel(self)
        #self.direction.setGeometry(380, 52, 400, 80)
        self.btnDemarer = QPushButton(self)
        self.btnDemarer.setText('Debuter')
        self.btnDemarer.setGeometry(40, 25, 200, 27)
        self.btnDemarer.clicked.connect(self.demarerRoutine)
        self.btnDemarer = QPushButton(self)
        self.btnDemarer.setText('Deplacement station')
        self.btnDemarer.setGeometry(40, 70, 200, 27)
        self.btnDemarer.clicked.connect(self.demarerRoutine)
        self.btnDemarer = QPushButton(self)
        self.btnDemarer.setText('Se charger')
        self.btnDemarer.setGeometry(40, 100, 200, 27)
        self.btnDemarer.clicked.connect(self.demarerRoutine)
        self.btnDemarer = QPushButton(self)
        self.btnDemarer.setText('Deplacement tresor')
        self.btnDemarer.setGeometry(40, 130, 200, 27)
        self.btnDemarer.clicked.connect(self.demarerRoutine)
        self.btnDemarer = QPushButton(self)
        self.btnDemarer.setText('Prendre tresor')
        self.btnDemarer.setGeometry(40, 160, 200, 27)
        self.btnDemarer.clicked.connect(self.demarerRoutine)
        self.btnDemarer = QPushButton(self)
        self.btnDemarer.setText('Deplacement ile cible')
        self.btnDemarer.setGeometry(40, 190, 200, 27)
        self.btnDemarer.clicked.connect(self.demarerRoutine)
        self.btnDemarer = QPushButton(self)
        self.btnDemarer.setText('Depot tresor')
        self.btnDemarer.setGeometry(40, 220, 200, 27)
        self.btnDemarer.clicked.connect(self.demarerRoutine)
        #self.tensionCondensateur = QLabel(self)
        #self.tensionCondensateur.setGeometry(480, 22, 640, 50)
        self.initTextBox()

    def demarerRoutine(self):
        self.threadStationBase = StationBase()
        self.threadStationBase.start()
        self.connect(self.threadAfficherImageVirtuelle, QtCore.SIGNAL("update()"), self.update_gui)
        self.threadAfficherImageVirtuelle.start()


    def update_gui(self):
        self.feed.setPixmap(self.threadAfficherImageVirtuelle.imageConvertie)
        #self.tensionCondensateur.setText(QString(self.threadStationBase.tensionCondensateur))
        QtGui.QApplication.processEvents()
        #if(not self.threadStationBase.carte.infoRobot is None):
            #self.orientation.setText(QString(str(self.threadStationBase.carte.infoRobot.centre_x) + 'x ' + str(self.threadStationBase.carte.infoRobot.centre_y) +'y '+ str(self.threadStationBase.carte.infoRobot.orientation)+'\xb0'))
        self.feed.repaint()
        #self.tensionCondensateur.setText(QString(self.threadStationBase.threadCommunication.tensionCondensateur + 'V'))
        #self.orientation.repaint()
        #self.direction.repaint()
        #self.tensionCondensateur.repaint()

    def dessinerRobotActive(self, qp):
        qp.setBrush(QtGui.QColor(0, 200, 120, 250))
        qp.setPen(QtGui.QColor(0, 200, 120))
        qp.drawEllipse(1005, 55, 40, 40)

    def initTextBox(self):
        self.text = QtGui.QTextEdit(self)
        self.text.setGeometry(self.feed.frameGeometry().width()+10, 5, self.largeur-(5+self.feed.frameGeometry().width()+10), self.hauteur-(self.buffer+10))
        self.text.setReadOnly(True)
        self.text.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        font = self.text.font()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.text.moveCursor(QtGui.QTextCursor.End)
        self.text.setCurrentFont(font)
        sb = self.text.verticalScrollBar()
        sb.setValue(sb.maximum())
        self.text.ensureCursorVisible()
        pal = QtGui.QPalette()
        bgc = QtGui.QColor(0, 0, 0)
        pal.setColor(QtGui.QPalette.Base, bgc)
        self.text.setPalette(pal)
        self.text.setTextColor(QtCore.Qt.white)
        self.text.insertPlainText('Black Pearl\n')
        sys.stdout = RedirigeurTexte(self.text, "stdout")
        sys.stderr = RedirigeurTexte(self.text, "stderr")