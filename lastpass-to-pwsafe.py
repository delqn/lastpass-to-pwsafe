#!/usr/bin/env python2.7

import base64
import collections
import csv
import sys

def _encode_key(string):
    return base64.b64encode(string).replace('=', '_')

def _decode_key(key):
    return base64.b64decode(key.replace('_', '='))

LastPassRow = collections.namedtuple(
    'LastPassRow',
    field_names=['url', 'username', 'password', 'extra', 'name', 'grouping', 'fav'])

PWSafeRow = collections.namedtuple(
    'PWSafeRow',
    field_names=[_encode_key(x) for x in (
        'Group/Title', 'Username', 'Password', 'URL', 'AutoType', 'Created Time',
        'Password Modified Time', 'Last Access Time', 'Password Expiry Date',
        'Password Expiry Interval', 'Record Modified Time', 'Password Policy',
        'Password Policy Name', 'History', 'Run Command', 'DCA', 'Shift+DCA',
        'e-mail', 'Protected', 'Symbols', 'Keyboard Shortcut', 'Notes')])

LP_TO_PWS_REMAP = {
    'url': 'URL',
    'username': 'Username',
    'password': 'Password',
    'extra': 'Notes',
    'name': 'Notes',
    'grouping': 'Group/Title',
    'fav': 'Protected',
}

def from_LP_to_PWS(lp_record):
    lp_dict = lp_record._asdict()
    pws_record = {}
    for field in LastPassRow._fields:
        pws_record[_encode_key(LP_TO_PWS_REMAP[field])] = lp_dict[field]
    missing_keys = set(PWSafeRow._fields).difference(pws_record.keys())
    pws_record.update({k: None for k in missing_keys})
    return PWSafeRow(**pws_record)

def get_lastpass_records(fname):
    with open(fname, mode='r') as f:
        reader = csv.reader(f)
        headers = tuple(reader.next())
        assert headers == LastPassRow._fields, '{} <> {}'.format(headers, LastPassRow._fields)
        passwords = [LastPassRow(**dict(zip(headers, row))) for row in reader]
    return passwords

       


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print('What is the file you want to convert?')
        sys.exit(1)

    if len(sys.argv) <= 2:
        print('What is the file you want to write to?')
        sys.exit(1)

    with open(sys.argv[2], mode='w') as f:
        csv_writer = csv.writer(f, delimiter='\t', quotechar='"', quoting=csv.QUOTE_ALL)
        csv_writer.writerow([_decode_key(k) for k in PWSafeRow._fields])
        for lp in get_lastpass_records(sys.argv[1]):
            pws_dict = from_LP_to_PWS(lp)._asdict()
            csv_writer.writerow([pws_dict[k] for k in PWSafeRow._fields])
    



            

