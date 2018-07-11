#!/usr/local/bin/python
# -*- coding: utf-8 -*-


import base
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

import product

from matplotlib.font_manager import FontProperties
myfont = FontProperties(fname='/System/Library/Fonts/PingFang.ttc')

prods = product.Product.read('iceboxes.xls')
keys = ('总容积', '额定耗电量', 'price', '产品重量')
units = ('L', '度', '元', 'kg')

sns.set(style="darkgrid")

# Set up the matplotlib figure
f, axes = plt.subplots(2, 2, figsize=(2, 2))

# Rotate the starting point around the cubehelix hue circle
for ax, key, unit in zip(axes.flat, keys, units):
    data = []
    for prod in prods:
        if prod[key] and isinstance(prod[key], str):
            d = float(base.decimal_rx.match(prod[key])[0])
            data.append(d)
        elif isinstance(prod[key], int):
            d = prod[key]
            data.append(d)

    # Generate and plot a random bivariate dataset
    # sns.distplot(data, label=' '.join(pypinyin.lazy_pinyin(key)), ax=ax)
    ax.hist(data, bins=40)
    ax.set_xlabel('%s / %s' % (key, unit), fontproperties=myfont)

# f.tight_layout()
plt.show()
