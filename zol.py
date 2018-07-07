#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import re

import base


ZOL_HOME = "http://detail.zol.com.cn"

soup = base.url2soup(ZOL_HOME)

category = soup.find('div', {'class':'category-nav'})
for a in category.find_all('a'):
    print(a.text)


def f(tag):
    return tag.name == 'div' and tag.has_attr('class') and len(tag.get('class')) ==2 and \
    tag.get('class')[0] == 'section' and tag.get('class')[1].startswith('floor')

for floor in soup.find_all(f):
    klass = floor.find('strong')

    hot = floor.find('div', {'class':'hot-search'})
    print(klass.text, ':')
    for a in hot.find_all('a'):
        print(a.text)