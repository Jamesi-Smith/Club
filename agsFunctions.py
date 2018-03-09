# -*- coding: utf-8 -*-
from login import *
from bs4 import BeautifulSoup as soup
import datetime

def wkns():
    page_soup = soup(get_page("https://www.ag-spiel.de/index.php?section=agliste").text, "html.parser")

    wkn_list = []
    for i in page_soup.findAll("a"):
        if "index.php?section=profil&amp;aktie=" in str(i) and 'newMessageCounter' not in str(i):
            wkn = str(i).replace('<a href="index.php?section=profil&amp;aktie=',"")
            wkn = wkn.split('"')[0]
            if str(wkn).isdigit() == True:
                wkn_list.append(wkn)
            else:
                i = i
        else:
            i = i

    wkn_list = list(set(wkn_list))
    wkn_list = sorted(wkn_list, reverse=True)
    return wkn_list

def profileCrawler():
    wkn_list = wkns()
    all_profiles = []

    l = len(wkn_list)
    i = 0
    while i < l:
        # Seite parsen
        data = get_page("https://www.ag-spiel.de/index.php?section=profil&aktie=" + wkn_list[i]).text

        # Prüfen ob AG i.L. ist oder nicht mehr Eingeloggt
        if "index.php?section=register" in str(data):
            time.sleep(15)
            ags_login()
            data = get_page("https://www.ag-spiel.de/index.php?section=profil&aktie=" + wkn_list[i]).text
        elif "erloschen auf AG-Spiel.de" in str(data):
            print "Eine erloschene AG wurde entdeckt!"
            i = i + 1
        elif "Sie müssen sich registrieren" in str(data):
            time.sleep(15)
            ags_login()
            data = get_page("https://www.ag-spiel.de/index.php?section=profil&aktie=" + wkn_list[i]).text

        player_page = soup(data, "html.parser")

        all_profiles.append([wkn_list[i],kurs14d(player_page),alter_grob(player_page),bw_gesamt(player_page),bar_gesamt(player_page),bw_aktie(player_page),agsx_points(player_page),sw_aktie(player_page),ksd(player_page),spread(player_page),aktivitaet(player_page),kurs_aktuell(player_page),bw_14(player_page),bw_30(player_page),bw_60(player_page),bw_90(player_page),sw_14(player_page),sw_30(player_page),sw_60(player_page),sw_90(player_page),ag_gruendung(player_page),aktien_zahl(player_page),dividende(player_page),zertifikate_volumen(player_page),uebernahmeschutz(player_page)])

        #print all_profiles
        #print all_profiles[i]

        print l - i
        time.sleep(1)
        i = i + 1
    return all_profiles

def onlineNewLiq():
    stats_page = soup(get_page("https://www.ag-spiel.de/index.php?section=statistiken").text , "html.parser")
    suppe = stats_page.find("table", {"class": "menu2"})

    menu2 = []
    for tabellen in suppe.findAll("tr"):
        menu2.append(tabellen)

    count = 0
    newAG_list = []
    online_list = []
    playerGes_list = []
    date = datetime.datetime.today().strftime('%Y-%m-%d')
    alleDaten = {"Neu24": "", "Online24": "", "I.L.24": "", "Datum":"","PlayerGesamt":""}

    while count < len(menu2):
        if "neue AGs" in str(menu2[count]):
            newAG = menu2[count]
            for tds in newAG.findAll("td"):
                newAG_list.append(tds)
            alleDaten["Neu24"] = int(newAG_list[1].text)
        elif "24 Std. online" in str(menu2[count]):
            online = menu2[count]
            for tdf in online.findAll():
                online_list.append(tdf)
            alleDaten["Online24"] = int(online_list[1].text)
        elif "AGs am Markt" in str(menu2[count]):
            playerGes = menu2[count]
            for tdp in playerGes.findAll():
                playerGes_list.append(tdp)
            alleDaten["PlayerGesamt"] = int(playerGes_list[1].text.replace(".",""))
        else:
            count = count
        count +=1
    tab_Allgemeines = stats_page.find("td", {"style":"padding-right: 20px;"})
    tab_Allgemeines = tab_Allgemeines.text.split("Liquidationen: ")
    alleDaten["I.L.24"] = int(tab_Allgemeines[1].split("\n")[0])
    alleDaten["Datum"] = date

    return alleDaten

