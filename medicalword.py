from bs4 import BeautifulSoup as bs
import requests

pages = ["https://www.medicinenet.com/script/main/alphaidx.asp?p="+x+"_dict" for x in "abcdefghijklmnopqrstuvwxyz"]
medical_terms = []
for url in pages:
    page = requests.get(url)
    soup = bs(page.content,'html.parser')
    term_links = soup.find_all(class_= "AZ_results")
    for tag in term_links:
        division = list(tag.children)
        for subtag in division:
            if str(type(subtag)) != "<class 'bs4.element.NavigableString'>" :
                terms = list(subtag.children)
                # print("term:",terms)
                for element in terms:
                    if str(type(element)) != "<class 'bs4.element.NavigableString'>" and element.name == 'li':
                        # print(element.name)
                        print(element.get_text())
                        medical_terms.append(element.get_text())
    print(medical_terms)
