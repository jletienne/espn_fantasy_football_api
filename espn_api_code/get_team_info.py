
import pandas as pd
import requests

def get_team_info(swid, espn_s2, league_id, year):
    url = "https://fantasy.espn.com/apis/v3/games/ffl/seasons/" + str(year) + "/segments/0/leagues/" + str(league_id)

    r = requests.get(url, cookies={"swid": swid,"espn_s2": espn_s2},  params={"view": "mTeams"})


    a = r.json()

    team_info = pd.DataFrame()

    team_info = team_info.append(a['teams'], ignore_index=True)
    team_info['team_name'] =  team_info['location'] + ' ' +  team_info['nickname']


    team_info = team_info[['id', 'abbrev', 'team_name']]
    team_info.columns = ['team_id', 'manager', 'team_name']
    team_info.to_csv('prod_data/team_info.csv', index=False)

    print('team info is done')

    return team_info
