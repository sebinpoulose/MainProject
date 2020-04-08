flag = 0
with open("final_model.obo","w+") as h:
    with open("ICD10_Chapter.obo","r") as f:
        with open("model.obo","r") as g:
            for x in f:
                row_icd = x.split(":")
                if row_icd[0] != "id":
                    h.write(x)


                else:
                    print(row_icd[1].strip(" ").strip("\n"))
                    if len(row_icd[1].strip(" ").strip("\n")) != 5:
                        h.write(x)
                    else:
                        h.write(x)
                        for y in g:
                            row_model = y.split(":")
                            print("row model:",row_model)
                            if row_model[0] != "[Term]\n":
                                h.write(y)



                # if row_icd[0] == "id:" and len(row_icd[1].strip(" "))==5:
                #     for y in g:
                #         row_model = y.split(":")
                #
                #         if row_model[0] == "synonym":
                #             f.write("\n%s"%y)
                #
                #         if row_model[0] == "id:" and row_model[1][:3]+"_"+row_model[3:] == row_icd[1]:
                #             # row_model = g.readline().split(" ")
                #             f.write("\n%s"%g.readline())
                #             flag = 1
                #         # if row_model[0] =="[Term]":
                #         #     flag =0
