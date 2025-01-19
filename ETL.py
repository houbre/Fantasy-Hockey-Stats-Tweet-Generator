import ExtractSkatersStats
import TransformSkaterStats
import LoadCsvIntoDB
import CreateSeasonFantasyRankings
import DisplayTop20FantasyPlayers
import argparse

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
    DisplayTop20FantasyPlayers.main(Password)
    print("successfully created the fantasy season rankings table! \n")


if __name__ == '__main__':
    main()