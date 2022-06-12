# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 16:13:11 2022

@author: Huzihu
"""

import pandas as pd
import streamlit as st

pd.set_option('display.max_columns', None)

# Tab 1
st.set_page_config(page_title="Tab 1: General Statistics")

st.header("General Statistic")

#path = r"D:/UCD/classes/Sports & Performance Analytics/Sports Analytics Tool/"
filename = "general_statistics.csv"
#df1 = pd.read_csv(path + filename)
df1 = pd.read_csv(filename)

df1.drop(["Unnamed: 0","hand","ioc"],axis=1,inplace=True)
df1.rename(columns={"dob":"date_of_birth"},inplace=True)

players = df1["name"]
option_player1 = st.selectbox(label="Please choose your player", options=players)
option_player2 = st.selectbox(label="Please choose your opponent", options=players)

#player_stats=pd.Series({"ID":df1[(df1.name==option_player1)].player_id,"Hand":df1[(df1.name==option_player1)].hand,"Date of Birth":df1[(df1.name==option_player1)].dob,"Nationality":df1[(df1.name==option_player1)].ioc,"Rank":df1[(df1.name==option_player1)].rank,"Points":df1[(df1.name==option_player1)].points,"Number of Wins":df1[(df1.name==option_player1)].wins,"Number of Losses":df1[(df1.name==option_player1)].losses,"Total Number of Games":df1[(df1.name==option_player1)].total})
#opponent_stats=pd.Series({"ID":df1[(df1.name==option_player2)].player_id,"Hand":df1[(df1.name==option_player2)].hand,"Date of Birth":df1[(df1.name==option_player2)].dob,"Nationality":df1[(df1.name==option_player2)].ioc,"Rank":df1[(df1.name==option_player2)].rank,"Points":df1[(df1.name==option_player2)].points,"Number of Wins":df1[(df1.name==option_player2)].wins,"Number of Losses":df1[(df1.name==option_player2)].losses,"Total Number of Games":df1[(df1.name==option_player2)].total})
#combined=pd.DataFrame({'{}'.format(option_player1):player_stats, '{}'.format(option_player2):opponent_stats})

if option_player1!=option_player2:
    player_stats=df1[df1["name"]==option_player1].iloc[:,:-1]
    opponent_stats=df1[df1["name"]==option_player2].iloc[:,:-1]
    combined=pd.concat([player_stats,opponent_stats],ignore_index=True).T
    combined.columns=[option_player1,option_player2]
    st.table(combined)
else:
    player_stats=df1[df1["name"]==option_player1]
    player_stats=player_stats.set_index("name")
    st.table(player_stats.T)
