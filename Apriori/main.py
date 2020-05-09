from Apriori import apriori,generateRule

def loadDataSet():
    return [[1, 3, 4], [3, 4, 5], [1, 3, 4, 5], [1, 4, 6]]


if __name__ == "__main__":
    dataSet = loadDataSet()
    L, supportData = apriori.apriori(dataSet, 0.5)
    #print(supportData)
    M = generateRule.generateRules(L, supportData, 0.5)
    for t in M:
        print(t)