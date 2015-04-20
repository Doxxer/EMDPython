from json import loads

from scipy.stats import rankdata

import numpy as np


__author__ = 'doxer'


def rescale(a):
    return (a - a.min()) / (a.max() - a.min())


def json_to_data_format(d):
    x, y, t = np.array(d["x"], dtype=np.float), np.array(d["y"], dtype=np.float), np.array(d["t"], dtype=np.float)
    x = rescale(x)
    y = rescale(-y)
    t = rescale(rankdata(t, method='min'))
    w = np.repeat(1.0 / len(x), len(x))
    return d["tag"], np.vstack((w, x, y, t)).T


def get_data_from_json(file_name):
    with open(file_name) as jsonFile:
        json_data = loads(jsonFile.read())

    return map(json_to_data_format, json_data)