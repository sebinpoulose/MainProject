from Database import Database
from nltk.corpus import stopwords
import nltk
import ncrmodel
import tensorflow as tf
from Extractor import Extractor
import threading
from datetime import datetime


tf.enable_eager_execution()
param_dir = "C:\\Users\\sadiq naizam\\Desktop\\python_workspace\\ncr_hpo_params\\params"
word_model_file = "C:\\Users\\sadiq naizam\\Desktop\\python_workspace\\ncr_hpo_params\\params\\pmc_model_new.bin"
model = ncrmodel.NCR.loadfromfile(param_dir, word_model_file)

#nltk.download('stopwords')
#nltk.download('averaged_perceptron_tagger')
#nltk.download('punkt')

from nltk.tokenize import word_tokenize, sent_tokenize

class myThread(threading.Thread):
    def __init__(self,diagnosis):
        threading.Thread.__init__(self)
        self.diagnosis = diagnosis
        self.count = 0
        self.error = 0
        self.same_category = 0
        self.right = 0
        self.predicted_icd =[]

        self.invalid_count = 0
    def run(self):
        starttime = datetime.now()


        for x in diagnosis:
            print("finding for: ",x)
            list.append(map.map(x))
        for i in list:
            print(i)

        self.output()



        print("Total Diagnosis: ",self.count,"\nTotal Errors: ",self.count - self.right)
        print("Same category:",self.same_category)
        print("Accuracy:",self.right/self.count)
        print("Runtime : ", datetime.now() - starttime)


    def output(self):
        # same_category = []
        for i in range(len(list)):
            true_icd = results[i][1]
            self.predicted_icd.clear()
            for x in list[i]:
                self.predicted_icd.append(x[1])
                for diagnosis in true_icd:
                    if diagnosis == x[1]:
                        self.right += 1
                    elif diagnosis[:3] == x[1][:3]:
                        self.same_category += 1


            print("True : ", true_icd, "\t", "Predicted : ", set(self.predicted_icd), "Error:",
                  set(self.predicted_icd) - set(true_icd))
            self.count += len(true_icd)

            # self.error += len(set(predicted_icd) - set(true_icd))


