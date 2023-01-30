# Lexing 
We have made the following token types as for now: Num | Bool | Keyword | Identifier | Operator | EndOfLine | String
Keywords in our language: var true false print if else for while return end do
Symbolic operators in our language: , . ; + - * % > < >= <= == ! != ^ :
Word operators in our language: and or not quot rem

Lexer.py takes a string, converts into a stream of characters. The lexer class then separates the stream into tokens which are then used by the parse to convert them into ASTs.


# Parsing

For defining the Context Free Grammar of our language we recognize the following symbols: 


|Symbol | Name|
|:---|:---|
|^   |    power|
|-, !|    unary|
|/, *  |  mult|
|+, -   | add|
|>, <, >=, <= | comp|
|==, !=  | equality|
|&&, \|\| |log-exp|
|||


We have defined the CFG as follows:


```
expr —> log-exp
log-exp —> equality(&&,||)log-exp | equality
equality —> comp(==,!=)comp | comp
comp —> add(>, <, >=, <=)add | add
add —> mult(+, -)add | mult
mult —> mult(/,*)unary | unary
unary —> (!,-)unary | power
power —> power(^)primary | primary
primary —> Num | Bool | Keyword | Identifier | Operator | EndOfLine | String
```

Some points to note:-
We have allowed nesting of unary operators.
We have not allowed nesting of comp (comparison operators) and equality.
