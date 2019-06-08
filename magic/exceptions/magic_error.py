# !/usr/bin/env python
#
# Author: Magic Foundation <support@hologram.io>
#
# Copyright 2018 - Magic Foundation
#
# LICENSE: Distributed under the terms of the MIT License
#
# MagicError.py - This file contains a list of custom Exception
# implementations.


class MagicError(Exception):

    def __repr__(self):
        return '%s: %s' % (type(self).__name__, str(self))

    pass
