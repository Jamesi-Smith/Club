# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from AG import *

class Crawler(AG):

    __AGListe = []

    def __init__(self, AGS):
        self.AGS = AGS
        self.AlleAGs = []
        self.AuszulesendeAGs = []

    def get_AGListe(self):
        return self.__AGListe

    def set_AGListe(self, liste):
        self.__AGListe = liste

    def AG_Hinzufuegen(self, AG):
        self.__AGListe.append(AG)

    def get_AGListeAusAGSpiel(self):
        return self.AGS.get_AGListeAusAGSpiel()

