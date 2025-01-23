import pandas as pd
import csv

def ProcessCsv(Paths):

    for Path in Paths:

        with open(Path, 'r') as file:
            content = file.read()

        content = content.replace(',,', ', ,')

        with open(Path, 'w') as file:
            file.write(content)

        df = pd.read_csv(Path)

        # Some players might have two teams because of a trade, take the last one.
        df['teamAbbrevs'] = df['teamAbbrevs'].apply(lambda x: x[:3] if len(x) > 3 else x)

        df.to_csv(Path, index=False)

def main():
    ProcessCsv(['./CsvFiles/SkaterSummaryStats.csv',
                './CsvFiles/SkatersMiscellaneousStats.csv',
                './CsvFiles/SkatersSummaryGameStats.csv', 
                './CsvFiles/SkatersMiscellaneousGameStats.csv'])

if __name__ == '__main__':
    main()