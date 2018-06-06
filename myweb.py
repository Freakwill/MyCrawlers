# -*- coding: utf-8 -*-

'''web programming with python
example:
    import urllib.request as ur

    url='www.baidu.com'
    myurl=ur.urlopen(url)     # open url
    page=myurl.read()         # read web page
    page=page.decode('utf-8') # decode what is read
    url.close()               # close
'''

import urllib.request as ur
from urllib.parse import urlparse
from os.path import *
import re
import bs4


baidu="http://www.baidu.com"
wiki="https://en.wikipedia.org/wiki/Modulation_space"


def urlread(url, dec='utf-8'):
    ''' url is Uniform Resoure Locator
    '''
    with ur.urlopen(url) as myurl:
        page = myurl.read()
    if dec:
        page = page.decode(dec) # turn to str
    return page

'''
def urlheader(url):
    # header of url
    return ur.urlopen(url).info()
'''

def url2file(url, file, dec='utf-8'):
    ''' input:
        url
        file is a filename (with extension)
    '''
    # open and read
    page = ur.urlopen(url).read()
    url.close()
    if dec:
        page = page.decode(dec) # turn to str
        fo = open(file,"w")  #
    else:
        fo = open(file,"wb") # with open(file,'wb') as fo:

    # save as file
    fo.write(page)
    fo.close()


def urlsave(url, file='myfile'):
    ''' example:
          >>> target=baidu
          >>> urlsave(target)
    '''
    url2file(url, file+'.html', False)


def urlfind(url, rx, dec='utf-8'):
    ''' url: a web page
        pattern: a regular expression in the page
        dec: the decoding method (look for <meta charset=.../>)

        example: get title of target
          >>> string='<title>(.+?)</title>'
          >>> A=urlfind(baidu,string)
          >>> A
          ['百度一下，你就知道']
    '''
    # open and read
    page = urlread(url, dec) # turn to str
    # find a string in the page
    if isinstance(rx, str):
       rx=re.compile(rx)
    return rx.findall(page)


from chardet.universaldetector import UniversalDetector
def urlcode(url):
    '''
    example:
    urlcode('http://www.baidu.com')
    '''
    url = ur.urlopen(url)
    # create a detector
    detector = UniversalDetector()
    for line in url.readlines():
        detector.feed(line)
        if detector.done:
            break
    # close
    detector.close()
    url.close()
    # output the result
    return detector.result

'''
def urlcode(target,dec='utf-8'):

    url=ur.urlopen(target)
    page=url.read()
    if dec:
        page=page.decode(dec)
    r=re.compile('<meta[^>]+charset=([^\s";]+)')
    return r.findall(page)[0]
'''

def url2filename(url,defname='index.htm'):
    p=urlparse(url)
    path=p[1]+p[2]
    ext=splitext(path)
    if ext[1] =='':
        if path[-1]=='/':
            path+=defname
        else:
            path+='/'+defname
    return path



string='<title>(.+?)</title>'
A=urlfind(baidu,string)
print(A)