from SentiAnalyzer import *
import csv

f1 = open('word.csv')
rdr1 = csv.reader(f1)
word = []
for row in rdr1:
    word.append(row)
f1.close()

f2 = open('sentidata.csv', 'r')
rdr2 = csv.reader(f2)
sentidata = []
for row in rdr2:
    sentidata.append(row)
f2.close()

s = SentiAnalyzer()
# 1)
print('1)')
s.runAnalysis(sentidata, word, 10)
# 2)
print('2)')
s.runAnalysis(sentidata, word, 120)
# 3)
print('3)')
pos, neg, sent = s.runAnalysis(sentidata, word, 120)
print(pos)
print(neg)
print(sent)
# 코드 실행결과 확인 및 공유