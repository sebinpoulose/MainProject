from Extractor import Extractor
from maaaap import Mapper
from Database import Database
import os
database = Database()
database.connect('localhost', 'root', 'root123', 'icd')
query = 'SELECT * FROM synonym where diagnosis like "% and %"'
print("heloo")
datadir = './Discharge2/'
inputfiles = os.listdir(datadir)
for i in range(len(inputfiles)):
    inputfiles[i] = datadir+inputfiles[i]
#print(inputfiles
result = Extractor(inputfiles)
ans = result.getalldiagnosis()
#print(ans)
new = []
mapp = Mapper()
fe = ("left",)
data_element = database.fetch_data(query, None)
for h in data_element:
    print(h)
f = open("testcases.txt", "r")

for x in f:
    i = x.split()
    print("File name:"+i[0])
    try:
        diag = ans[datadir + i[0] + ".txt"]
        sicd = ", ".join(i[1:])
        icd = sicd.split(",")
        print(icd)
        icd1 = icd
        for el in icd1:
            if el == ' ':
                icd.remove(el)
        print(icd)
        print("Expected Outcome:" + ", ".join(icd))
        for t in icd:
            for y in range(3):
                fe = (t.replace('.', '')+"0"*y,)
                data_element = database.fetch_data(query, fe)
                for temp in data_element:
                    print("\t",temp[0],":",temp[1])
        print("\nExtracted diagnosis:" + ", ".join(diag), end="\n\nMapping:\n")
        bre = -1
        di = ""
        for co in diag:
            re = co.find("- ?")
            if re != -1:
                bre = re
                di = co
        if bre != -1:
            diag.remove(di)
            diag.append(di[:bre])
        num = 1
        for co in diag:
            print("Disease " + num.__str__() + ":" + co)
            num += 1
            print("Mapped ICD-10 Code:"+mapp.map([co, ])[0][1], end="\n\n")
    except KeyError:
        print("invalid key")
    print("***")
f.close()