#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import re
import bs4
import pandas as pd

import base
import product


name_rx = re.compile(r'(?P<name>\w+ ?\w+((-|\/)\w+)*)(?P<anothername>\(|（\w+(\)|）)?)? *(?P<description>\w+)')

HOME = "http://detail.zol.com.cn"


class IceBoxes(product.Product):

    pages = 15

    @staticmethod
    def read_url():
        iceboxes = []
        for k in range(1, pages):

            ICEBOX = HOME + "/icebox/%d.html" % k
            try:
                soup = base.url2soup(ICEBOX)
            except:
                break

            prods = soup.find('ul', {'id': 'J_PicMode'})
            for prod in prods.find_all('li'):
                h3 = prod.find('h3')
                if h3:
                    href = prod.find('a', {'class': 'pic'})['href']
                    t = name_rx.match(h3.a.text.strip())
                    name, description = t['name'], t['description']
                    score = prod.find('span', {'class': 'score'}).text
                    if score.isdigit():
                        score = float(score)
                    else:
                        score = 0
                    comment_num = prod.find('a', {'class': 'comment-num'}).text.strip()
                    comment_num = int(base.digit_rx.match(comment_num)[0])
                    price = prod.find('b', {'class': 'price-type'}).text
                    if price.endswith('万'):
                        price = int(float(base.decimal_rx.search(price)[0]) * 10000)
                    elif price.isdigit():
                        price = int(price)
                    else:
                        continue
                    p = product.Product(name, description, price, comment_num, href)
                    soup2 = base.url2soup(HOME + p.href)
                    a = soup2.find('a', {'class': '_j_MP_more section-more'})
                    soup2 = base.url2soup(HOME + a.get('href'))
                    paras = soup2.find('div', {'class': 'detailed-parameters'})
                    p.parameter = {para.find('th').text:para.find('td').find('span').text
                    for table in paras.find_all('table')[:-1] for para in table.find_all('tr')[1:]}
                    iceboxes.append(p)
        return iceboxes


iceboxes = IceBoxes.read_url()
df =pd.DataFrame([p.toDict() for p in iceboxes])
df.to_excel('iceboxes.xls')

