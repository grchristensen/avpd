import numpy as np
from numpy import ndarray
from notebooks.thresholders import BaseThresholder


class SimpleThresholder(BaseThresholder):
    """
    Tests each observation for the best cutoff point and then picks the median of that
    observation and the one before it.
    """

    def __init__(self, score_func):
        """
        :param score_func: The benchmarking function to use for choosing the cutoff.
        """
        self._score_func = score_func

    def _threshold(self, distances: ndarray, labels: ndarray) -> float:
        sorted_distances = np.sort(distances)
        # We should also check if all distances should be flagged
        sorted_distances = np.insert(sorted_distances, 0, -1.0)

        # classifications[i] should be the classifications for the ith sorted distance
        classifications = distances[None, :] > sorted_distances[:, None]

        scores = self._score_func(classifications, labels[None, :])

        best_index = np.argmax(scores)

        if best_index == 0:
            # If the chosen threshold was -1.0, just return that and flag everything
            return -1.0
        elif best_index == len(sorted_distances) - 1:
            # If the chosen threshold is the greatest distance, we should not flag
            # anything.
            return float("inf")

        best_cutoff = sorted_distances[best_index]
        after_cutoff = sorted_distances[best_index + 1]

        # We want the median of the cutoff and the next distance, since this should
        # generalize a bit better.
        return (best_cutoff + after_cutoff) / 2
