#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

DOUBAN_MOVIE_URL = 'https://movie.douban.com'

header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) Gecko/20100101 Firefox/57.0'}

CN_STOPWORDS = {' ', '，', '。', '？', '！', '～', "'", '的', '了', '啊', '呵', '也'}

STOPWORDS |= CN_STOPWORDS

class Comment(object):
    '''Comment has 4 (principal) propteries
    user: user
    time: time
    vote: vote
    content: content'''
    def __init__(self, user='', time='', vote=0, content=''):
        self.user = user
        self.time = time
        self.vote = vote
        self.content = content

    def __str__(self):
        return '%s(%s): %s'%(self.user, self.time, self.content)

    def cut(self, stopwords=STOPWORDS):
        import jieba
        return [w for w in jieba.cut(self.content) if w not in stopwords]

class Movie(object):
    '''Movie has 2 (principal) propteries
    info: info
    comments: comments'''
    def __init__(self, name='', info={}, comments=[]):
        self.name = name
        self.info = info
        self.comments = comments

    @staticmethod
    def fromSoup(bs:BeautifulSoup):
        return Movie(get_name(bs), get_info(bs), get_comments(bs))

    def __str__(self):
        return '%s:\n%s'%(self.name, '\n'.join('  %s: %s'%(k, v) for k, v in self.info.items()))

    def wordCould(self):
        import numpy as np
        from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
        wl_space_split = " ".join(self.words)
        wordcloud = WordCloud(background_color="white",
                         max_font_size=50, random_state=42,
                         max_words=2000,
                         stopwords=STOPWORDS,
                         font_path='/System/Library/Fonts/PingFang.ttc').generate(wl_space_split)
        wordcloud.to_file('%s.png'%self.name)

    def stat(self):
        # frequency of the words in comments
        import collections
        return collections.Counter(self.words)

    @property
    def words(self):
        import itertools
        return itertools.chain.from_iterable(comment.cut() for comment in self.comments)

    def __getitem__(self, key):
        return self.info[key]


# def search(keyword):
    # return a list of urls
    # url = DOUBAN_MOVIE_URL + '/subject_search?search_text=%s&cat=1002'%keyword
    # resp = requests.get(url, headers=header_dict)
    # bs = BeautifulSoup(resp.content.decode('utf-8'), "lxml")
    # print(bs.find('div', {'class':'sc-dnqmqq eXEXeG'}))
    # return [div.find('a')['href'] for div in bs.find('div', {'class': 'sc-dnqmqq eXEXeG'}).find_all('div')]


def get_name(bs:BeautifulSoup)->str:
    '''get information from bs object
    
    get information of a movie
    
    Returns:
        str -- name of the movie
    '''
    name = bs.find('span', {'property':'v:itemreviewed'})
    year = bs.find('span', {'class':'year'})

    return name.text + year.text


def get_info(bs:BeautifulSoup)->dict:
    '''get information from bs object
    
    get information of a movie
    
    Returns:
        dict -- dictionary of information
    '''
    info = bs.find('div', {'id':'info'})
    info_dict = {}
    for span in info.find_all('span', recursive=False):
        if span.find_all('span'):
            key, val = span.find_all('span')
            key = key.text
            val = val.text
        elif span.text.startswith('类型'):
            key = span.text.strip(':')
            val = [span.text for span in span.find_next_siblings('span', {'property':'v:genre'})]
        elif span.has_attr('class') and span['class'][0] == 'pl':
            key = span.text.strip(':')
            if '/' in span.next_sibling:
                items = span.next_sibling.split('/')
                val = [item.strip() for item in items]
            else:
                val = span.next_sibling.next_sibling.text
        if isinstance(val, str) and '/' in val:
            val = [v.strip() for v in val.split('/')]
        info_dict.update({key:val})
    return info_dict


def get_comments(bs:BeautifulSoup)->[Comment]:
    # get a list of comments
    hot_comments = bs.find('div', {'id':'hot-comments'})
    hot_comment_list = []
    for div in hot_comments.find_all('div', {'class':'comment-item'}):
        comment_info = div.find('span', {'class':'comment-info'})
        comment_time = div.find('span', {'class':'comment-time'})
        vote = div.find('span', {'class':'votes'})
        vote = int(vote.text)
        user = comment_info.a.text
        time = comment_time.text.strip()
        comment = div.find('p').text.strip()
        hot_comment_list.append(Comment(user=user, time=time, vote=vote, content=comment))
    return hot_comment_list


if __name__ == '__main__':
    url = DOUBAN_MOVIE_URL + '/subject/26816017'  # 居里夫人 Marie Curie -> url ???
    resp = requests.get(url, headers=header_dict)
    bs = BeautifulSoup(resp.content.decode('utf-8'), "lxml")
    movie = Movie.fromSoup(bs)
    print(movie)
    print(movie.stat())
    movie.wordCould()  # generate word cloud
