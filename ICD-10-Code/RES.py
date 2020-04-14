from Database import Database
flag = 1
with open("C:\\Users\\sadiq naizam\\Desktop\\python_workspace\\synonym.tsv","r") as f:
    string = f.readlines()
    print(string)
    if len(string) != 0:
        c = string[-1].split("\t")[0]
        flag = 0
    print("flag:",flag)
database = Database()
database.connect('localhost', 'root', 'root123', 'icd')
query = "select icd from icds group by icd"

icd = database.fetch_data(query,())
icd = [x[0] for x in icd]
data = []
selector = "select diagnosis from icd_synonym where icd like %s"
with open("C:\\Users\\sadiq naizam\\Desktop\\python_workspace\\synonym.tsv","a+") as f:
    for code in icd:
        if not flag:
            if code == c:
                flag = 1
            else:
                continue
        else:
            if len(code) == 4:
                insert = (code+"%",)
            else:
                insert = (code,)
            row = database.fetch_data(selector,insert )
            data = [code, [x[0] for x in row]]
            f.write("%s\t%s\n"%(data[0], "\t".join(data[1])))
            print(data[0])
            data.clear()



