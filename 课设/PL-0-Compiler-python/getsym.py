from symbol import *

# 读入源程序
Error = 0


def getsym(filename):
    global Error
    idNum = 0
    f = open(filename, 'r')
    fw = open('词法.txt', 'w')
    lines = f.readlines()
    line_num = 0
    for line in lines:
        line_num += 1
        i = 0
        while i < len(line):
            while line[i] == ' ':  # 空格跳过
                i = i + 1
            if line[i] == '\n':
                break
            if line[i].isalpha():  # 字母开头
                word = line[i]
                i = i + 1
                while i < len(line) and (line[i].isalpha() or line[i].isdigit()):
                    word += line[i]
                    i = i + 1
                if word in KEYWORDS:
                    SYM.append(KEYWORDS[word])  # 是关键字
                    Position.append((line_num, i - len(word) + 1))  # 出现位置
                    print(line_num, '<', word, ',关键字', '>')
                    fw.writelines('<' + word + ',关键字' + '>' + '\n')
                elif word in OPERATORS:  # 是write read等
                    SYM.append(OPERATORS[word])
                    Position.append((line_num, i - len(word) + 1))
                    print(line_num, '<', word, ',关键字', '>')
                    fw.writelines('<' + word + ',关键字' + '>' + '\n')
                else:
                    SYM.append(ident)  # 是标识符
                    Position.append((line_num, i - len(word) + 1))
                    if word not in ID:
                        ID[word] = idNum
                        idNum = idNum + 1
                    IDi.append(word)
                    print(line_num, '<', word, ',标识符', '>')
                    fw.writelines('<' + word + ',标识符' + '>' + '\n')
                del word  # 清空缓冲区
            elif line[i].isdigit():  # 数字开头
                word = line[i]
                i = i + 1
                while i < len(line) and line[i].isdigit():
                    word += line[i]
                    i = i + 1
                SYM.append(number)
                NUM.append(int(word))
                Position.append((line_num, i - len(word) + 1))
                if line[i].isalpha():  # 判断错误信息
                    while line[i].isalpha() or line[i].isdigit():
                        word += line[i]
                        i += 1
                    print('# 第{}行，第{}列，词法错误（数字后面跟字符）'.format(line_num, i - len(word) + 1))
                    Error = 1
                    fw.writelines('# 第{}行，第{}列，词法错误（数字后面跟字符）\n'.format(line_num, i - len(word) + 1))
                else:
                    print(line_num, '<', word, ',常数', '>')
                    fw.writelines('<' + word + ',常数' + '>' + '\n')
                del word
            elif line[i] == ':' and i + 1 < len(line):
                if line[i + 1] == '=':  # 赋值
                    SYM.append(OPERATORS[':='])
                    Position.append((line_num, i + 1))
                    print(line_num, '<', ':=', ',赋值运算符', '>')
                    fw.writelines('<' + ':=' + ',赋值运算符' + '>' + '\n')
                    i = i + 2
                else:
                    print('# 第{}行，第{}列，词法错误（:后面没有=）'.format(line_num, i))
                    Error = 1
                    fw.writelines('# 第{}行，第{}列，词法错误（数字后面跟字符）'.format(line_num, i) + '\n')
                    i += 1
            elif line[i] == '<' and i + 1 < len(line):
                if line[i + 1] == '=':
                    SYM.append(OPERATORS['<='])
                    Position.append((line_num, i + 1))
                    print(line_num, '<', '>=', ',运算符', '>')
                    fw.writelines('<' + '>=' + ',运算符' + '>' + '\n')
                    i = i + 2
                elif line[i + 1] == '>':
                    SYM.append(OPERATORS['<>'])
                    Position.append((line_num, i + 1))
                    print(line_num, '<', '<>', ',运算符', '>')
                    fw.writelines('<' + '<>' + ',运算符' + '>' + '\n')
                    i = i + 2
                else:
                    SYM.append(OPERATORS['<'])
                    Position.append((line_num, i + 1))
                    print(line_num, '<', '<', ',运算符', '>')
                    fw.writelines('<' + '<' + ',运算符' + '>' + '\n')
                    i += 1
            elif line[i] == '>' and i + 1 < len(line):
                if line[i + 1] == '=':
                    SYM.append(OPERATORS['>='])
                    Position.append((line_num, i + 1))
                    print(line_num, '<', '>=', ',运算符', '>')
                    fw.writelines('<' + '>=' + ',运算符' + '>' + '\n')
                    i = i + 2
                else:
                    SYM.append(OPERATORS['>'])
                    Position.append((line_num, i + 1))
                    print(line_num, '<', '>', ',运算符', '>')
                    fw.writelines('<' + '>' + ',运算符' + '>' + '\n')
                    i += 1
            elif line[i] in OPERATORS:
                SYM.append(OPERATORS[line[i]])
                Position.append((line_num, i + 1))
                print(line_num, '<', line[i], ',运算符', '>')
                fw.writelines('<' + line[i] + ',运算符' + '>' + '\n')
                i = i + 1
            elif line[i] in DELIMITERS:
                SYM.append(DELIMITERS[line[i]])
                Position.append((line_num, i + 1))
                print(line_num, '<', line[i], ',界符', '>')
                fw.writelines('<' + line[i] + ',界符' + '>' + '\n')
                i = i + 1
            else:
                print('# 第{}行，第{}列，非法字符'.format(line_num, i + 1), line[i])
                Error = 1
                fw.writelines('# 第{}行，第{}列，非法字符 '.format(line_num, i + 1) + line[i] + '\n')
                i = i + 1
    f.close()
    fw.close()
    if Error == 1:
        print("词法分析出错")
        exit(-1)
    for i in range(0, len(SYM)):
        print(i, SYM[i], Position[i])  # 词法类型（在symbol表内），出现位置
