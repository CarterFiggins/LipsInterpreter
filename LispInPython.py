from random import random, randint
import os


#**********************************
#*********ASSIGNMENT THREE*********
#**********************************



#*************PART ONE*************
'''
This is the gramer for the interpeter.
Writen in python and interperting lisp.

BNF 

<operator> ::= +|-|*|/
<digit> ::= 1|2|3|4|5|6|7|8|9
<number> ::= <digit> | <digit> <number>
<whitechar>::=  \t|_ (tab or empty space)
<whiteSpace> ::= <whiteChar> | <whitechar><whitespace>
<expresion> ::= <number> | <operator> <whiteSpace> <expresion> <whiteSpace> <expresion>


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


def prettyPrintParsing(expression, f, depth = 0):
    if isinstance(expression, str):
        if(expression.isdecimal()):        
            f.write("%s %s" % (' ' * depth, expression) + "\n")    
    else:        
        f.write("%s(%s " % (' ' * depth, expression[0])+ "\n")
        prettyPrintParsing(expression[1],f, depth+2)        
        prettyPrintParsing(expression[2],f, depth+2)        
        f.write("%s) " % (' ' * (depth+1))+ "\n")

#**********************************
#*********ASSIGNMENT FOUR**********
#**********************************

#*************PART ONE*************
# Write a Parser

def parsingTree(tokenList):
    parsingList = []
    op = ["+","-","/","*"]
    if isinstance(tokenList, str):
        raise Exception("ERROR Not enough Parentheses")
    token = tokenList.pop(0)
    if token.isdecimal():
        return token
    elif token in op:
        raise Exception("Not enough Parentheses")
    else:
        parsingList.append(tokenList.pop(0))
        parsingList.append(parsingTree(tokenList))
        if tokenList[0] == ')':
            # print("ERROR not enough Expressions")
            raise Exception("Not enough Expressions")
        parsingList.append(parsingTree(tokenList))
        if len(tokenList) <=0:
            raise Exception("Missing parentheses")

        test =tokenList.pop(0)
        if test != ')':
            # print("ERROR Too meny Expressions")
            raise Exception("Expressions Missing")
    
    return parsingList

#*************PART TWO*************
# Test With text files
def runFiles():
    with open("prettyPrintCorrect.txt", "w+") as printCorrect:
        with open("correctSyntax.txt") as fileCorrect:
            for line in fileCorrect:
                
                prettyPrintParsing(parsingTree(tokenize(line)),printCorrect,0)
                printCorrect.write("*************NEW LINE**************\n")
    with open("error.txt", "w+") as errors:
        with open("errorSyntax.txt")as fileErrors:
            for line in fileErrors:
                try:
                    prettyPrintParsing(parsingTree(tokenize(line)),errors,0)
                except Exception as error:
                    errors.write("Parse error: "+ str(error) + "\n")


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
    tests.append("(*(+(- 9 5)(+(/ 58 7)(* 3 2)))5)") # Will Work
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


def testingParser():
    print("should be")
    print("[* 73 98]")
    print(" ------------------")
    test=parsingTree(tokenize("(* 73 98)"))
    print(test)
    print("__________________")
    print("Should Be")
    print("( +( /( *(+ 5 2)(- 5 8) ) 2)(* 5 6))")
    print(" ------------------")
    print(parsingTree(tokenize("( +( /( *(+ 5 2)(- 5 8) ) 2)(* 5 6))")))
    print("__________________")
    print("Should Be")
    print("(*(+ 5 2)(/ 6 8))")
    print(" ------------------")
    print(parsingTree(tokenize("(*(+ 5 2)(/ 6 8))")))
    print("__________________")
    print("Too meny expressions")
    # need to try block to test!!!
    try:
        print(parsingTree(tokenize("(* 5 (/ 8 9 3)")))
        print("__________________")
        print("not enough expressions")
        print(parsingTree(tokenize("(* 5 (+ 5))")))
    except Exception as error:
                    print(str(error) + "\n")


#MAIN CODE
if __name__ == '__main__':
    # print("TESTING TOKENIZE AND PRETTY PRINT")
    # print("_________________________________\n")
    # testingTokenize()
    # testingPrettyPrint()

    # print("\n________________________________")
    # print("TESTING PARSER \n")
    testingParser()

    #runs the files
    # runFiles()


