"""
Author: Daniel Droder
This script when ran will create a webapp that
allows the user to find information about who they should
draft for their fantasy teams. 
"""


from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
@st.cache(suppress_st_warning=True)
def get_basketball_data():
    """
    This function is the webscraper that ,when the user selects
    the basketball portion of the website, scrapes the basketball
    data from the URL specified
    """

    # NBA season we will be analyzing
    year = 2020
    # URL page we will scraping 
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
@st.cache(suppress_st_warning=True)
def get_football_data():
    # NFL season we will be analyzing
    year = 2019
    # URL page we will scraping 
    url = "https://www.pro-football-reference.com/years/{}/fantasy.htm".format(year)
    # this is the HTML from the given URL
    html = urlopen(url)
    soup = BeautifulSoup(html, features='html.parser')

    # use findALL() to get the column headers
    soup.findAll('tr', limit=2)
    # use getText()to extract the text we need into a list
    headers = [th.getText() for th in soup.findAll('tr', limit=2)[1].findAll('th')]
    # exclude the first column as we will not need the ranking order from Football Reference for the analysis
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

def football_compare_trade():
    players_to_trade = st.sidebar.multiselect('Which players are you going to trade?', data_important['Player'].unique())
    players_to_recieve= st.sidebar.multiselect('Which players are you going to recieve?', data_important['Player'].unique())
    players_to_trade_df = data_important[data_important['Player'].isin(players_to_trade)]
    players_to_recieve_df = data_important[data_important['Player'].isin(players_to_recieve)]
    new_df = data_important[(data_important['Player'].isin(players_to_trade)) | (data_important['Player'].isin(players_to_recieve))]
    #st.write(new_df[['Player','G','Pos','Tm','fantasy_points','scalar_evaluation_value']])
    pts_for_give = players_to_trade_df['scalar_evaluation_value'].sum()
    pts_for_recieve = players_to_recieve_df['scalar_evaluation_value'].sum()
    if st.button("Compare your trade?"):
        st.write("your total evaluation")
        st.write(pts_for_give)
        st.write("other persons total evaluation")
        st.write(pts_for_recieve)
        if (pts_for_give - pts_for_recieve) == 0:
            st.header("this is an even trade")
        if (pts_for_give - pts_for_recieve) < 0:
            st.header("this is a favorable trade")
            st.balloons()
        if(pts_for_give - pts_for_recieve) > 0:
            st.header("this is an unfavorable trade")

def football_testing_button_predict_winner():
    if st.button("Compare 2 teams to predict who will win?"):
        your_team_points_estimate = main_users_team_df['total_points'].sum()
        challenger_team_points_estimate = other_users_team_df['total_points'].sum()
        st.header("Your points projection with this team lineup")
        st.write(your_team_points_estimate)
        st.header("Challenger points projection with their team lineup")
        st.write(challenger_team_points_estimate)
        pts_for_users_team = main_users_team_df['scalar_evaluation_value'].sum()
        pts_for_challenger_team= other_users_team_df['scalar_evaluation_value'].sum()
        if your_team_points_estimate < challenger_team_points_estimate:
            st.header("=(")
            st.header("You are likely going to lose this matchup!")
        if  your_team_points_estimate > challenger_team_points_estimate:
            st.header("You are likely going to win this matchup!")
            st.balloons()
        if your_team_points_estimate == challenger_team_points_estimate:
            st.header("Eh,")
            st.header("this is going to be a tie!")

def testing_button_predict_winner():
    if st.button("Compare 2 teams to predict who will win?"):
        your_team_points_estimate = main_users_team_df['fantasy_points'].sum()
        challenger_team_points_estimate = other_users_team_df['fantasy_points'].sum()
        st.header("Your points projection with this team lineup")
        st.write(your_team_points_estimate)
        st.header("Challenger points projection with their team lineup")
        st.write(challenger_team_points_estimate)
        pts_for_users_team = main_users_team_df['scalar_evaluation_value'].sum()
        pts_for_challenger_team= other_users_team_df['scalar_evaluation_value'].sum()
        if your_team_points_estimate < challenger_team_points_estimate:
            st.header("=(")
            st.header("You are likely going to lose this matchup!")
        if  your_team_points_estimate > challenger_team_points_estimate:
            st.header("You are likely going to win this matchup!")
            st.balloons()               
        if your_team_points_estimate == challenger_team_points_estimate:
            st.header("Eh,")
            st.header("this is going to be a tie!")
