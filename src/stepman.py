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
import shlex
import math
from stackman import Stack

class Step:
    output = None
    stack = Stack()
    user_functions = {}
    
    def __init__(self, content, params = []):
        # Convert string parameters to float
        self.params = []
        for i in params:
            if self.is_float(i):
                self.params.append(float(i))
            else:
                sys.exit('Step error: invalid parameter ' + i)
        
        # Intermediate process
        content = self.extract_output(content)
        content = self.remove_comments(content)
        content = self.extract_user_functions(content)
        
        # Eval intermediate code
        self.eval(shlex.split(content))
        
    def extract_output(self, content):
        output = []
        lines = content.split('\n')
        for i in range(len(lines)):
            line = lines[i]
            if i == 0 and len(line) > 2 and line[0] == ':':
                    # Set output file
                    self.output = open(line[1:], "w")
                    continue
            output.append(line)
        return ' '.join(output)
    
    def extract_user_functions(self, content):
        output = ''
        in_string = False
        in_function = False
        recollector = ''
        for i in list(content):
            # Avoid parentheses inside strings
            if i == '"':
                in_string = not in_string
            
            if i == '(' and not in_string:
                in_function = True
                continue
            elif i == ')' and not in_string:
                # Parse function
                func = shlex.split(recollector)
                if len(func) >= 2:
                    func_name = func[0]
                    func_body = func[1:]
                    self.user_functions[func_name] = func_body
                else:
                    sys.exit("Step error: function must contain title and body")
                    
                # Restore state and clear recollector
                in_function = False
                recollector = ''
            elif not in_function:
                output += i
                
            if in_function:
                recollector += i
        return output
    
    def remove_comments (self, content):
        output = ""
        in_comment = False
        
        for i in list(content):
            if i == '{':
                in_comment = True
            elif i == '}':
                in_comment = False
            elif not in_comment:
                output += i
                
        return output
    
    def eval(self, content):
        # Atom functions
        atom_function = {
            # Arithmetic functions
            '+': self.__sum,
            '-': self.__sub,
            '*': self.__mul,
            '/': self.__div,
            'pow': self.__pow,
            'sqrt': self.__sqrt,
            # Trigonometric functions
            'sin': self.__sin,
            'cos': self.__cos,
            'tan': self.__tan,
            'exp': self.__exp,
            'log': self.__log,
            # Stack functions
            'clear': self.__clr,
            'print': self.__pout,
            'println': self.__plout,
            'pop': self.__pop,
            'dup': self.__dup,
            'drop': self.__drop,
            'swap': self.__swap
        }
        
        atom_constant = {
            'pi': math.pi,
            'e': math.e
        }
        
        for atom in content:
            if self.is_float(atom):
                # Push atom to stack
                self.stack.push(float(atom))
                continue
            elif atom in atom_function:
                # Eval step function
                atom_function[atom]()
            elif atom in atom_constant:
                # Step constant
                self.stack.push(atom_constant[atom])
            elif atom[0] == '@':
                # Eval user defined function
                if atom[1:] in self.user_functions:
                        self.eval(self.user_functions[atom[1:]])
                else:
                    sys.exit("Step error: undefined user defined function \"" + atom + "\"")
            elif atom[0] == '$':
                if atom[1:].isdigit() and len(atom) > 1:
                    index = atom[1:]
                    try:
                        # Push param
                        self.stack.push(self.params[int(index)])
                    except IndexError:
                        sys.exit("Step error: invalid param index $" + index)
                else:
                    sys.exit("Step error: invalid param index $" + atom[1:])
            elif atom[0] == '_':
                # Print single word to stdout or file
                string = bytes(atom[1:], "utf-8").decode('unicode_escape')
                if self.output is None:
                    print(string, end='')
                else:
                    self.output.write(string)
            else:
                sys.exit("Step error: undefined function \"" + atom + "\"")
                
    # Math functions
    
    def is_float(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False
    # Step functions
    
    # Add two numbers together 
    def __sum(self):
        # params: 2
        self.stack.check_params(2, '+')
        result = self.stack.pop() + self.stack.pop()
        self.stack.push(result)
    
    # Substract two numbers
    def __sub(self):
        # params: 2
        self.stack.check_params(2, '-')
        result = self.stack.pop() - self.stack.pop()
        self.stack.push(result)
    
    # Multiply two numbers
    def __mul(self):
        # params: 2
        self.stack.check_params(2, '*')
        result = self.stack.pop() * self.stack.pop()
        self.stack.push(result)
    
    # Divide two numbers
    def __div(self):
        # params: 2
        self.stack.check_params(2, '/')
        result = self.stack.pop() / self.stack.pop()
        self.stack.push(result)
        
    # Raise a number to the nth power    
    def __pow(self):
        # params: 2
        self.stack.check_params(2, 'pow')
        x = self.stack.pop()
        y = self.stack.pop()
        result = math.pow(x, y)
        self.stack.push(result)
    
    # Square root of a number
    def __sqrt(self):
        # params: 1
        self.stack.check_params(1, 'sqrt')
        result = math.sqrt(self.stack.pop())
        self.stack.push(result)
    
    # Sine function of a number
    def __sin(self):
        # params: 1
        self.stack.check_params(1, 'sin')
        result = math.sin(self.stack.pop())
        self.stack.push(result)
    
    # Cosine funcion of a number
    def __cos(self):
        # params: 1
        self.stack.check_params(1, 'cos')
        result = math.cos(self.stack.pop())
        self.stack.push(result)
    
    # Tangent function of a number
    def __tan(self):
        # params: 1
        self.stack.check_params(1, 'tan')
        result = math.tan(self.stack.pop())
        self.stack.push(result)
        
    def __exp(self):
        # params: 1
        self.stack.check_params(1, 'exp')
        result = math.exp(self.stack.pop())
        self.stack.push(result)
        
    def __log(self):
        # params: 1
        self.stack.check_params(1, 'log')
        result = math.log(self.stack.pop())
        self.stack.push(result)
    
    # Clear stack
    def __clr(self):
        self.stack = Stack()
    
    # Pop and print top of stack
    def __pout(self):
        # params: 1
        self.stack.check_params(1, 'print')
        if self.output is None:
            print(self.stack.pop(), end='')
        else:
            self.output.write(str(self.stack.pop()))
            
    # Pop and print top of stack - with line break
    def __plout(self):
        # params: 1
        self.stack.check_params(1, 'println')
        if self.output is None:
            print(self.stack.pop())
        else:
            self.output.write(str(self.stack.pop()) + '\n')
    
    # Pop without print
    def __pop(self):
        # params: 1
        self.stack.check_params(1, 'pop')
        self.stack.pop()
    
    # Duplicate the value on top of stack
    def __dup(self):
        # params: 1
        self.stack.check_params(1, 'dup')
        self.stack.dup()
    
    # Pop last two numbers on stack without print
    def __drop(self):
        # params: 2
        self.stack.check_params(2, 'drop')
        self.stack.drop()
    
    # Swap positions of last two numbers on stack
    def __swap(self):
        # params: 2
        self.stack.check_params(2, 'swap')
        self.stack.swap()
