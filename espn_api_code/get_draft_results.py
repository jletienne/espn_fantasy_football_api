import requests
import pandas as pd

def get_draft_results(swid, espn_s2, league_id, year):

    url = "https://fantasy.espn.com/apis/v3/games/ffl/seasons/" + str(year) + "/segments/0/leagues/" + str(league_id)

    r = requests.get(url,cookies={"swid": swid, "espn_s2": espn_s2}, params={"view": "mDraftDetail"})
    a = r.json()

    picks =  a['draftDetail']['picks']


    draft = [{'player_id': pick['playerId'],
    'pick_number': pick['id'],
    'round': pick['roundId'],
    'roundPickNumber': pick['roundPickNumber'],
    'team_id': pick['teamId']} for pick in picks]

    draft_results = pd.DataFrame(draft)

    draft_results.to_csv("prod_data/draft_results.csv", index=False)

    print('draft results are done')
    return None

if __name__ == '__main__':
    get_draft_results()
