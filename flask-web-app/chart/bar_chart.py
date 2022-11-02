#!/usr/bin/env python


from io import BytesIO
import base64
import matplotlib.pyplot as plt
import numpy as np
from app import cnFontProp


def league_bar_chart(names, week_scores, total_scores, title, week):
    '''Generate a bar chart displaying the total score of each team
    '''
    pos = list(range(1, len(names)+1))

    width = 0.25

    # Plotting the bars
    fig, ax = plt.subplots(figsize=(12,9))

    # Create a bar with week score,
    # in position pos,
    plt.bar([p - width/2 for p in pos], total_scores, width, alpha=0.5, color='#1aaf6c', edgecolor='#1aaf6c', label='Total')
    plt.bar([p + width/2 for p in pos], week_scores, width, alpha=0.25, color='#429bf4', edgecolor='#429bf4', label='Week')


    # Set the y axis label
    ax.set_ylabel('Score')

    # Set the chart's title
    ax.set_title(title, fontproperties = cnFontProp)

    # Make the y-axis (0-100) labels smaller.
    # ax.tick_params(labelsize=8)

    # Set the position of the x ticks
    ax.set_xticks([p for p in pos])
    # Set the labels for the x ticks
    ax.set_xticklabels(names, rotation=30, ha='right', fontproperties = cnFontProp)



    # Setting the x-axis and y-axis limits
    # plt.xlim(min(pos)-width, max(pos)+width*4)
    # plt.ylim(0, 180 )

    # Adding the legend and showing the plot
    plt.legend(['Total', 'Week '+ str(week)], loc='upper right')
    plt.grid(linestyle='--', linewidth=1, axis='y', alpha=0.7)

    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)  # rewind to beginning of file
    figdata_png = base64.b64encode(figfile.getvalue())
    figdata_png = figdata_png.decode('utf8')

    return figdata_png


