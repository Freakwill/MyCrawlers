#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import pandas as pd

class Product(object):
    '''Product has 5 (principal) propteries
    name: name
    description: description
    price: price
    comment_num: comment_num
    href: href'''
    def __init__(self, name='', description='', price=0, comment_num=0, href='', parameter={}, comment=[]):
        self.name = name
        self.description = description
        self.price = price
        self.comment_num = comment_num
        self.href = href
        self.parameter = parameter
        self.comment = comment

    def __format__(self, spec=None):
        if spec is None:
            return str(self)
        elif spec == 's':
            return '%s: %s'(self.name, self.description)
        else:
            super(Product, self).__format__(spec)

    def __str__(self):
        return '%s (%d): %s. [%d人点评]' % (self.name, self.price, self.description, self.comment_num)


    def toDict(self):
        d = {'name':self.name, 'price':self.price, 'comment_num':self.comment_num}
        d.update(self.parameter)
        return d

    @staticmethod
    def fromDice(d):
        p = Product(name=d.name, price=d.price, comment_num=d.comment_num)
        d.pop('name')
        d.pop('price')
        d.pop('comment_num')
        p.parameter = d
        return p

    @staticmethod
    def read(path):
        # return [Product]
        df = pd.read_excel(path)
        keys = df.columns
        values = df.values
        ps = []
        for vals in values:
            p = Product()
            for key, val in zip(keys, vals):
                if key == 'name':
                    p.name = val
                elif key == 'price':
                    p.comment_num = val
                elif key == 'comment_num':
                    p.comment_num = val
                else:
                    p.parameter.update({key:val})
            ps.append(p)
        return ps

