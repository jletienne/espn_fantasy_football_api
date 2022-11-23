
import pandas as pd
import numpy as np
from sklearn import metrics

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

import datetime

def get_expected_wins(week_end):

    #first_thursday_of_season = datetime.datetime(2022, 9, 8) # Date of First Thursday
    #days_in_season_elapsed = datetime.datetime.today() - first_thursday_of_season
    #week = days_in_season_elapsed.days // 7 + 1 #pulls the week number


    team_data = pd.read_csv('prod_data/fantasy_team_stats.csv')

    team_data = team_data[team_data['Week'] < week_end] #ignore current_week



    fant = team_data.copy() #dataset used for model
    fant = fant[fant['Week'] < week_end] #ignore current_week



    #result is a win
    fant['result'] = (fant['Points'] > fant['Points_Against']).astype(int)

    X = fant[['Points']] #independent variable
    y = fant.result #dependent variable

    #train test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=16)

    # model building
    model = LogisticRegression(random_state=0)
    model.fit(X_train, y_train)
    LogisticRegression(random_state=0)

    #model results
    expected_wins_model = {'intercept': model.intercept_[0], 'coefficient': model.coef_[0][0]}

    #create expected wins column
    team_data['expected_wins'] = 1 / (1+np.exp(-(expected_wins_model['intercept'] + team_data['Points'] * expected_wins_model['coefficient'])))


    #overwrite team data
    team_data.to_csv('prod_data/fantasy_team_stats.csv', index=False)

    expected_wins_df = pd.DataFrame([expected_wins_model])
    expected_wins_df.to_csv('prod_data/expected_wins.csv', index=False)

    print ('expected wins are done')

if __name__ == '__main__':
    get_expected_wins()
