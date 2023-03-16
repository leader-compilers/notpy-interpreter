import lexer as l
import Parser as p
import eval as e
#import typechecking as tc


def main(filename):
    with open(filename) as f:
        code = f.read()
    # print(code)
    stream = l.Stream.streamFromString(code)
    tokens = l.lexer.lexerFromStream(stream)
    parse = p.Parser.call_parser(tokens)
    ast = p.Parser.parse_expr(parse)
    # typed_ast = tc.typecheck(ast)
    print(ast)
    output = e.eval_ast(ast)
    
if __name__ == "__main__":
    main("euler4.txt")
