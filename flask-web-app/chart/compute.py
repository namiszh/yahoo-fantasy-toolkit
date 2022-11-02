#-*- coding: utf-8 -*-

from audioop import reverse
import pandas as pd
from pandas import DataFrame
from scipy.stats import rankdata
# import re
import matplotlib.pyplot as plt
# import os
import numpy as np
from io import BytesIO
import base64



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

def league_bar_chart(names, scores, title):
    '''Generate a bar chart displaying the total score of each team
    '''

    # print(names)
    # print(scores)

    pos = list(range(1, len(names)+1))
    print(pos)

    width = 0.3

    # Plotting the bars
    fig, ax = plt.subplots(figsize=(18,12))

    # Create a bar with week score,
    # in position pos,
    plt.bar([p + width for p in pos],
            
            scores,
            # of width
            width,
            # with alpha 0.5
            alpha=0.5,
            # with color
            color='#EE3224',
            edgecolor='red',
            # with label the first value in first_name
            label='Week')


    # Set the y axis label
    ax.set_ylabel('Score')

    # Set the chart's title
    ax.set_title(title, name='Arial')

    # Set the position of the x ticks
    ax.set_xticks([p + 1.5 * width for p in pos])

    # Make the y-axis (0-100) labels smaller.
    ax.tick_params(labelsize=8)

    # Set the labels for the x ticks
    ax.set_xticklabels(names, rotation=60)

    # Setting the x-axis and y-axis limits
    plt.xlim(min(pos)-width, max(pos)+width*4)
    plt.ylim(0, 180 )

    # Adding the legend and showing the plot
    # plt.legend(['Week', 'Season'], loc='upper right')
    plt.grid(True)

    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)  # rewind to beginning of file
    figdata_png = base64.b64encode(figfile.getvalue())
    figdata_png = figdata_png.decode('utf8')

    return figdata_png


def team_bar_chart(names, df_scores):
    '''Generate a bar chart on polar axis displaying the separate stat score of each team
    '''
    charts = []

    # get the stat names, need to remove the last column 'total'
    stat_names = df_scores.columns.pop()

    for team_name in names:
        # get the stat scores, need to remove the last column 'total'
        team_scores = df_scores.loc[team_name].pop()
        chart = team_stat_chart(team_name, stat_names, team_scores)
        charts.append(chart)
    
    return charts


def team_stat_chart(team_name, stat_names, stat_scores):
    '''Generate bar chart on polar axis for a team
    '''
    pass
