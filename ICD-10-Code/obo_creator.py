with open("C:\\Users\\sadiq naizam\\Desktop\\python_workspace\\synonym.tsv","r") as f:
    with open("model.obo","w+") as g:
        for x in f:
            row = x.split("\t")
            row = [x.strip("\n").strip(" ") for x in row]
            g.write("[Term]\nid: %s\nname: %s\n"%(row[0],row[1]))
            for x in row[3:]:
                print(x)
                g.write("synonym: \"%s\" RELATED []\n"%x)




