#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# pyStep - Python implementation of Step mathematic stack-based interpreter
# Copyright (C) 2018  Iván Ávalos 
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import sys
import shlex
from stackman import Stack
from stepman import Step
from shellman import Shell

help_message = '''Usage: pystep file ...
Or:    pystep [-i|-h]

Options:
  -i  Start interactive shell
  -h  Show this help menu
'''

# Verify arguments
if len(sys.argv) <= 1:
    sys.exit(help_message)
else:
    if sys.argv[1] == '-h':
        sys.exit(help_message)
    elif sys.argv[1] == '-i':
        Shell ().start ()
        sys.exit (0)

# Read input
fileName = sys.argv[1]
fileObject = open(fileName, "r")
fileContent = fileObject.read()

# Eval input
if len(sys.argv) >= 3:
    Step(fileContent, sys.argv[2:])
else:
    Step(fileContent)
