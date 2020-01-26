from random import random, randint
import os


#*************PART ONE*************
'''
This is the gramer for the interpeter.
Writen in python and interperting lisp.

BNF 

<operator> ::= +|-|*|/
<digit> ::= 1|2|3|4|5|6|7|8|9
<specialOp> ::= +|-|*
<number> ::= <digit> | <digit> <number>
<whitechar>::=  \t|_ (tab or empty space)
<whiteSpace> ::= <whiteChar> | <whitechar><whitespace>
<expresion> ::= <number> | <operator> <whiteSpace> <expresion> <whiteSpace> <expresion>
| <specialOp> <whiteSpace> <expresion> <whiteSpace> <argument>
<argument> ::= <expresion> | <expresion> <whitespace> <argument>

'''

#*************PART TWO************* 
#Tokenizer

Operators = ['+', '-', '*', '/']

# takes in a string and changes it into a list of tokens
def tokenize(chars):
    # takes a string representing an expression in simple lisp and returns a list of tokens
    badtoken = []
    check = chars.replace('(', ' ( ').replace(')', ' ) ').split()
    correct = True

    # Checks to make sure they are valid tokens
    for i in check:
        if(i in Operators or i == '(' or i ==')' or i.isdecimal() ):
            pass
        
        else:
            correct = False
            badtoken.append(i)
    if(correct):
        return check
    else:
        return"ERROR Incorrect Token" + str(badtoken)


# *************PART Three************* 
# Pretty Print
# Makes easy to read depth tree

def prettyPrintFromTokens(tokens, depth = 0):
    spaces = "    " * depth

    if tokens[0] == ')':
        if(depth > 0):
            spaces = "    " * (depth -1)
        print(spaces + tokens[0])
        depth -= 1
        if depth == 0:
            return
        else:
            prettyPrintFromTokens(tokens[1:], depth)

    if tokens[0].isdecimal() and len(tokens) <=1:
        print(spaces + tokens[0])
        return

    if tokens[0].isdecimal():
        print(spaces + tokens[0])
        prettyPrintFromTokens(tokens[1:], depth)

    if tokens[0] == '(':
         print(spaces + tokens[0] + tokens[1])
         prettyPrintFromTokens(tokens[2:], depth+1)

# parsing tree is 

def parsingTree(tokenList):
    token = tokenList.pop(0)
    if( token instenceOf int):



'''
Add stuff to gramer and parser assn 5
(and (or True False)(not True))
(eq(and True False)(or False True))
(eq 5 (+ 7 10))
'''


#*************TESTING*************


# testing the Tokenize Function 0 - 5 tests 0-2 should work 3-5 sould not work
def testingTokenize():
    tests = []
    tests.append("5") # Will Work
    tests.append("(* 73 982)") # Will Work
    tests.append("(*(+(- 9 5)(+(/ 58 7)(* 3 2))))") # Will Work
    tests.append("!") # Will Fail
    tests.append("(^ 5 8)") # Will Fail
    tests.append("(/(+(+ d f)5)(* 5(* 5 2)))") # Will Fail
    print("Testing the tokenize Function")
    count = 0
    print("Tests 0-2 Should work. Tests 3-5 sould trow an error")
    for test in tests:
        print("------------")
        print("Test" + str(count))
        count +=1
        print(tokenize(test))
    print("----------------------- \n")

# Make sure Tokenize function work first befor testing PrettyPrint
# Makes the output more readable and can see depth
def testingPrettyPrint():
    print("Testing PrettyPrint functioin all print outs should be correct") 
    tests = []
    tests.append("5") # Will Work
    tests.append("(* 73 982)") # Will Work
    tests.append("(*(+(- 9 5)(+(/ 58 7)(* 3 2)))5)") # Will Work
    tests.append("(+(/ 5 2)(* 3 2))") # Will work
    tests.append("(/ (+ (+ 21 31) (* 92 75)) (- (* 57 55) (/ 26 94)))") # Will work
    count = 0
    for test in tests:
        print("------------")
        print("Test" + str(count))
        count +=1
        prettyPrintFromTokens(tokenize(test))

print("TESTING TOKENIZE AND PRETTY PRINT")
print("_________________________________\n")
testingTokenize()
testingPrettyPrint()











#FROM STARTER CODE random generater

# def generateRandomExpression(maxDepth = 10):
#     # generates a string that is a legal sentence in the grammar of our simple lisp language
#     if random() < 0.1 or maxDepth < 0:
#         return str(randint(0, 100))
#     else:
#         return "(%s %s %s)" % (Operators[randint(0, 3)], 
#                                 generateRandomExpression(maxDepth - 1), 
#                                 generateRandomExpression(maxDepth - 1))
                

    
# def atom(token):
#     # changes a token to an actual integer 
#     if token.isdigit():
#         return int(token)
#     return token
    
# print(atom('56'))
# print(atom('('))
# print(atom('0.344'))
# print(atom('+'))

# for _ in range(0, 10):
#     exp = generateRandomExpression(2)
#     print(exp)
#     print(tokenize(exp))

