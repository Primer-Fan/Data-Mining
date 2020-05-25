import sys

def load_data():
    points = [(0, 2), (0, 0), (1.5, 0), (5, 0), (5, 2)]
    labels = ['A', 'B', 'C', 'D', 'E']
    return points, labels


def cal_square_distance(points):
    """
    计算打表点之间的距离, 因为只是用来比较, 使用欧几里得距离的方表示距离

    :param points: 点的分布表
    :return: 欧几里得距离的方
    """
    points_num = len(points)
    square_distance = [[0] * points_num for i in range(points_num)]
    for i in range(points_num):
        for j in range(i, points_num):
            square_distance[i][j] = float((points[i][0] - points[j][0]) ** 2 + (points[i][1] - points[j][1]) ** 2)
            square_distance[j][i] = square_distance[i][j]
    return square_distance


def choose_max_diameter_cluster(distance, clusters):
    """
    选择直径最大的簇

    :param distance: 点距离表
    :param clusters: 当前簇集
    :return: 直径最大的簇的下标
    """
    split_idx, max_diameter = None, 0
    for i in range(len(clusters)):
        diameter = 0
        for j in range(len(clusters[i])):
            for k in range(j + 1, len(clusters[i])):
                diameter = max(diameter, distance[clusters[i][j]][clusters[i][k]])
        if diameter > max_diameter:
            split_idx, max_diameter = i, diameter
    return split_idx


def spilt_cluter(cluter, distance):
    """
    分裂簇

    :param cluter: 簇
    :param distance: 距离表
    :return: 需要新加入的簇
    """
    if len(cluter) < 2: # 簇中数据低于两个时, 无法分裂, 为了完成分裂数目, 返回新的空簇
        return []

    splinter, old = list(), cluter
    idx, max_dis = 0, 0
    for i in range(len(old)):   # 找old簇中距离其他点最远的点, 分裂出来加入新簇
        ever_dis = 0
        for j in range(len(old)):
            ever_dis += distance[old[i]][old[j]]
        if ever_dis > max_dis:
            idx, max_dis = i, ever_dis
    splinter.append(old[idx])
    del old[idx]
    check = True
    while check:
        check = False
        for i in range(len(old)):   # 找距离splinter簇距离比old簇近的点, 如果有, 分裂出该点加入splinter簇
            splinter_dis, old_dis = float('inf'), float('inf')
            for j in range(len(splinter)):
                splinter_dis = min(splinter_dis, distance[old[i]][splinter[j]])
            for j in range(len(old)):
                if i == j:
                    continue
                old_dis = min(old_dis, distance[old[i]][old[j]])
            if splinter_dis < old_dis:
                idx = i
                check = True
                break
        if check:
            splinter.append(old[idx])
            del old[idx]
    return splinter


def diana(points, labels, num):
    """
    DIANA算法入口, 计算返回聚类好的列表

    :param points: 点位置表
    :param labels: 点标签表
    :param num: 目标簇数
    :return: 聚类好的列表
    """
    square_distance = cal_square_distance(points)   # 计算距离, 为方便采用欧氏距离的方

    clusters = [[i for i in range(len(points))]]    # 初始簇
    while len(clusters) < num:
        split_idx = choose_max_diameter_cluster(square_distance, clusters)
        splinter = spilt_cluter(clusters[split_idx], square_distance)
        clusters.append(splinter)
    return  [[labels[k] for k in items] for items in clusters]  # 返回时用label替代下标


if __name__ == '__main__':
    points, labels = load_data()
    result = diana(points, labels, 2)
    print(result)