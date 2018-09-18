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

def output(file_name, names, orders) :

    print('\n============== 抽签结果 ============== ')
    with open(file_name, 'w') as file:

        index = 1;
        while index <= len(names):
            for name, order in zip(names, orders):
                if order == index:
                    line = "{}\t{}".format(order, name)
                    print(line)
                    file.write(line + "\n") 
                    index+=1
                    break
    print('>>>>>>>> 已保存到 "{}"'.format(file_name))

def randomName(initial_names):

    names = []

    print('\n============ 打乱后的名单 ============ ')
    while len(initial_names) > 0:
        if len(initial_names) == 1:
            num = 0
        else:
            num = randint(0, len(initial_names)-1)
        name = initial_names[num]
        initial_names.remove(name)
        names.append(name)
        print(name)

    return names

def randomOrder(count):
    orders = []

    print('\n============ 打乱后的顺位 ============ ')
    while len(orders) < count:
        num = randint(1, count)
        if orders.count(num) == 0:
            print(num)
            orders.append(num)

    return orders

@click.command()
@click.option('--t', type=int, default=3, prompt='你想做什么？（1：打乱名单；2：打乱顺位；3：生成最后结果)')
@click.option('--f', prompt='请提供初始名单文件', help='文件格式为txt）')
def main(t, f):
    # read initial name from file.
    with open(f, 'r') as file:
        content = file.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    initial_names = [x.strip() for x in content]

    print('============ 初始名单(共{}人) ============ '.format(len(initial_names)))
    for name in initial_names:
        print(name)

    if t == 1:
        random_names = randomName(initial_names)
    elif t == 2:
        random_orders = randomOrder(len(initial_names))
    elif t == 3:
        random_names = randomName(initial_names)
        random_orders = randomOrder(len(random_names))
        file_name, ext = os.path.splitext(f)
        output_file = file_name + '_顺位' + ext
        output(output_file, random_names, random_orders)
    else:
        print('我不懂你想要干什么')


if __name__ == '__main__':
    main()
