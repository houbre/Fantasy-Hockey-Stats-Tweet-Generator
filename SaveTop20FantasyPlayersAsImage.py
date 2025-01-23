import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date, timedelta

def FetchTop20PlayersFromDB(Password, TableName):

    if TableName != 'seasonrankings' and TableName != 'daterankings':
        raise Exception(f'Wrong table name: {TableName}')

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
        FetchTop20Players = f"""
                             SELECT rank, skaterFullName as Name, positioncode as Position, teamabbrevs as Team, totalFantasyPoints as Fantasy_Points
                             FROM {TableName}
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

def PlotAndSaveTop20PlayersImage(df, TableName):
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.axis('tight')
    ax.axis('off')

    # Define colors for different rank groups
    cell_colors = []
    for i in range(len(df)):
        if i < 5:  # Top 5
            row_color = ["#d4f7d4"] * len(df.columns)  # Light green
        elif i < 10:  # 6th to 10th
            row_color = ["#d4e9f7"] * len(df.columns)  # Light blue
        elif i < 15:  # 11th to 15th
            row_color = ["#f7f7d4"] * len(df.columns)  # Light yellow
        else:  # 16th to 20th
            row_color = ["#e8e8e8"] * len(df.columns)  # Light gray
        cell_colors.append(row_color)

    table = plt.table(
        cellText=df.values,
        colLabels=df.columns,
        cellLoc='center',
        loc='center',
        colColours=["#4CAF50"] * len(df.columns),
        cellColours=cell_colors,
    )

    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.auto_set_column_width(col=list(range(len(df.columns))))


    today = date.today()
    yesterday = today - timedelta(days=1)
    day_of_week = yesterday.strftime("%A")

    if TableName == 'seasonrankings':
        Title = "Top 20 Fantasy Players, 2024-2025 Season"
    elif TableName == 'daterankings':
        Title = f"Top 20 Fantasy Players, {day_of_week} : {yesterday}"
    else:
        raise Exception(f'Wrong table name: {TableName}')

    plt.title(
        Title,
        fontsize=16,
        weight='bold',
        color="#333333",
        pad=3,
        y=0.80
    )

    plt.tight_layout()

    # Save img
    plt.savefig(f"./images/Top20FantasyPlayers_{TableName}.png", dpi=300, bbox_inches='tight')
    print(f"Image saved to Top20FantasyPlayers_{TableName}.png! \n")

    plt.close(fig)


def main(Password, TableName):

    Top20DF = FetchTop20PlayersFromDB(Password, TableName)
    
    if Top20DF is not None:
        PlotAndSaveTop20PlayersImage(Top20DF, TableName)

if __name__ == "__main__":
    main()
