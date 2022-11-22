#!/usr/bin/env python3

import sys
import doctest

sys.setrecursionlimit(10_000)

# NO ADDITIONAL IMPORTS!

#############################
# Scheme-related Exceptions #
#############################


class SchemeError(Exception):
    """
    A type of exception to be raised if there is an error with a Scheme
    program.  Should never be raised directly; rather, subclasses should be
    raised.
    """

    pass


class SchemeSyntaxError(SchemeError):
    """
    Exception to be raised when trying to evaluate a malformed expression.
    """

    pass


class SchemeNameError(SchemeError):
    """
    Exception to be raised when looking up a name that has not been defined.
    """

    pass


class SchemeEvaluationError(SchemeError):
    """
    Exception to be raised if there is an error during evaluation other than a
    SchemeNameError.
    """

    pass


############################
# Tokenization and Parsing #
############################


def number_or_symbol(x):
    """
    Helper function: given a string, convert it to an integer or a float if
    possible; otherwise, return the string itself

    >>> number_or_symbol('8')
    8
    >>> number_or_symbol('-5.32')
    -5.32
    >>> number_or_symbol('1.2.3.4')
    '1.2.3.4'
    >>> number_or_symbol('x')
    'x'
    """
    try:
        return int(x)
    except ValueError:
        try:
            return float(x)
        except ValueError:
            return x


def tokenize(source):
    """
    Splits an input string into meaningful tokens (left parens, right parens,
    other whitespace-separated values).  Returns a list of strings.

    Arguments:
        source (str): a string containing the source code of a Scheme
                      expression
    """
    print(source)
    
    tokens = []
    input_lines = source.splitlines()
    # print(f'input lines: {input_lines}')
    split_lines = [in_line.split(' ') for in_line in input_lines]
    # print(f'split lines: {split_lines}')
    
    for line in split_lines:
        isComment = False
        for pot_token in line:
            # if not isComment:
            if '(' not in pot_token and ')' not in pot_token and ';' not in pot_token and pot_token != '':
                tokens.append(pot_token)
            else:
                # pot_copy = pot_token
                c_idx = 0
                to_add = ''
                # print(line)
                # print(pot_token)
                while c_idx < len(pot_token):
                    if pot_token[c_idx] == ';':
                        isComment = True
                        break
                    elif pot_token[c_idx] != '(' and pot_token[c_idx] != ')':
                        to_add += pot_token[c_idx]
                    else:
                        if to_add:
                            tokens.append(to_add)
                            to_add = ''
                        if pot_token[c_idx] != '':
                            tokens.append(pot_token[c_idx])
                        
                    c_idx += 1
                if to_add != '':
                    tokens.append(to_add)
                # print(isComment)
                if isComment:
                    break
                    
                    
                # if pot_copy[c_idx] == '(' or pot_copy[c_idx] == ')':
                #     tokens.append(pot_token[c_idx])
                # # parenth_exists = False
                # for c_idx in range(len(pot_copy)):
                #     if pot_copy[c_idx] == '(' or pot_copy[c_idx] == ')':
                #         tokens.append(pot_token[c_idx])
                #         pot_token.replace(pot_copy[c_idx], '', 1)
                    
    return tokens

def check_syntax(tokens):
    """
    Checks if input is valid syntax; otherwise, raises SchemeSyntaxError 
    """
       
    parenth_dict = {}
    for token in tokens:
        if token == '(':
            parenth_dict[token] = parenth_dict.get(token, 0) + 1
        elif token == ')':
            if '(' not in parenth_dict:
                raise SchemeSyntaxError
            else:
                parenth_dict['('] -= 1
        
    if '(' in parenth_dict and parenth_dict['('] != 0:
        raise SchemeSyntaxError
    
    if len(tokens) > 1 and '(' not in parenth_dict:
        raise SchemeSyntaxError

def parse(tokens):
    """
    Parses a list of tokens, constructing a representation where:
        * symbols are represented as Python strings
        * numbers are represented as Python ints or floats
        * S-expressions are represented as Python lists

    Arguments:
        tokens (list): a list of strings representing tokens
    """
    
    check_syntax(tokens)
    
    def parse_expression(index):
        """
        Use recursive-descent method to parse the tokenization.
        """
        token = tokens[index]
        # base cases
        if token != '(' and token != ')':
            return number_or_symbol(token), index + 1
        # recursive case
        else:
            if token == '(':
                new_expression = []
                next_index = index + 1
                while tokens[next_index] != ')':
                    exprs, next_index = parse_expression(next_index)
                    new_expression.append(exprs)
                print(new_expression)
                return new_expression, next_index+1
        
    parsed_expression, next_index = parse_expression(0)
    return parsed_expression


######################
# Built-in Functions #
######################


scheme_builtins = {
    "+": sum,
    "-": lambda args: -args[0] if len(args) == 1 else (args[0] - sum(args[1:])),
}


##############
# Evaluation #
##############


def evaluate(tree):
    """
    Evaluate the given syntax tree according to the rules of the Scheme
    language.

    Arguments:
        tree (type varies): a fully parsed expression, as the output from the
                            parse function
    """
    raise NotImplementedError


########
# REPL #
########


def repl(raise_all=False):
    while True:
        # read the input.  pressing ctrl+d exits, as does typing "EXIT" at the
        # prompt.  pressing ctrl+c moves on to the next prompt, ignoring
        # current input
        try:
            inp = input("in> ")
            if inp.strip().lower() == "exit":
                print("  bye bye!")
                return
        except EOFError:
            print()
            print("  bye bye!")
            return
        except KeyboardInterrupt:
            print()
            continue

        try:
            # tokenize and parse the input, then evaluate and print the result
            tokens = tokenize(inp)
            ast = parse(tokens)
            print("  out> ", evaluate(ast))
        except SchemeError as e:
            # if raise_all was given as True, then we want to raise the
            # exception so we see a full traceback.  if not, just print some
            # information about it and move on to the next step.
            #
            # regardless, all Python exceptions will be raised.
            if raise_all:
                raise
            print(f"{e.__class__.__name__}:", *e.args)
        print()


if __name__ == "__main__":
    # code in this block will only be executed if lab.py is the main file being
    # run (not when this module is imported)

    # uncommenting the following line will run doctests from above
    # doctest.testmod()
#     print(tokenize("""(define circle-area
#   (lambda (r)
#     (* 3.14 (* r r))
#   )
# )""") == tokenize("(define circle-area (lambda (r) (* 3.14 (* r r))))"))
    
#     print(tokenize("(cat (dog (tomato)))") == ['(', 'cat', '(', 'dog', '(', 'tomato', ')', ')',')'])
    
#     print(tokenize(""";add the numbers 2 and 3
# (+ ; this expression
#  2     ; spans multiple
#  3  ; lines

# )"""))
    tokens1 = ['2']
    tokens2 = ['x']
    tokens3 = ['(', '+', '2', '(', '-', '5', '3', ')', '7', '8', ')']
    print(parse(tokens3))
    
    # repl()
