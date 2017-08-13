#!/usr/bin/env python

import pandas as pd
from pandas import DataFrame
from scipy.stats import rankdata
import re

def data_to_ranking_score(values, reverse = False):
    '''
    Given a list of value, return a list of ranking score.
    If reverse = False, the biggest value will get the biggest ranking score.
    If reverse = True, the biggest value will get the smallest ranking score.
    Only category 'TO' should set 'reverse' to 'True'.

    The smallest ranking score is 1, the biggest ranking score is the element
    number of this list.
    '''
    scores = rankdata(values)
    if reverse:
        scores = [(len(values) + 1 - score) for score in scores]

    return scores;


def parse_data_file(data_file_name):
    '''The method reads a league's raw data of for week or total season from a csv file, 
        then convert these data to scores and output to another csv file.
    '''
    df = pd.read_csv(data_file_name, encoding = "ISO-8859-1")
    headers = list(df)

    for header in headers[1:]:
        reverse = (header == 'TO')
        df[header] = data_to_ranking_score(df[header], reverse)

    # add a column 'Total', its value 
    df['Total'] = df[headers[1:]].sum(axis=1)

    score_file_name = re.sub(r'data(_\d+_\d+\.csv$)', r'score\1', data_file_name)
    print('write result to', score_file_name)
    df.to_csv(score_file_name, index=False)

if __name__ == '__main__':
    parse_data_file('../data/data_817_1.csv')
