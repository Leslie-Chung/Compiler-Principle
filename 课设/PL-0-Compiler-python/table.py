from enum import Enum

KIND = Enum('KIND', ('CONSTANT', 'VARIABLE', 'PROCEDURE'))
# print(list(KIND))
isConst = False
isVar = True


class Table:  # 符号表
    def __init__(self, parent=None):
        self.parent = parent  # 父节点
        self.entries = {}
        self.dx = 4  # 地址，初始值是4是因为0，1，2,3分别是返回地址，调用者的活动记录首地址（动态链），该过程直接外层的活动记录首地址（静态链），形参个数

        if parent == None:
            self.level = 0
        else:
            self.level = parent.level + 1

    def add(self, entry):
        if entry.name in self.entries:
            return 1
        entry.level = self.level
        if entry.kind == KIND.VARIABLE:
            entry.adr = self.dx
            self.dx += 1
        self.entries[entry.name] = entry

    def getSize(self):
        return self.dx

    def find(self, name):  # 当标识符是变量时返回层差和地址Flag=True，当标识符是常量时返回层差和值Flag=False
        if name in self.entries:
            if self.entries[name].adr is None:  # 是常量
                return 0, self.entries[name].val, isConst
            else:
                return 0, self.entries[name].adr, isVar
        elif self.parent is None:
            return 0, 0, 0
        else:
            l, a, flag = self.parent.find(name)
            return 1 + l, a, flag

    def __str__(self):
        msg = '___________________________________________________________\n'
        for i in self.entries.keys():
            msg += self.entries[i].__str__() + '\n'
        msg += '___________________________________________________________'
        return msg


class Entry:  # 变量类型及其数值
    def __init__(self, name, kind, val=None):
        self.name = name
        self.kind = kind
        if kind != KIND.CONSTANT and val != None:
            print('非常量无法初始化值')
            return 1
        else:
            self.val = val
        self.level = None
        self.adr = None

    def __str__(self):
        msg = 'NAME:' + self.name + '\t\t' + self.kind.name + '\t\t'
        if self.val != None:
            msg += 'VAL:' + str(self.val) + '\t\t'
        else:
            msg += 'LEVEL:' + str(self.level) + '\t\t'
        msg += 'ADR:' + str(self.adr)
        return msg
