from symbol import KEYWORDS, OPERATORS, DELIMITERS, SYM, ident, number, IDi, NUM, Position
from node import Node
from table import Table, Entry, isConst, KIND
from inst import Code

p = 0  # 扫描的当前单词(各种标识符和符号等)的位置
pid = 0  # 标识符的位置
pnum = 0
Error = 0
root = Node('<程序>')
table = Table()  # table表，符号表
code = []  # CODE数组，存储中间代码
startCode = Code('JMP', 0, None)
code.append(startCode)
code.append(Code('JMP', 0, 2))
tableList = []  # 每一层的符号表


def error(a=0):  # 出错
    case = [
        '0 '
    ]
    # print("Error:",p)
    exit(-1)


def advance():
    global p
    p = p + 1


# 开始语法分析、中间代码生成等工作 <prog> → program <id>；<block>
def program():
    if SYM[p] == KEYWORDS['program']:
        Table, entry = G2(table)  # 获取program信息
    else:
        print("缺少program关键字!!!")
        error()
        return

    tableList.append(Table)
    entry = None
    block(root, table, entry)  # 获取<block>


# <块> <block> → [<condecl>][<vardecl>][<proc>]<body>
def block(root, table, entry):
    startAddr = B(root, table, entry)
    startCode.a = startAddr
    if Error == 1:
        error()
    elif p == len(SYM):
        print("目标代码已生成")
    else:
        x, y = Position[p][0], Position[p][1]
        print('({},{})执行语句未在begin…end中'.format(x - 1, y))
        error()


# <块> [<condecl>][<vardecl>][<proc>]<body>
def B(parent, table, enrty=None):
    global p
    if SYM[p] != KEYWORDS['const'] and SYM[p] != KEYWORDS['var'] and SYM[p] != KEYWORDS['procedure'] and SYM[p] != \
            KEYWORDS['begin']:  # 检查是否是<condecl> <vardecl> <proc> <body>
        print(Position[p], 'block中需要关键词const or var or procedure or begin')
        global Error
        Error = 1
        while p < len(SYM) - 1 and SYM[p] != KEYWORDS['const'] and SYM[p] != KEYWORDS['var'] and SYM[p] != KEYWORDS[
            'procedure']:
            p += 1
    child = Node('<分程序>')
    parent.add(child)
    Const(child, table)  # 获取常量说明部分
    E(child, table)  # 获变量说明部分
    if SYM[p] == KEYWORDS['procedure']:
        F(child, table)  # 分析分程序
    startAddr = len(code)
    if enrty is not None:
        enrty.adr = startAddr
    code.append(Code('INT', 0, table.getSize()))  # 数据栈栈顶指针增加符号表的量
    J(child, table)  # 分析body
    code.append(Code('OPR', 0, 0))  # 执行运算，a表示执行某种运算，其数值参考symbol.py
    return startAddr


# <常量说明部分> <condecl> → const <const>{,<const>}
def Const(parent, table):
    if SYM[p] == KEYWORDS['const']:
        child = Node('<常量说明部分>')
        parent.add(child)
        child.add(Node('const'))
        advance()
        Define_const(child, table)
        while SYM[p] == DELIMITERS[',']:
            child.add(Node(','))
            advance()
            Define_const(child, table)
        if SYM[p] == DELIMITERS[';']:
            child.add(Node(';'))
            advance()
        else:
            print(Position[p], "行末缺少分号")
            global Error
            Error = 1


# <常量定义> <const> → <id>:=<integer>
def Define_const(parent, table):
    global Error
    child = Node('<常量定义>')
    parent.add(child)
    if SYM[p] != ident:
        print(Position[p], "常量定义类型错误，应为ident")
        Error = 1
    name = Ident(child, table)
    advance()
    if SYM[p] != OPERATORS[':=']:
        print(Position[p], "赋值号错误，赋值号为:=")
        Error = 1
    child.add(Node(':='))
    advance()
    if SYM[p] != number:
        print(Position[p], "常量赋值错误，只能用常数赋值")
        Error = 1
    val = W(child, table)
    advance()
    entry = Entry(name, KIND.CONSTANT, val)  # 常量赋值
    t = table.add(entry)
    if t == 1:
        print(Position[p], entry.name + ' 重定义')
        Error = 1


