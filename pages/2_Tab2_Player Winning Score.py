# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 13:59:47 2022

@author: Huzihu
"""

import pandas as pd
import streamlit as st

pd.set_option('display.max_columns', None)

# Tab 2
st.set_page_config(page_title="Tab 2: Player Winning Score")

st.header("Player Scheduling Optimization")

#path = r"D:/UCD/classes/Sports & Performance Analytics/Sports Analytics Tool/"
filename = "all_matches.csv"
#df2 = pd.read_csv(path + filename, header = [0])
df2 = pd.read_csv(filename)

# drop missing values
df_cleaned = df2.dropna()

h2h = df_cleaned[['player_id','opponent_id','player_victory']].copy(deep=True)
metrics_avg = df_cleaned[['player_id','serve_rating','return_rating']].copy(deep=True)
metrics_sum = df_cleaned[['player_id','tiebreaks_won','tiebreaks_total','break_points_made','break_points_attempted']].copy(deep=True)
stats_avg = metrics_avg.groupby('player_id').mean()
stats_sum = metrics_sum.groupby('player_id').sum()
stats_sum['tiebreak_per'] = stats_sum.apply(lambda row: row.tiebreaks_won / row.tiebreaks_total, axis=1)
stats_sum['breakpt_per'] = stats_sum.apply(lambda row: row.break_points_made / row.break_points_attempted, axis=1)
stats_sum['tiebreak_per'] = stats_sum['tiebreak_per'].fillna(0)
stats_sum['breakpt_per'] = stats_sum['breakpt_per'].fillna(0)
# features used
stats = pd.merge(stats_avg, stats_sum, on='player_id')

players = stats.index.values
option_player1 = st.selectbox(label="Please choose your player", options=players)
option_player2 = st.selectbox(label="Please choose your opponent", options=players)

# h2h_p -> head to head wins for player, h2h_o -> head to head wins for opponent, h2h_t -> head to head total 
# total number of head to head games for the selected player
a=h2h[(h2h.player_id==option_player1) & (h2h.opponent_id==option_player2)]
h2h_t=a.shape[0]

# selected player won in the head to head game
a=h2h[(h2h.player_id==option_player1) & (h2h.opponent_id==option_player2) & (h2h.player_victory=='t')]
h2h_p=a.shape[0]

# selected player lost in the head to head game
a=h2h[(h2h.player_id==option_player1) & (h2h.opponent_id==option_player2)& (h2h.player_victory=='f')]
h2h_o=a.shape[0]

h2h_stats = pd.Series({"total number of head to head games for the selected player vs opponent":h2h_t, "number of head to head wins for the selected player vs opponent":h2h_p,"number of head to head loses for the selected player vs opponent":h2h_o})
h2h_stats = pd.DataFrame(h2h_stats, columns=['number'])
st.table(h2h_stats)

player_stats=pd.Series({"Serve Rating":stats[(stats.index==option_player1)].serve_rating,"Return Rating":stats[(stats.index==option_player1)].return_rating,"Tiebreaker Percentage":stats[(stats.index==option_player1)].tiebreak_per,"Breakpoint Percentage":stats[(stats.index==option_player1)].breakpt_per})
opponent_stats=pd.Series({"Serve Rating":stats[(stats.index==option_player2)].serve_rating,"Return Rating":stats[(stats.index==option_player2)].return_rating,"Tiebreaker Percentage":stats[(stats.index==option_player2)].tiebreak_per,"Breakpoint Percentage":stats[(stats.index==option_player2)].breakpt_per})
player_stats=player_stats.astype(float)
opponent_stats=opponent_stats.astype(float)
combined=pd.DataFrame({'{}'.format(option_player1):player_stats, '{}'.format(option_player2):opponent_stats})

st.table(combined)

# formula used to calculate winning score

try:
    player_1=(0.4*(h2h_p/h2h_t)) + (0.2*0.01*stats[(stats.index==option_player1)].serve_rating) + (0.2*0.01*stats[(stats.index==option_player1)].return_rating) + (0.05*stats[(stats.index==option_player1)].tiebreak_per) + (0.05*stats[(stats.index==option_player1)].breakpt_per)
    player_2=(0.4*(h2h_o/h2h_t)) + (0.2*0.01*stats[(stats.index==option_player2)].serve_rating) + (0.2*0.01*stats[(stats.index==option_player2)].return_rating) + (0.05*stats[(stats.index==option_player2)].tiebreak_per) + (0.05*stats[(stats.index==option_player2)].breakpt_per)
    players_score=pd.DataFrame({'{}'.format(option_player1):player_1.values, '{}'.format(option_player2):player_2.values})
    players_score.index=["winning score"]
    st.table(players_score)
    if player_1.values > player_2.values:
        st.header("{} has better chance of winning than {}".format(option_player1,option_player2))
    elif player_1.values < player_2.values:
        st.header("{} has better chance of winning than {}".format(option_player2,option_player1))
    else:
        st.header("Players have equal chance of winning.")
except ZeroDivisionError:
    player_1=(0.4*0.01*stats[(stats.index==option_player1)].serve_rating) + (0.4*0.01*stats[(stats.index==option_player1)].return_rating) + (0.1*stats[(stats.index==option_player1)].tiebreak_per) + (0.1*stats[(stats.index==option_player1)].breakpt_per)
    player_2=(0.4*0.01*stats[(stats.index==option_player2)].serve_rating) + (0.4*0.01*stats[(stats.index==option_player2)].return_rating) + (0.1*stats[(stats.index==option_player2)].tiebreak_per) + (0.1*stats[(stats.index==option_player2)].breakpt_per)
    players_score=pd.DataFrame({'{}'.format(option_player1):player_1.values, '{}'.format(option_player2):player_2.values})
    players_score.index=["winning score"]
    st.table(players_score)
    if player_1.values > player_2.values:
        st.header("{} has better chance of winning than {}".format(option_player1,option_player2))
    elif player_1.values < player_2.values:
        st.header("{} has better chance of winning than {}".format(option_player2,option_player1))
    else:
        st.header("Players have equal chance of winning.")
        

