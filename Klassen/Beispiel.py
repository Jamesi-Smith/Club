# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from Crawler import *

AGS = AGSpiel()
C = Crawler(AGS)

#Um alle AGs in die Liste aufzunehmen
liste = C.get_AGListeAusAGSpiel()
print len(liste[0])
for i in range(0, len(liste[0])):
    neueAG = AG(AGS, i, liste[0][i])
    neueAG.set_AGName(liste[1][i])
    #neueAG.ProfilAuslesen()
    C.AG_Hinzufuegen(neueAG)
    print "Unter der WKN : " + C.get_AGListe()[i].get_WKN() + " wurde die AG: " + C.get_AGListe()[i].get_AGName() + " in die Liste aufgenommen."
    #print "Die AG " + neueAG.get_AGName() + " unter der Laufnummer " + neueAG.get_i() + " mit der WKN " + neueAG.get_WKN() + " hat einen Buchwert von " + neueAG.get_Buchwert() + " und einen Börsenwert von " + neueAG.get_Boersenwert()

#Um nur bestimmte Spieler auszulesen
James = AG(AGS, 0, 140037)
Earl = AG(AGS, 1, 140025)
Annie = AG(AGS, 2, 141098)
HWJ = AG(AGS, 3, 153062)

liste = [James, Earl, Annie, HWJ]
C.set_AGListe(liste)
for meineAG in C.get_AGListe():
    meineAG.ProfilAuslesen()
    print "Die AG " + meineAG.get_AGName() + "unter der Laufnummer " + meineAG.get_i() + " mit der WKN " + meineAG.get_WKN() + " hat einen Buchwert von " + meineAG.get_Buchwert() + " und einen Börsenwert von " + meineAG.get_Boersenwert()
