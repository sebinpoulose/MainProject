from Database import Database
from nltk.corpus import stopwords
import nltk
import ncrmodel
import threading
import tensorflow as tf
from threading import Lock

lock = Lock()

database = Database()
query = 'SELECT icd,diagnosis,hp,co FROM icd_synonym'
database.connect('localhost', 'root', 'root123', 'icd')

tf.enable_eager_execution()
param_dir = "C:\\Users\\student\\PycharmProjects\\ncr_hpo_params\\model_params"
word_model_file = "C:\\Users\\student\\PycharmProjects\\ncr_hpo_params\\model_params\\pmc_model_new.bin"
model = ncrmodel.NCR.loadfromfile(param_dir, word_model_file)


class myThread(threading.Thread):
    def __init__(self, threadID, data):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.data = data

    def run(self):
        print("Starting :", self.threadID)
        update = 'UPDATE icd_synonym SET hp = \'{}\', co = {} WHERE icd = \'{}\''
        n = 0
        flag = 0
        for x in self.data:
            n = n + 1
            print(self.threadID, ":", n)
            if x[2] is None:
                flag = 1
                hpx = model.get_match(x[1], 5)
                # print(hpx)
                point = 0
                # print(hpx[point][0])
                while hpx[point][0] == 'None':
                    point += 1
                    if point == 5:
                        break
                if point != 5:
                    x[2] = hpx[point][0]
                    x[3] = hpx[point][1]
        # print(self.data)
        if flag:
            lock.acquire()
            nl = 0
            for x in self.data:
                nl = nl + 1
                print(self.threadID, ":Database ", nl)
                database.update_no_commit(update.format(x[2], x[3], x[0]))
            database.commit()
            lock.release()
        print("Exiting :", self.threadID)


class Modifier:
    def mod(self):
        data_element = database.fetch(query)
        data_element = [[x[0], x[1], x[2], x[3]] for x in data_element]
        print(data_element[20000])
        select = 100
        for i in range(0, len(data_element), select):
            while threading.activeCount() > 20:
                pass
            thread = myThread(i, data_element[i:i + select])
            thread.start()


if __name__ == "__main__":
    m = Modifier()
    m.mod()
