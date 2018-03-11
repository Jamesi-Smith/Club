# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import datetime
import time
import re
from decimal import Decimal


from AGSpiel import *

class AG(AGSpiel):

    Anzahl = 0

    #Nicht unbedingt notwendig
    __i = ""
    __vorhanden = False
    __WKN = ""
    __AGName = ""
    __CEO = ""
    __AGAlter = ""
    __AktienAnzahl = ""
    __Kurs = ""
    __Briefkurs = ""
    __Geldkurs = ""
    __Bargeld = ""
    __BWjeAktie = ""
    __SWjeAktie = ""
    __Handelsaktivitaet = ""

    #Erstellt ein Objekt der Klasse AG
    def __init__(self, AGS, i, WKN):
        self.AGS = AGS
        self.__i = str(i)
        self.__WKN = str(WKN)
        AG.Anzahl += 1

    def __del__(self):
        AG.Anzahl -= 1

    #Liest die Profilseite aus
    def ProfilAuslesen(self):
        html_profil = self.AGS.get_seiteninhalt((self.AGS.get_profilurl()+ str(self.get_WKN())))
        if "Diese WKN ist nicht (mehr) gültig." in str(html_profil):
            self.set_AGName("ungültig")

        if self.get_AGName() <> "ungültig":
            try:
                self.set_AGName(str(html_profil.title).replace("<title>", "").replace(" auf AG-Spiel.de</title>", ""))
                self.set_CEO("CEO")
                alter = str(html_profil.find("table", {"class": "padding5"}).findAll("td")[3].text.replace("Stk.", "").replace(" ", "")).split(".")
                self.set_AGAlter((datetime.date.today() - datetime.date(int(alter[2]), int(alter[1]), int(alter[0]))).days)
                self.set_AktienAnzahl(html_profil.find("table", {"class": "padding5"}).findAll("td")[5].text.replace("Stk.", "").replace(".", "").replace(" ", ""))
                self.set_Kurs(html_profil.find("div", {"id": "handelskurs"}).findAll("span")[0].text.replace("€", "").replace("\n", "").replace(" ","").replace(".", "").replace(",", "."))
                self.set_Briefkurs(html_profil.find("div", {"id": "briefkurs"}).findAll("span")[0].text.replace("€", "").replace("\n", "").replace(" ","").replace(".", "").replace(",", "."))
                self.set_Geldkurs(html_profil.find("div", {"id": "geldkurs"}).findAll("span")[0].text.replace("€", "").replace("\n", "").replace(" ","").replace(".", "").replace(",", "."))
                self.set_Bargeld(html_profil.find("table", {"id": "tagesBilanz"}).findAll("td")[2].text.replace(".", "").replace("€", ""))
                self.set_BWjeAktie(html_profil.find("table", {"id": "tagesBilanz"}).findAll("td")[5].text.replace(".", "").replace(",", ".").replace("€", "").replace(" ", ""))
                self.set_SWjeAktie(html_profil.find("div", {"id": "sw"}).text.replace("SW/Aktie", "").replace("€", "").replace("\n", "").replace(" ", "").replace("(?)", "").replace(".", "").replace(",", "."))
                self.set_Handelsaktivitaet(html_profil.find("div", {"id": "handelsaktivität"}).text.replace(" ", "").replace("\n", "").replace("(?)","").replace("Aktivität", "").replace("%", ""))
            except:
                self.set_AGName("Fehler")
                self.set_AGAlter("0")
                self.set_AktienAnzahl("0")
                self.set_Kurs("0")
                self.set_Briefkurs("0")
                self.set_Geldkurs("0")
                self.set_Bargeld("0")
                self.set_BWjeAktie("0")
                self.set_SWjeAktie("0")
                self.set_Handelsaktivitaet("0")
            time.sleep(1)

    #Gibt AGSpiel-Objekt zurück, um auf dessen Funktionen zurück zugreifen
    def get_AGS(self):
        return self.AGS

    def get_i(self):
        return self.__i

    def get_WKN(self):
        return self.__WKN
    def set_WKN(self, WKN):
        self.__WKN = WKN

    def get_AGName(self):
        return self.__AGName
    def set_AGName(self, AGName):
        self.__AGName = AGName

    def get_CEO(self):
        return self.__CEO
    def set_CEO(self, CEO):
        self.__CEO = CEO

    def get_AGAlter(self):
        return self.__AGAlter
    def set_AGAlter(self, AGAlter):
        self.__AGAlter = AGAlter

    def get_AktienAnzahl(self):
        return self.__AktienAnzahl
    def set_AktienAnzahl(self, AktienAnzahl):
        self.__AktienAnzahl = AktienAnzahl

    def get_Kurs(self):
        return self.__Kurs
    def set_Kurs(self, Kurs):
        self.__Kurs = Kurs

    def get_Briefkurs(self):
        return self.__Briefkurs
    def set_Briefkurs(self, Briefkurs):
        self.__Briefkurs = Briefkurs

    def get_Geldkurs(self):
        return self.__Geldkurs
    def set_Geldkurs(self, Geldkurs):
        self.__Geldkurs = Geldkurs

    def get_Bargeld(self):
        return self.__Bargeld
    def set_Bargeld(self, Bargeld):
        self.__Bargeld = Bargeld

    def get_BWjeAktie(self):
        return self.__BWjeAktie
    def set_BWjeAktie(self, BWjeAktie):
        self.__BWjeAktie = BWjeAktie

    def get_SWjeAktie(self):
        return self.__SWjeAktie
    def set_SWjeAktie(self, SWjeAktie):
        self.__SWjeAktie = SWjeAktie

    def get_Handelsaktivitaet(self):
        return self.__Handelsaktivitaet
    def set_Handelsaktivitaet(self, Handelsaktivitaet):
        self.__Handelsaktivitaet = Handelsaktivitaet

    #Berechnungen
    def get_Buchwert(self):
        return str(Decimal(self.get_AktienAnzahl())* Decimal(self.get_BWjeAktie()))

    def get_Substanzwert(self):
        return str(Decimal(self.get_AktienAnzahl())* Decimal(self.get_SWjeAktie()))

    def get_Boersenwert(self):
        return str(Decimal(self.get_AktienAnzahl())* Decimal(self.get_Kurs()))
