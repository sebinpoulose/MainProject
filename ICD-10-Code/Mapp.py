from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from Database import Database
from difflib import SequenceMatcher


class Mapper():
    def __init__(self):
        self.database = Database()
        self.data = None
        self.query = 'SELECT icd,diagnosis FROM icduns where diagnosis like %s'
        self.database.connect('localhost', 'root', 'root123', 'icd')

    def map(self, diagnosis):
        result = []
        for item in diagnosis:

            t = ( '%'+item.split()[0]+'%',)
            print('%' + item.split()[0] + '%', t)
            data_element = self.database.fetch_data(self.query, t)
            print(data_element)
            self.icd = [x[0] for x in data_element]
            self.data = [x[1] for x in data_element]
            min = fuzz.WRatio(item,self.data[0])
            r = self.icd[0]
            for i in range(len(self.icd)):
                ratio = fuzz.WRatio(item,self.data[i])
                print(i)
                if ratio > min :
                    r = self.icd[i]
                    min = ratio
            result.append(r)
        return result
if __name__ == "__main__":
    m = Mapper()
    print(m.map(["hepatitis b"]))
