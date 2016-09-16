# -*- coding: utf-8 -*-
# facebook.py
# 
# Find hobby circle and popular people
#
# Kai Wang
# wangkai0112006@163.com
#
# Usage: python facebook.py --input=hobbies.txt --x=2 --y=10
#
# x is number of hobbies, y is the number of circles/networks.


import argparse

# create the initial itemset C1       
def createC1(dataSet):  
    C1 = []  
    for tran in dataSet:  
        for item in tran:  
            if not [item] in C1:  
                C1.append([item])  
    C1.sort()  
    return map(frozenset, C1)  
      
# scan the dataSet to filter C_k into L_k  
def scanD(D, Ck, minSupport):  
    ssCnt = {}  
    for tran in D:  
        for can in Ck:  
            if can.issubset(tran):  
                if not ssCnt.has_key(can):  
                    ssCnt[can] = 1  
                else:  
                    ssCnt[can] += 1  
    numItems = float(len(D))  
    # L_k  
    retList = []  
    # a dict combine C_k with its support  
    supportData = {}  
    for key in ssCnt:  
        support = ssCnt[key]/numItems  
        if support >= minSupport:  
            retList.insert(0,key)  
        supportData[key] = support  
    return retList, supportData  
  
  
### Apriori algorithm to find the frequent item sets  
# create the C_k  
# actually the Lk in function denotes L_k-1  
def aprioriGen(Lk,k):  
    retList = []  
    lenLk = len(Lk)  
    for ii in range(lenLk):  
        for jj in range(ii+1, lenLk):  
            L1 = list(Lk[ii])[:k-2]  
            L1.sort()  
            L2 = list(Lk[jj])[:k-2]  
            L2.sort()  
            if L1 == L2 :  
                retList.append(Lk[ii] | Lk[jj])   
    return retList  

def apriori(dataSet, minSupport=0):  
    C1 = createC1(dataSet)  
    D = map(set, dataSet)  
    L1,supportData = scanD(D, C1, minSupport)  
    L = [L1]  
    k = 2  
    while (len(L[k-2]) > 0):  
        Ck = aprioriGen(L[k-2], k)  
        Lk, supK = scanD(D, Ck, minSupport)  
        supportData.update(supK)  
        L.append(Lk)  
        k += 1  
    return L, supportData  

##########################################
## Options and defaults
##########################################
def getOptions():
    parser = argparse.ArgumentParser(description='python *.py [option]"')
    requiredgroup = parser.add_argument_group('required arguments')
    requiredgroup.add_argument('--input', dest='input', help='input hobby file', default='', required=True)
    requiredgroup.add_argument('--x', dest='x', help='number of hobbies in a circle.', default=1, type=int, required=True)
    requiredgroup.add_argument('--y', dest='y', help='popularity is defined by number of circles/networks a people belongs', default=1,type=int, required=True)

    args = parser.parse_args()

    return args

def findPeople(hobbyset,people):
    pR = []
    for p in people:
        if len(list(hobbyset.difference(set(people[p])))) == 0:
            pR.append(p)

    return pR

##########################################
## Master function
##########################################           
def main():
    options = getOptions()
    # REad hobby file
    people = {}
    hobby = []
    with open(options.input) as fin:
        for eachline in fin:
            line = eachline.strip().split(',')
            pid = line[0]
            temph = line[1:-1]
            people[pid] = temph
            hobby.append(temph)
            
    # apriori analysis
    a,supportData = apriori(hobby)
    circleCount = {}
    # find peopel id and output
    fcircles = open('circles.txt','w')
    for hobbyset in supportData:
        if len(hobbyset) == options.x:
            plist = findPeople(hobbyset,people)
            fcircles.write(','.join(plist))
            fcircles.write('\t')
            fcircles.write(','.join(list(hobbyset)))
            fcircles.write('\n')
            for p in plist:
                if p not in circleCount:
                    circleCount[p] = 1
                else:
                    circleCount[p] += 1
    fcircles.close()

    # find popular people
    fpopular = open('popular.txt','w')
    for p in circleCount:
        if circleCount[p] >= options.y:
            fpopular.write("%s\t%s\n" % (str(p),str(circleCount[p])))
    fpopular.close()
    
if __name__ == "__main__":
    main()