from SentiAnalyzer import *
import csv
import numpy as np

f1 = open('word.csv', 'r')
rdr1 = csv.reader(f1)
word = []
for row in rdr1:
    word.append(row)
f1.close()
word = np.asarray(word)

f2 = open('sentidata.csv', 'r')
rdr2 = csv.reader(f2)
sentidata = []
for row in rdr2:
    sentidata.append(row)
f2.close()
sentidata = np.asarray(sentidata, dtype=np.float32)

s = SentiAnalyzer(sentidata, word)
s.runExperiments(3)