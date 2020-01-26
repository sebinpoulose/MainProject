from bs4 import BeautifulSoup
import requests

file = open("synonymsk-l.txt","w")
f = open("urllist.txt","r")
def get_urls(urls):
    data = soup.findAll('div', attrs={'class': 'z32'})
    for div in data:
        links = div.find_all('a')
        for a in links:
            urls.append('https://www.icd10data.com' + a['href'])

#response = requests.get('https://www.icd10data.com/ICD10CM/Codes')
#soup = BeautifulSoup(response.text, 'lxml')

list2 = []

#get_urls(list)
# for line in f:
#     list.append(line)
# print(list,'\n',len(list))

list2 = f.read().splitlines()
print(list2,'\n',len(list2))
#list2 = []
# for item in list:
#     response = requests.get(item)
#     soup = BeautifulSoup(response.text, 'lxml')
#     get_urls(list2)
#     print(list2)
#f.writelines(["%s\n" % item for item in list2])

i=0
dis=[]
flag = 0
starturl = "https://www.icd10data.com/ICD10CM/Codes/S00-T88/S90-S99/S96-/S96.001D"
stopurl = "https://www.icd10data.com/ICD10CM/Codes/S00-T88/T80-T88/T88-/T88.9XXS"
for item in list2:
    if starturl in item:
        flag = 1
        continue
    if flag == 1 and stopurl not in item and item.count('/')==8:
        response = requests.get(item)
        icd =  item[item.rfind('/')+1:]
        #file.write(icd)
        soup = BeautifulSoup(response.text, 'lxml')
        data = soup.text
        templ = data.split('\n\n')
        i = 0
        for element in templ:
            if "Approximate Synonyms" in element:
                dis = templ[i+1].split('\n')
                for f in dis:
                    file.writelines(["%s\t%s\n" %(icd, f)])
            i = i + 1
        print(icd,"\t",dis)
        dis = []
    if stopurl in item:
        break
file.close()
f.close()