#!/usr/bin/env python3

import datetime
from decimal import Decimal
import xml.etree.ElementTree as ET


def convert_homebank_date(serial_date):
    new_date = datetime.datetime(1, 1, 1, 0, 0) + datetime.timedelta(serial_date - 1)
    return new_date.strftime("%Y-%m-%d")


def attribute_or_empty(node, attribute_name):
    if attribute_name in node.attrib:
        return node.attrib[attribute_name]
    else:
        return ''

def build_lookup(root, node_name):
    lookup = { '' : '' }
    for node in root.iter(node_name):
        lookup[node.attrib['key']] = node.attrib['name']
    return lookup

def parse_homebank(file_name):
    root = ET.parse(file_name).getroot()
    category_lookup = build_lookup(root, 'cat')
    account_lookup = build_lookup(root, 'account')
    for transfer_node in root.iter('ope'):
        date = convert_homebank_date(int(transfer_node.attrib['date']))
        src_account = account_lookup[transfer_node.attrib['account']]
        dst_account = account_lookup[attribute_or_empty(transfer_node, 'dst_account')]
        amount = Decimal(transfer_node.attrib['amount']).quantize(Decimal('.01'))
        wording = attribute_or_empty(transfer_node, 'wording')
        category = category_lookup[attribute_or_empty(transfer_node, 'category')]
        info = attribute_or_empty(transfer_node, 'info')
        # This is just a draft
        print('{} {} {}:{} -> {}'.format(date, amount, src_account, category, dst_account))


def main():
    parse_homebank('homebank.xhb')


if __name__ == '__main__':
    main()
