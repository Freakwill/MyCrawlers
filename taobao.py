# _*_ coding:utf-8 _*_

import requests
import bs4
import pandas as pd
import pyparsing

# PEG grammar
title_key = pyparsing.Literal('raw_title')
price_key = pyparsing.Literal('view_price')
val = pyparsing.quotedString

class BaseAction:
    def __init__(self, tokens):
        self.tokens = tokens

class ActionKey(BaseAction):
    def __init__(self, tokens):
        super(ActionKey, self).__init__(tokens)
        self.text = tokens.key

class ActionValue(BaseAction):
    def __init__(self, tokens):
        super(ActionValue, self).__init__(tokens)
        self.text = tokens.value[1:-1]

class ActionKeyValue(BaseAction):
    def __init__(self, tokens):
        super(ActionKeyValue, self).__init__(tokens)
        self.key, self.value = tokens.key.text, tokens.value.text

    def __str__(self):
        return '%s: %s'%(self.key, self.value)

# "raw_title" | "view_price" : "***"
key = pyparsing.Suppress('"') + (title_key| price_key)('key').setParseAction(ActionKey) + pyparsing.Suppress('"')
key_val = key + pyparsing.Suppress(':') + val('value').setParseAction(ActionValue)
key_val.setParseAction(ActionKeyValue)

url = 'https://s.taobao.com/search'
def getdata(goods, page=1):
    # get data of goods
    # DataFrame:
    # title | price
    # ------------
    # ...  | ...

    data = []
    for k in range(page):
        payload = {'q':goods, 's':k*44+1, 'ie':'utf8'}
        resp = requests.get(url, params=payload)
        resp.encoding = 'utf-8'
        bs = bs4.BeautifulSoup(resp.text, 'lxml')
        s = bs.find_all('script')[7].string
        s = s.partition('=')[2]
        data0 = [t[0].value for t in key_val.searchString(s)]
        for i in range(22):
            data.append([data0[2*i], float(data0[2*i+1])])
    return pd.DataFrame(data, columns=('title', 'price'))


def comb(df_list, money=500):
    if len(df_list) == 1:
        df = df_list[0]
        return df[df['price']<=money]
    df = df_list[0]
    lst = []
    for x in df.iterrows():
        if x[1]['price'] >= money:
            continue
        rest = comb(df_list[1:], money-x[1]['price'])
        for y in rest.iterrows():
            z = x[1]['title'] + ' + ' + y[1]['title']
            p = x[1]['price'] + y[1]['price']
            lst.append([z, p])
    return pd.DataFrame(lst, columns=('title', 'price'))


if __name__ == '__main__':
    
    goods_list = input('商品: ').split(' ')
    money = int(input('预算: '))

    options = comb([getdata(goods) for goods in goods_list], money)

    for a in options.iterrows():
        print(a[1]['title'], a[1]['price'])

     

