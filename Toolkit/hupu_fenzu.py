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

def output(file_name, leagues) :

    print('============ 分组结果 ============')

    with open(file_name, 'w') as file:
        for x in range(0, len(leagues)):
            line = '\n============ 第{}组 (共{}人)============'.format(x+1, len(leagues[x]))
            print(line)
            file.write(line + "\n") 
            for name in leagues[x]:
                print(name)
                file.write(name + "\n") 

    print('>>>>>>>> 已保存到 "{}"'.format(file_name))

# generate a list of continuous numbers, starts at 0
def generateRandomContinousNumbers(count):
    numbers = []

    while len(numbers) < count:
        num = randint(0, count - 1)
        if not num in numbers:
            numbers.append(num)

    print(numbers)
    return numbers;

def divideLeagueByLevel(initial_names, n):

    leagues = []
    for x in range(0,n):
        league = []
        leagues.append(league)

    for i in range(0,len(initial_names), n):
        count = min(n, len(initial_names) - i)
        numbers = generateRandomContinousNumbers(count)

        for j in range(0, count):
            idx = i + numbers[j]
            leagues[j].append(initial_names[idx])

    return leagues;

def divideLeagueByRandom(initial_names, n):
    leagues = []
    for x in range(0,n):
        league = []
        leagues.append(league)

    i = 0
    while len(initial_names) > 0:
        if len(initial_names) == 1:
            idx_name = 0
        else:
            idx_name = randint(0, len(initial_names)-1)
        name = initial_names[idx_name]
        initial_names.remove(name)

        idx_league = i % n
        leagues[idx_league].append(name)
        i+=1

    return leagues

@click.command()
@click.option('--f', prompt='请提供待分组名单文件', help='文件格式为txt）')
@click.option('--n', type=int, prompt='分成几组？')
@click.option('--t', type=bool, default=False, prompt='需要分档吗?')
def main(f, n, t):
    # read initial name from file.
    with open(f, 'r') as file:
        content = file.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    initial_names = [x.strip() for x in content]

    print('============ 待分组名单(共{}人)， 需分成{}组 ============'.format(len(initial_names), n))
    for name in initial_names:
        print(name)

    if t:
        leagues = divideLeagueByLevel(initial_names, n)
    else:
        leagues = divideLeagueByRandom(initial_names, n)

    file_name, ext = os.path.splitext(f)
    output_file = file_name + '_分组结果' + ext
    output(output_file, leagues)


if __name__ == '__main__':
    main()
