import pandas as pd
pd.options.display.max_rows = 999
pd.options.display.max_columns = 999

import json
import requests
import numpy as np

from pulp import *
import unidecode

import re

def remove_accents(a):
    return unidecode.unidecode(a)


def make_df_from_json(file):
    data = pd.read_json(file, typ='series')

    df = pd.DataFrame(data['elements'])
    df = df[['bonus', 'element_type', 'web_name', 'creativity', 'influence', 'threat', \
             'ict_index', 'team', 'now_cost', 'goals_conceded', 'goals_scored', 'assists', 'own_goals',
             'penalties_missed',
             'penalties_saved', 'saves', 'yellow_cards', 'red_cards', \
             'points_per_game', 'selected_by_percent', 'minutes', 'total_points']]

    pos_dict = {1: 'GKP', 2: 'DEF', 3: 'MID', 4: 'FWD'}
    team_dict = {1: 'ARS', 2: 'BOU', 3: 'BHA', 4: 'BUR', 5: 'CAR', 6: 'CHE', 7: 'CRY', 8: 'EVE', 9: 'FUL', 10: 'HUD', \
                 11: 'LEI', 12: 'LIV', 13: 'MCI', 14: 'MUN', 15: 'NEW', 16: 'SOU', 17: 'TOT', 18: 'WAT', 19: 'WHU',
                 20: "WOL"}

    df['position'] = df['element_type'].apply(lambda x: pos_dict[x])
    df['team_name'] = df['team'].apply(lambda x: team_dict[x])

    df.drop(['element_type', 'team'], inplace=True, axis=1)

    df.rename(columns={'web_name': 'Name', 'team_name': 'Team', 'position': 'Position', 'now_cost': 'Cost', \
                       'creativity': 'Creativity', 'influence': 'Influence', 'threat': 'Threat', \
                       'ict_index': 'ICT', 'goals_conceded': 'Goals_conceded', 'goals_scored': 'Goals_scored', \
                       'assists': 'Assists', 'own_goals': 'Own_goals', 'penalties_missed': 'Penalties_missed', \
                       'penalties_saved': 'Penalties_saved', 'saves': 'Saves', 'yellow_cards': 'Yellow_cards',
                       'red_cards': 'Red_cards', 'selected_by_percent': 'TSB', 'minutes': 'Minutes', \
                       'bonus': 'Bonus', 'total_points': 'Points'}, inplace=True)

    df.sort_values('Name', inplace=True)
    df['Name'] = df['Name'].apply(remove_accents)
    df.reset_index(inplace=True, drop=True)

    df = df[['Name', 'Team', 'Position', 'Cost', 'Creativity', 'Influence', 'Threat', 'ICT', \
             'Goals_conceded', 'Goals_scored', 'Assists', 'Own_goals', 'Penalties_missed', \
             'Penalties_saved', 'Saves', 'Yellow_cards', 'Red_cards', \
             'TSB', 'Minutes', 'Bonus', 'Points']]

    return df


def make_df_from_url(url):
    r = requests.get(url)
    data = json.loads(r.text)

    df = pd.DataFrame(data['elements'])
    df = df[['bonus', 'element_type', 'web_name', 'creativity', 'influence', 'threat', \
             'ict_index', 'team', 'now_cost', 'goals_conceded', 'goals_scored', 'assists', 'own_goals',
             'penalties_missed',
             'penalties_saved', 'saves', 'yellow_cards', 'red_cards', \
             'points_per_game', 'selected_by_percent', 'minutes', 'total_points']]

    pos_dict = {1: 'GKP', 2: 'DEF', 3: 'MID', 4: 'FWD'}
    team_dict = {1: 'ARS', 2: 'BOU', 3: 'BHA', 4: 'BUR', 5: 'CAR', 6: 'CHE', 7: 'CRY', 8: 'EVE', 9: 'FUL', 10: 'HUD', \
                 11: 'LEI', 12: 'LIV', 13: 'MCI', 14: 'MUN', 15: 'NEW', 16: 'SOU', 17: 'TOT', 18: 'WAT', 19: 'WHU',
                 20: "WOL"}

    df['position'] = df['element_type'].apply(lambda x: pos_dict[x])
    df['team_name'] = df['team'].apply(lambda x: team_dict[x])

    df.drop(['element_type', 'team'], inplace=True, axis=1)

    df.rename(columns={'web_name': 'Name', 'team_name': 'Team', 'position': 'Position', 'now_cost': 'Cost', \
                       'creativity': 'Creativity', 'influence': 'Influence', 'threat': 'Threat', \
                       'ict_index': 'ICT', 'goals_conceded': 'Goals_conceded', 'goals_scored': 'Goals_scored', \
                       'assists': 'Assists', 'own_goals': 'Own_goals', 'penalties_missed': 'Penalties_missed', \
                       'penalties_saved': 'Penalties_saved', 'saves': 'Saves', 'yellow_cards': 'Yellow_cards',
                       'red_cards': 'Red_cards', 'selected_by_percent': 'TSB', 'minutes': 'Minutes', \
                       'bonus': 'Bonus', 'total_points': 'Points'}, inplace=True)

    df.sort_values('Name', inplace=True)
    df['Name'] = df['Name'].apply(remove_accents)
    df.reset_index(inplace=True, drop=True)

    df = df[['Name', 'Team', 'Position', 'Cost', 'Creativity', 'Influence', 'Threat', 'ICT', \
             'Goals_conceded', 'Goals_scored', 'Assists', 'Own_goals', 'Penalties_missed', \
             'Penalties_saved', 'Saves', 'Yellow_cards', 'Red_cards', \
             'TSB', 'Minutes', 'Bonus', 'Points']]

    return df

if __name__ == "__main__":

    df = make_df_from_url("https://fantasy.premierleague.com/drf/bootstrap-static")
    
    df.to_csv('data/FPL_2018_19_new_dump.csv',index=False,header=True)

    #print(df.head())
    
    #df.to_json('data/FPL_data_WK2_17-18.json')
    
    #df = make_df_from_json('data/FPL_data_WK2_17-18.json')
    
    #df.to_csv('data/FPL_2018_19_Wk2.csv')
    
    