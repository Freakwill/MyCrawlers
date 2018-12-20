#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import bs4
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


URL = "https://www.meishij.net"

def prettyDict(d):
    return '\n'.join(['%s: %s' % (k, v) for k, v in d.items()])

def prettyList(l):
    return '\n'.join(['%s. %s' % (k, a) for k, a in enumerate(l, 1)])

class Recipe(object):
    '''Recipe Class
    '''
    def __init__(self, title='', steps=[], materials={}, info={}):
        """
        Keyword Arguments:
            title {str} -- 菜名 (default: {''})
            steps {list} -- 烹饪步骤 (default: {[]})
            materials {dict} -- 用料, 主料、辅料 (default: {{}})
            info {dict} -- 信息 (default: {{}})
        """
        self.title = title
        self.info = info
        self.steps = steps
        self.materials = materials

    def __getstate__(self):
        return self.title, self.steps, self.materials, self.info

    def __getstate__(self, state):
        self.title, self.steps, self.materials, self.info = state

    def __str__(self):
        return """{title}:
==========
信息: 
{info}
----------
主料: 
{zl}
辅料: 
{fl}
----------
步骤:
{steps}
""".format(title=self.title, info=self.info, zl=prettyDict(self.materials['主料']), fl=prettyDict(self.materials['辅料']), steps=prettyList(self.steps))

    @staticmethod
    def fromURL(URL):

        options = webdriver.ChromeOptions()
        options.set_headless(headless=True)

        options.add_argument('user-agent="Mozilla/5.0"')
        driver = webdriver.Chrome(chrome_options=options)

        driver.get(URL)
        soup = bs4.BeautifulSoup(driver.page_source, "lxml")

        main = soup.find('div', {'class': 'main clearfix'})
        title = main.find('h1', {'class': 'title'}).text

        info = {li.strong.text:li.a.text for li in main.find('div', {'class': 'info2'}).find_all('li')}
        
        materials = main.find('div', {'class': 'materials'})
        materials = {m: {li.h4.a.text:li.span.text for li in div.find_all('li')} for m, div in zip(('主料', '辅料'), materials.find_all('div'))}

        method = main.find('div', {'class': 'editnew edit'})
        steps = [step.text.partition('.')[-1].strip() for step in method.find_all('div', {'class': 'content clearfix'})]
        return Recipe(title, steps, materials, info)


r = Recipe.fromURL('https://www.meishij.net/zuofa/kaliyangroupeixiangjianmantoupian.html')
print(r)