def compare_trade():
    if st.button("Compare your trade?"):
        st.write("your total evaluation")
        st.write(pts_for_give * 100,"%")
        st.write("other persons total evaluation")
        st.write(pts_for_recieve * 100,"%")
        if (pts_for_give - pts_for_recieve) == 0:
            st.header("this is an even trade")
        if (pts_for_give - pts_for_recieve) < 0:
            st.header("this is a favorable trade")
            st.balloons()
        if(pts_for_give - pts_for_recieve) > 0:
            st.header("this is an unfavorable trade")
def generate_best_picks():
    top_2_in_position = pd.DataFrame()
    top_in_pos_sorted = pd.DataFrame()
    for position in filtered_arranged2['Pos'].unique():
        top_2_in_position2 = (filtered_arranged2.loc[filtered_arranged2['Pos'] == position].head(n=5))
        top_2_in_position = top_2_in_position.append(top_2_in_position2)
        top_in_pos_sorted = top_2_in_position.sort_values(by = ['scalar_evaluation_value'],ascending = False)
        top_in_pos_sorted.reset_index(inplace = True)
        top_in_pos_sorted['Draft Priority'] = (top_in_pos_sorted.index) + 1

    st.write(top_in_pos_sorted[['Player','Pos','Tm','Draft Priority','scalar_evaluation_value']])

def football_best_picks():
    top_2_in_position = pd.DataFrame()
    top_in_pos_sorted = pd.DataFrame()
    for position in data_important['Position'].unique():
        top_2_in_position2 = (data_important.loc[data_important['Position'] == position].head(n=5))
        top_2_in_position = top_2_in_position.append(top_2_in_position2)
        top_in_pos_sorted = top_2_in_position.sort_values(by = ['scalar_evaluation_value'],ascending = False)
        top_in_pos_sorted.reset_index(inplace = True)
        top_in_pos_sorted['Draft Priority'] = (top_in_pos_sorted.index) + 1
    st.write(top_in_pos_sorted[['Player','Position','Team','Draft Priority']])


def basketball_fantasy_points(dataframe):
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



sport = st.sidebar.radio('What sport would you like to analyze?',('Basketball','Football'))

if sport == "Basketball":
    games_slider=st.sidebar.slider('games played', 0,82,0) #to my knowledgte, 82 games in a season which is why 82 is cap
    fp_stats = basketball_fantasy_points(get_basketball_data())
    arranged = fp_stats.sort_values(by = ['fantasy_points'], ascending = False)
    filtered_arranged = arranged[arranged['G'] >= games_slider]



    positions = st.sidebar.multiselect('select position', arranged['Pos'].unique())


    filtered_arranged2 = arranged[(arranged['Pos'].isin(positions)) & (arranged['G'] >= games_slider)]
    fun_total_percent = filtered_arranged2['total_points_count'].sum()
    filtered_arranged2['scalar_evaluation_value'] = filtered_arranged2['total_points_count'] / fun_total_percent
    if st.button("Generate draft picks"):
        try:
            generate_best_picks()
        except:
            st.text("Be sure you have selected positions that you want before generating picks!")
            st.text("To do that, populate the dropdown located on the left hand side called 'Select Position'.")
    st.write(fun_total_percent)
    st.write(filtered_arranged2[['Player','G','Pos','Tm','fantasy_points','scalar_evaluation_value']])

    fp_stats['Pos'].unique()
    if st.button("Check importance of each position?"):
        st.write("importance of position")
        new_data = arranged.groupby(by = "Pos")['fantasy_points'].mean()
        new_data = new_data.to_frame()
        new_data.reset_index(inplace = True)
        st.write(new_data)

    players_to_trade = st.sidebar.multiselect('Which players are you going to trade?', filtered_arranged2['Player'].unique())
    players_to_recieve= st.sidebar.multiselect('Which players are you going to recieve?', filtered_arranged2['Player'].unique())

    players_to_trade_df = filtered_arranged2[filtered_arranged2['Player'].isin(players_to_trade)]
    players_to_recieve_df = filtered_arranged2[filtered_arranged2['Player'].isin(players_to_recieve)]
    new_df = filtered_arranged2[(filtered_arranged2['Player'].isin(players_to_trade)) | (filtered_arranged2['Player'].isin(players_to_recieve))]


    pts_for_give = players_to_trade_df['scalar_evaluation_value'].sum()
    pts_for_recieve = players_to_recieve_df['scalar_evaluation_value'].sum()



    main_users_team = st.sidebar.multiselect("Please enter your team",filtered_arranged2['Player'].unique())
    other_persons_team = st.sidebar.multiselect("Please enter the other players team (team you are comparing yours against)",filtered_arranged2['Player'].unique())
    main_users_team_df = filtered_arranged2[filtered_arranged2['Player'].isin(main_users_team)]
    other_users_team_df = filtered_arranged2[filtered_arranged2['Player'].isin(other_persons_team)]

    compare_trade()
    testing_button_predict_winner()


