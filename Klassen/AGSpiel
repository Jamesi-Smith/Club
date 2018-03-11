# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from bs4 import BeautifulSoup as soup
import requests

class AGSpiel():

    __useragent = 'cronBROWSE v0.92'
    __logindaten = {
        'User-Agent': __useragent,
        'username': 'TCRatingAgency',
        'userpass': "TCRATheClub1?",
            'permanent': '1',
        'login': 'Einloggen',
    }
    __token = "token"

    __baseurl = 'https://www.ag-spiel.de'
    __starturl = 'https://www.ag-spiel.de/index.php?section=start'
    __loginurl = 'https://www.ag-spiel.de/index.php?section=login'
    __profilurl = 'https://www.ag-spiel.de/index.php?section=profil&aktie='
    __depotanalyseurl = 'https://www.ag-spiel.de/index.php?section=depotanalyse&aktie='
    __bilanzurl = 'https://www.ag-spiel.de/index.php?section=bilanzen&wkn='

    req_session = requests.Session()

    def __init__(self):
        self.ags_login()
        self.set_token()

    def ags_login(self): #Einloggen ins Spiel
        self.req_session.post(self.get_loginurl(), self.get_logindaten())
        self.req_session.get(self.get_starturl())

    def get_useragent(self): #gibt useragent zurück
        return self.__useragent
    def get_logindaten(self): #gibt die Logindaten zurück
        return self.__logindaten

    def set_token(self):
        self.__token = soup(self.get_page("https://www.ag-spiel.de/index.php?section=agorderbuch&action=create&ele=").text, "html.parser").find("input", {"name": "token"}).get("value")
    def get_token(self): #gibt das token zurück
        return self.__token

    def get_baseurl(self):
        return self.__baseurl
    def get_starturl(self):
        return self.__starturl
    def get_loginurl(self):
        return self.__loginurl
    def get_profilurl(self):
        return self.__profilurl
    def get_depotanalyseurl(self):
        return self.__depotanalyseurl
    def get_bilanzurl(self):
        return self.__bilanzurl

    def get_page(self, url): #navigiert zu einer bestimmten Seite unter Angabe der URL
        return self.req_session.get(url)
    def get_seiteninhalt(self, url):  # gibt Seiteninhalt einer URL zurück
        return soup(self.get_page(url).text, "html.parser")

    def get_AGListeAusAGSpiel(self):
        ausgelesen= []
        Liste = ([], [])
        ausgelesen = self.get_seiteninhalt("https://www.ag-spiel.de/index.php?section=agliste").findAll("div",{"class": "aglistentry"})
        for i in range(0, len(ausgelesen)):
            Liste[0].append(ausgelesen[i].findAll("a")[0]["href"][len(ausgelesen[i].findAll("a")[0]["href"]) - 6:len(ausgelesen[i].findAll("a")[0]["href"])])
            Liste[1].append(ausgelesen[i].text)
        return Liste

    def message_chat(self, channel, message): #ermöglicht das Schreiben einer Chatnachricht
        url = "https://www.ag-spiel.de/index.php?section=chat"
        data = {"text" : message,
            "channel_id" : channel,
            "token" : self.get_token()
                }
        self.req_session.post("https://www.ag-spiel.de/ajax_chatpost.php", data)
        #message_chat("3", "Hallo")

    def message_player(self, receiver, title, text): #versendet eine Nachricht unter Angabe eines Spieler, eines Titels und der Nachricht
        url ="https://www.ag-spiel.de/index.php?section=nachrichten_erstellen&action=send"
        data = {'User-Agent': self.get_useragent(),
                'too[]': receiver,
                'title': title,
                'message': text,
                'token': self.get_token()
                }
        self.req_session.post(url, data)
        #message_player("-HWJ-", "Titel", "Nachricht")

    def get_Notiz(self, wkn):
        return self.get_seiteninhalt("https://www.ag-spiel.de/index.php?section=depotcomment&id="+ str(wkn)).textarea.text

    def set_Notiz(self, text, wkn, NotizErsetzen):
        url = "https://www.ag-spiel.de/index.php?section=depotcomment&action=change&id=" + str(wkn)
        if NotizErsetzen == False:
            text = self.get_Notiz(wkn) + "\n" + text
        data = {'User-Agent': self.get_useragent(),
                'text': text,
                'token': self.get_token()
                }
        self.req_session.post(url, data)
        #Notiz("Test", 153062, False)
