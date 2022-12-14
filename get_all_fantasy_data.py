import yaml
import datetime

from espn_api_code.get_expected_wins import get_expected_wins
from espn_api_code.get_team_info import get_team_info
from espn_api_code.get_player_stats import get_player_stats
from espn_api_code.get_team_stats import get_team_stats
from espn_api_code.get_draft_results import get_draft_results

year = 2022

first_thursday_of_season = datetime.datetime(2022, 9, 8) # Date of First Thursday
days_in_season_elapsed = datetime.datetime.today() - first_thursday_of_season

week_start = 1
week_end = 13 #days_in_season_elapsed.days // 7 + 1 #pulls the week number

config = yaml.safe_load(open('config.yaml'))


swid = config['SWID']
espn_s2 = config['espn_s2']

league_id = config['league_id']


team_info = get_team_info(swid, espn_s2, league_id, year)

get_player_stats(swid, espn_s2, league_id, year, week_start, week_end, team_info)

get_team_stats(swid, espn_s2, league_id, year, week_start, week_end, team_info)

get_expected_wins(week_end)

get_draft_results(swid, espn_s2, league_id, year)
