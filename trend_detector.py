import numpy as np
import pickle


class TrendDetector:

    def __init__(self, config, decay=.99):
        self.model_path = config['model']
        self.model = {}
        self.decay = decay

    def _compute_mean_std(self, history, window=28):
        """
        Compute mean and standard deviation for historical daily counts in given window.
        :param history: historical daily search counts
        :param window: size of moving window
        :return: mean, std
        """
        history = np.array(history[-window - 1: -1])
        decay_weights = [self.decay ** a for a in range(len(history), 0, -1)]
        weighted = history * decay_weights
        mean = weighted.mean()
        std = weighted.std()
        return mean, std

    def build(self, agg_df):
        """
        Compute mean and std for all queries in provided dataframe and dump it.
        :param agg_df: aggregated daily search counts
        :return:
        """
        queries = agg_df['query'].unique()
        for query in queries:
            history_df = agg_df[agg_df['query'] == query][['date', 'count']]
            counts = history_df['count']
            mean, std = self._compute_mean_std(counts)
            self.model[query] = {'mean': mean, 'std': std}

        pickle.dump(self.model, open(self.model_path, 'wb'))
        print("Model successfully built.")

    def load_model(self):
        """
        Load pre-computed model
        :return:
        """
        self.model = pickle.load(open(self.model_path, 'rb'))
        print("Model successfully loaded.")

    def is_trending(self, query, obs, threshold=2.0, verbose=False):
        """
        For a given query and the search count of a target day, print if it is a trending search.
        :param query: query of the search
        :param obs: search count of a target day
        :param threshold: trending threshold
        :param verbose: if True, print trending result, otherwise, only print if it is a trending search
        :return:
        """
        mean_std = self.model[query]
        mean = mean_std['mean']
        std = mean_std['std']
        if std == 0:
            return 0
        z_score = 0 if std == 0 else (obs - mean) / std
        if z_score >= threshold:
            print('Query: [{}]({:2f}) is a trending search for the given observation.'.format(query, z_score))
        elif verbose:
            print('Query: [{}]({:2f}) is not a trending search for the given observation.'.format(query, z_score))
