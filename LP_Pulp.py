import pandas as pd
pd.options.display.max_rows = 999
pd.options.display.max_columns = 999

import numpy as np

from pulp import *

import re

def create_dec_var(df):
    decision_variables = []
    
    for rownum, row in df.iterrows():
        variable = str('x' + str(rownum))
        variable = pulp.LpVariable(str(variable), lowBound = 0, upBound = 1, cat= 'Integer') #make variables binary
        decision_variables.append(variable)
                                  
    return decision_variables

def total_points(df,lst,prob):
    total_points = ""
    for rownum, row in df.iterrows():
        for i, player in enumerate(lst):
            if rownum == i:
                formula = row['Points']*player
                total_points += formula

    prob += total_points
    
    return prob

def cash(df,lst,prob,avail_cash=1000):
    total_paid = ""
    for rownum, row in df.iterrows():
        for i, player in enumerate(lst):
            if rownum == i:
                formula = row['Cost']*player
                total_paid += formula
    prob += (total_paid <= avail_cash), "Cash"
    
    return prob

def team_gkp(df,lst,prob,avail_gk=2):
    total_gk = ""
    for rownum, row in df.iterrows():
        for i, player in enumerate(lst):
            if rownum == i:
                if row['Position'] == 'GKP':
                    formula = 1*player
                    total_gk += formula

    prob += (total_gk == avail_gk), "GK"
    
    return prob

def team_def(df,lst,prob,avail_def=5):
    total_def = ""
    for rownum, row in df.iterrows():
        for i, player in enumerate(lst):
            if rownum == i:
                if row['Position'] == 'DEF':
                    formula = 1*player
                    total_def += formula

    prob += (total_def == avail_def), "DEF"
    
    return prob

def team_mid(df,lst,prob,avail_mid=5):
    total_mid = ""
    for rownum, row in df.iterrows():
        for i, player in enumerate(lst):
            if rownum == i:
                if row['Position'] == 'MID':
                    formula = 1*player
                    total_mid += formula

    prob += (total_mid == avail_mid), "MID"
    
    return prob

def team_fwd(df,lst,prob,avail_fwd=3):
    total_fwd = ""
    for rownum, row in df.iterrows():
        for i, player in enumerate(lst):
            if rownum == i:
                if row['Position'] == 'FWD':
                    formula = 1*player
                    total_fwd += formula

    prob += (total_fwd == avail_fwd), "FWD"
    
    return prob

def team_num(df,lst,prob):
    
    team_dict= {}
    for team in set(df.Team_code):
        team_dict[str(team)]=dict()
        team_dict[str(team)]['avail'] = 3
        team_dict[str(team)]['total'] = ""
        for rownum, row in df.iterrows():
            for i, player in enumerate(lst):
                if rownum == i:
                    if row['Team_code'] == team:
                        formula = 1*player
                        team_dict[str(team)]['total'] += formula

    prob += (team_dict[str(team)]['total'] <= team_dict[str(team)]['avail']), "Team_limit"
    
    return prob

def LP_optimize(df, prob):
    prob.writeLP('FantasyTeam.lp')
    
    optimization_result = prob.solve()
    assert optimization_result == pulp.LpStatusOptimal

    print("Status:", LpStatus[prob.status])
    
def find_prob(df,ca,gk,de,mi,fw):
    
    prob = pulp.LpProblem('FantasyTeam', pulp.LpMaximize)
    lst = create_dec_var(df)
    
    prob = total_points(df,lst,prob)
    prob = cash(df,lst,prob,ca)
    prob = team_gkp(df,lst,prob,gk)
    prob = team_def(df,lst,prob,de)
    prob = team_mid(df,lst,prob,mi)
    prob = team_fwd(df,lst,prob,fw)
    prob = team_num(df,lst,prob)
    
    return prob


def df_decision(df,prob):
    variable_name = []
    variable_value = []

    for v in prob.variables():
        variable_name.append(v.name)
        variable_value.append(v.varValue)

    df2 = pd.DataFrame({'variable': variable_name, 'value': variable_value})
    for rownum, row in df2.iterrows():
        value = re.findall(r'(\d+)', row['variable'])
        df2.loc[rownum, 'variable'] = int(value[0])

    df2 = df2.sort_index(by='variable')

    #append results
    for rownum, row in df.iterrows():
        for results_rownum, results_row in df2.iterrows():
            if rownum == results_row['variable']:
                df.loc[rownum, 'Decision'] = results_row['value']

    return df