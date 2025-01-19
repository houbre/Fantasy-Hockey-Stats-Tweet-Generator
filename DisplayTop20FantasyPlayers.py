import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

def FetchTop20PlayersFromDB(Password):
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            host="localhost",
            dbname="FantasyHockey",
            user="postgres",
            password=Password,
            port="5432"
        )
        
        # SQL query to fetch top 20 players
        FetchTop20Players = """
                            SELECT rank, skaterFullName as Name, positioncode as Position, teamabbrevs as Team, totalFantasyPoints as Fantasy_Points
                            FROM seasonrankings
                            ORDER BY rank ASC
                            LIMIT 20;
                            """
        
        df = pd.read_sql_query(FetchTop20Players, conn)
        return df
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
    finally:
        if conn:
            conn.close()

def PlotTop20Players(df):

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.axis('tight')
    ax.axis('off')

    table = plt.table(
        cellText=df.values,
        colLabels=df.columns,
        cellLoc='center',
        loc='center',
        colColours=["#4CAF50"] * len(df.columns),
    )

    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.auto_set_column_width(col=list(range(len(df.columns))))

    plt.title("Top 20 Fantasy Players, 2024-2025 season", fontsize=16, weight='bold', color="#333333", pad=3, y=0.80)

    plt.tight_layout()
    
    # Save img
    plt.savefig("Top20FantasyPlayers_20242025_season.png", dpi=300, bbox_inches='tight')
    print(f"Image saved to Top20FantasyPlayers_20242025_season.png! \n")

    plt.close(fig)


def main(Password):

    Top20DF = FetchTop20PlayersFromDB(Password)
    
    if Top20DF is not None:
        PlotTop20Players(Top20DF)

if __name__ == "__main__":
    main()