if sport == "Football":
    data = get_football_data()
    data.columns = ['Player','Team','Position','Age','Games','GS','Passes_Completed','Passes_attempted','Passing_Yards','Passing_Touchdowns','Interceptions_Thrown','Rushing_Attempts','Rushing_Yards_Gained','Rushing_Yards_attempted','Rushing_Touchdowns','Pass_Targets','Receptions','Recieving_Yards','Recieving_Yards_Per_Reception','Recieving_Touchdowns','Fumbles','Fumbles_By_Team','Touchdowns of every Type','2PM','2PP','Fantasy_Points','PPR','DKPt','FDPT','VBD','PosRank','PosOverall']
    data_important = data[['Player','Position','Team','Passing_Yards','Games','Passing_Touchdowns','Interceptions_Thrown','Rushing_Yards_Gained','Rushing_Touchdowns','Receptions','Recieving_Yards','Recieving_Touchdowns']]
    #cast numeric data as numeric
    data_important[['Passing_Yards','Games','Passing_Touchdowns','Interceptions_Thrown','Rushing_Yards_Gained','Rushing_Touchdowns','Receptions','Recieving_Yards','Recieving_Touchdowns']] = data_important[['Passing_Yards','Games','Passing_Touchdowns','Interceptions_Thrown','Rushing_Yards_Gained','Rushing_Touchdowns','Receptions','Recieving_Yards','Recieving_Touchdowns']].apply(pd.to_numeric,axis = 1)
    #begin the calculations (dear god why)
    data_important['passing_yards_pts'] = data_important['Passing_Yards'] / 25
    data_important['passing_touchdown_points'] = data_important['Passing_Touchdowns'] * 4
    data_important['interception_points'] = data_important['Interceptions_Thrown'] * -2
    data_important['rushing_yards_points'] =  data_important['Rushing_Yards_Gained'] / 10
    data_important['rushing_touchdowns_points'] = data_important['Rushing_Touchdowns'] * 6
    data_important['total_points'] = data_important[['passing_yards_pts','passing_touchdown_points','interception_points','rushing_yards_points','rushing_touchdowns_points']].sum(axis = 1)
    data_important['weighted_value'] = (data_important['total_points']/data_important['Games']) - 1
    fun_total_percent = data_important['total_points'].sum()
    data_important['scalar_evaluation_value'] = data_important['total_points'] / fun_total_percent
    main_users_team = st.sidebar.multiselect("Please enter your team",data_important['Player'].unique())
    other_persons_team = st.sidebar.multiselect("Please enter the other players team (team you are comparing yours against)",data_important['Player'].unique())
    main_users_team_df = data_important[data_important['Player'].isin(main_users_team)]
    other_users_team_df = data_important[data_important['Player'].isin(other_persons_team)]

   
    if st.button("Generate Best Picks"):
        football_best_picks()
    football_compare_trade()

    football_testing_button_predict_winner()

    st.write(data_important)




