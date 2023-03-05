import os
import matplotlib.pyplot as plt

i = 0
TerminalsStr = ""
NonTerminalsStr = ""
Table = []

path = os.path.abspath(__file__)
dirname = os.path.dirname(path)
print(dirname)
with open(dirname+'\\PredictionTable.txt','r') as f:
    for line in f.readlines():
        if i==0:
            TerminalsStr += line.strip().replace('蔚','ε')
            i += 1
        elif i==1:
            NonTerminalsStr += line.strip().replace('蔚','ε')
            i += 1
        else:
            Table.append(line.strip().replace('蔚','ε'))
            i += 1

Terminals = [element for element in TerminalsStr.split(':')[1].split(' ')]
NonTerminals = [element for element in NonTerminalsStr.split(':')[1].split(' ')]


PredictionTable = {}

for line in Table:
    left = line.split('<->')[0].strip()
    right = ("-" if line.split('<->')[1] == '' else line.split('<->')[1].strip())
    PredictionTable[left] = right

TableVal = []

for NonTerminator in NonTerminals:
    TmpList = []
    for Terminator in Terminals:
        TmpList.append(PredictionTable.get(NonTerminator + ' -> ' +Terminator))
    TableVal.append(TmpList)

table = plt.table(cellText=TableVal,
          rowLabels=NonTerminals,
          colLabels=Terminals,
          loc='center',
          colWidths=[0.15 for i in range(len(Terminals))],
          cellLoc='center')
plt.title('The Top-Down of Syntax Analysis by LL(1): Prediction Table')



for cell in table.properties()['child_artists']:
    cell.set_height(0.1)

plt.axis('off')
plt.show()