# <变量说明部分> <vardecl> → var <id>{,<id>}
def E(parent, table):
    global Error
    if SYM[p] == KEYWORDS['var']:
        child = Node('<变量说明部分>')
        parent.add(child)
        child.add(Node('var'))
        advance()
        if SYM[p] != ident:
            print(Position[p], "变量类型定义错误，只能是ident")
            Error = 1
        name = Ident(child, table)
        entry = Entry(name, KIND.VARIABLE)  # 变量赋值
        t = table.add(entry)
        if t == 1:
            print(Position[p], entry.name + ' 重定义')
            Error = 1
        advance()
        while SYM[p] == DELIMITERS[',']:
            child.add(Node(','))
            advance()
            if SYM[p] != ident:
                print(Position[p], "变量类型定义错误，只能是ident")
                Error = 1
            name = Ident(child, table)
            entry = Entry(name, KIND.VARIABLE)  # 变量赋值
            t = table.add(entry)
            if t == 1:
                print(Position[p], entry.name + ' 重定义')
                Error = 1
            advance()
        if SYM[p] == DELIMITERS[';']:
            child.add(Node(';'))
            advance()
        else:
            print(Position[p], "行末缺少分号")
            Error = 1


# <过程说明部分> <proc> → procedure <id>（[<id>{,<id>}]）;<block>{;<proc>}
def F(parent, table):
    child = Node('<过程说明部分>')
    parent.add(child)
    childTable, entry = G(child, table)  # 分析分程序
    tableList.append(childTable)  # 将新的符号包添加至总的符号包
    B(child, childTable, entry)
    # table.entries[name].adr=len(code)
    while SYM[p] == DELIMITERS[';']:  # 如果还存在{;<proc>}
        child.add(Node(';'))
        advance()
        if SYM[p] == KEYWORDS['procedure']:
            F(child, table)
        else:
            error()

# <分程序> <proc> → procedure <id>（[<id>{,<id>}]）;<block>{;<proc>}
def G(parent, table):
    global Error
    if SYM[p] == KEYWORDS['procedure']:
        child = Node('<过程首部>')
        parent.add(child)
        child.add(Node('procedure'))
        advance()
        if SYM[p] != ident:
            print(Position[p], 'procedure后面缺少ident')
            Error = 1
        name = Ident(child, table)
        entry = Entry(name, KIND.PROCEDURE)
        t = table.add(entry)
        if t == 1:
            print(Position[p], entry.name + ' 重定义')
            Error = 1
        childTable = Table(table)  # 建立子符号表
        advance()
        if SYM[p] != DELIMITERS['(']:
            print(Position[p], "procedure后面缺少()")
            Error = 1
        advance()
        while SYM[p] == ident:  # 分析形参
            name = Ident(child, table)
            entry1 = Entry(name, KIND.VARIABLE)
            childTable.add(entry1)
            advance()
            while SYM[p] == DELIMITERS[',']:
                child.add(Node(','))
                advance()
                if SYM[p] == ident:
                    name = Ident(child, table)
                    entry1 = Entry(name, KIND.VARIABLE)
                    childTable.add(entry1)
                    advance()
                else:
                    print(Position[p], "传参只能传ident")
                    Error = 1
        if SYM[p] == DELIMITERS[')']:
            advance()
        else:
            print(Position[p], "缺少‘)’")
            Error = 1
        if SYM[p] == DELIMITERS[';']:
            child.add(Node(';'))
            advance()
            return childTable, entry
        else:
            print(Position[p], "缺少分号")
            Error = 1
    else:
        print(Position[p], "递归错误！")
        Error = 1
        error()

