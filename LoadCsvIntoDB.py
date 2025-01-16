import psycopg2
import csv
import pandas as pd

# File paths for CSV files
SUMMARY_STATS = "SkaterSummaryStats.csv"
MISCELLANEOUS_STATS = "SkatersMiscellaneousStats.csv"

def ProcessCsv(file_path):

    with open(file_path, 'r') as file:
        content = file.read()

    # Replace consecutive commas (,,) with a comma followed by an empty string (space) (, )
    content = content.replace(',,', ', ,')

    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.write(content)

    print(f"Added empty string (space) between consecutive commas in {file_path}")

    df = pd.read_csv(file_path)

    # Truncate the 'teamAbbrevs' column to 3 characters if necessary
    df['teamAbbrevs'] = df['teamAbbrevs'].apply(lambda x: x[:3] if len(x) > 3 else x)

    # Save the updated DataFrame back to the CSV file
    df.to_csv(file_path, index=False)

    print(f"Team abbreviations have been truncated to 3 characters in {file_path}")

def CreateDataBase():

    try:
        conn = psycopg2.connect(
                host="localhost",
                dbname="FantasyHockey",
                user="postgres",
                password="Googoi80!",
                port="8080"
            )
        cur = conn.cursor()

        NewTable = """CREATE TABLE IF NOT EXISTS skatersummarystats(
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

        cur.execute(NewTable)
        conn.commit()

        print("Table 'skatersummarystats' created successfully (or it already exists)")

    except Exception as e:
        print(f"An error occurred while creating the table: {e}")
        
    finally:
        # Close the connection
        cur.close()
        conn.close()

   
def LoadCsvToDataBase():
    try:
        conn = psycopg2.connect(
                host="localhost",
                dbname="FantasyHockey",
                user="postgres",
                password="Googoi80!",
                port="8080"
            )
        cur = conn.cursor()

        with open('SkaterSummaryStats.csv', 'r') as f:
            next(f) # Skip the header row.
            cur.copy_from(f, 'skatersummarystats', sep=',', null=' ')

        conn.commit()
    
    except Exception as e:
        print(f"An error occurred while creating the table: {e}")
        
    finally:
        # Close the connection
        cur.close()
        conn.close()


def main():
    ProcessCsv('SkaterSummaryStats.csv')
    CreateDataBase()
    LoadCsvToDataBase()

if __name__ == "__main__":
    main()