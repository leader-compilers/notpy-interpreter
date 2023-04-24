# notpy-interpreter
This repository contains the source code and the documentation of the programming language "Notpy" for which we built the interpreter as a part of our Compilers course at IIT Gandhinagar under the professor Balagopal Komarath.

# Tutorial for Notpy Interpreter

## Power operations
The language provides power operation using “^” or “**” operator. 
```
>> y = 2^3;
8

>> z = 2**3;
8
```
## Unary Operations
For the time being, the language provides one unary operation in our language and it is “!” operator. It basically negates the value of the variable on which it is used. nesting of unary operators is not allowed.
```
>> y = True;
True

>> !y;
False
```
## Floor operation
The floor operation is used to get the floor value of a number. It is denoted by “//” operator.
```
>> y = 5//2;
2
```
## Multiplication, Division and Modulo
The language provides multiplication, division and modulo operations using “*”, “/” and “%” operators respectively.
```
>> y = 5*2;
10

>> z = 5/2;
2.5

>> a = 5%2;
1
```
## Addition and Subtraction
The language provides addition and subtraction operations using “+” and “-” operators respectively.
```
>> y = 5+2;
7

>> z = 5-2;
3
```
## Comparison Operations
The language provides comparison operations using “<”, “>” operators respectively. Nesting of comparison operators is not allowed.
```
>> y = 5<2;
False

>> z = 5>2;
True
```
## Equality and Inequality
The language provides equality and inequality operations using “==” and “!=” operators respectively. Nesting of equality operators is not allowed.
```
>> y = 5==2;
False

>> z = 5!=2;
True
```
## Logical Operations
The language provides logical operations using “and”, “or” operators respectively.
```
>> y = True and False;
False

>> z = True or False;
True
```
## Defining and Setting Variables values
The language provides a way to define variables using "var" keyword.
```
>> var x = 5;
5

>> x = 10;
10
```
## Print Statement
The language provides a way to print the value of a variable using "print" keyword.
```
>> var x = 5;
5

>> print x;
5
```
## Declaring  and Calling Functions
The language provides a way to declare functions using "def" keyword.
```
>> def add(x, y){
...     return x + y;
... }
...

>> var z = add(5, 6);
11
```
## Block expressions
The language provides a way to define block expressions using “{” and “}”.
```
>> {
...     var total = 0; 

...     for( i = 1 ; i < 1001 ; i = i + 1 ) {
...        if (i%3 == 0 or i%5==0) 
...        {
...            total = total + i;
...        } 
...        else 
...        {
...            total = total;
...        } 
...    }
...
...    print total;
...
...}
...
233168
```
## While loop
The language provides a way to define while loop using “while” keyword.
```
>> var i = 0;
0

>> while(i < 3) {
...     print i;
...     i = i + 1;
... }
...
0
1
2
```
## For loop
The language provides a way to define for loop using “for” keyword.
```
>> for( i = 1 ; i < 3 ; i = i + 1 ) {
...     print i;
... }
...
1
2
```
## If Statement
The language provides a way to define if statement using “if” keyword. We can either use if statement or if-else statement. If there is no else statement, then the if statement will be executed if the condition is true.
```
>> var j = 1;
1

>> if (j == 1) {
...     print "Hello World";
... }
...
Hello World

>> j = 2;
2
>> if (j == 2) {
...     print "Hello World";
... }
... else {
...     print "Hello World 2";
... }
...
Hello World 2
```
## Let Statement
The language provides a way to define let statement using “let” keyword.
```
>> let a = 1 in a + 1;
2
```



