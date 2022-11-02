#!/usr/bin/env python


from io import BytesIO
import base64
import matplotlib.pyplot as plt
import numpy as np
from app import cnFontProp

def league_radar_charts(week_df, total_df, week):
    # print(week_df)
    # print(total_df)
    charts = []

    # get the stat names, need to remove the last column 'total'
    stat_names = week_df.columns.values.tolist()[:-1]
    # print(stat_names)
    team_names = week_df.index.tolist()
    # print(team_names)

    for team_name in team_names:
        # get the stat scores, need to remove the last column 'total'
        week_score = week_df.loc[team_name].values.tolist()[:-1]
        total_score = total_df.loc[team_name].values.tolist()[:-1]
        chart = get_radar_chart(stat_names, team_name, total_score, week_score, len(team_names), week)
        charts.append(chart)
    
    return charts


def get_radar_chart(labels, title, season_values, week_values, limit, week):
    # print(season_values)
    # print(week_values)
    # print(limit)

    # Number of variables we're plotting.
    num_vars = len(labels)

    # Split the circle into even parts and save the angles
    # so we know where to put each axis.
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

    # The plot is a circle, so we need to "complete the loop"
    # and append the start value to the end.
    angles += angles[:1]
    season_values += season_values[:1]
    week_values += week_values[:1]

    # ax = plt.subplot(polar=True)
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))


    ax.plot(angles, season_values, color='#1aaf6c', linewidth=1, label='Total')
    ax.fill(angles, season_values, color='#1aaf6c', alpha=0.5)

    ax.plot(angles, week_values, color='#429bf4', linewidth=1, label=('Week '+ str(week)))
    ax.fill(angles, week_values, color='#429bf4', alpha=0.25)

    # Fix axis to go in the right order and start at 12 o'clock.
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    # Draw axis lines for each angle and label.
    ax.set_thetagrids(np.degrees(angles[:-1]), labels)

    # Go through labels and adjust alignment based on where
    # it is in the circle.
    for label, angle in zip(ax.get_xticklabels(), angles):
        if angle in (0, np.pi):
            label.set_horizontalalignment('center')
        elif 0 < angle < np.pi:
            label.set_horizontalalignment('left')
        else:
            label.set_horizontalalignment('right')

    # Ensure radar goes from 0 to limit.
    ax.set_ylim(0, limit)

    # Set position of y-labels (0-100) to be in the middle
    # of the first two axes.
    ax.set_rlabel_position(180 / num_vars)

    # Add some custom styling.
    # Change the color of the tick labels.
    ax.tick_params(colors='#222222')
    # Make the y-axis (0-100) labels smaller.
    ax.tick_params(axis='y', labelsize=8)
    # Change the color of the circular gridlines.
    ax.grid(color='#AAAAAA')
    # Change the color of the outermost gridline (the spine).
    ax.spines['polar'].set_color('#222222')
    # Change the background color inside the circle itself.
    ax.set_facecolor('#FAFAFA')

    ax.set_title(title, y=1.08, fontproperties = cnFontProp)

    # Add a legend as well.
    ax.legend(loc='upper right', frameon=False, bbox_to_anchor=(1.15, 1.1))

    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)  # rewind to beginning of file
    figdata_png = base64.b64encode(figfile.getvalue())
    figdata_png = figdata_png.decode('utf8')

    return figdata_png