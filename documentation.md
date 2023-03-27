# Lexing 
We have made the following token types as for now: Num | Bool | Keyword | Identifier | Operator | EndOfLine | String
<br>
Keywords in our language: var true false print if else for while return end do
<br>
Symbolic operators in our language: , . ; + - * % > < >= <= == ! != ^ :
<br>
Word operators in our language: and or not quot rem
<br>

Lexer.py takes a string, converts into a stream of characters. The lexer class then separates the stream into tokens which are then used by the parse to convert them into ASTs.


# Parsing

For defining the Context Free Grammar of our language we recognize the following symbols: 


|Symbol | Name|
|:---|:---|
|^   |    power|
|-, !|    unary|
|/, * , % |  mult|
|+, -   | add|
|>, <, >=, <= | comp|
|==, !=  | equality|
|&&, \|\| |log-exp|
|||


We have defined the CFG as follows:


```
expr —> log-exp | List | print | while | if | for
while —> "while" expr "do" expr "end"
if —> "if" expr "then" expr "else" expr "end"
for —> "for" expr ";" expr ";" expr "do" expr "end"
print —> "print" expr ";"
List —> "List" expr ";"
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

The implementation of the parser follows the recursive descent parsing technique. The parser class takes a list of tokens as input and then converts them into an AST. The AST is then used by the interpreter to evaluate the program. The parser class has a method for each non-terminal symbol in the CFG. The method for each non-terminal symbol takes a list of tokens as input and returns the AST for that non-terminal symbol. 