#!/usr/bin/env python

import pandas as pd
from pandas import DataFrame
from scipy.stats import rankdata
import re
import matplotlib.pyplot as plt
import os
import numpy as np
from io import BytesIO
import base64

# web application directory
WEB_APP_ROOT = os.path.abspath(os.path.dirname( __file__ ))
print(WEB_APP_ROOT)

DATA_ROOT = os.path.abspath(os.path.join(os.path.dirname( WEB_APP_ROOT ), 'data'))
print(DATA_ROOT)

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

    # replace 'data' in file name with score
    score_file_name = re.sub(r'(_week\d+_)data(\.csv$)', r'\1score\2', data_file_name)
    print('write result to', score_file_name)
    df.to_csv(score_file_name, index=False)

def get_week_csv_file(league_name, week, file_type='score'):
    file_name = '{}_week{}_{}.csv'.format(league_name, week, file_type)
    # print('week {} score file name of league "{}": "{}"'.format(week, league_name, file_name))

    file_path = os.path.abspath(os.path.join(DATA_ROOT, file_name))
    print('week {} score file path of league "{}": "{}"'.format(week, league_name, file_path))

    return file_path

def get_week_score_png(league_id, week):

    week_score_file = get_week_csv_file("Never Ending", 1, "score")
    week_df = pd.read_csv(week_score_file, encoding = "ISO-8859-1")

    season_score_file = get_week_csv_file("Never Ending", 0, "score")
    season_df = pd.read_csv(season_score_file, encoding = "ISO-8859-1")

    names = week_df['Team Name'].tolist()
    week_scores = week_df['Total'].tolist()
    season_scores = season_df['Total'].tolist()

    pos = list(range(1, len(names)+1))
    print(pos)

    width = 0.3

    # Plotting the bars
    fig, ax = plt.subplots(figsize=(20,12))

    # Create a bar with week score,
    # in position pos,
    plt.bar([p + width for p in pos],
            
            week_scores,
            # of width
            width,
            # with alpha 0.5
            alpha=0.5,
            # with color
            color='#EE3224',
            edgecolor='red',
            # with label the first value in first_name
            label='Week')

    # Create a bar with mid_score data,
    # in position pos + some width buffer,
    plt.bar([p + 2*width for p in pos],
            #using df['mid_score'] data,
            season_scores,
            # of width
            width,
            # with alpha 0.5
            alpha=0.2,
            # with color
            color='#F78F1E',
            edgecolor='#000000',
            # with label the second value in first_name
            label='Season')

    # Set the y axis label
    ax.set_ylabel('Score')

    # Set the chart's title
    ax.set_title('Week {} Power Ranking'.format(week))

    # Set the position of the x ticks
    ax.set_xticks([p + 1.5 * width for p in pos])

    # Set the labels for the x ticks
    ax.set_xticklabels(names, rotation=60)

    # Setting the x-axis and y-axis limits
    plt.xlim(min(pos)-width, max(pos)+width*4)
    plt.ylim(0, 180 )

    # Adding the legend and showing the plot
    plt.legend(['Week', 'Season'], loc='upper right')
    plt.grid(True)

    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)  # rewind to beginning of file
    figdata_png = base64.b64encode(figfile.getvalue())
    figdata_png = figdata_png.decode('utf8')

    return figdata_png

def compute_png_svg():
    """Return filename of plot of the damped_vibration function."""

    t = np.arange(0.0, 2.0, 0.01)
    s = 1 + np.sin(2*np.pi*t)
    plt.plot(t, s)

    plt.xlabel('time (s)')
    plt.ylabel('voltage (mV)')
    plt.title('About as simple as it gets, folks')
    plt.grid(True)

    # Make Matplotlib write to BytesIO file object and grab
    # return the object's string
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)  # rewind to beginning of file
    figdata_png = base64.b64encode(figfile.getvalue())
    figdata_png = figdata_png.decode('utf8')

    # figdata_png="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"
    # svg
    # figfile = BytesIO()
    # plt.savefig(figfile, format='svg')
    # figfile.seek(0)
    # figdata_svg = '<svg' + figfile.getvalue().split('<svg')[1]
    # figdata_svg = base64.b64encode(figfile.getvalue())
    return figdata_png

if __name__ == '__main__':

    for i in range(0,3):
        data_file_name = get_week_csv_file("Never Ending", i, "data")
        # print(data_file_name)
        parse_data_file(data_file_name)
