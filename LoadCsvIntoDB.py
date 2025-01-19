import psycopg2
import csv
import pandas as pd

SUMMARY_STATS_PATH = "SkaterSummaryStats.csv"
MISCELLANEOUS_STATS_PATH = "SkatersMiscellaneousStats.csv"

def DropTable(Password, TableToDrop):

    print(f'Dropping Table {TableToDrop}...')
    try:
        conn = psycopg2.connect(
                host="localhost",
                dbname="FantasyHockey",
                user="postgres",
                password=Password,
                port="8080"
            )
        cur = conn.cursor()

        DropTable = f"""DROP TABLE IF EXISTS {TableToDrop};"""

        cur.execute(DropTable)
        conn.commit()

        print(f"Table {TableToDrop} successfully dropped! \n")

    except Exception as e:
        print(f"An error occurred while dropping the table: {e}")
    
    finally:
        # Close the connection
        cur.close()
        conn.close()


def CreateDataBase(Password, TableName):

    try:
        print(f'Creating table {TableName}...')
        conn = psycopg2.connect(
                host="localhost",
                dbname="FantasyHockey",
                user="postgres",
                password=Password,
                port="8080"
            )
        cur = conn.cursor()

        if (TableName == 'skatersummarystats'):
        
            NewTable = f"""CREATE TABLE IF NOT EXISTS {TableName}(
                        assists integer,
                        evGoals integer,
                        evPoints integer,
                        faceoffWinPct double precision,
                        gameWinningGoals integer,
                        gamesPlayed integer,
                        goals integer,
                        lastName text,
                        otGoals integer,
                        penaltyMinutes integer,
                        playerId integer PRIMARY KEY,
                        plusMinus integer,
                        points integer,
                        pointsPerGame double precision,
                        positionCode text,
                        ppGoals integer,
                        ppPoints integer,
                        seasonId text,
                        shGoals integer,
                        shPoints integer,
                        shootingPct text,
                        shootsCatches text,
                        shots integer,
                        skaterFullName text,
                        teamAbbrevs text,
                        timeOnIcePerGame double precision
            );"""

        elif (TableName == 'skatermiscellaneousstats'):
                        
            NewTable = f"""CREATE TABLE IF NOT EXISTS {TableName}(
                        blockedShots integer,
                        blockedShotsPer60 double precision,
                        emptyNetAssists double precision,
                        emptyNetGoals integer,
                        emptyNetPoints double precision,
                        firstGoals integer,
                        gamesPlayed integer,
                        giveaways integer,
                        giveawaysPer60 double precision,
                        hits integer,
                        hitsPer60 double precision,
                        lastName text,
                        missedShotCrossbar integer,
                        missedShotGoalpost integer,
                        missedShotOverNet integer,
                        missedShotShort integer,
                        missedShotWideOfNet integer,
                        missedShots integer,
                        otGoals integer,
                        playerId integer PRIMARY KEY,
                        positionCode text,
                        seasonId integer,
                        shootsCatches text,
                        shotAttemptsBlocked integer,
                        skaterFullName text,
                        takeaways integer,
                        takeawaysPer60 double precision,
                        teamAbbrevs text,
                        timeOnIcePerGame double precision
            );"""
        
        else:
            raise Exception(f'Wrong table name provided: {TableName}')

        cur.execute(NewTable)
        conn.commit()

        print(f"Table {TableName} successfully created! \n")

    except Exception as e:
        print(f"An error occurred while creating the table: {e}")
        
    finally:
        # Close the connection
        cur.close()
        conn.close()

   
def LoadCsvToDataBase(Password, Path, TableName):
    try:
        print(f"Loading {TableName} with data...")
        conn = psycopg2.connect(
                host="localhost",
                dbname="FantasyHockey",
                user="postgres",
                password=Password,
                port="8080"
            )
        cur = conn.cursor()

        with open(Path, 'r') as f:
            next(f)
            cur.copy_from(f, TableName, sep=',', null=' ')

        conn.commit()
        print(f"Table {TableName} successfully loaded with data \n")
    
    except Exception as e:
        print(f"An error occurred while creating the table: {e}")
        
    finally:
        cur.close()
        conn.close()


def main(DBPassword):

    # Create skater summary stats table and load data
    SumaryStatsTableName = 'skatersummarystats'

    DropTable(DBPassword, SumaryStatsTableName)
    CreateDataBase(DBPassword, SumaryStatsTableName)
    LoadCsvToDataBase(DBPassword, SUMMARY_STATS_PATH, SumaryStatsTableName)

    print('SkaterSummaryStats table successfully created and loaded with data! \n')
    

    # Create skater miscellaneous stats table and load data
    MiscellaneousStatsTableName = 'skatermiscellaneousstats'

    DropTable(DBPassword, MiscellaneousStatsTableName)
    CreateDataBase(DBPassword, MiscellaneousStatsTableName)
    LoadCsvToDataBase(DBPassword, MISCELLANEOUS_STATS_PATH, MiscellaneousStatsTableName)

    print('SkaterMiscellaneousStats table successfully created and loaded with data! \n')


if __name__ == "__main__":
    main()