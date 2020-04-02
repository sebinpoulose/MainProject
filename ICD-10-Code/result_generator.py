from Database import Database
from nltk.corpus import stopwords
import nltk
import ncrmodel
import tensorflow as tf
from Extractor import Extractor
import threading
from datetime import datetime


tf.enable_eager_execution()
param_dir = "C:\\Users\\sadiq naizam\\Desktop\\python_workspace\\ncr_hpo_params\\model_params"
word_model_file = "C:\\Users\\sadiq naizam\\Desktop\\python_workspace\\ncr_hpo_params\\model_params\\pmc_model_new.bin"
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
        self.invalid_count = 0
    def run(self):
        starttime = datetime.now()


        for x in diagnosis:
            print("finding for: ",x)
            list.append(map.map(x))
        for i in list:
            print(i)
        for i in range(len(list)):
            true_icd = results[i][1]
            predicted_icd = [x[1][:3]+'.'+x[1][3:4] for x in list[i] if len(x[1])>3 and x[1]!="Invalid"]
            self.count+=len(true_icd)
            self.error+= len(set(predicted_icd)-set(true_icd))

            print("True : ",true_icd,"\t","Predicted : ",predicted_icd,"Error:",set(predicted_icd)-set(true_icd))
        print("Total Diagnosis: ",self.count,"\nTotal Errors: ",self.error)
        print("Accuracy:",(self.count-self.error)/self.count)
        print("Runtime : ", datetime.now() - starttime)



class Mapper():
    def __init__(self):
        self.database = Database()
        self.result = []
        self.icd = []
        self.data = []
        self.query = 'SELECT icd,diagnosis FROM icd_synonym where diagnosis like %s'
        self.retriever_query = 'SELECT max(co),icd,diagnosis FROM icd_synonym where hp = %s'
        # self.retriever = 'SELECT max(co),icd,diagnosis FROM icd_synonym where  hp = %s'
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
                if val > 0.3:
                    if val > maxi:
                        maxi = val
                        ricd = self.icd[i]
                        rdata = x
                i += 1
            print("val:",ricd,rdata)
            if ricd == "Ambiguous":
                #for x in self.data:
                    print(item," entered the model")
                    hpd = model.get_match([j], 5)
                    j = j.split(" ")
                    max = 0
                    selected = ""
                    for i in range(len(hpd[0])):
                        t = ( hpd[0][i][0],)
                        data = self.database.fetch_data(self.retriever_query, t)
                        #print(data)
                        if data[0][0] !=None:
                            if hpd[0][i][1]*data[0][0] > max:
                                selected = data
                                max = hpd[0][i][1]*data[0][0]


                    # for word in j:
                    #     for i in range(len(hpd[0])):
                    #         t = ('%' + word + '%',hpd[0][i][0],)
                    #         print(self.retriever_query%t)
                    #         data = self.database.fetch_data(self.retriever_query, t)
                    #         print(data)
                    #         if data[0][0] != None:
                    #             res.append(data[0])
                    # print("r: ", res)
                    # res.sort()
                    # print(res)



                    if len(selected) == 0:
                        ricd = "No match"
                        maxi = 0
                    else:
                        ricd = selected[0][1]
                        maxi = -1*selected[0][0]
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
                if len(mapp) == 1:
                    self.result.append(mapp[0][0])
                print("mapp",mapp)
                for m in mapp:
                    if " and " in m[0][0]:      # Only considers the case where there is only one "and" in
                        if m[1] < 0:            # the diagnosis. In such case there is only 3 possible
                            checker = 0         # diagnosis. If the diagnosis containing "and" was passed to
                                                # the model ,then the other two diagnosis are different diagnosis
                                                # else we take the diagnosis containing "and". [185-198]
                        else:
                            self.result.append(m[0])
                        break
                if not checker:
                    for element in mapp:
                        if " and " in element[0][0]:
                            pass
                        else:
                            self.result.append(element[0])

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
            # if c == 6:
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


