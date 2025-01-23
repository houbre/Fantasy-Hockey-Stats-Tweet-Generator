import pandas as pd
import requests
import json
from datetime import date, timedelta

BASE_URL = "https://api.nhle.com/stats/rest/en/skater"

def GetYesterdayGamesId():

    today = date.today()
    yesterday = today - timedelta(days=1)

    URL =  f"https://api-web.nhle.com/v1/score/{yesterday}"
    response = requests.get(URL)

    if response.status_code == 200:
        data = response.json()
        game_ids = [game['id'] for game in data['games']]
        return game_ids
    else:
        raise Exception(f'Unable to fetch gameIds for todays date')
    
def GetSkatersSummaryStatsForSpecificGameIds(GameIds):

    combined_data = []

    for id in GameIds:
        URL = BASE_URL + f"/summary?limit=-1&cayenneExp=gameId={id}"
        response = requests.get(URL)

        if response.status_code == 200:
            data = response.json()['data']
            combined_data.extend(data)
        else:
            raise Exception(f'Unable to fetch the summary stats for gameId {id}')
        
    return combined_data


def GetSkatersMiscellaneousStatsForSpecificGameIds(GameIds):

    combined_data = []

    for id in GameIds:
        URL = BASE_URL + f"/realtime?limit=-1&cayenneExp=gameId={id}"
        response = requests.get(URL)

        if response.status_code == 200:
            data = response.json()['data']
            combined_data.extend(data)
        else:
            raise Exception(f'Unable to fetch the miscellaneous stats for gameId {id}')
        
    return combined_data
        

def GetSkatersSummaryStats():

    URL = BASE_URL + "/summary?limit=-1&cayenneExp=seasonId=20242025%20and%20gameTypeId=2"

    response = requests.get(URL)

    if response.status_code == 200:
        data =  response.json()
        return data['data']
    else:
        raise Exception(f'Unable to fetch skaters summary statistics')
    

def GetSkatersMiscellaneousStats():

    URL = BASE_URL + "/realtime?limit=-1&cayenneExp=seasonId=20242025%20and%20gameTypeId=2"

    response = requests.get(URL)

    if response.status_code == 200:
        data =  response.json()
        return data['data']
    else:
        raise Exception(f'Unable to fetch skaters miscellaneous statistics')


def main():

    # Get skaters summary data for the current season
    SkatersSummaryData = GetSkatersSummaryStats()
    SkatersSummaryStatsDf = pd.DataFrame(SkatersSummaryData)
    SkatersSummaryStatsDf.to_csv(f"./CsvFiles/SkaterSummaryStats.csv", index=False)
    print(f"Skater summary statistics have been successfully saved.\n")

    # Get skaters summary data for the current season
    SkatersMiscellaneousStats = GetSkatersMiscellaneousStats()
    SkatersMiscellaneousStatsDf = pd.DataFrame(SkatersMiscellaneousStats)
    SkatersMiscellaneousStatsDf.to_csv(f"./CsvFiles/SkatersMiscellaneousStats.csv", index=False)
    print(f"Skater miscellaneous statistics have been successfully saved.\n")

    # Get skaters summary data for yesterday's games
    GameIds = GetYesterdayGamesId()
    SkatersSummaryGameData = GetSkatersSummaryStatsForSpecificGameIds(GameIds)
    SkatersSummaryGameStatsDf = pd.DataFrame(SkatersSummaryGameData)
    SkatersSummaryGameStatsDf.to_csv(f"./CsvFiles/SkatersSummaryGameStats.csv", index=False)
    print(f"Skater summary statistics for yesterday's games have been successfully saved.\n")

    # Get skaters Miscellaneous data for yesterday's games
    SkatersMiscellaneousGameData = GetSkatersMiscellaneousStatsForSpecificGameIds(GameIds)
    SkatersMiscellaneousGameStatsDf = pd.DataFrame(SkatersMiscellaneousGameData)
    SkatersMiscellaneousGameStatsDf.to_csv(f"./CsvFiles/SkatersMiscellaneousGameStats.csv", index=False)
    print(f"Skater Miscellaneous statistics for yesterday's games have been successfully saved.\n")

if __name__ == '__main__':
    main()