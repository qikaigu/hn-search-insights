import argparse
import yaml

from search_loader import SearchLoader
from preprocessor import Preprocessor
from trend_detector import TrendDetector


def main(mode):
    if mode != 'build' and mode != 'detect':
        raise Exception('Unknown execution mode: {}'.format(mode))

    with open("config/config.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    td = TrendDetector(cfg)

    if mode == 'build':
        sl = SearchLoader(cfg)
        df = sl.load()
        pp = Preprocessor(df)
        agg_df = pp.run()
        td.build(agg_df)

    else:  # 'detect' mode
        td.load_model()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A HN Search Trend Detector.')
    parser.add_argument('-mode', help='Execution mode, "build" for building model with historical search actions, '
                                      '"detect" for detecting if a given point is a trending search.', default='build')
    args = parser.parse_args()
    main(args.mode)
