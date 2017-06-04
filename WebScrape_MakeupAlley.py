import urllib
import urllib2
from bs4 import BeautifulSoup
import os
import csv

def make_soup(url):
        thepage = urllib2.urlopen(url)
        soupdata = BeautifulSoup(thepage, "html.parser")
        return soupdata

makeupdatasaved = ""
for brandnumber in range (1,2001):
        makeupdatasaved = ""
        for pagenumber in range (0,68):
                soup = make_soup ("https://www.makeupalley.com/product/searching.asp/Brand="+str(brandnumber)+"/page="+str(pagenumber))
                table = soup.find(attrs={"class":"search-results"})
                for record in table.findAll("tr"):
                        makeupdata = ""
                        for data in record.findAll("td"):
                                if len(data.findAll("a")) ==0:
                                        makeupdata = makeupdata + "|" + data.text
                                else:
                                        makeupdata = makeupdata + "|" + data.findAll("a")[0].text
                        if len(makeupdata)!=0:
                                makeupdatasaved = makeupdatasaved + "\n" + makeupdata [1:]
                if len(table.findAll("tr")) ==0:
                         break
        with open("./makeupalleyscrape/makeupalley"+str(brandnumber)+".csv", 'a') as f:
                f.write (makeupdatasaved.encode("utf-8"))
        print (makeupdatasaved)

                
