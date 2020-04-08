with open("newmodel.tsv","r") as f:
    with open("model.obo","w+") as g:
        for x in f:
            row = x.split("\t")
            g.write("[Term]\nid: %s\nname: %s\n"%(row[0],row[1]))
            for x in row[3:]:
                print(x)
                g.write("synonym: \"%s\" RELATED []\n"%x)




