# coding=utf-8
import pickle
import sys
import time
from math import sqrt

import numpy as np
from pandas import crosstab
import Cluster

from dataFromJSON import get_data_from_json
from emd.emdist import emdist


PREDICTION_COEFFICIENT = 0.02


def distance(x, y):
    # return abs((x[0] - y[0]) + (x[1] - y[1]))
    return sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2) + 1000 * abs(x[2] ** 8 - y[2] ** 8) ** 3


errors = []
times = []


def predict(clusters, matrix):
    """

    :type clusters: dict
    """
    start_time = time.time()
    tags = np.array([tag for tag, _ in clusters.items()])
    cluster_radiuses = np.array([radius for _, (radius, _) in clusters.items()])
    distance_to_matrix = np.array([emdist(centroid, matrix, distance) for _, (radius, centroid) in clusters.items()])
    characteristic = (distance_to_matrix - cluster_radiuses) / cluster_radiuses

    # print tags
    # print cluster_radiuses
    # print distance_to_matrix
    # print characteristic

    errors.append(np.min(characteristic[np.where(characteristic > PREDICTION_COEFFICIENT)]) * 100)
    times.append(time.time() - start_time)

    index_matched = np.where(characteristic <= PREDICTION_COEFFICIENT)
    return zip(tags[index_matched], characteristic[index_matched])


if __name__ == "__main__":
    np.set_printoptions(precision=4, threshold='nan', linewidth='nan')
    data_matrix = get_data_from_json("data/10_10_S.json")
    Cluster.clusterize(data_matrix)

    with open('clusters.pkl') as f:
        clusters = pickle.load(f)

    predicted = []
    for tag, matrix in data_matrix:
        pred = predict(clusters, matrix)
        if len(pred) == 1:
            predicted.append(pred[0][0])
        else:
            sys.stderr.write("Prediction error: actual pattern: '{0}', predicted: '{1}'\n".format(tag, pred))
            predicted.append('--')

    act = np.array(map(lambda (x, _): x, data_matrix))
    predicted = np.array(predicted)

    print crosstab(act, columns=predicted, colnames=['predicted'], rownames=['actual'])
    print "-- {0}% --".format(np.mean(act == predicted) * 100)

    print u"top 3 errors: {0}".format(sorted(errors)[:3])
    print u"mean recognize time: {0} ms".format(np.mean(times) * 1000.0)