import itertools
import pickle

import numpy as np

from emd.emdist import emdist
from main import distance


def find_centroid(cluster):
    """
    Find centroid in cluster

    :param cluster: list of numpy matrices: [(w, x, y, t)...]
    :return: tuple of (max_distance, (w, x, y, t)--centroid)
    """
    size = len(cluster)
    cluster = map(lambda (tag, d): d, cluster)

    dist_matrix = np.full((size, size), -np.inf).tolist()

    for i, d1 in enumerate(cluster):
        for j, d2 in enumerate(cluster):
            if i == j:
                continue
            if dist_matrix[i][j] == -np.inf:
                dist_matrix[i][j] = dist_matrix[j][i] = emdist(d1, d2, distance)

    dist_matrix = np.array(dist_matrix).reshape((size, size))
    max_distance_from_each = np.max(dist_matrix, axis=0)
    centroid_index = np.argmin(max_distance_from_each)

    return max_distance_from_each[centroid_index], cluster[centroid_index]


def clusterize(data):
    get_tag = lambda (tag, matrix): tag
    clusters = {tag: find_centroid(list(group)) for tag, group in
                itertools.groupby(sorted(data, key=get_tag), key=get_tag)}
    with open('clusters.pkl', 'w') as f:
        pickle.dump(clusters, f, pickle.HIGHEST_PROTOCOL)