###Webscapes NY Senate website to find senate vers of assembly bill###

from bs4 import BeautifulSoup
import requests

def findSameAs(aBill):
    if(aBill[-1].isalpha()):
       amnd = aBill[-1]
       aBill = aBill.replace(amnd,'')
       page = "https://www.nysenate.gov/legislation/bills/2023/" + aBill + "/amendment/" + amnd
    else:
        page = "https://www.nysenate.gov/legislation/bills/2023/" + aBill
    pageToScrape = requests.get(page)
    doc = BeautifulSoup(pageToScrape.text, "html.parser")
    
    vers = doc.find_all(string="See Senate Version of this Bill:")
    branch = vers[0].parent.parent
    sBill = branch.find("a")
    out = sBill.string
    out = out.replace(' ','')
    out = out.replace('None','')
    out = out.replace('\n','')
    return(out)

aBill = input("Assembly Bill:")
aBill = aBill.replace('.','')
aBill = aBill.replace(' ','')
print(findSameAs(aBill))
