import lexer as l
import Parser as p
import eval as e
import typechecking as t
import resolver as r
import os
import bytecode as b


def main(filename):
    with open(filename) as f:
        code = f.read()
    code = '{' + code + '}'
    stream = l.Stream.streamFromString(code)
    tokens = l.lexer.lexerFromStream(stream)
    parse = p.Parser.call_parser(tokens)
    ast = p.Parser.parse_expr(parse)
 
   
   
   # resolvedast = r.resolve(ast)
    # print(ast)
    # print(resolvedast)
    # typedast = t.typecheck(resolvedast)
    output = e.eval_ast(ast)
#     v = b.VM()
#     v.load(b.compile(resolvedast))
#    # print(v.bytecode.insns)
#     output = v.execute()
# #     # print(output)


main("tester/q6.txt")

#call main on all the files in the tester folder
# for filename in os.listdir("tester"):
#     if filename.endswith(".txt"):
#         print(filename)
#         main("tester/" + filename)

