"""launcher/wrapper for executing CLI"""
import collections
from datetime import datetime
import logging
from os import path
import platform


from plumbum import cli
import pandas as pd

import prosper.common.prosper_cli as p_cli
import prosper.datareader.news as p_news

from vincent import _version, exceptions

HERE = path.abspath(path.dirname(__file__))
PROGNAME = 'GetNews'
IntrinioAuth = collections.namedtuple('IntrinioAuth', ['username', 'password'])

def fetch_news(
        ticker_list,
        source,
        intrinio_auth,
        logger=logging.getLogger(PROGNAME),
):
    """fetch news from desired source

    Args:
        ticker_list (list): list of tickers to fetch
        source (str): name of service to fetch news from
        intrinio_auth (:obj:`IntrinioAuth`): username/password container
        logger (:obj:`logging.logger`): logging handle

    Returns:
        pandas.DataFrame: news for all tickers

    Raises:
        MissingAuthentication: lacking credentials for `intrinio` endpoints
        NotImplementedError: unsupported source type

    """
    now = pd.Timestamp.now('UTC')
    if source == 'intrinio' and not intrinio_auth:
        raise exceptions.MissingAuthentication(
            'Need `intrinio_username` and `intrinio_password'
        )
    logger.info('fetching news from: %s', source)
    results_df = pd.DataFrame()
    for ticker in cli.terminal.Progress(ticker_list.split(',')):
        logger.debug('fetching: %s', ticker)

        news_df = pd.DataFrame()
        if source == 'intrinio':
            news_df = p_news.company_news_intrinio(
                ticker,
                intrinio_auth.username,
                intrinio_auth.password,
                logger=logger,
            )
        elif source == 'robinhood':
            news_df = p_news.company_news_rh(ticker, logger=logger)
        elif source == 'yahoo':
            news_df = p_news.company_headlines_yahoo(ticker, logger=logger)
        else:
            raise NotImplementedError(f'Unexpected source type `{source}`')

        news_df['gen_ticker'] = ticker
        news_df['gen_time'] = now
        news_df['gen_source'] = source

        # append news into master dataframe
        results_df = pd.concat([results_df, news_df], ignore_index=True)

    return results_df


class GetNewsCLI(p_cli.ProsperApplication):
    PROGNAME = PROGNAME
    VERSION = _version.__version__

    config_path = path.join(HERE, 'app.cfg')

    ticker_list = cli.SwitchAttr(
        ['--tickers'],
        str,
        help='Stock ticker list to fetch news on',
    )
    @cli.switch(
        ['--ticker-csv'],
        cli.ExistingFile,
        help='Stock ticker list from .csv file',)
    def ticker_csv(self, ticker_csv_path):
        """load and parse csv file into self.ticker_list"""
        csv_df = pd.read_csv(ticker_csv_path)
        self.ticker_list = ','.join(csv_df['ticker'].tolist())

    source = cli.SwitchAttr(
        ['s', '--source'],
        cli.Set('intrinio', 'robinhood', 'yahoo'),
        help='Where to fetch news from',
    )

    def main(self):
        """launcher logic"""
        self.logger.info('hello world')
        intrinio_auth = IntrinioAuth(
            self.config.get_option(self.PROGNAME, 'intrinio_username'),
            self.config.get_option(self.PROGNAME, 'intrinio_password'),
        )

        news_df = fetch_news(
            self.ticker_list.split(','),
            self.source,
            intrinio_auth,
            logger=self.logger,
        )




def run_main():  # pragma: no cover
    """entry point for launching app"""
    GetNewsCLI.run()

if __name__ == '__main__':  # pragma: no cover
    run_main()
