def loadDataSet():
    return [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]

def createC1(dataSet):
    C1 = set()
    for t in dataSet:
        for item in t:
            item_set = frozenset([item])
            C1.add(item_set)
    return C1

def scanD(dataSet, ck, minSupport):
    ssCnt = {}
    for tid in dataSet:
        for can in ck:
            if can.issubset(tid):
                if can not in ssCnt.keys():
                    ssCnt[can] = 1
                else:
                    ssCnt[can] += 1
    numItems = len(dataSet)
    reList = []
    supportData = {}
    for key in ssCnt:
        support = ssCnt[key] / numItems
        if support >= minSupport:
            reList.append(key)
        supportData[key] = support
    return reList, supportData

def aprioriGen(Lk, k):
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i+1, lenLk):
            L1 = list(Lk[i])[k:-2]
            #print(L1)
            L2 = list(Lk[j])[:k-2]
            #print(L2)
            if L1 == L2:
                retList.append(Lk[i] | Lk[j])
    return retList

def apriori(dataSet, minSupport):
    dataSet = list(map(set, dataSet))
    C1 = createC1(dataSet)
    L1, supportData = scanD(dataSet, C1, minSupport)
    L = [L1]
    k = 2

    while(len(L[k - 2]) > 1):
        Ck = aprioriGen(L[k - 2], k)
        Lk, Supk = scanD(dataSet, Ck, minSupport)
        supportData.update(Supk)
        L.append(Lk)
        k += 1
    return L, supportData