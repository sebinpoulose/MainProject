
icd10 = []
model = []
#
# with open("ICD10_Chapter.obo","r") as f:
#     with open("model.obo","r") as g:
#         for x in f:
#             string = x.split(":")
#             if string[0] == 'id' and len(string[1].strip(" ").strip("\n"))==5:
#                 icd10.append(string[1].strip(" ").strip("\n"))
#         for x in g:
#             string = x.split(":")
#             if string[0] == 'id':
#                 model.append(string[1].strip(" ").strip("\n"))
#         print(icd10)
#         print(model)
#         print(len(icd10))
#         print(len(model))
#         i = []
#         for x,y in zip(icd10,model):
#             x = x[:3]+x[4:]
#             i.append(x)
#             print(x,y)
#         icd10 = list(set(model) - set(i))
#         print(icd10)
#
# flag = 1
# with open("final_model.obo","w+") as h:
#     with open("ICD10_Chapter.obo","r") as f:
#         with open("model.obo","r") as g:
#             for x in f:
#                 row_icd = x.split(":")
#                 if not flag:
#                     h.write(x)
#                     continue
#                 if row_icd[0] != "id":
#                     h.write(x)
#                     print(x)
#                 else:
#                     if len(row_icd[1].strip(" ").strip("\n"))==5:
#                         h.write(x)
#                         print(x)
#                         string = g.readline()
#                         # print("str",string.split(":")[0])
#                         while(string.split(":")[0] != '[Term]\n'):
#                             print("here")
#                             if string.split(":")[0] != 'id':
#                                 h.write(string)
#                                 print(string)
#                             else:
#                                 if string.split(":")[1].strip(" ").strip("\n") in icd10:
#                                     string = g.readline()
#                                     while(string.split(":")[0] != '[Term]\n'):
#                                         print("hey")
#                                         string = g.readline()
#                                         if string == "":
#                                             flag = 0
#                                             break
#                             if not flag:
#                                 break
#
#                             string = g.readline()
#
#                     else:
#                         h.write(x)
#                         print(x)

dict = {}
flag = 0
# with open("ICD10_Chapter.obo","r") as f:
with open("C:\\Users\\sadiq naizam\\Desktop\\python_workspace\\synonym.tsv","r") as g:
    data = g.readlines()
    for item in data:
        element = item.split("\t")
        dict[element[0]] = element[1:]
with open("ICD10_Chapter.obo","r") as f:
    with open("final_model.obo", "w+") as h:
        for x in f:
            string = x.split(":")
            h.write(x)
            if string[0] == "id":
                code = string[1].strip("\n").strip(" ")
                code = code[:3] + code[4:]
                if code in dict:
                    h.write("name: %s\n"%dict[code][0])
                    for element in dict[code][1:]:
                        h.write("synonym: \"%s\" RELATED []\n"%element.strip("\n").strip(" "))

