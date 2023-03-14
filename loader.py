import lexer as l
import Parser as p
import eval as e
# import typechecking as tc


def main():
    # with open(filename) as f:
    #     code = f.read()
    code = "var num = 600851475143; var factor = 2; while factor * factor <= num do if num / factor == 0 then num = num / factor; factor = 2; else factor += 1; print num;"
    stream = l.Stream.streamFromString(code)
    tokens = l.lexer.lexerFromStream(stream)
    
    parse = p.Parser.call_parser(tokens)
    ast = p.Parser.parse_expr(parse)
    # typed_ast = tc.typecheck(ast)
    output = e.eval_ast(ast)
    print(output)

main()
# if __name__ == "__main__":
#     main("test2.txt")
