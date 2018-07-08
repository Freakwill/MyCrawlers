#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import bs4

import base
import product


ICEBOX = "http://detail.zol.com.cn/icebox"

soup = base.url2soup(ICEBOX)

iceboxes = soup.find('ul', {'id': 'J_PicMode'})
for prod in iceboxes.find_all('li'):
    h3 = prod.find('h3')
    if h3:
        href = prod.find('a')['href']
        t = base.name_rx.match(h3.a.text.strip())

        name, description = t['name'], t['description']
        score = prod.find('span', {'class': 'score'}).text
        if not score:
            score = 0
        else:
            score = float(score)
        comment_num = prod.find('a', {'class': 'comment-num'}).text.strip()
        comment_num = int(base.digit_rx.match(comment_num)[0])
        price = prod.find('b', {'class': 'price-type'}).text
        if price.endswith('万'):
            price = int(float(base.decimal_rx.search(price)[0]) * 10000)
        else:
            price = int(price)
        p = product.Product(name, description, price, comment_num, href)
        print(p)

