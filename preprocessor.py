import numpy as np
import pandas as pd
import re

from utils import get_date_range


class Preprocessor:

    def __init__(self, df):
        self.df = df.copy()

    def drop_columns(self):
        self.df.drop(['query_id', 'app_id', 'timestamp',
                      'clicks', 'conversions', 'filters',
                      'hits', 'index', 'nb_hits'], axis=1, inplace=True)

    def add_date(self):
        self.df['date'] = self.df['timestamp'].apply(lambda x: x[:10])

    def add_click_counts(self):
        self.df['click_cnt'] = self.df['clicks'].apply(lambda x: 0 if x is np.nan else len(x))

    @staticmethod
    def clean_query(pattern, query):
        return ' '.join(pattern.findall(query.lower().strip()))

    def clean_queries(self):
        pattern = re.compile('\w+')
        self.df['query'] = self.df['query'].apply(
            lambda x: Preprocessor.clean_query(pattern, x))

    def drop_empty_query(self):
        self.df.drop(self.df[self.df['query'] == ''].index, inplace=True)

    def drop_low_frequency_queries(self, threshold=300):
        frequency = self.df.groupby('query').size()
        high_freq_queries = frequency[frequency >= threshold].index.tolist()
        self.df.drop(self.df[~self.df['query'].isin(high_freq_queries)].index, inplace=True)

    def aggregate(self):
        start_date = self.df['date'].min()
        end_date = self.df['date'].max()
        date_range = get_date_range(start_date, end_date, '%Y-%m-%d')
        multi_index = pd.MultiIndex.from_product(
            [self.df['query'].unique(), date_range],
            names=['query', 'date'])
        agg_df = self.df.groupby(['query', 'date']).size().to_frame('count') \
            .reindex(multi_index, fill_value=0).reset_index()

        return agg_df

    def run(self):
        self.add_date()
        self.clean_queries()
        self.drop_columns()
        self.drop_empty_query()
        self.drop_low_frequency_queries()
        return self.aggregate()
