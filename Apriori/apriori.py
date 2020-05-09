def createC1(dataSet):
    C1 = []
    for tid in dataSet:
        for item in tid:
            if [item] not in C1:        #因为C1里存放一元项集, 要使用 [item] 而不是 item
                C1.append([item])
    return sorted(list(map(frozenset, C1)))     #冻结转化为列表并排序, 转化为列表是为了后面使用时不需要每次转化, 排序可以通过调整k项集构造函数, 达到不需要每次进行排序, 降低时间复杂度的效果

def scanD(dataSet, Ck, minSupport):
    scanCount = {}      #扫描记录每一个项集在dataSet中出现的次数
    for tid in dataSet:
        for can in Ck:
            if can.issubset(tid):
                if can not in scanCount.keys(): scanCount[can] = 1
                else: scanCount[can] += 1

    numItems = len(dataSet)     #记录dataSet的项数, 用以计算支持度
    Lk = []
    supportData = {}
    for key in scanCount:
        support = scanCount[key] / numItems     # 支持度计算
        if support >= minSupport:
            Lk.append(key)              #添加符合支持度的右项
        supportData[key] = support      #记录项集支持度
    return Lk, supportData

# k+1项集构造
def aprioriGen(Lk):
    lenLk = len(Lk)
    L = []
    for i in range(lenLk):
        for j in range(i + 1, lenLk):
            L1 = list(Lk[i])[:-1]       #得益于C1构造时的排序操作, 构造L1,L2时不需要每次进行排序, 因为我们自始至终构造的项集都是有序的
            L2 = list(Lk[j])[:-1]
            '''
            比较Lk[i]于Lk[j]的前len(Lk[i]) - 1项, 若相同可以拼接Lk[i]与Lk[j]构造出长度为len(Lk[i]) + 1的项集, 
            因Lk[z]有序, 根据频繁项集的子集必定为频繁项集, 非频繁项集的超集必定不为频繁项集的特性, 
            我们可以排除 [1, 2], [2, 3]不能构造出[1, 2, 3]的情况, 因为[1,2,3]为频繁项集的时候, 
            [1, 2], [1, 3]必定存在于我们构造的二元频繁项集中
            '''
            if L1 == L2:
                L.append(Lk[i] | Lk[j])
    return L

def apriori(dataSet, minSupport):
    dataSet = list(map(set, dataSet))
    C1 = createC1(dataSet)
    L1, supportData = scanD(dataSet, C1, minSupport)
    L = [L1]    # 频繁项集
    k = 2   # 从L[0]即L1开始

    #有两个或以上项集才有必要使用aprioroGen构造更大的项集
    while(len(L[k - 2]) > 1):
        Ck = aprioriGen(L[k - 2])
        #print("Ck:", k, Ck)
        Lk, Supk = scanD(dataSet, Ck, minSupport)
        supportData.update(Supk)    # 更新支持度数据
        L.append(Lk)    # 更新频繁项集
        k += 1
    return L, supportData