def agName(profile):
    name = profile.find("title").text.replace(" auf AG-Spiel.de","")
    return name

def kurs14d(profile):
    kurs14 = profile.find("div", {"id": "kurs14d"}).text.replace("\n", "").replace("Kurs 14d", "").replace(" ","").replace("%", "").replace(",", ".")
    return kurs14

def alter_grob(profile):
    alter = profile.find("div", {"id": "agalter"}).text.replace("\n", "").replace("Alter", "").replace(",",".").replace(" ", "")
    if "Tage" in str(alter):
        alter = alter.replace("Tage", "")
    elif "Jahre" in str(alter):
        alter = alter.replace("Jahre", "")
        alter = float(alter) * 365
    elif "Min." in str(alter):
        alter = alter.replace("Min.", "")
        alter = 0
    else:
        alter = 0
    return alter

def bw_gesamt(profile):
    tr_list = []
    tabelle_TB = profile.find("table", {"id": "tagesBilanz"}).tbody.tr
    for r in tabelle_TB.findAll("td"):
        tr_list.append(r)
    bw_ges = int(tr_list[3].text.replace(".", "").replace("€", ""))
    return bw_ges

def bar_gesamt(profile):
    tr_list = []
    tabelle_TB = profile.find("table", {"id": "tagesBilanz"}).tbody.tr
    for r in tabelle_TB.findAll("td"):
        tr_list.append(r)
    bar_ges = int(tr_list[2].text.replace(".", "").replace("€", ""))
    return bar_ges

def bw_aktie(profile):
    tr_list = []
    tabelle_TB = profile.find("table", {"id": "tagesBilanz"}).tbody.tr
    for r in tabelle_TB.findAll("td"):
        tr_list.append(r)
    bw = float(tr_list[5].text.replace("€", "").replace(".", "").replace(",", "."))
    return bw

def agsx_points(profile):
    agsxP = int(profile.find("div", {"id": "agsxp"}).text.replace("AGSX-P.", "").replace("\n", "").replace(" ", "").replace("(?)", "").replace(".", ""))
    return agsxP

def sw_aktie(profile):
    sw = float(profile.find("div", {"id": "sw"}).text.replace("SW/Aktie", "").replace("€", "").replace("\n", "").replace(" ", "").replace("(?)", "").replace(".", "").replace(",", "."))
    return sw

def ksd(profile):
    KSD = profile.find("div", {"id": "ksd"}).text.replace("KSD ", "").replace("%", "").replace("\n", "").replace(" ", "").replace("(?)", "").replace("KSD", "").replace(".", "").replace(",", ".")
    return KSD

def spread(profile):
    SPREAD = profile.find("div", {"id": "spread"}).text.replace(" ", "").replace("\n", "").replace("Spread","").replace("(?)","").replace("%", "")
    return SPREAD

def aktivitaet(profile):
    ha = int(profile.find("div", {"id": "handelsaktivität"}).text.replace(" ", "").replace("\n", "").replace("(?)","").replace("Aktivität", "").replace("%", ""))
    return ha

def kurs_aktuell(profile):
    kurs_suppe = profile.find("div", {"id": "handelskurs"})
    kurs_tab = []
    for g in kurs_suppe.findAll("span"):
        kurs_tab.append(g)
    kurs = float(
        kurs_tab[0].text.replace("<span style='font-size:130%' >", "").replace("€", "").replace("\n", "").replace(" ","").replace(".", "").replace(",", "."))
    return kurs

def bw_14(profile):
    performance_tabelle = profile.find("table", {"class": "normalborder"})
    perf_tab = []
    for f in performance_tabelle.findAll("tr"):
        perf_tab.append(f)
    bw14 = perf_tab[1].findAll("td")[2].text.replace("%", "").replace(".", "").replace(",", ".").replace(" ", "")
    if not any(char.isdigit() for char in str(bw14)):
        bw14 = "n/a"
    else:
        bw14 = bw14
    return bw14

def bw_30(profile):
    performance_tabelle = profile.find("table", {"class": "normalborder"})
    perf_tab = []
    for f in performance_tabelle.findAll("tr"):
        perf_tab.append(f)
    bw30 = perf_tab[2].findAll("td")[1].text.replace("%", "").replace(".", "").replace(",", ".").replace(" ", "")
    if not any(char.isdigit() for char in str(bw30)):
        bw30 = "n/a"
    else:
        bw30 = bw30
    return bw30

