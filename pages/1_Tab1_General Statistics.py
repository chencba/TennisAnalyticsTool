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

df1.drop(["Unnamed: 0"],axis=1,inplace=True)
df1["dob"]=df1["dob"].astype(int)
df1["rank"]=df1["rank"].astype(int)
df1["points"]=df1["points"].astype(int)
df1["wins"]=df1["wins"].astype(int)
df1["losses"]=df1["losses"].astype(int)
df1["total"]=df1["total"].astype(int)

ranks = df1.sort_values("rank")[["name","rank"]].reset_index()
ranks.drop("index", axis=1, inplace=True)

players = df1["name"]
option_player = st.selectbox(label="Please choose your player", options=players)

#player_stats=pd.Series({"ID":df1[(df1.name==option_player1)].player_id,"Hand":df1[(df1.name==option_player1)].hand,"Date of Birth":df1[(df1.name==option_player1)].dob,"Nationality":df1[(df1.name==option_player1)].ioc,"Rank":df1[(df1.name==option_player1)].rank,"Points":df1[(df1.name==option_player1)].points,"Number of Wins":df1[(df1.name==option_player1)].wins,"Number of Losses":df1[(df1.name==option_player1)].losses,"Total Number of Games":df1[(df1.name==option_player1)].total})
#opponent_stats=pd.Series({"ID":df1[(df1.name==option_player2)].player_id,"Hand":df1[(df1.name==option_player2)].hand,"Date of Birth":df1[(df1.name==option_player2)].dob,"Nationality":df1[(df1.name==option_player2)].ioc,"Rank":df1[(df1.name==option_player2)].rank,"Points":df1[(df1.name==option_player2)].points,"Number of Wins":df1[(df1.name==option_player2)].wins,"Number of Losses":df1[(df1.name==option_player2)].losses,"Total Number of Games":df1[(df1.name==option_player2)].total})
#combined=pd.DataFrame({'{}'.format(option_player1):player_stats, '{}'.format(option_player2):opponent_stats})

player_stats=df1[df1["name"]==option_player]
#player_stats=player_stats.set_index("name")
col1, col2, col3, col4 = st.columns([2,2,2,2])
col1.metric("Country", player_stats["ioc"].iloc[0])
col1.metric("Hand", player_stats["hand"].iloc[0])
col1.metric("Date Of Birth", player_stats["dob"])
col2.metric("Rank", player_stats["rank"])
col2.metric("Points", player_stats["points"])
col3.metric("Games Won", player_stats["wins"])
col3.metric("Games Lost", player_stats["losses"])
col3.metric("Total Games", player_stats["total"])
ix = ranks[ranks["name"]==option_player].index[0]
col4.subheader("Players who Ranked before This Player")
col4.dataframe(ranks.iloc[:ix+1, :])
