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
from errorman import StepError
from stackman import Stack

class Step:
    shell_mode = False
    output = None
    stack = Stack()
    params = []
    user_functions = {}
    
    def __init__(self, content, params = []):
        self.shell_mode = False
        self.parse_params(params)
        self.eval(content)
        
    def __init__(self):
        self.shell_mode = True
        self.stack = Stack (shell_mode = True)
        
    def parse_params (self, params = []):
        # Convert string parameters to float
        for i in params:
            if self.is_float (i):
                self.params.append (float (i));
            else:
                StepError.error (
                    StepError.INVALID_PARAM, self.shell_mode, i)
    
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
                    func_body = ' '.join(func[1:])
                    self.user_functions[func_name] = func_body
                else:
                    StepError.error (
                        StepError.FUNC_TITLE_BODY, self.shell_mode)
                    
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
        # Intermediate process
        if not self.shell_mode:
            content = self.extract_output(content)
            content = self.remove_comments(content)
            
        content = self.extract_user_functions(content)
        content = shlex.split (content)
        
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
                    return
                else:
                    StepError.error(
                        StepError.UNDEF_FUNC_USER,
                        self.shell_mode,
                        atom
                    )
            elif atom[0] == '$':
                if atom[1:].isdigit() and len(atom) > 1:
                    index = atom[1:]
                    try:
                        # Push param
                        self.stack.push(self.params[int(index)])
                    except IndexError:
                        StepError.error (
                            StepError.INVALID_PARAM_INDEX, 
                            self.shell_mode,
                            atom
                        )
                else:
                    StepError.error (
                        StepError.INVALID_PARAM_INDEX,
                        self.shell_mode,
                        atom
                    )
            elif atom[0] == '_':
                # Print single word to stdout or file
                string = bytes(atom[1:], "utf-8").decode('unicode_escape')
                if self.output is None:
                    print(string, end='')
                else:
                    self.output.write(string)
            else:
                StepError.error (
                    StepError.UNDEF_FUNC,
                    self.shell_mode,
                    atom
                )
        
        if self.shell_mode:
            self.stack.print_stack ()
                
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
        if not self.stack.check_params(2, '+'): return
        result = self.stack.pop() + self.stack.pop()
        self.stack.push(result)
    
    # Substract two numbers
    def __sub(self):
        # params: 2
        if not self.stack.check_params(2, '-'): return
        result = self.stack.pop() - self.stack.pop()
        self.stack.push(result)
    
    # Multiply two numbers
    def __mul(self):
        # params: 2
        if not self.stack.check_params(2, '*'): return
        result = self.stack.pop() * self.stack.pop()
        self.stack.push(result)
    
    # Divide two numbers
    def __div(self):
        # params: 2
        if not self.stack.check_params(2, '/'): return
        result = self.stack.pop() / self.stack.pop()
        self.stack.push(result)
        
    # Raise a number to the nth power    
    def __pow(self):
        # params: 2
        if not self.stack.check_params(2, 'pow'): return
        x = self.stack.pop()
        y = self.stack.pop()
        result = math.pow(x, y)
        self.stack.push(result)
    
    # Square root of a number
    def __sqrt(self):
        # params: 1
        if not self.stack.check_params(1, 'sqrt'): return
        result = math.sqrt(self.stack.pop())
        self.stack.push(result)
    
    # Sine function of a number
    def __sin(self):
        # params: 1
        if not self.stack.check_params(1, 'sin'): return
        result = math.sin(self.stack.pop())
        self.stack.push(result)
    
    # Cosine funcion of a number
    def __cos(self):
        # params: 1
        if not self.stack.check_params(1, 'cos'): return
        result = math.cos(self.stack.pop())
        self.stack.push(result)
    
    # Tangent function of a number
    def __tan(self):
        # params: 1
        if not self.stack.check_params(1, 'tan'): return
        result = math.tan(self.stack.pop())
        self.stack.push(result)
        
    def __exp(self):
        # params: 1
        if not self.stack.check_params(1, 'exp'): return
        result = math.exp(self.stack.pop())
        self.stack.push(result)
        
    def __log(self):
        # params: 1
        if not self.stack.check_params(1, 'log'): return
        result = math.log(self.stack.pop())
        self.stack.push(result)
    
    # Clear stack
    def __clr(self):
        self.stack.clear ()
    
    # Pop and print top of stack
    def __pout(self):
        # params: 1
        if not self.stack.check_params(1, 'print'): return
        if self.output is None:
            print(self.stack.pop(), '')
        else:
            self.output.write(str(self.stack.pop()))
            
    # Pop and print top of stack - with line break
    def __plout(self):
        # params: 1
        if not self.stack.check_params(1, 'println'): return
        if self.output is None:
            print(self.stack.pop())
        else:
            self.output.write(str(self.stack.pop()) + '\n')
    
    # Pop without print
    def __pop(self):
        # params: 1
        if not self.stack.check_params(1, 'pop'): return
        self.stack.pop()
    
    # Duplicate the value on top of stack
    def __dup(self):
        # params: 1
        if not self.stack.check_params(1, 'dup'): return
        self.stack.dup()
    
    # Pop last two numbers on stack without print
    def __drop(self):
        # params: 2
        if not self.stack.check_params(2, 'drop'): return
        self.stack.drop()
    
    # Swap positions of last two numbers on stack
    def __swap(self):
        # params: 2
        if not self.stack.check_params(2, 'swap'): return
        self.stack.swap()
