from bs4 import BeautifulSoup
import requests
import re
import os

def clean(name):
    name = name.replace('.','')
    name = name.replace('-','')
    name = name.replace(' ','')
    name = name.replace('\n','')
    return(name)

def clean2(name):
    name = name.replace('None ','')
    translationTable = str.maketrans('', '', '\'{}[]\"()\n')
    return name.translate(translationTable)

def findBillNames(inputFile):
    with open(inputFile, 'r', encoding='utf-8') as doc:
        content = doc.read()
    content = content.replace('=20',' ')
    pattern = r'\b[A|S]\s?[-.]?\s?\d{2,4}[A-Z]?[-]?\b'
    bill_names = re.findall(pattern, content)
    bill_names = list(set([name.upper() for name in bill_names]))
    return bill_names

def findSameAs(aBill):
    aBill = clean(aBill)
    if(aBill[-1].isalpha()):
       amnd = aBill[-1]
       aBill = aBill.replace(amnd,'')
       page = "https://www.nysenate.gov/legislation/bills/2023/" + aBill + "/amendment/" + amnd
    else:
        page = "https://www.nysenate.gov/legislation/bills/2023/" + aBill
    pageToScrape = requests.get(page)
    doc = BeautifulSoup(pageToScrape.text, "html.parser")

    vers = doc.find_all(string="See Senate Version of this Bill:")
    if(len(vers) != 0):
        branch = vers[0].parent.parent
        sBill = branch.find("a")
        sBill = clean(sBill.text)
        return(sBill)

if __name__ == "__main__":
    allEdits = [] # List of list of sBills
    emailNames = []
    emails = "/Users/ronalddeng/Desktop/internship/email sort/emails"
    csv = "/Users/ronalddeng/Desktop/internship/email sort/email csv.txt"
    for filename in os.listdir(emails):
        if filename.endswith(".eml"):
            inputFilePath = os.path.join(emails, filename)
            billNames = findBillNames(inputFilePath)
            editedBills = [] # List of sBills
            for bill in billNames:
                if bill[0] == 'A':
                    editedBills.append(findSameAs(bill))
                else:
                    editedBills.append(clean(bill))
            editedBills = str(list(set(editedBills))).replace(',',' ')
            allEdits.append(editedBills)
            emailNames.append({filename})
            
    with open(csv, 'w') as file:
        file.write("Email name,Bills\n")
        for i in range(len(allEdits)):
            line = emailNames[i],str(allEdits[i])
            line = clean2(str(line))
            file.write(str(line))
            file.write("\n")
            
    print("done")


            
