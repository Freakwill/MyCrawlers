# -*- coding: utf-8 -*-

import time
import pathlib

import requests
import urllib.request as ur

from PIL import Image, ImageEnhance
import pytesseract
import bs4

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

import pandas as pd

url = r'http://10.248.7.35/WFManager/login.jsp'

options = Options()
if False:
    options.set_headless(headless=True)
driver = webdriver.Chrome(executable_path='/usr/local/Caskroom/chromedriver/2.40/chromedriver', chrome_options=options)
driver.get(url)

driver.implicitly_wait(5)

username = driver.find_element_by_name('textfield')
password = driver.find_element_by_name('textfield2')
username.send_keys('800052')
password.send_keys('800052')

checkcode = driver.find_element_by_name('textfield3')
button = driver.find_element_by_id('loginbtn2')

pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'

while True:
    driver.save_screenshot("a.png")
    imgelement = driver.find_element_by_id('checkcodeImg')
    coderange = (1845, 645, 1845+138, 645+42) #写成我们需要截取的位置坐标

    im = Image.open("a.png")    # 打开截图
    c = im.crop(coderange)      # 使用Image的crop函数，从截图中再次截取我们需要的区域
    c.save("checkcode.png")
    im2 = Image.open("checkcode.png")
    sharpness = ImageEnhance.Contrast(im2.convert('L'))  # 对比度增强
    im3 = sharpness.enhance(2.0)  # 3.0为图像的饱和度
    im3.save("checkcode.png")

    cc = pytesseract.image_to_string(Image.open('checkcode.png')).strip()
    cc = ''.join(c for c in cc if c.isdigit())[:4]

    checkcode.send_keys(cc)
    button.click()
    try:
        button = driver.find_elements(by=By.CLASS_NAME, value='syslink')[1]
        button.click()
        break
    except:
        checkcode.clear()

driver.switch_to_frame(driver.find_element_by_xpath('//*[@id="WF_CWBS"]/iframe'))

button = driver.find_element_by_partial_link_text('我的到款查询')
button.click()

# button = driver.find_element_by_xpath('//*[@id="leftMenu"]/ul/li[2]/ul/li[1]')
button = driver.find_element_by_partial_link_text('个人工资查询')
button.click()

select = Select(driver.find_element_by_xpath('//*[@id="formWF_CWBS_5574_d-funcno"]'))
item = '工资'
value = {'工资':'2', '党费':'4'}[item]
select.select_by_value(value)
select = Select(driver.find_element_by_xpath('//*[@id="formWF_CWBS_5574_d-year"]'))
year='2018'
select.select_by_value(year)
select = Select(driver.find_element_by_xpath('//*[@id="formWF_CWBS_5574_d-month_1"]'))
fromMonth='01'
select.select_by_value(fromMonth)
select = Select(driver.find_element_by_xpath('//*[@id="formWF_CWBS_5574_d-month_2"]'))
toMonth='07'
select.select_by_value(toMonth)

button = driver.find_element_by_xpath('//*[@id="foot_winWF_CWBS_5609"]/button')
button.click()

soup = bs4.BeautifulSoup(driver.page_source, 'lxml')
table = soup.find('div', {'id':'winWF_CWBS_6240'})
title = table.find('span', {'id':'winWF_CWBS_6240_title'}).text
labels = table.find('tr', {'class':'ui-jqgrid-labels'})
ths = labels.find_all('th')
index = pd.Index([th.text for th in ths[1:] if th.text], name='Date')
 

time.sleep(2)
body = table.find('tbody')
print(body)
data = {}
for tr in body.find_all('tr', {'role':'row'})[1:]:
    tds = [td.text for td in tr.find_all('td')]
    data.update({tds[0]:tds[1:]})
    print(tds)

df = pd.DataFrame(data, index=index)

print(df)