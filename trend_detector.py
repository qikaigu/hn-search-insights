import numpy as np
import pickle as pkl


class TrendDetector:

    def __init__(self, history, decay=.99):
        decay_weights = [decay ** a for a in range(len(history), 0, -1)]
        weighted = np.array(history) * decay_weights
        self.mean = weighted.mean()
        self.std = weighted.std()

    def is_trending(self, obs, threshold=2.0):
        if self.std == 0:
            return 0
        z_score = (obs - self.mean) / self.std

        return 0 if z_score < threshold else z_score
