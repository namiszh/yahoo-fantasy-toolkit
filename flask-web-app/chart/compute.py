#-*- coding: utf-8 -*-

# from audioop import reverse
import pandas as pd
from pandas import DataFrame
from scipy.stats import rankdata
# import re
# import matplotlib.pyplot as plt
# import os
# import numpy as np
# from io import BytesIO
# import base64



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

    return scores

def stat_to_score(stat_df, sort_orders):
    '''Give then stats of a league for a week or the whole season, compute the ranking score
    '''
    score_df = stat_df.copy()

    idx = 0
    for (stat_name, stat_value) in stat_df.items():
        sort_order = sort_orders[idx]
        idx += 1

        reverse = (sort_order == '0')
        scores = data_to_ranking_score(stat_value.values, reverse)
        score_df[stat_name] = scores

    # add a column to display the total score of each team (row)
    score_df['Total'] = score_df.sum(axis=1)

    return score_df