class Mapper():
    def __init__(self):
        self.database = Database()
        self.result = []
        self.icd = []
        self.data = []
        self.query = 'SELECT icd,diagnosis FROM icd_synonym where diagnosis like %s'
        self.retriever_query = 'SELECT max(co),icd,diagnosis FROM icd_synonym where hp = %s'
        self.retriever = 'SELECT max(co),icd,diagnosis FROM icd_synonym where diagnosis like %s and hp = %s'
        self.database.connect('localhost', 'root', 'root123', 'icd')
        stopword = list(stopwords.words('english'))
        stopword.remove('other')
        stopword.extend(['-?','-'])
        stopw = [',', '/', '[', ']', '(', ')', 'unspecified','-?']
        stopword.remove('a')
        #stopword.remove('with')
        self.stopwordsearch = list(stopword)#stopwordsearch and stopwordcompare (more refined)
        self.stopwordsearch.extend(['acute', 'small', 'under', 'right', 'left', 'positive', 'negative', 'normal'])
        self.stopwordcompare = list(stopw)

    def mapd(self, item):
        j = item.lower()
        tempd = []
        tempi = []
        string = ""
        flag = 1
        self.icd = []
        self.data = []
        wordsList = nltk.word_tokenize(j)
        wordsList = [w for w in wordsList if not w in self.stopwordsearch]  # removing stop words from wordList
        tagged = nltk.pos_tag(wordsList)  # tagging for words
        c = 0
        for i in wordsList:
            if len(i) != 1:  #and tagged[c][1] != 'JJ':#i not in self.stopwordsearch:
                if flag:
                    flag = 0
                else:
                    self.icd += tempi
                    self.data += tempd
                t = ('% ' + i + ' %',)  # assuming that a
                string = i
                data_element = self.database.fetch_data(self.query, t)
                tempi = [x[0] for x in data_element]
                tempd = [x[1] for x in data_element]
            else:
                flag = 1
                t = ('% ' + string + " " + i + ' %',)
                data_element = self.database.fetch_data(self.query, t)
                self.icd += [x[0] for x in data_element]
                self.data += [x[1] for x in data_element]
            c += 1
        if flag == 0:
            self.icd += tempi
            self.data += tempd
        if len(self.data):
            maxi = 0
            i = 0
            ricd = "Ambiguous"
            rdata = "Not Mapped"
            for x in self.data:
                val = self.matcherRatio(j, x)
                if val > 0.1:
                    if val > maxi:
                        maxi = val
                        if len(self.icd[i]) > 3:
                            ricd = self.icd[i][:3]+'.'+self.icd[i][3:4]
                        else:
                            ricd = self.icd[i]
                        rdata = x
                i += 1
            print("val:",ricd,rdata)
            if ricd == "Ambiguous":
                hpd = model.get_match(j, 1)
                if hpd[0][0] != None:
                    if len(hpd[0][0]) > 3:
                        ricd = hpd[0][0][:3] +'.'+ hpd[0][0][4:]
                    else:
                        ricd = hpd[0][0]
                    maxi = hpd[0][1]



            return [(item, ricd), maxi]
        else:

            return [(item, "Invalid"), 0]

    def map(self, diagnosis):#diagnosis :- list of diagnosis
        self.result = []
        lastd = len(diagnosis) - 1  #last diagnosis index
        for item in diagnosis:
            if item == diagnosis[lastd]:
                sub = item.split(" and ")
                l_sub = len(sub)
                j = l_sub
                dia = sub
                mapp = []
                for i in range(0, l_sub):
                    for j in range(i+2,l_sub+1):
                        dia.append(" and ".join(sub[i:j]))
                    # for l in range(i, l_sub):
                        # tem_d = sub[l]
                        # for k in range(l + 1, l + j):
                    # tem_d = tem_d + " and " + sub[k]
                    # dia.append(tem_d)
                    # j = j - 1
                for d in dia:
                    mapp.append(self.mapd(d))
                checker = 1
                # if len(mapp) == 1:
                #     self.result.append(mapp[0][0])
                print("mapp",mapp)
                highest = -1
                selected = ""
                for m in mapp:
                    if m[1] > highest:
                        highest = m[1]
                        selected = m[0]
                if highest > 0:
                    if "and" not in selected:
                        for m in mapp:
                            if "and" not in m[0]:
                                self.result.append(m[0])
                    else:
                        self.result.append(selected)
                else:
                    if "and" in selected:
                        for m in mapp:
                            if "and" not in m[0]:
                                self.result.append(m[0])
                    else:
                        self.result.append(selected)


            else:
                res = self.mapd(item)
                self.result.append(res[0])
        print("result:",self.result)
        return self.result

    def matcherRatio(self, item, x):
        temp = len(set(x.split())-set(self.stopwordcompare)) * len(item.split())
        return (len(set(item.split()) & (set(x.split())-set(self.stopwordcompare))) ** 2) / temp

if __name__ == "__main__":
    map = Mapper()
    c = 0
    with open("Sample.csv","r+") as f:
        results = []
        for x in f:
            c += 1
            # if c==7:
            #     break
            element = x.split(",")
            results.append(["C:\\Users\\sadiq naizam\\Desktop\\python_workspace\\MainProject\\ICD-10-Code\\Discharge2\\"+element[0]+".txt",[x.strip("\n").strip(" ").strip('"') for x in element[2:]]])
            print(c,":",element[0])
            print("result:",results)
    extractor = Extractor([x[0] for x in results])
    diagnosis = list(extractor.getalldiagnosis().values())
    print(diagnosis)
    prev = 0
    list = []
    for i in range(1):
        thread = myThread(diagnosis)
        thread.start()