def bw_60(profile):
    performance_tabelle = profile.find("table", {"class": "normalborder"})
    perf_tab = []
    for f in performance_tabelle.findAll("tr"):
        perf_tab.append(f)
    bw60 = perf_tab[3].findAll("td")[1].text.replace("%", "").replace(".", "").replace(",", ".").replace(" ", "")
    if not any(char.isdigit() for char in str(bw60)):
        bw60 = "n/a"
    else:
        bw60 = bw60
    return bw60

def bw_90(profile):
    performance_tabelle = profile.find("table", {"class": "normalborder"})
    perf_tab = []
    for f in performance_tabelle.findAll("tr"):
        perf_tab.append(f)
    bw90 = perf_tab[4].findAll("td")[1].text.replace("%", "").replace(".", "").replace(",", ".").replace(" ", "")
    if not any(char.isdigit() for char in str(bw90)):
        bw90 = "n/a"
    else:
        bw90 = bw90
    return bw90

def sw_14(profile):
    performance_tabelle = profile.find("table", {"class": "normalborder"})
    perf_tab = []
    for f in performance_tabelle.findAll("tr"):
        perf_tab.append(f)
    sw14 = perf_tab[6].findAll("td")[2].text.replace("%", "").replace(".", "").replace(",", ".").replace(" ", "")
    if not any(char.isdigit() for char in str(sw14)):
        sw14 = "n/a"
    else:
        sw14 = sw14
    return sw14

def sw_30(profile):
    performance_tabelle = profile.find("table", {"class": "normalborder"})
    perf_tab = []
    for f in performance_tabelle.findAll("tr"):
        perf_tab.append(f)
    sw30 = perf_tab[7].findAll("td")[1].text.replace("%", "").replace(".", "").replace(",", ".").replace(" ", "")
    if not any(char.isdigit() for char in str(sw30)):
        sw30 = "n/a"
    else:
        sw30 = sw30
    return sw30

def sw_60(profile):
    performance_tabelle = profile.find("table", {"class": "normalborder"})
    perf_tab = []
    for f in performance_tabelle.findAll("tr"):
        perf_tab.append(f)
    sw60 = perf_tab[8].findAll("td")[1].text.replace("%", "").replace(".", "").replace(",", ".").replace(" ", "")
    if not any(char.isdigit() for char in str(sw60)):
        sw60 = "n/a"
    else:
        sw60 = sw60
    return sw60

def sw_90(profile):
    performance_tabelle = profile.find("table", {"class": "normalborder"})
    perf_tab = []
    for f in performance_tabelle.findAll("tr"):
        perf_tab.append(f)
    sw90 = perf_tab[9].findAll("td")[1].text.replace("%", "").replace(".", "").replace(",", ".").replace(" ", "")
    if not any(char.isdigit() for char in str(sw90)):
        sw90 = "n/a"
    else:
        sw90 = sw90
    return sw90

def ag_gruendung(profile):
    infos = profile.find("table", {"class": "padding5"})
    weitere_infos = []
    for da in infos.findAll("td"):
        weitere_infos.append(da)
    AG_grundung = weitere_infos[3].text
    return AG_grundung

def aktien_zahl(profile):
    infos = profile.find("table", {"class": "padding5"})
    weitere_infos = []
    for da in infos.findAll("td"):
        weitere_infos.append(da)
    anzahl = int(weitere_infos[5].text.replace(" ", "").replace("Stk.", "").replace(".", ""))
    return anzahl

def dividende(profile):
    infos = profile.find("table", {"class": "padding5"})
    weitere_infos = []
    for da in infos.findAll("td"):
        weitere_infos.append(da)
    divi = int(weitere_infos[7].text.replace("%", ""))
    return divi

def zertifikate_volumen(profile):
    infos = profile.find("table", {"class": "padding5"})
    weitere_infos = []
    for da in infos.findAll("td"):
        weitere_infos.append(da)
    zerti_vol = float(weitere_infos[9].text.split("%")[0])
    return zerti_vol