# <程序>  program <id>;<block>
def G2(table):
    global Error
    if SYM[p] != KEYWORDS['program']:
        print(Position[p], "缺少程序开始标志program")
        exit(-1)
    advance()
    if SYM[p] == '(':
        print(Position[p], 'program后面缺少ident')
        Error = 1
    elif SYM[p] != ident:
        print(Position[p], "类型错误program后面定义为ident类型")
        Error = 1
    child1 = Node('program')  # program
    name = Ident(child1, table)  # <id>
    entry = Entry(name, KIND.PROCEDURE)  # 入口名称, 类型, 值
    t = table.add(entry)  # 添加至符号表中
    if t == 1:
        print(Position[p], entry.name + ' 重定义')  # 变量重定义
        Error = 1
    advance()
    if SYM[p] == DELIMITERS[';']:
        child1.add(Node(';'))
        advance()
        return table, entry
    else:
        child1.add(Node(';'))
        print(Position[p], "行末缺少分号")
        Error = 1
        return table, entry


# <statement>
def H(parent, table):
    child = Node('<语句>')
    if SYM[p] == ident:
        I(child, table)  # 分析赋值
    elif SYM[p] == KEYWORDS['if']:
        R(child, table)
    elif SYM[p] == KEYWORDS['while']:
        T(child, table)
    elif SYM[p] == KEYWORDS['call']:
        S(child, table)
    elif SYM[p] == OPERATORS['read']:
        U(child, table)
    elif SYM[p] == OPERATORS['write']:
        V(child, table)
    elif SYM[p] == KEYWORDS['begin']:
        J(child, table)  # 分析复合语句
    else:
        return
    parent.add(child)


# <赋值语句> <id> := <exp>
def I(parent, table):
    global Error
    if SYM[p] == ident:
        child = Node('<赋值语句>')
        parent.add(child)
        name = Ident(child, table)
        advance()
        if SYM[p] != OPERATORS[':=']:
            print(Position[p], "赋值号错误！")
            Error = 1
        child.add(Node(':='))
        advance()
        L(child, table)  # 分析表达式<exp>

        l, a, flag = table.find(name)
        if str(flag) == '0':
            print(Position[p], '错误，未定义的标识符', name)
            Error = 1
        if flag == isConst:
            print(Position[p], '对常量的非法赋值:' + name)
            Error = 1
        else:
            code.append(Code('STO', l, a))  # 将数据栈栈顶的内容存入变量（相对地址为a，层次差为L）
    else:
        print(Position[p], '递归错误')
        error()


# <复合语句> begin <statement>{;<statement>}end
def J(parent, table):
    child = Node('<复合语句>')
    parent.add(child)
    if SYM[p] == KEYWORDS['begin']:
        child.add(Node('begin'))
        advance()
        H(child, table)  # 分析<statement>
        while SYM[p] == DELIMITERS[';'] or SYM[p] == ident or SYM[p] == KEYWORDS['if'] or SYM[p] == KEYWORDS['begin'] or \
                SYM[p] == OPERATORS['read'] or SYM[p] == OPERATORS['write'] or SYM[p] == KEYWORDS['call']:  # 判断是否还存在<statement>
            if SYM[p] == DELIMITERS[';']:
                child.add(Node(';'))
                advance()
                H(child, table)
            else:
                print(Position[p], "行末缺少分号")
                global Error
                Error = 1
                child.add(Node(';'))
                H(child, table)
        if SYM[p] == KEYWORDS['end']:
            child.add(Node('end'))
            advance()
        else:
            print(Position[p], "begin后面缺少end")
            Error = 1
    else:
        print(Position[p], "递归错误!")
        error()


