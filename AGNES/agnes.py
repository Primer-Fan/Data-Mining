def load_data():
    points = [(0, 2), (0, 0), (1.5, 0), (5, 0), (5, 2)]
    labels = ['A', 'B', 'C', 'D', 'E']
    return points, labels

def choose_nearest_cluster(cluster, distance):
    """
    选择最近的簇

    :param cluster: 当前聚类情况
    :param distance: point距离表
    :return: 距离最近的两个簇的下标
    """
    cluster_len = len(cluster)
    nearest_dis, reti, retj = float('inf'), 0, 0
    for i in range(cluster_len):
        for j in range(i + 1, cluster_len):
            dis = float('inf')
            for x in cluster[i]:
                for y in cluster[j]:
                    dis = min(dis, distance[x][y])
            if dis < nearest_dis:
                nearest_dis, reti, retj = dis, i, j
    return reti, retj


def agnes(points, num, labels):
    """
    agnes聚类算法

    :param points: 点的位置表
    :param num: 结束条件, 簇的数目
    :param labels: 各点标号
    :return: 簇数为num的label列表
    """
    points_num = len(points)
    square_distance = [[0] * points_num for i in range(points_num)]
    # 打表点之间的距离, 因为只是用来比较, 使用欧几里得距离的方表示距离
    for i in range(points_num):
        for j in range(i, points_num):
            square_distance[i][j] = float((points[i][0] - points[j][0]) ** 2 + (points[i][1] - points[j][1]) ** 2)
            square_distance[j][i] = square_distance[i][j]

    cluster = [[i] for i in range(points_num)]  # 初始聚类情况, 每一个点为一个独立的簇

    while len(cluster) > num:
        mergei, mergej = choose_nearest_cluster(cluster, square_distance)
        cluster[mergei].extend(cluster[mergej])
        del cluster[mergej]

    result = [[labels[k] for k in items] for items in cluster]  # 用label标签替代聚类中的下标
    return result


if __name__ == '__main__':
    points, labels = load_data()
    result = agnes(points, 2, labels)
    print(result)


