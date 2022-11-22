import pandas as pd
import requests

def organize_team_stats(team_info):

    return None

def get_team_stats(swid, espn_s2, league_id, year, week_start, week_end, team_info):
    url = "https://fantasy.espn.com/apis/v3/games/ffl/seasons/" + str(year) + "/segments/0/leagues/" + str(league_id)
    r = requests.get(url, cookies={"swid": swid,"espn_s2": espn_s2},  params={"view": "mMatchupScore"})
    x = r.json()

    team_stats = [[
            game['matchupPeriodId'],
            game['home']['teamId'], game['home']['totalPoints'],
            game['away']['teamId'], game['away']['totalPoints']
        ] for game in x['schedule']]

    team_stats = pd.DataFrame(team_stats, columns=['Week', 'Team1', 'Score1', 'Team2', 'Score2'])
    team_stats['Type'] = ['Regular' if w<=14 else 'Playoff' for w in team_stats['Week']]

    team_stats2 = team_stats.copy()
    team_stats2.columns = ['Week', 'Opp_Team', 'Points_Against', 'team_id', 'Points', 'Type']
    team_stats.columns = ['Week', 'team_id', 'Points', 'Opp_Team', 'Points_Against', 'Type']
    team_stats2 = team_stats2[['Week', 'team_id', 'Points', 'Opp_Team', 'Points_Against', 'Type']]
    team_stats_final = pd.concat([team_stats, team_stats2] , ignore_index=True)
    team_stats_final.drop_duplicates()
    team_stats_final.to_csv('raw_data/fantasy_team_stats.csv', index=False)

    final_team = team_stats_final.merge(team_info)
    final_team
    final_team.to_csv('prod_data/fantasy_team_stats.csv', index=False)

    print('team data is done')
    return None
