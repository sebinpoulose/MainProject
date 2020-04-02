class Extractor:
    def __init__(self, files):
        import re
        import string
        from ParseRTF import striprtf
        assert type(files) is list, "List of file paths expected"
        self.files = files
        self.terminate = ["surgery done", "operation:", "allergies:", "birth parameters:", "hopi:", "condition at discharge", "allergy", "complaints", "history", "discharge advise", "procedure", "drug allergies", "presenting complaints", "drug allergy:"]
        # self.terminate.append()
        self.result = {}
        for document in files:
            diagnosisfound = 0
            text = ''
            doc = open(document, "r").readlines()
            for lines in doc:
                text += lines
            text = striprtf(text)
            text = text.split('\n')
            append = False
            extract = []
            for i in text:
                i = i.lower()
                if "diagnosis" in i:
                    if diagnosisfound == 0:
                        append = True
                        diagnosisfound = 1
                else:
                    for word in self.terminate:
                        if word in i:
                            append = False
                            break
                if append:
                    extract.append(i)
            while "diagnosis" in extract:
                extract.remove("diagnosis")
            for elem in range(len(extract)):
                if "co-morbidities" in extract[elem] or "comorbidities" in extract[elem]:
                    extract[elem] = extract[elem].split('morbidities')[1]
            diagnosis = extract
            if len(diagnosis) > 0:
                if ":" in diagnosis[0]:
                    diagnosis[0] = diagnosis[0].split(":")[1]
            i = 0
            while i < len(diagnosis):
                diagnosis[i] = diagnosis[i].strip()
                if diagnosis[i].strip() == '':
                    del diagnosis[i]
                    i = i - 1
                i += 1
            while ":" in diagnosis:
                diagnosis.remove(":")
            for i in range(len(diagnosis)):
                diagnosis[i] = re.sub(r'[^\x00-\x7F]', '', diagnosis[i]).strip()
                diagnosis[i]= re.sub('[(){}<>.,!]', '',diagnosis[i])
            self.result[document] = diagnosis

    def getalldiagnosis(self):
        return self.result

    def getdiagnosis(self, document):
        assert document in self.files, "Specified file doesn't exist"
        return self.result[document]


if __name__=="__main__":
    e = Extractor(["161240.rtf"])
    print(e.getalldiagnosis())
