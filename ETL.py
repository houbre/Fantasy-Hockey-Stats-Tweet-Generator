import ExtractSkatersStats
import TransformSkaterStats
import LoadCsvIntoDB
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--password", required=True, help="Password to Postgres")

    args =  parser.parse_args()

    return args


def main():
    args = parse_arguments()

    ExtractSkatersStats.main()
    TransformSkaterStats.main()
    LoadCsvIntoDB.main(args.password)

    print("Data was successfully extracted, transformed and loaded into a Postgres database")


if __name__ == '__main__':
    main()