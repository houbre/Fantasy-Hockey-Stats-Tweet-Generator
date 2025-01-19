import ExtractSkatersStats
import TransformSkaterStats
import LoadCsvIntoDB
import CreateSeasonFantasyRankings
import SaveTop20FantasyPlayersAsImage
import PostImageToTwitter
import argparse
from datetime import date

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

    # Create postgres table with aggregated data using only fanatsy relevant columns
    CreateSeasonFantasyRankings.main(Password)
    SaveTop20FantasyPlayersAsImage.main(Password)
    print("successfully created the fantasy season rankings table! \n")


    # Post image to twitter
    today = date.today()

    TwitterPost = f"Top 20 fantasy players in Ligue du Collège. The rankings are calculated following the games played on {today}. #bergtropfort"
    Top20RankingsImg = "./images/Top20FantasyPlayers_20242025_season.png"
    PostImageToTwitter.main(TwitterPost, Top20RankingsImg)


if __name__ == '__main__':
    main()