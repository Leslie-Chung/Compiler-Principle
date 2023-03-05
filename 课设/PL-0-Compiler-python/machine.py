from inst import Code, FUN
from symbol import OPERATORS


class Reg:
    def __init__(self, data=None):
        self.__data = data

    def set(self, data):  # 设置内容
        self.__data = data

    def get(self):  # 获取内容
        return self.__data

    def __add__(self, other):
        return self.get() + other.get()

    def inc(self):  # 寄存器自增一
        self.__data += 1

    def dec(self):  # 寄存器自减一
        self.__data -= 1


class Machine:
    def __init__(self, code, debugFlag=False):  # 初始化虚拟机
        self.code = code  # 代码段
        self.data = []  # Stack，存放活动记录
        self.I = Reg()  # 存放当前要执行的代码
        self.P = Reg()  # 存放下一条要执行的指令地址
        self.T = Reg()  # 当前活动数据栈的高度-1
        self.B = Reg()  # 基地址寄存器
        self.debugFlag = debugFlag

    def top(self):
        return self.data[len(self.data) - 1]

    def push(self, data):
        self.data.append(data)
        self.T.inc()

    def pop(self):
        self.T.dec()
        return self.data.pop()

    def initReg(self):
        self.P.set(0)
        self.T.set(-1)
        self.B.set(0)

    def debug(self, info):
        if self.debugFlag:
            print('*********************************************************')
            print(info)
            print('P=', self.P.get(), 'B=', self.B.get(), 'T=', self.T.get())
            print(self.data)

    def run(self):
        self.debug('开始运行')
        self.initReg()
        while self.P.get() != 1:
            addr = self.P.get()  # 获取指令地址
            inst = self.code[addr]  # 获取指令
            self.I.set(inst)  # 读指令
            if inst.f == FUN.LIT:  # 如果操作码是LIT，将常数放到运栈顶，a 为常数。
                self.push(inst.a)
                self.P.inc()
            elif inst.f == FUN.STO:  # 将数据栈顶的内容送到某变量单元中。a 为变量在所说明层中的相对位置，l 为调用层与说明层的层差值。
                badr = self.B.get()  # 获取当前运行过程的数据区在STACK中的起始地址，即活动记录首地址
                if inst.l > 0:
                    for _ in range(1, inst.l + 1):
                        badr = self.data[badr + 2]  # 获取活动记录首地址
                self.data[badr + inst.a + self.data[badr + 3]] = self.pop()  # 获取数据栈顶元素的数值，赋值给该变量
                self.P.inc()
            elif inst.f == FUN.LOD:  # 将变量放到数据栈顶。a 为变量在所说明层中的相对位置，l 为调用层与说明层的层差值。
                badr = self.B.get()
                # print(inst.l)
                if inst.l > 0:
                    for _ in range(1, inst.l + 1):
                        badr = self.data[badr + 2]
                self.push(self.data[badr + inst.a + self.data[badr + 3]])  # 基址 + 相对位置 + 形参个数
                self.P.inc()
            elif inst.f == FUN.CAL:  # 调用过程的指令。a 为被调用过程的目标程序的入口地址，l 为层差。
                if inst.l == 0:  # 子过程调用,新过程的静态链为旧过程的首地址
                    sl = self.B.get()
                else:  # 同级过程调用,新过程的静态链为旧过程的静态链
                    sl = self.data[self.B.get() + 2]
                if self.T.get() + self.B.get() < len(self.data) - 1:  # 如果不需要新开辟空间
                    self.data[self.T.get() + self.B.get() + 1] = self.P.get()
                    self.data[self.T.get() + self.B.get() + 2] = self.B.get()
                    self.data[self.T.get() + self.B.get() + 3] = sl
                    self.data[self.T.get() + self.B.get() + 4] = 0
                    self.P.set(inst.a)  # 设定入口地址
                    self.B.set(self.B + self.T + 1)  # 设置基址寄存器
                    self.T.set(3)  # 设置栈指针寄存器
                else:
                    self.data.append(self.P.get())  # 设定返回地址
                    self.data.append(self.B.get())  # 设定动态链
                    self.data.append(sl)  # 设定静态链
                    self.data.append(0)  # 设定形参个数
                    self.P.set(inst.a)  # 设定入口地址
                    self.B.set(self.B + self.T + 1)  # 设置基址寄存器
                    self.T.set(3)  # 设置栈指针寄存器
            elif inst.f == FUN.INT:  # 为被调用的过程（或主程序）在运行栈中开辟数据区。a 域为开辟的个数，始终添加0。
                while len(self.data) < self.B.get() + inst.a:
                    self.push(0)
                self.P.inc()
            elif inst.f == FUN.JMP:  # 无条件转移指令，a 为转向地址。
                self.P.set(inst.a)
            elif inst.f == FUN.JPC:  # 条件转移指令，当栈顶的布尔值为非真时，转向a 域的地址，否则顺序执行。
                if self.pop() == 0:  # 为假
                    self.P.set(inst.a)
                else:  # 为真
                    self.P.inc()
            elif inst.f == FUN.OPR:  # 关系和算术运算。具体操作由a 域给出。运算对象为栈顶和次顶的内容进行运算，结果存放在次顶。a 域为0 时是退出数据区。
                if inst.a == OPERATORS['+']:  # 加法
                    b = self.pop()
                    a = self.pop()
                    self.push(a + b)
                elif inst.a == OPERATORS['-']:  # 减法
                    b = self.pop()
                    a = self.pop()
                    self.push(a - b)
                elif inst.a == OPERATORS['*']:  # 乘法
                    b = self.pop()
                    a = self.pop()
                    self.push(a * b)
                elif inst.a == OPERATORS['/']:  # 除法
                    b = self.pop()
                    a = self.pop()
                    self.push(a // b)
                elif inst.a == OPERATORS['<>']:  # 不等于
                    b = self.pop()
                    a = self.pop()
                    if a != b:
                        self.push(1)
                    else:
                        self.push(0)
                elif inst.a == OPERATORS['<']:  # 小于
                    b = self.pop()
                    a = self.pop()
                    if a < b:
                        self.push(1)
                    else:
                        self.push(0)
                elif inst.a == OPERATORS['<=']:  # 小于等于
                    b = self.pop()
                    a = self.pop()
                    if a <= b:
                        self.push(1)
                    else:
                        self.push(0)
                elif inst.a == OPERATORS['>']:  # 大于
                    b = self.pop()
                    a = self.pop()
                    if a > b:
                        self.push(1)
                    else:
                        self.push(0)
                elif inst.a == OPERATORS['>=']:  # 大于等于
                    b = self.pop()
                    a = self.pop()
                    if a >= b:
                        self.push(1)
                    else:
                        self.push(0)
                elif inst.a == OPERATORS['odd']:  # 判断奇数
                    a = self.pop()
                    if a % 2 == 1:
                        self.push(1)
                    else:
                        self.push(0)
                elif inst.a == OPERATORS['read']:  # 读
                    s = input('input:')
                    if not s.isdigit():
                        print('输入错误')
                        exit(-1)
                    else:
                        self.push(int(s))
                elif inst.a == OPERATORS['write']:  # 写
                    print('output:' + str(self.pop()))

                elif inst.a == OPERATORS['post']:  # post 传参
                    post = self.pop()
                    badr = self.T.get() + 1 + self.B.get() + inst.l   # l为形参所在相对位置

                    while badr >= len(self.data):
                        self.data.append(0)
                    self.data[self.T.get() + 1 + self.B.get() + 3] += 1  # 形参个数+1
                    # print(badr, self.data)
                    self.data[badr] = post

                elif inst.a == 0:  # 退出数据区
                    badr = self.data[self.B.get() + 1]  # 获取动态链
                    self.P.set(self.data[self.B.get()])  # 恢复返回地址
                    while len(self.data) > self.B.get():  # 退栈
                        self.data.pop()
                    self.T.set(self.B.get() - 1)  # 恢复栈指针寄存器
                    self.B.set(badr)  # 恢复基址寄存器
                    self.T.set(self.T.get() - self.B.get())  # 恢复栈指针寄存器
                self.P.inc()

            self.debug('Addr:' + str(addr) + '\t|\tInst:' + str(inst))
