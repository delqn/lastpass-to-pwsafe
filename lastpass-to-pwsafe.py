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

PWS_FROM_LP_REMAP = {
    'Group/Title': ['grouping', 'name'],
    'Username': ['username'],
    'Password': ['password'],
    'URL': ['url'],
    'AutoType': [],
    'Created Time': [],
    'Password Modified Time': [],
    'Last Access Time': [],
    'Password Expiry Date': [],
    'Password Expiry Interval': [],
    'Record Modified Time': [],
    'Password Policy': [],
    'Password Policy Name': [],
    'History': [],
    'Run Command': [],
    'DCA': [],
    'Shift+DCA': [],
    'e-mail': [],
    'Protected': [],
    'Symbols': [],
    'Keyboard Shortcut': [],
    'Notes': ['fav'],
}

def from_LP_to_PWS(lp_record):
    lp_dict = lp_record._asdict()
    pws_record = {}
    for pw_field in PWSafeRow._fields:
        pw_values = []
        for lp_key in PWS_FROM_LP_REMAP[_decode_key(pw_field)]:
            val = lp_dict.get(lp_key, '_')
            if lp_key == 'name':
                val = val.replace('.', '_')
            pw_values.append(val)
        pws_record[pw_field] = '.'.join(pw_values)
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
        csv_writer = csv.writer(f, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONE)
        csv_writer.writerow([_decode_key(k) for k in PWSafeRow._fields])
        for lp in get_lastpass_records(sys.argv[1]):
            pws_dict = from_LP_to_PWS(lp)._asdict()
            csv_writer.writerow([pws_dict[k] for k in PWSafeRow._fields])
    



            

