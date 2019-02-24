#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from dataclasses import *

from bs4 import BeautifulSoup
import requests
import fake_useragent

BAIKE_URL = 'https://baike.baidu.com'
ITEM_URL = BAIKE_URL + '/item'

try:
    from fake_useragent import UserAgent
    ua = UserAgent()
    header_dict = {'User-Agent': ua.chrome}
except:
    header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) Gecko/20100101 Firefox/57.0'}


def get_content(bs):
    content = bs.find('div', {'class':'main-content'})
    return content.text

def get_summary(bs):
    summary = bs.find('div', {'class':'lemma-summary'})
    return summary.text

def get_basic_info(bs):
    info = bs.find('div', {'class':'basic-info cmn-clearfix'})
    keys = info.find_all('dt')
    values = info.find_all('dd')
    return {k.text.replace('\xa0', ''):v.text.strip() for k, v in zip(keys, values)}

def get_catalog(bs):
    catalog = bs.find('div', {'class':'lemma-catalog'})
    return catalog.text

def get_polysement(bs):
    polysement = bs.find('div', {'class':'polysemantList-wrapper cmn-clearfix'})
    if polysement:
        return polysement.text


def get_references(bs):
    references = bs.find('ul', {'class':'reference-list'})
    if references:
        return [reference.text.strip() for reference in references.find_all('li')]
    else:
        return []


def _bs(name:str)->BeautifulSoup:
    url = ITEM_URL + '/%s' % name
    resp = requests.get(url, headers=header_dict)
    return BeautifulSoup(resp.content.decode('utf-8'), "lxml")


@dataclass
class BaiduItem:
    '''Class for keeping track of an item in inventory.'''
    name: str = ''
    summary: float = ''
    basic_info: dict = field(default_factory=dict)
    content: str = ''
    catalog: str = ''
    polysement: str = ''
    references: list = field(default_factory=list)

    def __str__(self):
        return f'{self.name}: {self.summary}'

    @staticmethod
    def get(name):
        item = BaiduItem(name)
        bs = _bs(name)
        G = globals()
        for p in ('summary', 'basic_info', 'content', 'catalog', 'polysement', 'references'):
            setattr(item, p, G['get_'+p](bs))
        return item



if __name__ == '__main__':
    item = BaiduItem.get('百度百科')

    print(item.references)