import ExtractSkatersStats
import TransformSkaterStats
import LoadCsvIntoDB
import CreateSeasonFantasyRankings
import SaveTop20FantasyPlayersAsImage
import PostImageToTwitter
import argparse
from datetime import date, timedelta

Top20SeasonRankingsImgPATH = "./images/Top20FantasyPlayers_seasonrankings.png"
Top20DateRankingsImgPATH = "./images/Top20FantasyPlayers_daterankings.png"

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--password", required=True, help="Password to Postgres")

    args =  parser.parse_args()

    return args

def main():
    args = parse_arguments()
    Password=args.password

    # Create postgres table for raw data 
    ExtractSkatersStats.main()
    TransformSkaterStats.main()
    LoadCsvIntoDB.main(Password)
    print("Data was successfully extracted, transformed and loaded into a Postgres database! \n")

    # Create postgres table for season stats with aggregated data using only fanatsy relevant columns
    CreateSeasonFantasyRankings.main(Password, 'season')
    SaveTop20FantasyPlayersAsImage.main(Password, 'seasonrankings')
    print("successfully created the fantasy season rankings table! \n")

    # Create postgres table for date specific stats with aggregated data using only fanatsy relevant columns
    CreateSeasonFantasyRankings.main(Password, 'date')
    SaveTop20FantasyPlayersAsImage.main(Password, 'daterankings')
    print("successfully created the fantasy season rankings table! \n")


    # Post image to twitter
    today = date.today()
    yesterday = today - timedelta(days=1)

    TwitterPost = f"Top 20 fantasy players in Ligue du Collège for yesterday's games and overall this season. The rankings are calculated following the games played on {yesterday}. #bergtropfort"
    PostImageToTwitter.main(TwitterPost, [Top20DateRankingsImgPATH, Top20SeasonRankingsImgPATH])


if __name__ == '__main__':
    main()