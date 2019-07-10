#!/usr/bin/env python
#
# Author: Magic Foundation <support@hologram.io>
#
# Copyright 2018 - Magic Foundation
#
# LICENSE: Distributed under the terms of the MIT License

import os
from subprocess import PIPE
import psutil


def test_version():

    verfile = os.path.dirname(__file__) + '/../version.txt'
    version = open(verfile).read().split()[0]

    # This basically doesn't work because the file location when the test is run is not the same
    # p = psutil.Popen(["magic-network", "version"], stdout=PIPE)
    # no_agent_result = p.communicate()

    p = psutil.Popen(["magic-network", "gateway", "version"], stdout=PIPE)
    gateway_result = p.communicate()

    p = psutil.Popen(["magic-network", "payment", "version"], stdout=PIPE)
    payment_result = p.communicate()

    # assert version in no_agent_result[0].decode()
    assert version in gateway_result[0].decode()
    assert version in payment_result[0].decode()
