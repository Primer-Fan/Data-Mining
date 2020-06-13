import math


def load_data_set():
    points = [(0, 0), (1, 2), (3, 1), (8, 8), (9, 10), (10, 7), (10, 1)]
    labels = [1, 2, 3, 4, 5, 6, 7]
    return points, labels


def k_means(points, labels, k):
    central_points = [points[i] for i in range(k)]
    distance = [[0 for i in range(k)] for i in range(len(points))]
    cluster = [[] for i in range(k)]
    while True:
        cal_dis(distance, central_points, points, k)

        tmp_cluster = [[] for i in range(k)]

        for i in range(len(points)):
            min_idx = distance[i].index(min(distance[i]))
            tmp_cluster[min_idx].append(i)

        if tmp_cluster == cluster:
            break

        cluster = tmp_cluster.copy()
        central_points.clear()
        for i in range(k):
            central_points.append((sum(points[k][0] for k in cluster[i]) / len(cluster[i]),
                                   (sum(points[k][1] for k in cluster[i]) / len(cluster[i]))))

    of2 = [0 for i in range(k)]
    for i in range(k):
        for j in range(k):
            of2[i] += len(cluster[j]) / len(points) * math.sqrt((central_points[i][0] - central_points[j][0]) ** 2
                                                                + (central_points[i][1] - central_points[j][1]) ** 2)

    return [[labels[i] for i in item] for item in cluster], of2


def cal_dis(distance, centralpoints, points, k):
    for i in range(len(points)):
        for j in range(k):
            distance[i][j] = math.sqrt((points[i][0] - centralpoints[j][0]) ** 2 + (points[i][1] - centralpoints[j][1]) ** 2)


if __name__ == "__main__":
    points, labels = load_data_set()
    clusters, of2s = k_means(points, labels, 3)
    for i in range(3):
        print(clusters[i], '\tof2:', of2s[i])

