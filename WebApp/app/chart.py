#!/usr/bin/env python


from io import BytesIO
import base64
import matplotlib.pyplot as plt
import numpy as np


def get_week_score_bar_chart(names, scores, title):
    ind = np.arange(len(scores))
    width = 0.5  # the width of the bars

    fig, ax = plt.subplots(figsize=(21,14))
    rects = ax.bar(ind, scores, width, color='IndianRed', alpha=0.7, edgecolor='#000000')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_title(title, fontsize=36)
    ax.set_ylabel('Scores', fontsize=16)
    ax.set_xticks(ind)
    ax.set_xticklabels(names, rotation=40, ha='right', fontsize=16)
    ax.legend()

    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()*0.5, 1.01*height,
                '{}'.format(height), ha='center', va='bottom', fontsize=16)

    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)  # rewind to beginning of file
    figdata_png = base64.b64encode(figfile.getvalue())
    figdata_png = figdata_png.decode('utf8')

    return figdata_png

def get_team_stats_chart(weeks, stat_scores):
    '''
    weeks is a list, element is week
    stat scores is a dict, key is stat display name, value is a list of scores
    '''
    fig, ax = plt.subplots(figsize=(21,14))
    for stat_name, scores in stat_scores.items():
        ax.plot(weeks, scores, label=stat_name)

    # put text outside the figure
    ax.legend(loc='upper left', prop={'size':6}, bbox_to_anchor=(1,1))
    # plt.tight_layout(pad=7)

    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)  # rewind to beginning of file
    figdata_png = base64.b64encode(figfile.getvalue())
    figdata_png = figdata_png.decode('utf8')

    return figdata_png



