#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
    Cardapio do dia da Unicamp

    @author: gomesar
    2018
'''

import requests
from re import sub
from pandas import read_html

_page = requests.get('https://www.prefeitura.unicamp.br/apps/site/cardapio.php')
page = sub('[\n\t]+[\n\t\ ]*', '', _page.text)
tables = read_html(page)

# table[2:6]
titulos=("[Almoço]", "[Almoço Vegetariano]", "[Jantar]", "[Jantar Vegetariano]")
count=0
for t in tables[2:6]:
    c = titulos[count] + '\n'
    count += 1

    for i, row in t.iterrows():
        if row[0].find('CANECA') == -1:
            c += row[0] + '\n'
    print(c)

