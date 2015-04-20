__author__ = 'doxer'

from .emd import emd


def emdist(a, b, distance_function):
    """
    Return Earth Mover's distance

    :type distance_function: function
    :type b: numpy matrix
    :type a: numpy matrix
    """
    w1, w2 = a[:, 0], b[:, 0]
    feature1, feature2 = a[:, 1:], b[:, 1:]
    feature1 = (feature1.tolist(), w1.tolist())
    feature2 = (feature2.tolist(), w2.tolist())

    return emd(feature1, feature2, distance_function)
