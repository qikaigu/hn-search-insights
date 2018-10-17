from search_loader import SearchLoader
from preprocessor import Preprocessor
from trend_detector import TrendDetector


def main():
    sl = SearchLoader()
    df = sl.load()
    pp = Preprocessor(df)
    agg_df = pp.run()

    queries = agg_df['query'].unique()
    for query in queries:
        history_df = agg_df[agg_df['query'] == query][['date', 'count']]
        counts = history_df['count'].values
        td = TrendDetector(counts[:-1])
        trending = td.is_trending(counts[-1])
        if trending > 0:
            print('Query {} {} is a trending search on {}'.format(query, trending, history_df['date'].values[-1]))


if __name__ == '__main__':
    main()
