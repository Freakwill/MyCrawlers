# -*- coding: utf-8 -*-

import re
import random

import bs4
import requests
import furl


HOME = furl.furl("http://www.brainyquote.com")

# def tosuffix(s):
#     return ''.join(c.lower() for c in s if c.isalpha())
TOPICS = ['Motivational', 'Friendship', 'Love', 'Smile', 'Life', 'Inspirational', 'Family', 'Nature', 'Positive', 'Attitude']


def get_quoteList(url, filter=None):
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, "lxml")
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
    url = HOME / 'topics'
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, "lxml")
    topics = soup.find_all('div', {'class':'row bq_left'})[1]
    return [t.get_text() for t in topics.find_all('span', {'class':'topicContentName'})]

def get_PopTopicList():
    url = HOME / 'topics'
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, "lxml")
    topics = soup.find_all('div', {'class':'row bq_left'})[1]
    return [t.get_text() for t in topics.find_all('span', {'class':'topicContentName'}) if t.next_sibling.next_sibling.name == 'img']


def get_authorList():
    # get the list of authors
    url = HOME / 'authors'
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, "lxml")
    return [t.text.strip() for t in soup.find_all('span', {'class':'authorContentName'})]


# class BaseSearcher filter

class Quote(object):
    '''Quote class
    
    Quotes of famous peaple

    Example
    -------
    >>> q = Quote.today()
    >>> print(q)   # 2018-10-25
    >>> He that lives upon hope will die fasting. --- Benjamin Franklin
    '''
    def __init__(self, text='', topic='', author='', info=''):
        '''
        Keyword Arguments:
            text {str} -- [content of the quote] (default: {''})
            topic {str} -- [topic of the quote] (default: {''})
            author {str} -- [the author] (default: {''})
            info {str} -- related information (default: {''})
        '''
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
        return random.choice(Quote.find_all(topic, author, index))

    @staticmethod
    def find(topic='', author='', index=''):
        pass

    @staticmethod
    def find_all(topic='', author='', index=''):
        pass

    @staticmethod
    def fromTag(tag):
        text = tag.find('a', {'title': 'view quote'})
        author = tag.find('a', {'title': 'view author'})
        return Quote(text=text.get_text(), author=author.get_text())

    @staticmethod
    def today(topic=None):
        # get today quote
        url = HOME / 'quote_of_the_day'
        response = requests.get(url)
        soup = bs4.BeautifulSoup(response.text, "lxml")
        container = soup.find('div', {'class': 'container bqQOTD'})

        if isinstance(topic, str):
            quote_of_the_day = [topic.capitalize()]
        elif isinstance(topic, (tuple, list, set)):
            quote_of_the_day = [t.capitalize() for t in topic]
        else:
            quote_of_the_day = ['']
        def f(tag):
            try:
                t = tag.find('h2', {'class':'qotd-h2'}).text.partition('Quote of the Day')[0]
                return t in quote_of_the_day
            except:
                pass
        return Quote.fromTag(container.find(f))


