from getsym import getsym
from block import program, code, tableList
from machine import Machine

filename = input('请输入测试用例文件名：')  # 测试用例包括test.txt和4.txt
print('开始词法分析')
getsym(filename)
print('词法分析完成')
print('开始语法和语义分析')
program()  # 语法分析
print('\n')
print('语法和语义分析完成')
f1 = open('符号表.txt', 'w')
for i in tableList:
    f1.write(str(i))
    f1.write('\n\n\n')
    print(i)
f1.close()
f2 = open('三地址代码.txt', 'w')
flag = True
for i, x in enumerate(code):
    if x.a == 11 and x.f.name is 'OPR':  # read
        x.set('RED', x.l, x.a)
        flag = False
        f2.writelines(str(i) + ':\t' + str(x) + '\n')
        print(str(i) + ':\t\t' + str(x))
        x.set('OPR', x.l, x.a)
        continue
    elif x.a == 12 and x.f.name is 'OPR':  # write
        l = x.l
        a = x.a
        x.set('WRT', 0, 0)
        flag = False
        f2.writelines(str(i) + ':\t' + str(x) + '\n')
        print(str(i) + ':\t\t' + str(x))
        x.set('OPR', l, a)
        continue

    if flag:
        f2.writelines(str(i) + ':\t' + str(x) + '\n')
        print(str(i) + ':\t\t' + str(x))
    else:
        flag = True


f2.close()
machine = Machine(code)  # 指令运行
machine.run()
print('目标程序结束')
