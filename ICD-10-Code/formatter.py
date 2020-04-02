c=0
m=1
with open("sample.txt","r+") as f:
    with open("Sample.csv","w+") as g:
        for x in f:

            if x!="\n":
                x = x.strip("\n")
                if m%3 == 1:
                    filename = x
                elif m%3 == 2 :
                    patientid = x
                else:
                    x = '"' + x + '"'
                    g.write("%s,%s,%s\n"%(filename,patientid,x))
                m+=1


            print(x)
            # new = string.replace("HP","\nHP")
            # f.write(new)
        print(c)