#!/usr/bin/env python3

import argparse
import datetime
from decimal import Decimal
import xml.etree.ElementTree as ET


def convert_homebank_date(serial_date):
    start_date = datetime.datetime(1, 1, 1, 0, 0)
    new_date = start_date + datetime.timedelta(serial_date - 1)
    return new_date.strftime("%Y-%m-%d")


def attrib_or_empty(node, attribute_name):
    if attribute_name in node.attrib:
        return node.attrib[attribute_name]
    else:
        return ''

def build_lookup(root, node_name):
    lookup = { '' : '' }
    for node in root.iter(node_name):
        lookup[node.attrib['key']] = node.attrib['name']
    return lookup


def to_decimal(number_string):
    return Decimal(number_string).quantize(Decimal('.01'))


def parse_homebank(file_name):
    root = ET.parse(file_name).getroot()
    category_lookup = build_lookup(root, 'cat')
    account_lookup = build_lookup(root, 'account')
    print('date,src_account,dst_account,category,amount,payee,text')
    for transfer_node in root.iter('ope'):
        date = convert_homebank_date(int(transfer_node.attrib['date']))
        src_account = account_lookup[transfer_node.attrib['account']]
        dst_account = account_lookup[attrib_or_empty(
            transfer_node, 'dst_account')]
        amount = to_decimal(transfer_node.attrib['amount'])
        wording = attrib_or_empty(
            transfer_node, 'wording').replace(";", "").replace(",", "")
        category = category_lookup[attrib_or_empty(transfer_node, 'category')]
        info = attrib_or_empty(transfer_node, 'info')
        print('{},{},{},{},€{},{},{}'.format(
            date, src_account, dst_account, category, amount, wording, info))


def main():
    parser = argparse.ArgumentParser(
        description='Converts a homebank .xhb file into a csv output')
    parser.add_argument('source', help='The homebank .xhb file')
    args = parser.parse_args()
    parse_homebank(args.source)


if __name__ == '__main__':
    main()
