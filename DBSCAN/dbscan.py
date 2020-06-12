import numpy as np

def load_data():
    points = [[1, 3], [1, 2], [2, 4], [2, 3], [2, 2], [2, 1], [3, 2], [4, 2], [5, 3], [5, 2], [5, 1], [6, 2]]
    labels = [i for i in range(1, 13)]
    return points, labels


def dbscan(r, minPoints, points, labels):
    distance = np.zeros([len(points), len(points)], dtype=float)
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            distance[i][j] = np.sqrt(np.square(points[i][0] - points[j][0]) + np.square(points[i][1] - points[j][1]))
            distance[j][i] = distance[i][j]
    central_points = []
    noise_points = []
    edge_points = []
    for i in range(len(points)):
        num = len([t for t in distance[i] if t <= r])
        if num >= minPoints:
            central_points.append(i)
        else:
            noise_points.append(i)
    len_noise = len(noise_points)
    for i in central_points:
        j = 0
        while j < len_noise:
            if distance[i][noise_points[j]] <= r:
                edge_points.append(noise_points[j])
                noise_points.pop(j)
                len_noise -= 1
                j -= 1
            j += 1

    result = []
    while len(central_points) > 0:
        tmp = set()
        remove_point = []
        for i in range(len(central_points)):
            if distance[central_points[0]][central_points[i]] <= r:
                for t in edge_points:
                    if distance[central_points[i]][t] <= r:
                        tmp.add(t)
                remove_point.append(central_points[i])
        for item in remove_point:
            tmp.add(item)
            central_points.remove(item)
        result.append(list(tmp))
    return [[labels[i] for i in items]for items in result]


if __name__ == '__main__':
    points, label = load_data()
    result = dbscan(1, 4, points, label)
    print(result)


