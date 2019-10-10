#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
A Crawler for baidupedia

Just use yaml to dump the object

Example:
item = BaiduItem.get('杨幂')
print(item.summary)
# other properties: 'basic_info', 'content', 'catalog', 'polysement', 'references'
"""

from dataclasses import *
from treelib import Node, Tree

from bs4 import BeautifulSoup
import requests

BAIKE_URL = 'https://baike.baidu.com'
ITEM_URL = BAIKE_URL + '/item'

try:
    from fake_useragent import UserAgent
    ua = UserAgent(verify_ssl=False)
    header_dict = {'User-Agent': ua.random}
except:
    header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) Gecko/20100101 Firefox/57.0'}

def get_content(bs):
    content = bs.find('div', {'class':'main-content'})
    s = ''
    for div in content.find_all('div'):
        if div.has_attr('class'):
            if div['class'][0] == 'para-title':
                if div.span:
                    div.span.decompose()
                if div.a:
                    div.a.decompose()
                title = div.text.strip()
                s += '\n' + title + '\n'
            elif div['class'][0] == 'para':
                text = div.text.strip().replace('\n', '')
                s += text + '\n'
    return s

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
    tree = Tree()
    tree.create_node('目录', 0)
    for li in catalog.find_all('li'):
        if li['class'][0] == 'level1':
            title = li.text.lstrip('1234567890\n ').rstrip()
            tree.create_node(title, title, parent=0, data=li.a['href'])
            current = title
        elif li['class'][0] == 'level2':
            subtitle = li.find('span', {'class':'text'}).text
            tree.create_node(subtitle, parent=current, data=li.a['href'])
    return tree

def get_polysement(bs):
    polysement = bs.find('ul', {'class':'polysemantList-wrapper'})
    if polysement:
        return [item.a.text for item in polysement.find_all('li') if item.a]


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
    '''Class for keeping track of an item in inventory.
    Properties:
        'summary', 'basic_info', 'content', 'catalog', 'polysement', 'references'

    Example:
    item = BaiduItem.get('杨幂')

    print(item.catalog)
    print(item.summary)
    '''

    name: str = ''
    summary: float = ''
    basic_info: dict = field(default_factory=dict)
    content: str = ''
    catalog: str = ''
    polysement: str = ''
    references: list = field(default_factory=list)

    props = ('summary', 'basic_info', 'content', 'catalog', 'polysement', 'references')

    def __str__(self):
        return f'{self.name}:\n{self.summary}'

    @staticmethod
    def get(name):
        item = BaiduItem(name)
        bs = _bs(name)
        G = globals()
        for p in BaiduItem.props:
            setattr(item, p, G['get_'+p](bs))
        return item

    def __setstat__(self, stat):
        self.name = stat['name']
        for p in BaiduItem.props:
            getattr(self, stat[p])

 
if __name__ == '__main__':
    item = BaiduItem.get('杨幂')
    print(item.content)
