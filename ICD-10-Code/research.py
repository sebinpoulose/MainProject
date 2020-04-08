from Extractor import Extractor
import nltk
c = 0
filename = []
with open("Sample.csv", "r+") as f:
    results = []
    for x in f:
        c+=1
        # if c == 6:
        #     break
        element = x.split(",")
        results.append(["C:\\Users\\sadiq naizam\\Desktop\\python_workspace\\MainProject\\ICD-10-Code\\Discharge2\\" +
                        element[0] + ".txt", [x.strip("\n").strip(" ").strip('"') for x in element[2:]]])
        filename.append(element[0])
        # print(c, ":", element[0])
        # print("result:", results)
extractor = Extractor([x[0] for x in results])
diagnosis = list(extractor.getalldiagnosis().values())
m = 0
for u in diagnosis:
    print(filename[m],":",u)
    m+=1

# for item in diagnosis:
#     for x in item:
#         tokens = nltk.word_tokenize(x)
#         tag = nltk.pos_tag(tokens)
#         nouns = [x for x in tag if x[1] == "NN"]
#         print(tag)