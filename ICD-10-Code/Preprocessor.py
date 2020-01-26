from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict

class Preprocessor:

    def __init__(self):
        self.FILE_PATH = "data/icd10cm_codes_2019.txt"
        self.dictionary = defaultdict()
        self.data = []
        self.icd = []
        self.diagnosis = []

    def get_full_data(self):

        stopword = list(stopwords.words('english'))
        stopword = list(filter(lambda a: a != 'other', stopword))
        stopword.extend( [',','/','due','[',']','(',')'] )

        output = open('output.txt', 'w+')

        with open( self.FILE_PATH, 'r') as file:
            for line in file:
                #line = line.lower()
                tokens = word_tokenize(line.lower())
                filtered_tokens = [t for t in tokens if not t in stopword]
                self.data.append(filtered_tokens)
                self.icd.append(filtered_tokens[0].upper())
                self.diagnosis.append( filtered_tokens[1:])
                output.write( ( ' '.join(filtered_tokens)+"\n" )  )

        return ( self.icd, self.diagnosis )