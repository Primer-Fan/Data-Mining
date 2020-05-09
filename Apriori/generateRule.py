from Apriori.apriori import aprioriGen

# 可信度计算, 计算机关联规则可信度, 并将置信度满足要求的规则加入规则列表
def calcConf(freqSet, H, supportData, ruleList, minConf=0.5):   #当前频繁项集, 可作为规则右项的集, 支持度数据, 规则列表, 最小置信度
    prunedH = []    #修剪后右项集, 根据置信度的反单调性, 不满足置信度要求的右项的超集也不满足置信度要求, 应剪枝以降低时间复杂度
    for RightSet in H:
        conf = supportData[freqSet]/supportData[freqSet-RightSet]
        if conf >= minConf:
            ruleList.append((freqSet - RightSet, RightSet, conf))
            prunedH.append(RightSet)
    return prunedH

# 不断增大规则右件, 以挖掘该频繁项集下所有符合要求的关联规则
def miningRules(freqSet, H, supportData, ruleList, minConf=0.5):
    m = len(H[0])
    if len(freqSet) > m:    # 当频繁项集的项数多于右项集的项数, 才能保证左项不为空
        Hmp1 = calcConf(freqSet, H, supportData, ruleList, minConf) #计算当前右项集下的规则, 并筛选出满足置信度要求的右项集
        Hmp1 = aprioriGen(Hmp1)     # 构造增大一项的右项集
        if len(Hmp1) > 0:   # 若右项集不为空, 继续挖掘
            miningRules(freqSet, Hmp1, supportData, ruleList, minConf)

def generateRules(L, supportData, minConf=0.5):
    ruleList = []   # 规则集
    for i in range(1, len(L)):
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]
            if i > 1:   # 频繁项集下有很多项, 需要不断增大右项以挖掘全部规则
                miningRules(freqSet, H1, supportData, ruleList, minConf)
            else:   # 当前频繁项集只有两项, 右项只能为单项
                calcConf(freqSet, H1, supportData, ruleList, minConf)
    return ruleList



