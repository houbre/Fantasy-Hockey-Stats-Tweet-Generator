import psycopg2


def DropSeasonRankingsTable(Password):
    print(f'Dropping Table seasonrankings...')
    try:
        conn = psycopg2.connect(
                host="localhost",
                dbname="FantasyHockey",
                user="postgres",
                password=Password,
                port="5432"
            )
        cur = conn.cursor()

        DropTable = f"""DROP TABLE IF EXISTS seasonrankings;"""

        cur.execute(DropTable)
        conn.commit()

        print(f"Table seasonrankings successfully dropped! \n")

    except Exception as e:
        print(f"An error occurred while dropping the table: {e}")
    
    finally:
        # Close the connection
        cur.close()
        conn.close()

def CreateSeasonRankingsTable(Password):
    print('Creating table seasonrankings...')
    try:
        conn = psycopg2.connect(
            host="localhost",
            dbname="FantasyHockey",
            user="postgres",
            password=Password,
            port="5432"
        )
        cur = conn.cursor()

        CreateTable = """CREATE TABLE seasonrankings AS
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
                                skatersummarystats s
                            INNER JOIN 
                                skatermiscellaneousstats m 
                            ON 
                                s.playerId = m.playerId
                         ) AS subquery

                         ORDER BY 
                            rank ASC;"""
        
        cur.execute(CreateTable)
        conn.commit()

        print(f"Table seasonrankings successfully created! \n")

    except Exception as e:
        print(f"An error occurred while creating the table: {e}")
        
    finally:
        cur.close()
        conn.close()

def main(Password):
    DropSeasonRankingsTable(Password)
    CreateSeasonRankingsTable(Password)

if __name__ == '__main__':
    main()