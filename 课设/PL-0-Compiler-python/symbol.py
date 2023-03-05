KEYWORDS = {'program': 0, 'const': 1, 'var': 2, 'procedure': 3, 'begin': 4, 'end': 5,
            'if': 6, 'then': 7, 'call': 8, 'while': 9, 'do': 10, 'else': 32}
OPERATORS = {'read': 11, 'write': 12, 'odd': 13,'=': 14, ':=': 15, '+': 16, '-': 17, '*': 18,
             '/': 19, '<>': 20, '<': 21, '<=': 22, '>': 23, '>=': 24, 'post': 29}  # post表示参数传递
DELIMITERS = {',': 25, ';': 26, '(': 27, ')': 28}
ident = 30
number = 31
SYM = []  # 单词类型，对应上述的数值
Position = []  # 单词出现位置
ID = {}  # 分析出的标识符
IDi = []  # 分析出的的单词
NUM = []  # 数字，不包括符号
