from Database import Database

database = Database()
database.connect('localhost', 'root', 'root123', 'icd')
dict = {}
synonyms = []
query = "SELECT diagnosis from icd_synonym where icd like %s "
icd  = database.fetch_data("SELECT icd,diagnosis from icd_synonym WHERE length(icd)=4 group by icd",())
print(icd)
c = 0
flag = 0
with open("newmodel.tsv","r") as f:
    pointer = f.readlines()
    if len(pointer)!=0:
        pointer = pointer[-1].split("\t")[0]
    else:
        flag = 1
    print("p",pointer)

with open("newmodel.tsv","a+") as f:
    for code in icd:
        # if c==100:
        #     break
        c+=1
        if code[0] == pointer:
            flag =1
        if flag:
            insert = (code[0]+"%",)
            print(query, insert)
            diagnosis  = database.fetch_data(query, insert)
            synonyms = [y[0] for y in diagnosis[1:]]
            string = "\t".join(synonyms)
            dict[code[0]] = [code[1], synonyms]
            # print(dict)
            f.write("%s\t%s\t%s\n"%(code[0],code[1],string))

