# -*- coding: utf-8 -*-

import re
import random

import bs4
import requests


HOME = "http://www.brainyquote.com"

def tosuffix(s):
    return ''.join(c.lower() for c in s if c.isalpha())


def get_url(suffix):
    return HOME + '/' + suffix

def get_quoteList(url, filter=None):
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    quotes = soup.find('div', {'id':'quotesList'})
    quoteList = []
    for q in quotes.children:
        if isinstance(q, bs4.element.Tag):
            text = q.find('a', {'title': 'view quote'})
            author = q.find('a', {'title': 'view author'})
            if text and author:
                quote = Quote(text=text.get_text(), author=author.get_text())
                quoteList.append(quote)
    return quoteList


def get_topicList():
    url = HOME +'/topics'
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    topics = soup.find_all('div', {'class':'row bq_left'})[1]
    return [t.get_text() for t in topics.find_all('span', {'class':'topicContentName'})]

def get_PopTopicList():
    url = HOME +'/topics'
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    topics = soup.find_all('div', {'class':'row bq_left'})[1]
    return [t.get_text() for t in topics.find_all('span', {'class':'topicContentName'}) if t.next_sibling.next_sibling.name == 'img']


# class BaseSearcher filter

class Quote(object):
    '''Quote has 4 (principal) propteries
    text: the content
    topic: which topic
    author: the author of the quote
    info: info'''
    def __init__(self, text='', topic=None, author='', info=''):
        self.text = text
        self.topic = topic
        self.author = author
        self.info = info

    def __str__(self):
        return '{0:tight}'.format(self)

    def __format__(self, spec):
        if spec == 'signature':
            return ('--- ' + self.author).rjust(len(self.text))
        elif spec == 'text':
            return self.text
        elif spec == 'tight':
            return '{0.text} --- {0.author}'.format(self)
        else:
            L = len(self.text)
            return '{0:text}\n{0:signature}'.format(self)

    def __getstate__(self):
        return self.text, self.topic, self.author, self.info

    def __setstate__(self, state):
        self.text, self.topic, self.author, self.info = state


    @staticmethod
    def random(topic='', author='', index=''):
        pass

    @staticmethod
    def find(topic='', author='', index=''):
        pass

    @staticmethod
    def fromTag(tag):
        text = tag.find('a', {'title': 'view quote'})
        author = tag.find('a', {'title': 'view author'})
        return Quote(text=text.get_text(), author=author.get_text())

    @staticmethod
    def today(topic=None):
        url = 'https://www.brainyquote.com/quote_of_the_day'
        response = requests.get(url)
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        if topic:
            quote_of_the_day = topic.capitalize() + ' ' + 'Quote of the Day'
        else:
            quote_of_the_day = 'Quote of the Day'
        def f(tag):
            return tag.find('h2', {'class':'qotd-h2'}) and tag.find('h2', {'class':'qotd-h2'}).get_text() == quote_of_the_day
        return Quote.fromTag(soup.find(f))


