from math import log
import operator


def load_data():
    train_data = [['青年', '否', '否', '中', '否'],
                  ['青年', '否', '否', '高', '否'],
                  ['青年', '是', '否', '高', '是'],
                  ['青年', '是', '是', '中', '是'],
                  ['青年', '否', '否', '中', '否'],
                  ['中年', '否', '否', '中', '否'],
                  ['中年', '否', '否', '高', '否'],
                  ['中年', '是', '是', '高', '是'],
                  ['中年', '否', '是', '很高', '是'],
                  ['中年', '否', '是', '很高', '是'],
                  ['老年', '否', '是', '很高', '是'],
                  ['老年', '否', '是', '高', '是'],
                  ['老年', '是', '否', '高', '是'],
                  ['老年', '是', '否', '很高', '是'],
                  ['老年', '否', '否', '中', '否']]
    test_data = [['青年', '否', '否', '中'],
                 ['中年', '否', '否', '高'],
                 ['老年', '是', '否', '高']]

    labels = ['年龄段', '婚否', '车否', '身高', '贷款']

    return train_data, test_data, labels


def calEnt(dataset):
    """
    计算香农信息熵

    :param dataset: 待求熵值数据集
    :return: 香农信息熵
    """
    numEntries = len(dataset)
    labelCounts = {}
    # 给所有可能分类创建字典
    for featVec in dataset:
        currentlabel = featVec[-1]
        if currentlabel not in labelCounts.keys():
            labelCounts[currentlabel] = 0
        labelCounts[currentlabel] += 1
    Ent = 0.0
    for key in labelCounts:
        p = float(labelCounts[key]) / numEntries
        Ent = Ent - p * log(p, 2)  # 以2为底求对数
    return Ent


def splitdataset(dataset, bestFeat, value):
    """
    划分数据集

    :param dataset: 当前数据集
    :param bestFeat: 最高增益率特征下标
    :param value: 最高增益率标签取值
    :return: 最高增益率标签取值为value的数据项删掉最高增益率标签的数据子集
    """
    retdataset = []  # 创建返回的数据集列表
    for featVec in dataset:  # 抽取符合划分特征的值
        if featVec[bestFeat] == value:
            reducedfeatVec = featVec[:bestFeat]  # 去掉bestFeat特征
            reducedfeatVec.extend(featVec[bestFeat + 1:])  # 将符合条件的特征添加到返回的数据集列表
            retdataset.append(reducedfeatVec)
    return retdataset


def C45_chooseBestFeatureToSplit(dataset):
    """
    选择最高增益率的特征

    :param dataset: 当前数据集
    :return: 最高增益率特征的下标
    """
    numFeatures = len(dataset[0]) - 1
    baseEnt = calEnt(dataset)
    bestInfoGain_ratio = 0.0
    bestFeature = -1
    for i in range(numFeatures):  # 遍历所有特征
        featList = [example[i] for example in dataset]
        uniqueVals = set(featList)  # 将特征列表创建成为set集合，元素不可重复。创建唯一的分类标签列表
        newEnt = 0.0
        IV = 0.0
        for value in uniqueVals:  # 计算每种划分方式的信息熵
            subdataset = splitdataset(dataset, i, value)
            p = len(subdataset) / float(len(dataset))
            newEnt += p * calEnt(subdataset)
            IV = IV - p * log(p, 2)
        infoGain = baseEnt - newEnt
        if (IV == 0):  # 固有值为0时不能作为分母
            continue
        infoGain_ratio = infoGain / IV  # 当前特征增益率
        if (infoGain_ratio > bestInfoGain_ratio):  # 选择增益率最大的特征
            bestInfoGain_ratio = infoGain_ratio
            bestFeature = i
    return bestFeature


def majorityCnt(classList):
    """
    统计当前标签出现次数最多的取值

    :param classList:
    :return: 当前标签出现次数最多的取值
    """
    c_count={}
    for i in classList:
        if i not in c_count.keys():
            c_count[i]=0
        c_count[i]+=1
    ClassCount = sorted(c_count.items(),key=operator.itemgetter(1),reverse=True)#按照统计量降序排序
    # ClassCount = sorted(c_count.items(), key=lambda v: v[1], reverse=True)  # 按照统计量降序排序
    return ClassCount[0][0]#reverse=True表示降序，因此取[0][0]，即最大值



def C45_createTree(dataset, labels):
    """
    建立C4.5决策树

    :param dataset: 训练数据集
    :param labels: 数据标签
    :return: C4.5决策树
    """
    classList = [example[-1] for example in dataset]
    if classList.count(classList[0]) == len(classList):
        # 类别完全相同，停止划分
        return classList[0]
    if len(dataset[0]) == 1:
        # 遍历完所有特征时返回出现次数最多的
        return majorityCnt(classList)
    bestFeat = C45_chooseBestFeatureToSplit(dataset)    # 最高增益率的特征下标
    bestFeatLabel = labels[bestFeat]                    # 最高增益率的特征
    C45Tree = {bestFeatLabel: {}}
    del (labels[bestFeat])
    # 得到列表包括节点所有的属性值
    featValues = [example[bestFeat] for example in dataset]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels.copy()
        C45Tree[bestFeatLabel][value] = C45_createTree(splitdataset(dataset, bestFeat, value), subLabels)  # 递归创建决策树
    return C45Tree


def classify(inputTree, featLabels, testVec):
    """
    分析测试数据项, 得出分类结果

    :param inputTree: C4.5决策树
    :param featLabels: 特征标签
    :param testVec: 测试数据项
    :return: 结果
    """
    firstStr = list(inputTree.keys())[0]
    secondDict = inputTree[firstStr]
    featIndex = featLabels.index(firstStr)
    classLabel = '否'
    for key in secondDict.keys():
        if testVec[featIndex] == key:
            if type(secondDict[key]).__name__ == 'dict':
                classLabel = classify(secondDict[key], featLabels, testVec)  # 递归分类
            else:
                classLabel = secondDict[key]
    return classLabel


if __name__ == '__main__':
    train_data, test_data, labels = load_data()
    feaLabels = labels.copy()
    Tree = C45_createTree(train_data, labels)
    print('C4.5决策树:', Tree)
    for item in test_data:
        classLabel = classify(Tree, feaLabels, item)
        print(item, classLabel)