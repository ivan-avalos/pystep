# -*- coding: utf-8 -*-
# pyStep - Python implementation of Step mathematic self.stack-based interpreter
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

class StepError:
    INVALID_PARAM = "Invalid parameter {}"
    INVALID_PARAM_INDEX = "Invalid param index {}"
    FUNC_TITLE_BODY = "Function must have title and body"
    UNDEF_FUNC_USER = "Undefined user function {}"
    UNDEF_FUNC = "Undefined function {}"
    MISSING_PARAMS = "Missing parameters: Provided {} of {} for function `{}'"
    
    def error (message, shell_mode, *args):
        message = 'Step error: ' + message.format (*args) + '.'
        if shell_mode:
            print (message)
        else:
            sys.exit (message)
