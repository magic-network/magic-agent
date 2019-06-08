# Current format for auth object is just pipe separated
# <address>|<password>
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import (bytes, str)
import json


class AuthObject(object):
    def __init__(self, address='', password='', sess=''):
        self.params = {
            'address': address,
            'password': password,
            'sessionId': sess
        }
        self.required = ('address', 'password')

    def __repr__(self):
        return "<{} {}>".format(type(self).__name__,
                                repr(self.params))

    @property
    def address(self):
        return self.params['address']

    @property
    def password(self):
        return self.params['password']

    @property
    def sessionId(self):
        return self.params['sessionId']

    def decode(self, input_string):
        decoded = json.loads(input_string.decode('utf8'))
        for field in self.required:
            if field not in decoded:
                raise ValueError('Auth string is missing field %s', field)
        self.params = decoded

    def encode(self):
        jsonstr = json.dumps(self.params) + '\n'
        return jsonstr.encode('utf8')
