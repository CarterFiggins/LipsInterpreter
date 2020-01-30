from random import random, randint
from newCode import evaluate, createParseTree
import os

    
# define all the possible operators and how many arguments they take
Operators = ['+', '-', '*', '/', 'if', 'and', 'or', 'not', '>', 'eq' ]
NumberOfArguments = {}
ArgumentCount = [(1, ['not']),(2, ['+', '-', '*', '/', 'and', 'or', 'eq']), (3, ['if'])]
# fill the mapping from operator to argument count
for (count, operators) in ArgumentCount:
    for op in operators:
        NumberOfArguments[op] = count
    
############## STARTER CODE ####################################################
# only simple math to start with
def generateRandomExpression(maxDepth = 10):
    # generates a string that is a legal sentence in the grammar of our simple lisp language
    if random() < 0.1 or maxDepth < 0:
        return str(randint(0, 100))
    else:
        return "(%s %s %s)" % (Operators[randint(0, 3)], 
                                generateRandomExpression(maxDepth - 1), 
                                generateRandomExpression(maxDepth - 1))

def atom(token):
    # changes a token to an actual integer 
    if token.isdigit():
        return int(token)
    return token
    
def genGood ():
    # Generate a set of correct random test problems
    with open(PATH + 'correctSyntax.txt', 'w') as file:  # Use file to refer to the file object
        for _ in range(0, 1000):
            file.write(generateRandomExpression(1 + randint(0,10)) + "\n")
            
def genBad ():
    with open(PATH + 'errorSyntax.txt', 'w') as file:  # Use file to refer to the file object
        for _ in range(0, 1000):
            program = generateBadRandomExpression(1 + randint(0,10)) #(1 + randint(0,10))
            try: #try to parse the expression
                parseTree = parse(program)
            # Only if it does not parse then we save
            except Exception as error:
                file.write(program + "\n")
                
BadOps = ['_', '=','(','%']
BadNumbers = ['1.2344','x','y']
def generateBadRandomExpression(maxDepth = 10):
    # generates a string that is a legal sentence in the grammar of our simple lisp language
    if random() < 0.1 or maxDepth < 0:
        return str(randint(0, 100))
    if random() < 0.05 or maxDepth < 0:
        return str(BadNumbers[randint(0, len(BadNumbers)-1)])
    elif random() < 0.05:
        return "(%s %s %s" % (Operators[randint(0, 3)], 
                                generateBadRandomExpression(maxDepth - 1), 
                                generateBadRandomExpression(maxDepth - 1))
    elif random() < 0.05:
        return "%s %s %s)" % (Operators[randint(0, 3)], 
                                generateBadRandomExpression(maxDepth - 1), 
                                generateBadRandomExpression(maxDepth - 1))
    else:
        return "(%s %s %s)" % (Operators[randint(0, 3)], 
                                generateBadRandomExpression(maxDepth - 1), 
                                generateBadRandomExpression(maxDepth - 1))
                        
                        
### takes a program string and returns a parse tree
def parse(programStr):
    # returns the input string as a parse tree, represented as either an int or a list of expressions
    return createParseTree(tokenize(programStr))
                          
### prettyPrint an expression (parsed list of tokens)
def prettyPrintExp(expression, depth = 0):
    # takes a parse tree and prints it out so it is easier to read (maybe)
    if isinstance(expression, int):
        print("%s %d" % (' ' * depth, expression))
    else:
        print("%s(%s " % (' ' * depth, expression[0]))
        prettyPrintExp(expression[1], depth+2)
        prettyPrintExp(expression[2], depth+2)
        print("%s) " % (' ' * (depth+1)))
        
### prettyPrint a list of tokens
def prettyPrint(tokenList, depth = 0):
    token = tokenList.pop(0)
    # atom, just print at depth and return
    if isinstance(token, int):
        print("%s%d" % (' ' * depth, token))
    else:
        # compound expression
        operator = tokenList.pop(0)
        print("%s(%s" % (' ' * depth, operator))
        prettyPrint(tokenList, depth+1)
        prettyPrint(tokenList, depth+1)
        tokenList.pop(0) # remove )
        print("%s)" % (' ' * depth,))
        