# <条件> <lexp> → <exp> <lop> <exp>|odd <exp>
def K(parent, table):
    child = Node('<条件>')
    parent.add(child)
    if SYM[p] == OPERATORS['+'] or SYM[p] == OPERATORS['-'] or SYM[p] == ident or SYM[p] == number or SYM[p] == \
            DELIMITERS['(']:  # <exp> → [+|-]<term>{<aop><term>}
        L(child, table)  # 分析表达式<exp>
        opr = Q(child, table)  # 分析关系运算符 <lop>
        L(child, table)  # 分析表达式<exp>
        code.append(Code('OPR', 0, opr))  # 执行运算
    elif SYM[p] == OPERATORS['odd']:
        child.add(Node('odd'))
        advance()
        L(child, table)
        code.append(Code('OPR', 0, OPERATORS['odd']))
    else:
        print(Position[p], "无法识别的条件判断")
        global Error
        Error = 1


# <表达式> <exp> → [+|-]<term>{<aop><term>}
def L(parent, table):
    child = Node('<表达式>')
    parent.add(child)
    if SYM[p] == OPERATORS['+']:
        child.add(Node('+'))
        advance()
        M(child, table)  # 分析项<term>
    elif SYM[p] == OPERATORS['-']:
        child.add(Node('-'))
        advance()
        M(child, table)
        code.append(Code('LIT', 0, -1))  # 取常量-1放入数据栈栈顶
        code.append(Code('OPR', 0, OPERATORS['*']))  # 如果是-号做取负运算 用-1乘某个数
    else:
        M(child, table)
    while SYM[p] == OPERATORS['+'] or SYM[p] == OPERATORS['-']:  # 如果存在<aop>
        # print('符号',SYM[p])
        opr = SYM[p]
        O(child, table)  # 分析加减运算符
        M(child, table)  # 分析<term>
        code.append(Code('OPR', 0, opr))  # 执行运算


# <项> <term> → <factor>{<mop><factor>}
def M(parent, table):
    child = Node('<项>')
    parent.add(child)
    N(child, table)  # 分析因子<factor>
    while SYM[p] == OPERATORS['*'] or SYM[p] == OPERATORS['/']:  # 先乘除，后加减，分析<mop>
        opr = SYM[p]
        P(child, table)  # 分析乘除
        N(child, table)  # 分析因子
        code.append(Code('OPR', 0, opr))


# <因子> <factor>→<id>|<integer>|(<exp>)
def N(parent, table):
    global Error
    child = Node('<因子>')
    parent.add(child)
    if SYM[p] == ident:  # <id>
        name = Ident(child, table)
        advance()
        l, a, flag = table.find(name)
        if str(flag) == '0':
            print(Position[p], '错误，未定义的标识符', name)
            Error = 1
        if flag == isConst:  # 常量
            code.append(Code('LIT', 0, a))
        else:  # 变量
            code.append(Code('LOD', l, a))
    elif SYM[p] == number:   # <integer>
        val = W(child, table)
        advance()
        code.append(Code('LIT', 0, val))
    elif SYM[p] == DELIMITERS['(']:   # (<exp>)
        child.add(Node('('))
        advance()
        L(child, table)  # 分析表达式
        if SYM[p] == DELIMITERS[')']:
            child.add(Node(')'))
            advance()
        else:
            print(Position[p], '缺少右括号)')
            Error = 1
    else:
        print(Position[p], "缺少括号")
        Error = 1


# <加减运算符>
def O(parent, table):
    child = Node('<加减运算符>')
    parent.add(child)
    if SYM[p] == OPERATORS['+']:
        child.add(Node('+'))
        advance()
    elif SYM[p] == OPERATORS['-']:
        child.add(Node('-'))
        advance()
    else:
        print(Position[p], "只能是+或—运算符")
        global Error
        Error = 1


