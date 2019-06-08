# -*- coding:utf-8 -*-

# 数字を読む
def readNumber(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        keta = 0.1
    while index < len(line) and line[index].isdigit():
        number += int(line[index]) * keta
        keta /= 10
        index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index

# '+'を読む
def readPlus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1

# '-'を読む
def readMinus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

# '*'を読む
def readAsterisk(line, index):
    token = {'type': 'ASTERISK'}
    return token, index + 1

# '/'を読む
def readSlash(line, index):
    token = {'type': 'SLASH'}
    return token, index + 1

# 数字・演算子など、意味のある言葉に分ける
def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = readNumber(line, index)
        elif line[index] == '+':
            (token, index) = readPlus(line, index)
        elif line[index] == '-':
            (token, index) = readMinus(line, index)
        elif line[index] == '*':
            (token, index) = readAsterisk(line, index)
        elif line[index] == '/':
            (token, index) = readSlash(line, index)
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens


# 1st evaluation *, /
# (3.0 + 2 / 5 - 3 * 4) -> (3.0 + 0.4 -12)
def evaluate1(tokens):
    tokens2 = []
    index = 0
    while index < len(tokens):
        
        if tokens[index]['type'] == 'ASTERISK' or tokens[index]['type'] == 'SLASH':
            
            calc_result = tokens2.pop()['number']
            # calc_result : calc '*' or '/' like 2*3/4
            # the case 2*3/4, token of Number:2 is already in tokens2
            # so pop it from tokens2 and add to calc_result  
            
            while index < len(tokens) and (tokens[index]['type'] == 'ASTERISK' or tokens[index]['type'] == 'SLASH'):
                  
                if tokens[index]['type'] == 'ASTERISK':
                    calc_result *= tokens[index + 1]['number']
                if tokens[index]['type'] == 'SLASH':
                    if tokens[index + 1]['number'] == 0: # division by 0
                        print('ZeroDivisinError')
                        exit(1)
                    calc_result /= tokens[index + 1]['number']
                index += 2
                
            tokens2.append({'type': 'NUMBER', 'number': calc_result})

            
        else: # 掛け算・割り算部以外のtokenはそのまま格納
            tokens2.append(tokens[index])
            index += 1
            
    return tokens2


# 2nd evaluation +, -
# (3.0 + 0.4 -12) -> -8.6
def evaluate2(tokens2):
    answer = 0
    tokens2.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    index = 1
    while index < len(tokens2):
        if tokens2[index]['type'] == 'NUMBER':
            if tokens2[index - 1]['type'] == 'PLUS':
                answer += tokens2[index]['number']
            elif tokens2[index - 1]['type'] == 'MINUS':
                answer -= tokens2[index]['number']
            else:
                print('Invalid syntax')
                exit(1)
        index += 1
    return answer


def test(line):
    tokens = tokenize(line)
    tokens2 = evaluate1(tokens)
    actualAnswer = evaluate2(tokens2)
    expectedAnswer = eval(line)
    if abs(actualAnswer - expectedAnswer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expectedAnswer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expectedAnswer, actualAnswer))

        
# Add more tests to this function :)
def runTest():
    print("==== Test started! ====")
    test("2.0")
    test("1+2")
    test("1-2.0")
    test("1.0+2.1-3")
    test("3*2")
    test("3*2.0")
    test("3/2")
    test("3/2.0")
    test("2*3*4")
    test("1/2/4")
    test("2*3/4")
    test("0.5/2*3")
    test("2.1+0.5/2*3-1")
    test("2.1+0.5/2*3-2/1")
    print("==== Test finished! ====\n")


# main
runTest()
while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line) 
    tokens2 = evaluate1(tokens)  # evaluate '*', '/'
    answer = evaluate2(tokens2)  # evaluate '+', '-'
    print("answer = %f\n" % answer)
