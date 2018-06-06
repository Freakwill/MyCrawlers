#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests

BAIKE_URL = 'https://baike.baidu.com'
ITEM_URL = BAIKE_URL + '/item'

header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) Gecko/20100101 Firefox/57.0'}

url = ITEM_URL + '/Python'
resp = requests.get(url, headers=header_dict)
bs = BeautifulSoup(resp.content.decode('utf-8'), "lxml")
summary = bs.find('div', {'class':'lemma-summary'})
print(summary.text)