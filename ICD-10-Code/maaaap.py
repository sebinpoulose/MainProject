from Database import Database
from nltk.corpus import stopwords
import nltk
import ncrmodel
import tensorflow as tf
# print("entered maaaqaapppppp")
tf.enable_eager_execution()
param_dir = "C:\\Users\\sadiq naizam\\Desktop\\python_workspace\\ncr_hpo_params\\model_params"
word_model_file = "C:\\Users\\sadiq naizam\\Desktop\\python_workspace\\ncr_hpo_params\\model_params\\pmc_model_new.bin"
model = ncrmodel.NCR.loadfromfile(param_dir, word_model_file)

#nltk.download('stopwords')
#nltk.download('averaged_perceptron_tagger')
#nltk.download('punkt')

from nltk.tokenize import word_tokenize, sent_tokenize


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
                if val > 0.5:
                    if val > maxi:
                        maxi = val
                        ricd = self.icd[i]
                        rdata = x
                i += 1
            print("val:",ricd,rdata)
            if ricd == "Ambiguous":
                #for x in self.data:
                    token = nltk.word_tokenize(j)
                    tag = nltk.pos_tag(token)
                    print("tag:",tag)
                    noun = [" "]
                    nouns = [x[0] for x in tag if x[1] not in ["CD","IN","TO",":","DT","CC"]]
                    print("nouns:",nouns)
                    j = " ".join(nouns)
                    print(item," entered the model")
                    hpd = model.get_match([j], 5)

                    max = 0
                    selected = ""
                    # for i in range(len(hpd[0])):
                    #     t = ( hpd[0][i][0],)
                    #     data = self.database.fetch_data(self.retriever_query, t)
                    #     #print(data)
                    #     if data[0][0] !=None:
                    #         if hpd[0][i][1]*data[0][0] > max:
                    #             selected = data
                    #             max = hpd[0][i][1]*data[0][0]

                    res = []
                    j = j.split(" ")
                    for word in j:
                        for i in range(len(hpd[0])):
                            t = ('%' + word + '%',hpd[0][i][0],)
                            print(self.retriever%t)
                            data = self.database.fetch_data(self.retriever, t)
                            print(data)
                            if data[0][0] != None:
                                if hpd[0][i][1] * data[0][0] > max:
                                    max = hpd[0][i][1] * data[0][0]
                                    selected = data
                                    # res.append(data[0])
                        if selected!="":
                            res.append(selected[0])
                    print("r: ", res)
                    res.sort()
                    print(res)
                    # selected = res[0]

                    if len(res) == 0:
                        ricd = "No match"
                        maxi = 0
                    else:
                        ricd = res[-1][1]
                        maxi = -1 * res[-1][0]



                    # if len(selected) == 0:
                    #     ricd = "No match"
                    #     maxi = 0
                    # else:
                    #     ricd = selected[0][1]
                    #     maxi = -1*selected[0][0]
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
    # list = map.map(['Bilateral lower limb pain and ulcer left ankle. History of evlt bilaterally in 2017.']) #,
    #                 # 'Ischemic heart disease post angioplasty',
    #                 # 'Thyroidectomy - on replacement',
    #                 # 'Bilateral vocal cord palsy',
                    # 'Hypertension',
                    # 'Steroid induced hyperglycemia',
                    # 'Chronic obstructive pulmonary disease',
                    # 'Chronic kidney disease',
                    # 'Gastroesophageal reflux disease - large hiatus hernia',
    #                 # 'Lower respiratory tract infection'])
    # for i in list:
    #     print(i)