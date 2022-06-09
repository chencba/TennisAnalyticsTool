# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 13:59:47 2022

@author: Huzihu
"""

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)

#path = r"D:/UCD/classes/Sports & Performance Analytics/Sports Analytics Tool/"

#filename = "events.csv"

#df = pd.read_csv(path + filename)

# Tennis Court

height_court = 10.97
width_court = 11.89*2
service_box = 6.4
double_field = 1.37
baseline_serviceline = 5.5
breite_einzel = 8.23
serviceline_net = 6.4

def draw_court(hide_axes = False):

    fig = plt.figure(figsize=(height_court/2, width_court/2))
    fig.patch.set_facecolor('#5080B0')

    axes = fig.add_subplot(1, 1, 1, facecolor='#5080B0')

    if hide_axes:
        axes.xaxis.set_visible(False)
        axes.yaxis.set_visible(False)
        axes.axis('off')

    axes = draw_patches(axes)
    
    return fig, axes

def draw_patches(axes):
    plt.xlim([-2,height_court+2])
    plt.ylim([-6.5,width_court+6.5])
    
    #net
    axes.add_line(plt.Line2D([height_court, 0],[width_court/2, width_court/2],
                    c='w'))
    
    # court outline
    y = 0
    dy = width_court
    x = 0 #height_court-double_field
    dx = height_court
    axes.add_patch(plt.Rectangle((x, y), dx, dy,
                       edgecolor="white", facecolor="#5581A6", alpha=1))
    # serving rect
    y = baseline_serviceline
    dy = serviceline_net*2
    x = 0 + double_field 
    dx = breite_einzel
    axes.add_patch(plt.Rectangle((x, y), dx, dy,
                       edgecolor="white", facecolor="none", alpha=1))
    
    # net
    axes.add_line(plt.Line2D([height_court/2, height_court/2], [width_court/2 - service_box, width_court/2 + service_box],
                    c='w'))
    
    axes.add_line(plt.Line2D([height_court/2, height_court/2], [0, 0 + 0.45], 
                    c='w'))

    axes.add_line(plt.Line2D([height_court/2, height_court/2], [width_court, width_court - 0.45], 
                c='w'))
    
    axes.add_line(plt.Line2D([1.37, 1.37], [0, width_court], 
            c='w'))
    
    axes.add_line(plt.Line2D( [height_court - 1.37, height_court - 1.37], [0, width_court],
        c='w'))

    return axes


uploaded_file = st.file_uploader("Please choose the events & points csv files in order:", accept_multiple_files = True)

if len(uploaded_file) == 2:
    
    df = pd.read_csv(uploaded_file[0])
    
    df1 = df.copy()
    df1.drop(["receiver_x","receiver_y","receiver"], axis=1, inplace=True)
    df1["type"] = "hit position"
    df1.rename(columns={'hitter_x':'x', 'hitter_y':'y','hitter':'player'}, inplace=True)
    
    df2 = df.copy()
    df2.drop(["hitter_x", "hitter_y","hitter"], axis=1, inplace=True)
    df2["type"] = "receive position"
    df2.rename(columns={'receiver_x':'x', 'receiver_y':'y','receiver':'player'}, inplace=True)
    
    df_new = pd.concat([df1,df2], axis = 0, join = 'outer', ignore_index = False) 
    
    df_new = df_new[df_new["stroke"]!="__undefined__"]

    st.title("Hit & Receive Positions")

    fig, ax = draw_court(hide_axes = True)
    
    types = df_new["type"].unique()
    types = list(types)
    types.append('Select all')
    option1 = st.selectbox(label="Which position would you like to display?", options=types)
    
    serve = df_new["serve"].unique()
    serve = list(serve)
    serve.append('Select all')
    option2 = st.selectbox(label="Which serve type would you like to display?", options=serve)
    
    stroke = df_new["stroke"].unique()
    stroke = list(stroke)
    stroke.append('Select all')
    option3 = st.selectbox(label="Which stroke type would you like to display?", options=stroke)
    
    if ('Select all' in option1) and ('Select all' in option2) and ('Select all' in option3):
    	df_option = df_new
    if ('Select all' in option1) and ('Select all' not in option2) and ('Select all' in option3):
        df_option = df_new[df_new["serve"]==option2]
    if ('Select all' in option1) and ('Select all' in option2) and ('Select all' not in option3):
        df_option = df_new[df_new["stroke"]==option3]
    if ('Select all' not in option1) and ('Select all' in option2) and ('Select all' in option3):
        df_option = df_new[df_new["type"]==option1]
    if ('Select all' not in option1) and ('Select all' not in option2) and ('Select all' in option3):
        df_option = df_new[(df_new["type"]==option1) & (df_new["serve"]==option2)]
    if ('Select all' in option1) and ('Select all' not in option2) and ('Select all' not in option3):
    	df_option = df_new[(df_new["serve"]==option2) & (df_new["stroke"]==option3)]
    if ('Select all' not in option1) and ('Select all' in option2) and ('Select all' not in option3):
    	df_option = df_new[(df_new["type"]==option1) & (df_new["stroke"]==option3)]
    if ('Select all' not in option1) and ('Select all' not in option2) and ('Select all' not in option3):
    	df_option = df_new[(df_new["type"]==option1) & (df_new["serve"]==option2) & (df_new["stroke"]==option3)]    
    
    players = df_new["player"].unique()
    p1 = df_option[df_option["player"]==players[0]]
    p2 = df_option[df_option["player"]==players[1]]
    
    ax.scatter(p1["x"], p1["y"], c = 'coral', label = players[0])
    ax.scatter(p2["x"], p2["y"], c = 'y', label = players[1])
    ax.legend(loc='upper right')
    
    st.pyplot(fig)

# streamlit run tennis_analytics.py

#path = r"D:/UCD/classes/Sports & Performance Analytics/Sports Analytics Tool/"

#filename = "points.csv"

#data = pd.read_csv(path + filename)

    data = pd.read_csv(uploaded_file[1])
    
    players2 = data["winner"].unique()
    player1 = players2[0]
    player2 = players2[1]
    
    st.title("Trajectory of the Ball")
    
    fig3, ax3 = draw_court(hide_axes = True)
    
    reasons = data["reason"].unique()
    reasons = list(reasons)
    reasons.append('Select all')
    option4 = st.selectbox(label="Which reason would you like to display?", options=reasons)
    
    if option4 == 'Select all':
        data_option = data
    else:
        data_option = data[data["reason"]==option4]
    
    one = data_option[data_option["winner"]==player1]
    two = data_option[data_option["winner"]==player2]
    
    ax3.plot(one["x"], one["y"], c = 'coral', label="Winner is {}".format(player1))
    ax3.plot(two["x"], two["y"], c = 'y', label="Winner is {}".format(player2))
    ax3.legend(loc='upper right')
    
    st.pyplot(fig3)
    
    st.title("Winning Reasons")
    
    fig2, ax2 = plt.subplots(figsize=(10,6))
    
    win_reasons = data.groupby("reason")["winner"].value_counts().unstack()
    
    ax2.bar(win_reasons.index,win_reasons[player1], color = 'coral', width=-0.3, label=player1, align='edge')
    ax2.bar([i+0.3 for i in range(5)],win_reasons[player2], color = 'y', width=-0.3, label=player2, align='edge')
    ax2.set_ylabel("Number of Wins")
    
    ax2.legend(loc='upper right')
    
    st.pyplot(fig2)
