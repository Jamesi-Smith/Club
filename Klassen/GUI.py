# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from Tkinter import *
import tkinter.messagebox

from Crawler import *

AGS = AGSpiel()
C = Crawler(AGS)

from tkinter import *
import tkinter.messagebox

app = Tk()
app.title("AG-Spiel Crawler")
app.geometry("1000x600+100+100")

def AuslesenStarten():
    inArb.set("In Arbeit")
    app.update()
    Eingabe = Eingabefeld.get().split(",")
    txtAusgabe.delete("1.0", END)
    for i in range(0, len(Eingabe)):
        Eingabe[i] = Eingabe[i].replace(" ", "")
        print Eingabe[i]
        C.AG_Hinzufuegen(AG(AGS, i, Eingabe[i]))
    for meineAG in C.get_AGListe():
        meineAG.ProfilAuslesen()
        txtAusgabe.insert(END, "Die AG " + meineAG.get_AGName() + " mit der WKN " + meineAG.get_WKN() + " hat einen Buchwert von " + meineAG.get_Buchwert() + " und einen Börsenwert von " + meineAG.get_Boersenwert() + "\n")
    inArb.set("Alle AGs erfolgreich ausgelesen")

lblEingabe = Label(app, text= "Hier die auszulesenden AGs mit Kommata getrennt eingeben:").place(x = 10, y = 30, width=330, height=20)

WKNListe = StringVar()
Eingabefeld = Entry(app, textvariable=WKNListe)
Eingabefeld.place(x = 10, y = 50, width=800, height= 20)

btnStart = Button(app, text= "Auslesen starten", command=AuslesenStarten).place(x = 10, y = 80, width=150, height=20)

inhalt = StringVar()
inhalt.set("")

ausgabe = "Ausgabe:"
txtAusgabe = Text(app)
txtAusgabe.place(x=10, y=110, width = 980, height=480)
txtAusgabe.insert(END, ausgabe)

inArb= StringVar()
inArb.set("")
lblinArbeit = Label(app, textvariable=inArb).place(x=170, y=80, width=200, height=20)

app.mainloop()

#Eingabe möglicherweise: 153062, 140037, 100001, 140025, 141098, 164057
#ergibt die Ausgabe:
#Die AG HWJ VC Trust Fund mit der WKN 153062 hat einen Buchwert von 2842975796.90 und einen Börsenwert von 1632005000.00
#Die AG Smith AG mit der WKN 140037 hat einen Buchwert von 1492233389.39 und einen Börsenwert von 1091656849.60
#Die AG Rady mit der WKN 100001 hat einen Buchwert von 1660528831.62 und einen Börsenwert von 1104766950.00
#Die AG Bankhaus Silberstein mit der WKN 140025 hat einen Buchwert von 1979574000.00 und einen Börsenwert von 1850000000.00
#Die AG Trololski AG mit der WKN 141098 hat einen Buchwert von 939788000.00 und einen Börsenwert von 728000000.00
#Die AG DK Capital Markets mit der WKN 164057 hat einen Buchwert von 356932000.00 und einen Börsenwert von 412800000.00
