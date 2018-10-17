import argparse
import yaml

from search_loader import SearchLoader
from preprocessor import Preprocessor
from trend_detector import TrendDetector


def main(mode, other_args):
    if mode != 'build' and mode != 'detect':
        raise Exception('Unknown execution mode: {}'.format(mode))

    with open("config/config.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    td = TrendDetector(cfg)

    if mode == 'build':
        # Build model
        sl = SearchLoader(cfg)
        df = sl.load()
        pp = Preprocessor(df)
        agg_df = pp.run()
        td.build(agg_df)

        # Detect trending for all queries on the last day
        max_date = agg_df['date'].max()
        for _, row in agg_df[agg_df['date'] == max_date].iterrows():
            query = row['query']
            count = row['count']
            td.is_trending(query, count)

    else:  # 'detect' mode
        # Load model
        td.load_model()

        # Detect trending for the given query and search count
        query = other_args.query
        obs = other_args.obs
        td.is_trending(query, obs, verbose=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A HN Search Trend Detector.')
    parser.add_argument('-mode', help='Execution mode, "build" for building model with historical search actions, '
                                      '"detect" for detecting if a given point is a trending search.', default='build')
    parser.add_argument('-query', help='Target query for detect mode.')
    parser.add_argument('-obs', type=int, help='Number of searches for a target day for detect mode.')
    args = parser.parse_args()
    main(args.mode, args)
