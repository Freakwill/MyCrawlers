#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import bs4

import base


ZOL_CATE = "http://detail.zol.com.cn/price_cate_52.html"

soup = base.url2soup(ZOL_CATE)

brands = soup.find('div', {'class': 'mod-cate-box mod-cate-brand'})

for prod in brands.find_all('h3'):
    print(prod.text, ':')
    for brand in prod.next_elements:
        if isinstance(brand, bs4.element.Tag) and brand.name == 'div':
            for a in brand.find_all('a'):
                print(a.text, a.get('href'))
