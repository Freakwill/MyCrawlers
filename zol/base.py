#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import re
import requests
import bs4

digit_rx = re.compile(r'\d+')
decimal_rx = re.compile(r'\d+(\.\d+)?')
page_rx = re.compile(r'\d/(\d+)')

# print(name_rx.match('heeh 232-kk/sss lili')['name'])

def url2soup(url):
    # url -> soup
    response = requests.get(url)
    if response.encoding == 'ISO-8859-1':
        encodings = requests.utils.get_encodings_from_content(response.text)
        if encodings:
            encoding = encodings[0]
        else:
            encoding = response.apparent_encoding
    encode_content = response.content.decode(response.encoding, 'replace')
    return bs4.BeautifulSoup(encode_content, "html.parser")


def extract(rx, s):
    return rx.search(s)[0]