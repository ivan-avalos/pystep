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
from errorman import StepError

class Stack:
    stack = []
    shell_mode = None
    
    def __init__ (self, shell_mode = False):
        self.shell_mode = shell_mode
        
    def print_stack (self):
        stack = self.stack
        stack = [
            str (i).rstrip ('0').rstrip ('.') 
            if '.' in str(i) else str(i)
            for i in stack
        ]
        print ('[', end='')
        print (*stack, sep=', ', end='')
        print (']')
    
    # Basic stack operations
    
    def pop(self):
        return self.stack.pop()
    
    def push(self, element):
        self.stack.append(element)
        
    def clear (self):
        self.stack = []
    
    # Complex stack  operations
    
    def dup(self):
        tos = self.pop()
        self.push(tos)
        self.push(tos)
        
    def drop(self):
        self.pop()
        self.pop()
        
    def swap(self):
        tos = self.pop()
        _2os = self.pop()
        self.push(tos)
        self.push(_2os)
    
    def check_params(self, min_params, atom_function):
        if len(self.stack) >= min_params:
            return True
        else:
            StepError.error(
                StepError.MISSING_PARAMS, 
                self.shell_mode,
                str (len (self.stack)),
                str (min_params),
                str (atom_function)
            )
