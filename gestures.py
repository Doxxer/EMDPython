from math import sqrt

import numpy as np
from pandas import crosstab

from dataFromJSON import get_data_from_json
from emd.emdist import emdist


def distance(x, y):
    return sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2) + 100 * abs(x[2] - y[2]) ** 3


if __name__ == "__main__":
    data_matrix = get_data_from_json("data/10_5_S.json")
    size = len(data_matrix)

    dist = np.full((size, size), np.inf).tolist()

    for i, (tag1, d1) in enumerate(data_matrix):
        for j, (tag2, d2) in enumerate(data_matrix):
            if i == j:
                continue
            if dist[i][j] == np.inf:
                dist[i][j] = dist[j][i] = emdist(d1, d2, distance)
    dist = np.array(dist).reshape((size, size))

    act = np.array(map(lambda (x, _): x, data_matrix))
    pred = act[np.argmax(-dist, axis=0)]

    print crosstab(act, columns=pred, colnames=['pred'], rownames=['actual'])
    print "-- {0}% --".format(np.mean(act == pred) * 100)