### very simple code that just checks whether the number of open parentheses
### is the same as the number of closed parentheses
def checkBalanced(tokenList):
    depth = 0
    while not tokenList == []:
        token = tokenList.pop(0)
        if token == '(': #consume and add 1 to depth
            depth = depth + 1
        if token == ')':
            depth = depth - 1
    return depth == 0
    
### takes a string representing an expression in simple lisp and returns a list of tokens
def tokenize(programStr):
    tokens = programStr.replace('(', ' ( ').replace(')', ' ) ').split()
    if all(legalToken(token) for token in tokens):
        return [atom(token) for token in tokens]
    else:
        badTokens = str([token for token in tokens if not legalToken(token)])[1:][:-1]
        raise Exception("Unknown token found %s" % (badTokens,))
  
### returns True if the token is legal      
def legalToken(token):
    # returns True if legal for our simple lisp
    return token.isdigit() or token in Operators + [')', '(']
            

# Do some testing
# for _ in range(100): 
#     exp = generateBadRandomExpression(3)
#     try: #try to parse the expression
#         parseTree = parse(exp)
#         # prettyPrint(tokenize(exp))
#         # prettyPrintExp(parseTree)    
#     except Exception as error:
#         print("\n")
#         print(exp)
#         print("Parse error: %s" % (error,))
# 
# for _ in range(100): 
#     exp = generateRandomExpression(3)
#     parseTree = parse(exp)
#     prettyPrint(tokenize(exp))

def prettyPrintToFile(expression, f, depth = 0):
    if isinstance(expression, int):        
        f.write("%s %s" % (' ' * depth, expression) + "\n")    
    else:        
        f.write("%s(%s " % (' ' * depth, expression[0])+ "\n")
        prettyPrintToFile(expression[1],f, depth+2)        
        prettyPrintToFile(expression[2],f, depth+2)        
        f.write("%s) " % (' ' * (depth+1))+ "\n")


#TODO: Make assiment 6 check to see if (and 5 2) is ok or should the 
# parser know about booleans or not

def testingParser():
    print("should be")
    print("[* 73 98]")
    print(" ------------------")
    test=createParseTree(tokenize("(* 73 98)"))
    print(test)
    print("__________________")
    print("Should Be")
    print("( +( /( *(+ 5 2)(- 5 8) ) 2)(* 5 6))")
    print(" ------------------")
    print(createParseTree(tokenize("( +( /( *(+ 5 2)(- 5 8) ) 2)(* 5 6))")))
    print("__________________")
    print("Should Be")
    print("(*(+ 5 2)(/ 6 8))")
    print(" ------------------")
    print(createParseTree(tokenize("(*(+ 5 2)(/ 6 8))")))
    try:
        print("__________________")
        # need to find out if we accept (and 5 2)
        print(createParseTree(tokenize("((((+(if (eq 5  12 6) 6 15) 20)")))
    except Exception as error:
                    print(str(error) + "\n") 
def runFiles():
    with open("prettyPrintCorrect.txt", "w+") as printCorrect:
        with open("correctSyntax.txt") as fileCorrect:
            for line in fileCorrect:
                
                prettyPrintToFile(createParseTree(tokenize(line)),printCorrect,0)
                printCorrect.write("*************NEW LINE**************\n")
    with open("error.txt", "w+") as errors:
        with open("errorSyntax.txt")as fileErrors:
            for line in fileErrors:
                try:
                    prettyPrintToFile(createParseTree(tokenize(line)),errors,0)
                except Exception as error:
                    errors.write("Parse error: "+ str(error) + "\n")


# testingParser()
runFiles()

#genGood()
#genBad()             
                                
                                
                                