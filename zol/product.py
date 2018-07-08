#!/usr/local/bin/python
# -*- coding: utf-8 -*-

class Product(object):
    '''Product has 5 (principal) propteries
    name: name
    description: description
    price: price
    comment_num: comment_num
    href: href'''
    def __init__(self, name, description, price, comment_num=0, href='', parameter={}, comment=[]):
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