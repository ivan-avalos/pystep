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

class Stack:
    stack = []
    
    # Basic stack operations
    
    def pop(self):
        return self.stack.pop()
    
    def push(self, element):
        self.stack.append(element)
    
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
            sys.exit("Stack error: Missing parameters: Provided " + str(len(self.stack)) + " of " + str(min_params) + " for function '" + str(atom_function) + "'")
