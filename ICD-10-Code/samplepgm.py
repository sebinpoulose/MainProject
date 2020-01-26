from Extractor import Extractor
inputfiles=["sample1.rtf", "sample2.rtf", "sample3.rtf", "sample4.rtf", "sample5.rtf", "sample6.rtf"]
result = Extractor(inputfiles)
ans = result.getalldiagnosis()
new = []
for i, j in ans.items():
    new += j
for i in new:
    print(i)
