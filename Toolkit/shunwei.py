#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Script to generate draft order for standard league.

    :copyright: (c) 2017 by HuangShaozuo.
"""

from pandas import DataFrame
from random import randint
import click
import csv
import os
import pandas as pd

def output_to_csv(file_name, names, orders) :

    print('Write to result to file "{}"'.format(file_name))
    with open(file_name, 'w', newline='') as csvfile:
        fieldnames = ['名单', '顺位']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        index = 1;
        while index <= len(names):
            for name, order in zip(names, orders):
                if order == index:
                    writer.writerow({'名单': name, '顺位': order})
                    index+=1
                    break

def randomName(initial_names):

    names = []

    print('打乱后的名单：')
    while len(initial_names) > 1:
        num = randint(0, len(initial_names)-1)
        tmp_name = initial_names[num]
        print(tmp_name)
        names.append(tmp_name)
        initial_names.remove(tmp_name)

    print(initial_names[0])
    names.append(initial_names[0])

    return names

def randomOrder(count):
    orders = []

    print('打乱后的顺位：')
    while len(orders) < count:
        num = randint(1, count)
        if orders.count(num) == 0:
            print(num)
            orders.append(num)

    return orders

@click.command()
@click.option('--t', type=int, default=3, prompt='你想做什么？（1：生成最后结果；2：打乱名单；3：打乱顺位)')
@click.option('--f', prompt='初始名单csv文件', help='文件格式为（txt|csv）')
def main(t, f):
    # read initial name from csv file.
    df = pd.read_csv(f, encoding = "ISO-8859-1")
    initial_names = df[df.columns[0]].tolist()
    print('初始名单(共{}人):'.format(len(initial_names)))
    for name in zip(initial_names):
        print(name)

    if t == 1:
        random_names = randomName(initial_names)
    elif t == 2:
        random_orders = randomOrder(len(initial_names))
    elif t == 3:
        random_names = randomName(initial_names)
        random_orders = randomOrder(len(random_names))
        file_name, ext = os.path.splitext(f)
        output_file = file_name + '_result' + ext
        output_to_csv(output_file, random_names, random_orders)
    else:
        print('我不懂你想要干什么')


if __name__ == '__main__':
    main()
