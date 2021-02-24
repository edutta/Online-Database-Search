# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 17:13:43 2021

@author: EnakshyLaptop
"""
"""
This code is for searching publications in Pubmed using multiple search query
"""
from Bio import Entrez, Medline
import numpy as np
import pandas as pd

'''
function for counting the id's with the search query - This function returns the 
number of pmid's for the specific search query
'''

def countid(query):
    Entrez.email = "your.email@example.com"     
    handle = Entrez.egquery(term=query,mindate=2000)
    result = Entrez.read(handle)
    handle.close()
    for row in result["eGQueryResult"]:
        if row["DbName"]=="pubmed":
            results=row["Count"]
        return results
    
'''

'''
def searchid(query,count):
    handle = Entrez.esearch(db="pubmed", term=query, retmax=count)
    record = Entrez.read(handle)
    idlist = sorted(record["IdList"])
    return idlist
    

'''
function for searching the the text with the common id's
'''
def fetchpub(idlist):
    handle = Entrez.efetch(db="pubmed", id=idlist, rettype="medline", retmode="text")
    records = Medline.parse(handle)
    records = list(records)
    return records


'''
Search Strategy - Here two different queries are added and 
then the id's common in them are selected
'''

#the search terms
term1="metabolic syndrome[MESH] OR metabolic syndrome[ALL] OR MetS[ALL]"
term2="diet[MESH] OR dietary pattern[ALL] OR eating pattern[ALL] OR food pattern[ALL] OR dietary habit[ALL] OR dietary score[ALL] OR dietary index[ALL] OR nutrient pattern[ALL] OR diet diversity[ALL] OR diet variety[ALL] OR diet quality[ALL] OR diet index[ALL] OR diet score[ALL]"
query=np.array([term1,term2],dtype=np.str)

#Finding the id's using the search criterion
lists=[]
for i in query:
    lists.append(searchid(i,countid(i)))
    
#Finding the common id's in the two lists  - lists[0] is the smallest  
idlist=[item for item in lists[1] if item in lists[0]]    
len(idlist) #7546 common

#Fetching the publication
results=fetchpub(idlist)

#Puting the information in a dataframe
rows=[[result.get("TI"),result.get("AB"),result.get("AU"),result.get("PT"),result.get("TA"),result.get("AID"),result.get("SO"),result.get("MH")] for result in results]
df=pd.DataFrame(rows,columns=["Title","Abstract","Author","Type","Journal Name","DOI","Source","Keywords"])


