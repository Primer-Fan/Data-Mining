import Apriori.apriori

if __name__ == "__main__":
    dataSet = Apriori.apriori.loadDataSet()
    L, supportData = Apriori.apriori.apriori(dataSet, minSupport=0)
    print(L, supportData)

