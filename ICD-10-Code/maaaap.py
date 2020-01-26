from Database import Database
from nltk.corpus import stopwords
import nltk
import ncrmodel
param_dir = "C:/Users/sadiq naizam/Desktop/python_workspace/ncr_hpo_params/model_params"
word_model_file = "C:/Users/sadiq naizam/Desktop/python_workspace/ncr_hpo_params/model_params/pmc_model_new.bin"
model = ncrmodel.NCR.loadfromfile(param_dir, word_model_file)
#nltk.download('stopwords')
from Extractor import Extractor
from nltk.tokenize import word_tokenize, sent_tokenize
#nltk.download('averaged_perceptron_tagger')

class Mapper():
    def __init__(self):
        self.database = Database()
        self.result = []
        self.icd = []
        self.data = []
        self.query = 'SELECT icd,diagnosis FROM icd_synonym where diagnosis like %s'
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
            if ricd == "Ambiguous":
                #for x in self.data:
                    hpd = model.get_match([j], 5)
                    print(hpd)
                    hpx = model.get_match(self.data, 5)
                    print(hpx)
                    print(j)
                    print(hpd[0][0][0])
                    fl = 1
                    hpt = ("Ambiguous","Ambiguous")
                    large = 0
                    point = 0
                    while hpd[0][point][0] == "None":
                        point = point + 1
                    for hi in range(len(hpx)):
                        if hpx[hi][0][0] == hpd[0][point][0]:
                            print(self.data[hi],self.icd[hi],hpx[hi][0][1])
                            if fl:
                                large = hpx[hi][0][1]
                                hpt = (self.data[hi],self.icd[hi])
                                fl = 0
                            elif large < hpx[hi][0][1]:
                                large = hpx[hi][0][1]
                                hpt = (self.data[hi],self.icd[hi])

                    print(hpt[0]+":"+hpt[1])
                    print(large)
                    ricd = hpt[1]
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
                dia = []
                mapp = []
                for i in range(0, l_sub):
                    for l in range(0, i + 1):
                        tem_d = sub[l]
                        for k in range(l + 1, l + j):
                            tem_d = tem_d + " and " + sub[k]
                        dia.append(tem_d)
                    j = j - 1
                for d in dia:
                    mapp.append(self.mapd(d))
                maxx = -1
                for m in mapp:
                    if m[1] > maxx:
                        maxx = m[1]
                        tem_res = m[0]
                self.result.append(tem_res)
            else:
                res = self.mapd(item)
                self.result.append(res[0])
        return self.result

    def matcherRatio(self, item, x):
        temp = len(set(x.split())-set(self.stopwordcompare)) * len(item.split())
        return (len(set(item.split()) & (set(x.split())-set(self.stopwordcompare))) ** 2) / temp

if __name__ == "__main__":
    map = Mapper()
    list = map.map(['Mantle cell lymphoma in leukemic phase',
                    'Ischemic heart disease post angioplasty',
                    'Thyroidectomy - on replacement',
                    'Bilateral vocal cord palsy',
                    'Hypertension',
                    'Steroid induced hyperglycemia',
                    'Chronic obstructive pulmonary disease',
                    'Chronic kidney disease',
                    'Gastroesophageal reflux disease - large hiatus hernia',
                    'Lower respiratory tract infection'])
    for i in list:
        print(i)