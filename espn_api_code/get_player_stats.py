import pandas as pd
import requests
import os

def organize_player_stats(team_info):
    file_list = []
    for root, dirs, files in os.walk("raw_data"):
        if root == 'raw_data':
            for filename in files:
                file_list.append(filename)

    player_files = [file for file in file_list if 'player_stats_week_' in file]


    final_player_stats = pd.DataFrame()

    for file in player_files:
        a = pd.read_csv('raw_data/'+file)
        final_player_stats = final_player_stats.append(a)

    final_player_stats = final_player_stats.merge(team_info)
    final_player_stats = final_player_stats.drop_duplicates()

    fantasy_positions = pd.read_csv('prod_data/espn_fantasy_positions.csv')
    actual_positions = pd.read_csv('prod_data/espn_actual_positions.csv')

    final_player_stats = final_player_stats.merge(fantasy_positions)
    final_player_stats = final_player_stats.merge(actual_positions)

    final_player_stats.to_csv("prod_data/player_stats.csv", index=False)

    return None

def get_player_stats(swid, espn_s2, league_id, year, week_start, week_end, team_info):
    for week in range(week_start,week_end):
        url = f'https://fantasy.espn.com/apis/v3/games/ffl/seasons/2022/segments/0/leagues/{league_id}?scoringPeriodId={week}&view=mRoster'
        r = requests.get(url, cookies={"swid": swid,"espn_s2": espn_s2})
        x = r.json()


        player_data = pd.DataFrame()


        for team in x['teams']:

            #nplayers = len()

            for player in team['roster']['entries']:

                actual_points_source_id = 0
                actual_points_list = [i for i in player['playerPoolEntry']['player']['stats'] if i['statSourceId'] == actual_points_source_id and i['scoringPeriodId'] ==  week]
                try:
                    actual_points = actual_points_list[0]['appliedTotal']
                except:
                    actual_points = 0

                projected_points_source_id = 1
                projected_points_list = [i for i in player['playerPoolEntry']['player']['stats'] if i['statSourceId'] == projected_points_source_id and i['scoringPeriodId'] ==  week]
                try:
                    projected_points = projected_points_list[0]['appliedTotal']
                except:
                    projected_points = 0



                new_row = {
                'week': week,
                'player_id': player['playerId'],
                'player_name': player['playerPoolEntry']['player']['fullName'],
                'player_SlotId': player['lineupSlotId'],
                'player_position': player['playerPoolEntry']['player']['defaultPositionId'],
                'team_id': team['id'],
                'player_team': player['playerPoolEntry']['player']['proTeamId'],
                'actual_points': round(actual_points,2),
                'projected_points': round(projected_points,1)

                }

                player_data = player_data.append(new_row, ignore_index=True)


        player_data=player_data[[
               'week', 'player_id', 'player_name', 'player_SlotId', 'actual_points',
               'player_position', 'player_team', 'projected_points',
               'team_id']]

        player_data.to_csv(f'raw_data/player_stats_week_{week}.csv', index=False)


    organize_player_stats(team_info)

    print('player data is done')
    return None
