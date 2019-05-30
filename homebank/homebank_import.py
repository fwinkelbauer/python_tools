#!/usr/bin/env python3

import argparse
import csv
import re


def parse_csv_file(file_name):
    with open(file_name, 'r', encoding='iso-8859-1') as f:
        homebank_lines = []
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            date = row['Buchungsdatum']
            memo = re.sub(r'\s+', ' ', row['Umsatztext'])
            amount = row['Betrag']
            homebank_lines.append('{};8;;;{};{};;'.format(date, memo, amount))
        return homebank_lines


def write_file(lines, file_name):
    with open(file_name, 'w') as f:
        for line in lines:
            f.write("{}\n".format(line))


def main():
    parser = argparse.ArgumentParser(
        description='Converts a Volksbank .csv file into a Homebank .csv file')
    parser.add_argument('source', help='The Volksbank .csv file')
    args = parser.parse_args()
    destination = 'homebank_{}.csv'.format(args.source.split('_')[1])
    homebank_lines = parse_csv_file(args.source)
    write_file(homebank_lines, destination)
    print('Created file {}'.format(destination))


if __name__ == '__main__':
    main()
