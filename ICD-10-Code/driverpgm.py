from Extractor import Extractor
import os
datadir = './Discharg/'
inputfiles = os.listdir(datadir)
for i in range(len(inputfiles)):
    inputfiles[i] = datadir+inputfiles[i]
print(inputfiles)
result = Extractor(inputfiles)
ans = result.getalldiagnosis()
print (ans)
new = []
for i, j in ans.items():
    new += j
for i in new:
    print (i)