def uebernahmeschutz(profile):
    infos = profile.find("table", {"class": "padding5"})
    weitere_infos = []
    for da in infos.findAll("td"):
        weitere_infos.append(da)
    ue = weitere_infos[17].text
    return ue

def median(list):
    sortedLst = sorted(list)
    lstLen = len(list)
    index = (lstLen - 1) // 2
    if (lstLen % 2):
        return sortedLst[index]
    else:
        return (sortedLst[index] + sortedLst[index + 1])/2.0

def mittelwert(list):
    return sum(list) / float(len(list))

def pushDictList(oldList, neuerWert):
    newList = []
    x = 0
    while x < len(oldList):
        newList.append(oldList[x])
        x +=1
    newList.append(neuerWert)
    return newList

def sw_gesamt(swAktie, AktienZahl):
    return swAktie * AktienZahl

def boersenwert(kursAktie, AktienZahl):
    return kursAktie * AktienZahl

def depotwert(profile):
    tr_list = []
    tabelle_TB = profile.find("table", {"id": "tagesBilanz"}).tbody.tr
    for r in tabelle_TB.findAll("td"):
        tr_list.append(r)
    depot_volumen = float(tr_list[1].text.replace(".", "").replace("€", ""))
    return depot_volumen

def aktien(profile):
    jsData = profile.findAll("script", {"type": "text/javascript"})[18].text.split("[")
    aktienVol = float(jsData[4].split(",")[1].replace("]", ""))
    return aktienVol

def anleihen(profile):
    jsData = profile.findAll("script", {"type": "text/javascript"})[18].text.split("[")
    anleihe = float(jsData[5].split(",")[1].replace("]",""))
    return anleihe

def zertifikate(profile):
    jsData = profile.findAll("script", {"type": "text/javascript"})[18].text.split("[")
    zertis = float(jsData[6].split(",")[1].split("]")[0])
    return zertis

def eigenkapital(profile):
    jsData = profile.findAll("script", {"type": "text/javascript"})[17].text.split("[")
    eigenKap = float(jsData[3].split(",")[1].replace("]",""))
    return eigenKap

def fremdkapital(profile):
    jsData = profile.findAll("script", {"type": "text/javascript"})[17].text.split("[")
    fremdKap = float(jsData[4].split(",")[1].split("]")[0])
    return fremdKap

def indexWkns(IndexURL):
    page_soup = soup(get_page(IndexURL).text, "html.parser").findAll("tr")
    del page_soup[0]
    index_wkns = []
    del page_soup[0]
    for i in page_soup:
        urls = i.find("a")
        if '<a href="index.php?section=profil&amp;aktie=' in str(urls):
            if ":" in str(urls.text):
                urls = int(urls.text.split(":")[0])
                if type(urls) == int:
                    index_wkns.append(str(urls))
    return index_wkns

def order(wkn, order, quantity, limit):
    url = 'https://www.ag-spiel.de/index.php?section=agorderbuch&action=create&ele='
    token = soup(get_page(url).text, "html.parser").find("input", {"name":"token"}).get("value")
    data = {'User-Agent': user_agent,
            'token': token,
            'aktie': wkn,
            'order': order,
            'anzahl': quantity,
            'limit': limit
            }
    return url, data
#ags_login()
#print(req_session.post(order('140025', 'buy', '1', '259')[0], data=order('140025', 'buy', '1', '259')[1]).text)

def Nachricht(receiver, title, text):
    url = "https://www.ag-spiel.de/index.php?section=nachrichten_erstellen&action=send"
    token = soup(get_page(url).text, "html.parser").find("input", {"name": "token"}).get("value")
    data = {'User-Agent': user_agent,
            'token': token,
            'too[]': receiver,
            'title': title,
            'message': text,
            }
    return url, data
#ags_login()
#print(req_session.post(Nachricht('-HWJ-', 'Test', "Inhalt")[0], data=Nachricht('-HWJ-', 'Test', "Inhalt")[1]))

#Channel 1 = AGS, 2 = Handelsparkett, 3 = Index, 4 = Off-Topic
def chat_message(channel, message):
    url = "https://www.ag-spiel.de/index.php?section=chat"
    data = {"text": message,
            "channel_id": channel,
            "token": soup(get_page(url).text, "html.parser").find("input", {"name": "token"}).get("value")
            }
    req_session.post("https://www.ag-spiel.de/ajax_chatpost.php", data)
