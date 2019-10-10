#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import bs4
import requests
import urllib.request as ur

#############
 
URL = "https://www.meizitu.com/"
response = requests.get(URL)

soup = bs4.BeautifulSoup(response.text, 'lxml')

for k,a in enumerate(soup.find_all('img')):
    if a.has_attr('src'):
        image = a['src']
        # name = image.split('/')[-1]
        # print('loading', name)
        try:
            ur.urlretrieve(a['src'], 'images/%d.jpg' %k)
        except:
            pass
