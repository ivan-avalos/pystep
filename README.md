# pyStep - stack-based interpreter

pyStep is a simple, functional, mathematical and stack-based interpreter written in Python that allows you to perform simple mathematical operations, is the extended Python implementation of the <a href="https://github.com/ivan-avalos/step">Step</a> interpreter written in C.

## Usage

```
step <file>
step -h
```

## The Step Guide

### Introduction

The main element on Step is the stack, which is where data is stored in order to be used later in the program. Step gives you basic operations you can use to manipulate and process the data contained in the stack in order to get an output. To display a result you can either print it to the standard output or write it into a file.

A program is composed by output, "atoms", comments, argument placeholders and function definitions. Atoms are basically space separated tokens and each token can contain a value or a function. There are diffent types of atoms, which can be used to manipulate stack, print data or write it to a file, retrieve arguments from input and push them to the stack, and more.

### Program structure

To write data to a file instead of printing it to the standard output, you can optionally define an include header on the first line with the name of the output file. You can only write to a single file, and therefore, you can only use a single include header.

```
:output file

...program...
```

### Atoms

| Syntax | Description |
|--------|-------------|
| `<value>` | When you write a valid floating point or integer value, it's automatically pushed into the stack. |
| `<function name>` | Call a language-defined function to perform a basic stack or aritmetic operation. |
| `<constant name>` | Push into the stack a language-defined constant. |
| `@<constant name>` | Call a custom user-defined function to perform a sequence of atoms. |
| `$<parameter index>` | Push into the stack a command line argument. |
| `_"<string>"` | Print a string or write it to a file if include header was defined. |

**Language-defined functions**

| Name      | No. parameters | Description |
|-----------|----------------|-------------|
| `+`       | 2              | Sum the last two items popping them from stack and push the result back. |
| `-`       | 2              | Substract the last two items popping them from stack and push the result back. |
| `*`       | 2              | Multiply the last two items popping them from stack and push the result back. |
| `/`       | 2              | Divide the last two items popping them from stack and push the result back. |
| `pow`     | 2              | Raise the last item to the second-last-itemth power and push the result to the stack. |
| `sqrt`    | 1              | Push the square root of the last item back to the stack. |
| `sin`     | 1              | Push the sine function of the last item back to the stack. |
| `cos`     | 1              | Push the cosine function of the last item back to the stack. |
| `tan`     | 1              | Push the tangent function of the last item back to the stack. |
| `exp`     | 1              | Push _e_ raised to the power of last item back to the stack. |
| `log`     | 1              | Push the natural logarithm of the last item back to the stack. |
| `print`   | 1              | Pop the last item from stack and print it to standard output or write it to a file if include header is defined. |
| `println` | 1              | Pop the last item from stack and write it to the output with a line break at the end. |
| `pop`     | 1              | Pop the last item from stack. |
| `dup`     | 1              | Duplicate the last item on stack. |
| `drop`    | 2              | Pop the last two items on stack, as the opposite of `dup`. |
| `swap`    | 2              | Swap the last two items on stack. |

**Language-defined constants**

| Name | Value |
|------|-------|
| `pi` | `math.pi` |
| `e`  | `math.e` |

### Comments

Comments are removed from the program before this is interpreted.

```
{comment}
```

### Command-line arguments

To run a Step program, you write the name of the file, optionally followed by a list of space separated floating-point or integer values. For example:

```
./pyStep.py foo.step 10 2.5 25.1
```

In order to retrieve them from the program, you simply write a dollar sign followed by the argument number (starting from zero). For example:

```
$0 $1 $2
```

### Define a custom function

A function is a block of atoms that can be executed many times without the need of writing it many times, writing its name instead. To define a number you need to give it a name and a body, which contains a set of space-separated atoms, or a single atom. For example:

```
{ variable functions }
(base 4)
(height 6)

(triangle_area * 2 swap / println)
("circle area" * println)
```

To call a custom user-defined function from the code, you write a '@' symbol followed by the name of the function. For example:

```
@base @height @tringle_area
@base @height @"circle area"
```

## Examples

### Triangle area

```
{formula: b*h/2}
{data: b=13, h=6}

2      {stack: [2]        <- push 2           }
13     {stack: [2, 13]    <- push 13          }
6      {stack: [2, 13, 6] <- push 6           }
*      {stack: [2, 78]    <- push (6)*(13)=78 }
/      {stack: [39]       <- push (78)/(2)=39 }
print  {stack: []}        <- pop              }
```

### Law of universal gravitation

```
:gravitation.step

{formula: F=(G*m1*m2)/d^2}

(G -11 10 pow 6.67 *) {i.e. 6.67e-11}
(m1 $0)
(m2 $1)
(d  $2)

_"m1" @m1 println
_"m2" @m2 println
_"d"  @d println

2 @d pow       {first:  d^2}
@G @m1 * @m2 * {second: G*m1*m2}
/              {result: second / first}

_"F=" println
```

## License 

```
pyStep - Python implementation of Step mathematic stack-based interpreter
Copyright (C) 2018  Iván Ávalos 

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
```