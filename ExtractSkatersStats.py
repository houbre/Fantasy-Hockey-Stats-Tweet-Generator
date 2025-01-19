import pandas as pd
import requests
import json

BASE_URL = "https://api.nhle.com/stats/rest/en/skater"

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

    # Get skaters summary data
    SkatersSummaryData = GetSkatersSummaryStats()
    SkatersSummaryStatsDf = pd.DataFrame(SkatersSummaryData)
    SkatersSummaryStatsDf.to_csv(f"./CsvFiles/SkaterSummaryStats.csv", index=False)
    print(f"Skater summary statistics have been successfully saved.")

    # Get skaters summary data
    SkatersMiscellaneousStats = GetSkatersMiscellaneousStats()
    SkatersMiscellaneousStatsDf = pd.DataFrame(SkatersMiscellaneousStats)
    SkatersMiscellaneousStatsDf.to_csv(f"./CsvFiles/SkatersMiscellaneousStats.csv", index=False)
    print(f"Skater miscellaneous statistics have been successfully saved.\n")

if __name__ == '__main__':
    main()