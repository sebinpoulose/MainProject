from Database import Database
from Preprocessor import Preprocessor
from Mapper import Mapper
from collections import defaultdict
#from Extractor import Extract
dictionary1 = defaultdict(list)
dictionary2 = defaultdict(list)
database_object = Database()
data_object = Preprocessor()

FILE_PATH = ['sample1.rtf','sample2.rtf','sample3.rtf','sample4.rtf','sample5.rtf','sample6.rtf']
file_object = Extract(FILE_PATH)
mapper = Mapper()

value = []
var = ['unspecified','other','others']

query = " SELECT * FROM ICD_data WHERE code LIKE %s AND diagnosis LIKE %s"
query1 = "UPDATE ICD_data SET diagnosis = %s WHERE code = %s "
query2 = 'SELECT code,diagnosis FROM ICD_data'

def update_data():
    
    (icd, diagnosis) = data_object.get_full_data()
    for i in range( len(icd) ): 
        value.append( ( ' '.join(diagnosis[i]) , icd[i].upper() ) ) 

    print(database_object.insert_many( query1, value  ))

'''
def fetch_data():   
    value = ('%anemia%', '%unspecified%')
    print ( x for x in database_object.fetch_data(query, value) )

'''

def map_data(diagnosis):

    data = database_object.fetch_data(query2, None)
    
    for disease in diagnosis:
        disease = disease.lower()
        dictionary1.clear()
        dictionary2.clear()
        for item in data:
            icds = list(item)

            if( disease in icds[1].split(' ') ):
                dictionary1[disease].append(icds[0])
                dictionary2[disease].append(icds[1])
        
        #print( dictionary2 )

        if ( len(dictionary1[disease]) > 1 ):
            for i in range(len(dictionary1[disease])):

                splitted_disease = []
                try:
                    splitted_icds = dictionary2[disease][i].split(' ')
                except:
                    splitted_icds = dictionary2[disease][i]
               
                if(disease.find(' ') != -1): 
                    splitted_disease.append(disease.split(' '))
                else:
                    splitted_disease.append(disease)
                
                #   splitted_disease = list(splitted_disease)
                #print(len(splitted_disease))
                #print( dictionary2[disease][i] )
                #print(disease)
                #print(splitted_disease)
                
                if ('unspecified' in splitted_icds or 'other' in splitted_icds) and (len(splitted_icds) == len(splitted_disease)+1):
                    print (disease + " - " + dictionary1[disease][i])

        elif( len(dictionary1[disease]) == 1 ):
            print (disease + ' - ' + ','.join(dictionary1[disease]))
        else:
            print( 'Not mapped(Sub string absent) !')
    print()

   # print(dictionary)   

if __name__ == '__main__':

    database_object.connect('localhost', 'root', 'zaraf', 'ICD')
    print()
    #update_data()

    diagnosis1 = ['Anemia','Isosporiasis', 'Cyclosporiasis','pancytopenia']
    #print( file_object.getalldiagnosis())

    #input : list of diagnosis
    map_data(diagnosis1 )
    
