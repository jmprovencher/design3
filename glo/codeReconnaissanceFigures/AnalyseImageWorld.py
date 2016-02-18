# import the necessary packages
import numpy as np
import cv2
from ElementCartographique import ElementCartographique
from Tresor import Tresor
from Ile import Ile
from DetectionIles import DetectionIles


class AnalyseImageWorld(object):
    def __init__(self):
        # self.imageCamera = cv2.imread('Image/test_imageTresor.png')
        self.elementsCartographiques = []
        self.chargerImage('Image/test_imageTresor.png')
        self.resolution = (480, 640)
        self.recadrerImage()
        self.estomperImage()

    def chargerImage(self, url):
        """
        Changement de l'image a traiter
        :param url: Le lien de l'image a charger dans le systeme de traitement
        """

        self.imageCamera = cv2.imread(url)

    def recadrerImage(self):
        """
        Recadrage de l'image pour supprimer les zones inutiles qui se trouvent hors de la table
        """

        # Hardcodage du crop
        # TODO: a verifier sur toute les tables
        crop = self.imageCamera[self.resolution[0] * 3 / 16:self.resolution[0] * 11 / 12, 0:self.resolution[1]]
        cv2.imwrite('Cropped.png', crop)
        self.imageCamera = cv2.imread('Cropped.png')

    def estomperImage(self):
        """
        On effectue un leger estompement de l'image afin de minimiser la fluctuation des pixels
        """

        blur = cv2.GaussianBlur(self.imageCamera, (5, 5), 0)
        cv2.imwrite('Cropped.png', blur)
        self.imageCamera = cv2.imread('Cropped.png')

    def trouverCentreForme(self, contoursForme):
        """
        Detection du centre de la forme
        :param contoursForme: Contours de la forme
        :return: Un tuple correspondant aux coordonnees x,y du centre de la forme
        """

        M = cv2.moments(contoursForme)
        centre_x = int(M['m10'] / M['m00'])
        centre_y = int(M['m01'] / M['m00'])
        return centre_x, centre_y

    def identifierForme(self, element):
        """
        Identification de la forme detectee sur l'image
        :param element: Forme identifiee avec le plus haut taux de compatibilite
        """

        font = cv2.FONT_HERSHEY_SIMPLEX

        contoursForme, nomForme, couleurForme = element

        centreForme = self.trouverCentreForme(contoursForme)

        # Afficher identification sur la photo
        cv2.putText(self.imageCamera, nomForme, centreForme, font, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

        if (couleurForme == "TRESOR"):
            tresor = Tresor(centreForme)
            self.elementsCartographiques.append(tresor)
        else:
            ile = Ile(centreForme, couleurForme, nomForme)
            self.elementsCartographiques.append(ile)

    def trouverElement(self):
        """
        Appelle toutes les fonctions de traitement visuel afin de trouver tous les elements
        """

        # cv2.imshow("Image", self.imageCamera)
        self.detectionIles = DetectionIles(self.imageCamera)
        self.detectionIles.definirFormesConnues()
        self.detectionIles.detecterIles()

        self.ilesIdentifiees = self.detectionIles.getIlesIdentifiees()
        print "Longueur de element: %d" % len(self.ilesIdentifiees)

        for element in self.ilesIdentifiees:
            self.identifierForme(element)
        # Affiche l'image apres detection
        cv2.imshow("Image2", self.imageCamera)

        # Permet de garder les images ouvertes
        cv2.waitKey(0)

    def getElementCartographiques(self):
        return self.elementsCartographiques