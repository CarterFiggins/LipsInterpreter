
'''
BNF
<operator> ::= +|-|*|/
<if> ::= "if"
<boolOp> ::= and|or
<notOp> :: = not
<compareOP> ::= eq|<|>|<=|>=
<digit> ::= 1|2|3|4|5|6|7|8|9
<boolean> ::= true | false
<number> ::= <digit> | <digit> <number>
<whitechar>::=  \t|_ (tab or empty space)
<ws> ::= <whiteChar> | <whitechar><whitespace>
<expresion> ::= <numberExpression> | <booleanExpressioin>
<numberExpression> ::= <number> | <operator> <ws> <numberExpression> <ws> <numberExpression>
<booleanExpression> ::= <boolean> | <boolOp> <ws> <booleanExpression> <ws> <booleanExpression> 
  | <compareOp> <ws> <numberExpression> <ws> <numberExpression> | <notOP> <ws> <booleanExpression>
<conditionalExpressions> ::= <if> <booleanExpression> <ws> <numberExpression> <ws> <numberExpression>
'''
ArgumentCount = [(1, ['not', "quote"]),(2, ['+', '-', '*', '/', 'and', 'or', 'eq']), (3, ['if'])]
Operators = ["quote",'+', '-', '*', '/', 'if', 'and', 'or', 'not', '>', 'eq' ]

def createParseTree(tokenList):
    parsingList = []
    op = Operators
    if len(tokenList) <=0:
        raise Exception("Missing ending Paretheses 1.0")
    token = tokenList.pop(0)
    if isinstance(token, int):
        return token
    elif token in op:
        raise Exception("Not enough Parentheses")
    else:
        if len(tokenList) <=0:
            raise Exception("Not enough Expressions 1.0")
        operator = tokenList.pop(0)
        parsingList.append(operator)
        numberOfArguments = howMenyArguments(operator)
        for _ in range(numberOfArguments):
            parsingList.append(createParseTree(tokenList))
        # parsingList.append(createParseTree(tokenList))
        # parsingList.append(createParseTree(tokenList))
        if len(tokenList) <=0:
            raise Exception("Not enough ending Parentheses")
        test =tokenList.pop(0)
        if test != ')':
            raise Exception("Too meny Expressions 1.0")
    
    return parsingList
def quote(expression):
    return(expression)         

def evaluate(parseTree):
    if isinstance(parseTree, int):
        return parseTree
    op = parseTree[0]
    if op == '+':
        return evaluate(parseTree[1]) + evaluate(parseTree[2])
    if op == '-':
        return evaluate(parseTree[1]) - evaluate(parseTree[2])
    if op == '*':
        return evaluate(parseTree[1]) * evaluate(parseTree[2])
    if op == '/':
        return evaluate(parseTree[1]) / evaluate(parseTree[2])
    if op == 'not':
        return evaluate(parseTree[1])
    if op == 'and':
        return evaluate(parseTree[1]) and evaluate(parseTree[2])
    if op == 'or':
        return evaluate(parseTree[1]) or evaluate(parseTree[2])
    if op == 'if':
        if evaluate(parseTree[1]):
            evaluate(parseTree[2])
        else:
            evaluate(parseTree[3])
    if op == 'eq':
        return evaluate(parseTree[1]) == evaluate(parseTree[2])
    if op == "quote":
        return quote(parseTree[1])

def howMenyArguments(word):
    for i in range(len(ArgumentCount)):
        if word in ArgumentCount[i][1]:
            return i+1
    return 2






