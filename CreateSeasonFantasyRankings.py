import psycopg2


def DropSeasonOrDateRankingsTable(Password, StatsType):
    print(f'Dropping Table...')
    
    try:
        conn = psycopg2.connect(
                host="localhost",
                dbname="FantasyHockey",
                user="postgres",
                password=Password,
                port="5432"
            )
        cur = conn.cursor()

        if StatsType == 'season':
            DropTable = f"""DROP TABLE IF EXISTS seasonrankings;"""
        elif StatsType == 'date':
            DropTable = f"""DROP TABLE IF EXISTS daterankings;"""
        else:
            raise Exception(f'Wrong type: {StatsType}')
        
        cur.execute(DropTable)
        conn.commit()

        print(f"Table successfully dropped! \n")

    except Exception as e:
        print(f"An error occurred while dropping the table: {e}")
    
    finally:
        # Close the connection
        cur.close()
        conn.close()

def CreateSeasonOrDateRankingsTable(Password, StatsType):
    print('Creating table...')
    try:
        conn = psycopg2.connect(
            host="localhost",
            dbname="FantasyHockey",
            user="postgres",
            password=Password,
            port="5432"
        )
        cur = conn.cursor()

        if StatsType == 'season':
            TableName = 'seasonrankings'
            SummaryTable = 'skatersummarystats'
            MiscellaneousTable = 'skatermiscellaneousstats'
        elif StatsType == 'date':
            TableName = 'daterankings'
            SummaryTable = 'skatersummarygamestats'
            MiscellaneousTable = 'skatermiscellaneousgamestats'
        else:
            raise Exception(f'Wrong type: {StatsType}')
        
        CreateTable = f"""CREATE TABLE {TableName} AS
                         SELECT 
                            RANK() OVER (ORDER BY totalFantasyPoints DESC) AS rank,
                            playerId,
                            skaterFullName,
                            positionCode,
                            teamAbbrevs,
                            goals,
                            assists,
                            plusMinus,
                            ppPoints,
                            shots,
                            hits,
                            blockedShots,
                            totalFantasyPoints
                         FROM (
                            SELECT
                                s.playerId,
                                s.skaterFullName,
                                s.positionCode,
                                s.teamAbbrevs,
                                s.goals,
                                s.assists,
                                s.plusMinus,
                                s.ppPoints,
                                s.shots,
                                m.hits,
                                m.blockedShots,
                                (s.goals * 6 + s.assists * 4 + s.plusMinus + s.ppPoints * 2 + s.shots * 0.9 + m.blockedShots + m.hits * 0.5) AS totalFantasyPoints
                            FROM 
                                {SummaryTable} s
                            INNER JOIN 
                                {MiscellaneousTable} m 
                            ON 
                                s.playerId = m.playerId
                         ) AS subquery

                         ORDER BY 
                            rank ASC;"""
        
        cur.execute(CreateTable)
        conn.commit()

        print(f"Table successfully created! \n")

    except Exception as e:
        print(f"An error occurred while creating the table: {e}")
        
    finally:
        cur.close()
        conn.close()

def main(Password, StatsType):
    DropSeasonOrDateRankingsTable(Password, StatsType)
    CreateSeasonOrDateRankingsTable(Password, StatsType)

if __name__ == '__main__':
    main()