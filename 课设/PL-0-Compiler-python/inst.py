from enum import Enum

FUN = Enum('FUN', ('LIT', 'LOD', 'STO', 'CAL', 'INT', 'JMP', 'JPC', 'OPR', 'RED', 'WRT'))


class Code:
    def __init__(self, f, l, a):
        f = f.upper()  # 操作码
        if f in FUN.__members__:
            self.f = FUN[f]
        else:
            print('未定义的操作码')
            exit(-1)
        self.l = l  # 层次差
        self.a = a  # 位移量

    def __str__(self):
        return self.f.name + '\t\t' + str(self.l) + '\t\t' + str(self.a)

    def set(self, f, l, a):
        f = f.upper()  # 操作码
        if f in FUN.__members__:
            self.f = FUN[f]
        else:
            print('未定义的操作码')
            exit(-1)
        self.l = l  # 层次差
        self.a = a  # 位移量
