# -*- coding: utf-8 -*-
"""
Created on Sun Aug 09 18:07:01 2015

"""

import requests
from pyquery import PyQuery as pq
from bs4 import BeautifulSoup
import hashlib
import time
#import MySQLdb as mdb
import sys
from data import *

BASE_URL = 'https://www.ag-spiel.de'
LOGIN_URL = 'https://www.ag-spiel.de/index.php?section=login'
PROFIL_BASE_URL = 'https://www.ag-spiel.de/index.php?section=profil&aktie='
DEPOTANALYSE_URL = 'https://www.ag-spiel.de/index.php?section=depotanalyse&aktie='
BILANZ_URL = 'https://www.ag-spiel.de/index.php?section=bilanzen&wkn='
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.'

login_data = {
    'User-Agent': user_agent,
    'username': USER,
    'userpass': PASSWORD,
    'permanent': '1',
    'login': 'Einloggen',
}

req_session = requests.Session()


def ags_login():
    # Einloggen, Startsektion besuchen.
    req_session.post(LOGIN_URL, data=login_data)
    req_session.get('https://www.ag-spiel.de/index.php?section=start')
    return None


def get_page(url):
    resp = req_session.get(url)
    return resp


def get_token():
    start_page = pq(
        get_page('https://www.ag-spiel.de/index.php?section=agorderbuch').content)
    soup = BeautifulSoup(str(start_page))
    soup = soup.findAll('input', {'name': 'token'})[0]
    soup = str(soup)
    soup = soup.replace('<input type="hidden" value="', '')
    soup = soup.replace('" name="token" />', '')
    # token = soup.find('input', {'name': 'token'})['value']

    return soup


def post_indexforum(thread, text, token):
    url = 'https://www.ag-spiel.de/index.php?section=thread&thread=' + thread + '&action=newpost'
    data = {'User-Agent': user_agent,
            'text': text,
            'token': token,
            }

    req_session.post(url, data)