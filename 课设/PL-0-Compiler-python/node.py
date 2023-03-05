class Node:
    def __init__(self, name):
        self.name = name
        self.child = []

    def add(self, node):  # 增加一个子节点
        self.child.append(node)

    def isLeaf(self):  # 当该节点是叶子时返回True
        if len(self.child) == 0:
            return True
        else:
            return False

    def getNumLeafs(self):  # 获取叶子节点数量
        if self.isLeaf():
            return 1
        else:
            numLeafs = 0
            for i in self.child:
                numLeafs += i.getNumLeafs()
            return numLeafs

    def getTreeDepth(self):  # 获取树的深度
        if self.isLeaf():
            return 1
        else:
            maxDepth = 0
            for i in self.child:
                if i.getTreeDepth() > maxDepth:
                    maxDepth = i.getTreeDepth()
            return maxDepth + 1

    def __str__(self):
        s = self.name
        if not self.isLeaf():  # 如果是叶子节点
            s += '{'
            for i in self.child:
                s += i.__str__() + ','
            s = s[0:len(s) - 1]
            s += '}'
        return s
