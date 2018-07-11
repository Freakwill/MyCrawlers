#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import re

import pandas as pd


class Quantity(object):
    '''Quantity has 3 (principal) propteries
    name: name
    value: value
    unit: unit
    '''

    rx = re.compile(r' *(?P<value>\d+(\.\d+)?) *(?P<unit>\w+)?')

    def __init__(self, name='', value=0, unit=''):
        self.name = name
        self.value = value
        self.unit = unit
        self.default_type = float

    def __bool__(self):
        return self.value

    def __str__(self):
        return '{0}'.format(self)
    
    @staticmethod
    def parse(s):
        try:
            value = Quantity.rx.match(s)['value']
            unit = Quantity.rx.match(s)['unit']
            return value, unit
        except:
            return None

    @staticmethod
    def fromStr(s, name=''):
        value, unit = Quantity.parse(s)
        return Quantity(name, value, unit)

    def __format__(self, spec=''):
        if spec == '':
            return '%.2f %s' % (self.default_type(self.value), self.unit)
        elif spec == 'int':
            return '%d %s' % (int(self.value), self.unit)
        elif spec == 'float':
            return '%.2f %s' % (float(self.value), self.unit)
        elif spec == 'name':
            return '%s /%s' % (self.name, self.unit)
        else:
            return '%.2f %s %s' % (self.default_type(self.value), spec, self.unit)


class Product(object):
    '''Product has 5 (principal) propteries
    name: name
    description: description
    price: price
    comment_num: comment_num
    href: href'''
    quantities = set()
    
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
            return super(Product, self).__format__(spec)

    def __str__(self):
        return '%s (%d): %s. [%d人点评]' % (self.name, self.price, self.description, self.comment_num)

    def __getitem__(self, key):
        if key == 'price':
            return self.price
        return self.parameter[key]

    def __setitem__(self, key, value):
        self.parameter[key] = value

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

    @classmethod
    def read(cls, path):
        # return [Product]
        df = pd.read_excel(path)
        keys = df.columns
        values = df.values
        ps = []
        for vals in values:
            p = Product()
            parameter = {}
            for key, val in zip(keys, vals):
                if key == 'name':
                    p.name = val
                elif key == 'price':
                    p.price = val
                elif key == 'comment_num':
                    p.comment_num = val
                elif key in cls.quantities:
                    parameter.update({key:Quantity.fromStr(val, key)})
                else:
                    parameter.update({key:val})
            p.parameter = parameter
            ps.append(p)
        return ps

    def convert(self, converter):
        for key, val in self.parameter:
            self[key] = converter(val)

