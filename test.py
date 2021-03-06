import os
import re
import math
import copy
from xlwt import Workbook

wb=Workbook()
sheet1=wb.add_sheet('Summary')
sheet1.col(0).width=4000
sheet1.col(1).width=4000
sheet1.col(2).width=4000
sheet1.col(3).width=11000
sheet1.col(4).width=5000
sheet1.col(5).width=4500
sheet1.col(6).width=4500
sheet1.write(0,0,'Document Name')
sheet1.write(0,1,'Cosine Similarity')
sheet1.write(0,2,'Adjacency Matrix')
sheet1.write(0,3,'Adjacency with CS')
sheet1.write(0,4,'Predegree')
sheet1.write(0,5,'Number of Outlinks')
sheet1.write(0,6,'Rank list parameter')
sheet2=wb.add_sheet('Ranking....')
sheet2.write(0,4,'Document According to the Ranking')
sheet2.col(4).width=9000

docwise={}
TFd={}
TFq={}
IDF={}
idfq={}
idfd={}
results={}
inlink={}
number_of_files=0
adjacency={}
x={}
rank={}
out={}

def tfquery(query):
    wordcount = {}
    totalword=0
    for word in query.split():
        if word not in wordcount:
            wordcount[word] = 1
        else:
            wordcount[word] += 1
        totalword+=1
    for c in wordcount:
        #print(c)
        TFq[c]=wordcount[c]/totalword
    #print(TFq)
        #tf of the query
def each_query(query):
    img_folder_path = "C:\\Users\\Aman Goyal\\PycharmProjects\\Web minning\\HTML"
    dirListing = os.listdir(img_folder_path)
    global number_of_files
    number_of_files = len(dirListing)
    totaloccur=0
    for word in query.split():
        if word not in TFd:
            TFd[word] = 1
        if word not in IDF:
            IDF[word] = 1
    for y in TFd:
        #print(y)
        firststep = {}
        idf=0
        totaloccur=0
        for i in range(number_of_files):
            file = "HTML\\" + dirListing[i]
            f = open(file, "r")
            x = f.read().lower()
            occur = 0;
            totalword = 0;
            wordcount = {}
            for word in x.split():
                if word not in wordcount:
                    wordcount[word] = 1
                else:
                    wordcount[word] += 1
                totalword += 1
            for c in wordcount:
                if c == y:
                    occur = wordcount[c]
            if occur != 0:
                totaloccur += 1
            firststep[dirListing[i]] = occur / totalword
           ###############
        ##tf  done in TFd now idf in IDF

        if totaloccur != 0:
            idf = 1 + math.log(number_of_files / totaloccur)
        else:
            idf = 0
        IDF[y]=idf
        TFd[y]=firststep
    #print(IDF)
        #tf and idf of the doc
def TIDFq():
    for i in TFd:
        idfq[i]=IDF[i]*TFq[i]
    #print(idfq)
def TFIDd():
    for i in IDF:
        x = {}
        for j in TFd[i]:
            x[j]=TFd[i][j]*IDF[i]
        idfd[i] = x
    #print(idfd)
def finalprep():
    for i in idfq:#mining
        for j in idfd[i]:#doc_name mining
            if j not in docwise:
                docwise[j]={i:idfd[i][j]}
            else:
                docwise[j].update({i:idfd[i][j]})
    #print(docwise)
def finale():
    #print(idfq)
    #print(docwise)
    for i in docwise:
        x1 = 1
        x2 = 1
        x3 = 1
        for j in idfq:
            x1+=docwise[i][j]*idfq[j]
            x2+=docwise[i][j]*docwise[i][j]
            x3+=idfq[j]*idfq[j]
        results[i]=x1/(math.sqrt(x2)*math.sqrt(x3))
def prepnex():
    global inlink
    q=results.__len__()
    temp=[]
    for i in results.keys():
        temp.append(i)
    for i in range(0,q):
        y=[]
        for j in range(0,q):
            x=0
            if i != j:
                print("link of",temp[i],"with",temp[j],"1 or 0")
                x=int(input())
            y.append(x)
        inlink[temp[i]]=y
def calLinkweight():
    global adjacency
    global inlink
    adjacency=copy.deepcopy(inlink)
    k=0
    for i in results:
        for j in range(0,len(adjacency)):
            inlink[i][j]=inlink[i][j]*results[i]
        k=k+1
    #print(inlink) cosine similarity and adjaceny matrix ka merge inlink hai or adjacency is new adjacency matrix
    #print(adjacency)
def degreein():
    global x
    for i in inlink:
        x[i]=0;
        out[i]=1;
    for i in inlink:
         for k in range(0,len(inlink)):
            x[i] +=inlink[i][k]
            #print(i,"xxxxxxxx",inlink[i][k],"xxxxx",x[i])
    for i in inlink:
        for j in inlink[i]:
            if(j>0):
                out[i]+=1
    k=0
    for i in x:
        x[i]/=len(x)
        k=k+x[i]
    for j in x:
        x[j]=x[j]/k
def pagerank():
    global x
    global results
    global rank
    d=0.35
    for i in x:
        #print(out[i],"ffffffffffff",x[i],"ffffffffff",results[i])
        rank[i]=math.pow(d,out[i])*x[i]*results[i]/out[i]
    print("Rank LIST: ",rank)
    j = 1
    for i in rank:
        sheet1.write(j, 6, rank[i])
        j += 1

    k=0
    for i in rank:
        k+=rank[i]
    for i in rank:
        rank[i]/=k;
    k=0
    j=0
    for i in rank:
       if(k!=0):
           if(k==rank[i]):
               j=j+1
       k = rank[i]
       if(j==len(rank)-1):
           print("\n\t\tAll ranking are same therefore no document is give special preference\n")
    #rank formula with normalized
def pagerankprint():
    global rank
    global sheet2
    print("\t\tFinale ranking:\t\n")
    j=1
    for i in sorted(rank, key=rank.get, reverse=True):
        print("\t",i)
        sheet2.write(j, 4,i)
        j += 1



def calculateCosSimilarity(query):
    each_query(query.lower())
    tfquery(query)
    TIDFq()
    TFIDd()
    finalprep()
    finale()
def calculateInOutDegree():
    prepnex()
    calLinkweight()
    degreein()
def calculateSugoRank():
    pagerank()
    pagerankprint()

#start of code
use_entry="web mining"
#doc calculation make corrction

calculateCosSimilarity(use_entry)

#make TF of query
#print(TFd)
#print(TFq)
#print(IDF)
#query * iDF
#doc* IDF
#print(idfd)
#print(idfq)
print("CS: ",results)
#TF wala kam
#In link outlink
#print(inlink)

calculateInOutDegree()
print("CS: ",results)
j=1
for i in results:
    sheet1.write(j, 0,i)
    sheet1.write(j, 1,results[i])
    j+=1

print("adjacency matrix: ",adjacency)
j=1
for i in adjacency:
    sheet1.write(j,2,str(adjacency[i]))
    j+=1

print("adjacency with cs: ",inlink)
j=1
for i in inlink:
    sheet1.write(j,3,str(inlink[i]))
    j+=1

print("inlinks: ",x)
j=1
for i in x:
    sheet1.write(j,4,x[i])
    j+=1

print("outlinks",out)
j=1
for i in out:
    sheet1.write(j,5,out[i])
    j+=1

calculateSugoRank()
wb.save('Book1.xls')
#print("RANK value of page",rank)

#print("RANK value of page",sorted(rank.items(), key=lambda t:t[1]))
#print("RANK value of page",sorted(rank, key=rank.get, reverse=True))
