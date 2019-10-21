# -*- coding: utf-8 -*-
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
@st.cache
def get_data():
    # NBA season we will be analyzing
    year = 2019
    # URL page we will scraping (see image above)
    url = "https://www.basketball-reference.com/leagues/NBA_{}_per_game.html".format(year)
    # this is the HTML from the given URL
    html = urlopen(url)
    soup = BeautifulSoup(html, features='html.parser')

    # use findALL() to get the column headers
    soup.findAll('tr', limit=2)
    # use getText()to extract the text we need into a list
    headers = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]
    # exclude the first column as we will not need the ranking order from Basketball Reference for the analysis
    headers = headers[1:]
    headers

    # avoid the first header row
    rows = soup.findAll('tr')[1:]
    player_stats = [[td.getText() for td in rows[i].findAll('td')]
                for i in range(len(rows))]

    stats = pd.DataFrame(player_stats, columns = headers)
    stats.head(10)
    stats.dropna(inplace = True)
    return stats
def fantasy_points(dataframe):
  print(dataframe.head())
  dataframe = dataframe.dropna()
  dataframe['PTS'] = pd.to_numeric(dataframe['PTS'])
  dataframe['TRB'] = pd.to_numeric(dataframe['TRB'])
  dataframe['AST'] = pd.to_numeric(dataframe['AST'])
  dataframe['STL'] = pd.to_numeric(dataframe['STL'])
  dataframe['3P'] = pd.to_numeric(dataframe['3P'])
  dataframe['BLK'] = pd.to_numeric(dataframe['BLK'])
  dataframe['TOV'] = pd.to_numeric(dataframe['TOV'])
  dataframe['G'] = pd.to_numeric(dataframe['G'])

  dataframe['pts_points'] = dataframe['PTS'] * 1
  dataframe['TRB_points'] = dataframe['TRB'] * 1.2
  dataframe['AST_points'] = dataframe['AST'] * 1.5
  dataframe['STL_points'] = dataframe['STL'] * 3
  dataframe['3P_points'] = dataframe['3P'] * 3
  dataframe['BLK_points'] = dataframe['BLK'] * 3
  dataframe['TOV_points'] = dataframe['TOV'] * -1
  dataframe['fantasy_points'] = dataframe[['pts_points','TRB_points','AST_points','STL_points','3P_points','BLK_points','TOV_points']].sum(axis = 1)
  dataframe['weighted_value'] = abs((dataframe['G']/dataframe['fantasy_points']) - 1)
  dataframe['total_points_count'] = dataframe['G'] * dataframe['fantasy_points']
  return dataframe
fp_stats = fantasy_points(get_data())
#fp_stats_more_than_15 = fp_stats.loc[fp_stats['G'] > 50]
arranged = fp_stats.sort_values(by = ['fantasy_points'], ascending = False)

#players_to_trade = st.sidebar.multiselect('Enter players to trade',arranged['Player'])
#players_to_recieve = st.sidebar.multiselect('Enter players you will recieve',arranged['Player'])


players_to_trade = st.sidebar.text_input('Enter a player you want to trade')
players_to_recieve = st.sidebar.text_input('Enter a player that you would recieve for the trade')

games_slider=st.sidebar.slider('games played', 0,82,30)
filtered_arranged = arranged[arranged['G'] >= games_slider]

#position = st.text_input('Enter Position abbrev.SG, PF, PG, C, SF, PF-SF, SF-SG, SG-PF, C-PF, SG-SF, PF-C')
#filtered_arranged = filtered_arranged.loc[filtered_arranged['Pos'] == position]
#st.write(filtered_arranged[['Player','G','Pos','Tm','fantasy_points']])


positions = st.sidebar.multiselect('select position', arranged['Pos'].unique())
player_to_drop = st.sidebar.multiselect('Enter name of player to drop',arranged['Player'])
#st.write(type(player_to_drop))

filtered_arranged2 = arranged[(arranged['Pos'].isin(positions)) & (arranged['G'] >= games_slider)]
fun_total_percent = filtered_arranged2['total_points_count'].sum()
filtered_arranged2['scalar_evaluation_value'] = filtered_arranged2['total_points_count'] / fun_total_percent
#player_to_drop = st.sidebar.multiselect('Enter name of player to drop',filtered_arranged2['Player'])
#filtered_arranged2 = filtered_arranged2[~filtered_arranged2['Player'].isin(player_to_drop)]
#filtered_arranged2 = filtered_arranged2[filtered_arranged2.Player != player_to_drop]
st.write(fun_total_percent)
st.write(filtered_arranged2[['Player','G','Pos','Tm','fantasy_points','scalar_evaluation_value']])


#top_10_in_position = filtered_arranged2.sort_values(by =['total_points_count'], ascending = False)
#if st.checkbox('Show Top 10 in positions selected'):
#    st.write(top_10_in_position[['Player','Pos','total_points_count']].head(n=10))
#new_df = df[(df['Club'].isin(clubs)) & (df['Nationality'].isin(nationalities))]
#st.write(new_df)
fp_stats['Pos'].unique()
test = 3
st.write("importance of position")
new_data = arranged.groupby(by = "Pos")['fantasy_points'].mean()
new_data = new_data.to_frame()
new_data.reset_index(inplace = True)
st.write(new_data)
#new_data.iloc[[0,2,5,6,8]]
# library & dataset
#import seaborn as sns
#import numpy as np
# Make boxplot for one group only
#plot = sns.barplot( y=new_data['fantasy_points'], x = new_data['Pos'])
#sns.plt.show()
#st.write(plot)
#sns.plt.show()
"""
drop_test = filtered_arranged
drop_test2 = drop_test[~drop_test['Player'].isin(player_to_drop)]
st.write(drop_test2)
len(arranged)
"""

players_to_trade_df = filtered_arranged2[filtered_arranged2['Player'] == (players_to_trade)]
st.write("this is players_to_trade_df")
st.write(players_to_trade_df[['Player','G','Pos','Tm','fantasy_points','scalar_evaluation_value']])

players_to_recieve_df = filtered_arranged2[filtered_arranged2['Player'] == (players_to_recieve)]
st.write("this is players to be received")
st.write(players_to_recieve_df[['Player','G','Pos','Tm','fantasy_points','scalar_evaluation_value']])

trading_df = players_to_recieve_df.append(players_to_trade_df)

st.write(arranged['PTS'][0] > arranged['PTS'][5])
st.write(trading_df['scalar_evaluation_value'][0] > trading_df['scalar_evaluation_value'][1])

# intialise data of lists.
data = {'Name':['Tom', 'nick', 'krish', 'jack'],
        'Age':[20, 21, 19, 18]}
data2 = {'Name':['Tom', 'nick', 'krish', 'jack'],
        'Age':[21, 22, 20, 19]}
# Create DataFrame
df = pd.DataFrame(data)
df2 = pd.DataFrame(data2)
df['Age'][0] > df2['Age'][1] 