# <乘除运算符>
def P(parent, table):
    child = Node('<乘除运算符>')
    parent.add(child)
    if SYM[p] == OPERATORS['*']:
        child.add(Node('*'))
        advance()
    elif SYM[p] == OPERATORS['/']:
        child.add(Node('/'))
        advance()
    else:
        print(Position[p], "只能是*或/运算符")
        global Error
        Error = 1


# <关系运算符> <lop> → =|<>|<|<=|>|>=
def Q(parent, table):
    child = Node('<关系运算符>')
    parent.add(child)
    if SYM[p] == OPERATORS['='] or SYM[p] == OPERATORS['<>'] or SYM[p] == OPERATORS['<'] or SYM[p] == OPERATORS['<='] or \
            SYM[p] == OPERATORS['>'] or SYM[p] == OPERATORS['>=']:
        opr = SYM[p]
        child.add(Node(list(OPERATORS.keys())[list(OPERATORS.values()).index(SYM[p])]))  # 获取运算符的符号
        advance()
        return opr
    else:
        print(Position[p], "不存在的关系运算符")
        global Error
        Error = 1


# <条件语句> if <lexp> then <statement>[else <statement>]
def R(parent, table):
    child = Node('<条件语句>')
    parent.add(child)
    if SYM[p] == KEYWORDS['if']:
        child.add(Node('if'))
        advance()
        K(child, table)  # 分析条件<lexp>
        ret = Code('JPC', 0, None)  # 条件转移指令，转移到地址为a的指令
        code.append(ret)
        if SYM[p] != KEYWORDS['then']:
            child.add(Node('then'))
            H(child, table)
            ret.a = len(code)
            print(Position[p], "缺少then")
            global Error
            Error = 1
        else:
            child.add(Node('then'))
            advance()
            H(child, table)  # 分析statement
            jmp = Code('JMP', 0, None)  # 为真则顺序执行，跳过else
            code.append(jmp)
            jmp.a = len(code)
            ret.a = len(code)  # 为假跳转到else 或 之后的语句
            if SYM[p] == KEYWORDS['else']:
                child.add(Node('else'))
                advance()
                H(child, table)  # 分析statement
                jmp.a = len(code)
        # while :
    else:
        print(Position[p], "递归错误")
        Error = 1


# <过程调用语句> call <id>[（<exp>{,<exp>}）]
def S(parent, table):
    global Error
    child = Node('<过程调用语句>')
    parent.add(child)
    if SYM[p] == KEYWORDS['call']:
        child.add(Node('call'))
        advance()
        if SYM[p] == ident:
            name1 = Ident(child, table)
            advance()
            if SYM[p] == DELIMITERS['(']:
                child.add(Node('('))
                advance()
                if SYM[p] == ident or SYM[p] == number:
                    temp = 4  # 形参的起始位置
                    L(child, table)  # 分析<exp>
                    code.append(Code('OPR', temp, 29))  # temp表示层差
                    while SYM[p] == DELIMITERS[',']:
                        advance()
                        temp += 1  # 层差加1
                        L(child, table)
                        code.append(Code('OPR', temp, 29))
                    if SYM[p] == DELIMITERS[')']:
                        child.add(Node(')'))
                        advance()
                    else:
                        print(Position[p], "缺少右括号")
                        Error = 1
                elif SYM[p] == DELIMITERS[')']:
                    child.add(Node(')'))
                    advance()
                else:
                    print(Position[p], "缺少右括号")
                    Error = 1

            l, a, _ = table.find(name1)  # 层差，（变量）地址/（常量）值，类型（常量/变量）
            if str(_) == '0':
                print(Position[p], '错误，未定义的标识符', name1)
                Error = 1
            code.append(Code('CAL', l, a))  # 调用过程,入口地址为a，层次差为L
        else:
            print(Position[p], "call后面缺少ident")
            Error = 1
    else:
        print(Position[p], "递归错误！")
        exit(-1)


# <当型循环语句> while <lexp> do <statement>
def T(parent, table):
    child = Node('<当型循环语句>')
    parent.add(child)
    if SYM[p] == KEYWORDS['while']:
        child.add(Node('while'))
        advance()
        ret = len(code)
        K(child, table)  # 分析<lexp>
        fret = Code('JPC', 0, None)
        code.append(fret)

        if SYM[p] == KEYWORDS['do']:
            child.add(Node('do'))
            advance()
            H(child, table)  # 分析<statement>
            code.append(Code('JMP', 0, ret))
            fret.a = len(code)
        else:
            print(Position[p], "while后面缺少do")
            global Error
            Error = 1
    else:
        print(Position[p], "递归错误")
        error()


# <读语句> read (<id>{，<id>})
def U(parent, table):
    global Error
    child = Node('<读语句>')
    parent.add(child)
    if SYM[p] == OPERATORS['read']:
        child.add(Node('read'))
        advance()
        if SYM[p] == DELIMITERS['(']:
            child.add(Node('('))
            advance()
            if SYM[p] == ident:
                name = Ident(child, table)
                advance()
                code.append(Code('OPR', 0, OPERATORS['read']))
                l, a, flag = table.find(name)
                if str(flag) == '0':
                    print(Position[p], '错误，未定义的标识符', name)
                    Error = 1
                if flag == isConst:
                    print(Position[p], '对常量的非法赋值:' + name)
                    Error = 1
                else:
                    code.append(Code('STO', l, a))  # 将数据栈栈顶的内容存入变量
                while SYM[p] == DELIMITERS[',']:
                    child.add(Node(','))
                    advance()
                    if SYM[p] == ident:
                        name = Ident(child, table)
                        advance()
                        code.append(Code('OPR', 0, OPERATORS['read']))  #
                        l, a, flag = table.find(name)
                        if str(flag) == '0':
                            print(Position[p], '错误，未定义的标识符', name)
                            Error = 1
                        if flag == isConst:
                            print(Position[p], '对常量的非法赋值:' + name)
                            Error = 1
                        else:
                            code.append(Code('STO', l, a))
                    else:
                        print(Position[p], '读操作只能对变量进行')
                        Error = 1
                if SYM[p] == DELIMITERS[')']:
                    child.add(Node(')'))
                    advance()
                else:
                    print(Position[p], "缺少右括号")
                    Error = 1
            else:
                print(Position[p], '读操作只能对变量进行')
                Error = 1
        else:
            print(Position[p], "read后缺少括号")
            Error = 1
    else:
        print(Position[p], "递归错误")
        error()

# <写语句> write (<exp>{,<exp>})
def V(parent, table):
    child = Node('<写语句>')
    parent.add(child)
    if SYM[p] == OPERATORS['write']:
        child.add(Node('write'))
        advance()
        if SYM[p] == DELIMITERS['(']:
            child.add(Node('('))
            advance()
            L(child, table)
            code.append(Code('OPR', 0, OPERATORS['write']))
            while SYM[p] == DELIMITERS[',']:
                child.add(Node(','))
                advance()
                L(child, table)
                code.append(Code('OPR', 0, OPERATORS['write']))
            if SYM[p] == DELIMITERS[')']:
                child.add(Node(')'))
                advance()
            else:
                print(Position[p], "缺少右括号")
                global Error
                Error = 1
        else:
            print(Position[p], "write后缺少括号")
            Error = 1
    else:
        print(Position[p], "递归错误")
        error()


# <无符号整数> <integer> → d{d}
def W(parent, table):
    global pnum
    child = Node('<无符号整数>')
    parent.add(child)
    val = NUM[pnum]
    child.add(Node(str(val)))
    pnum += 1
    return val


def Ident(parent, table):  # <标识符>
    global pid
    child = Node('<标识符>')
    parent.add(child)
    name = IDi[pid]  # 获取分析出的的单词
    child.add(Node(name))
    pid += 1
    return name
