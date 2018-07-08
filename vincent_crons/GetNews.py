"""launcher/wrapper for executing CLI"""
from os import path
import platform
import logging

from plumbum import cli
import pandas as pd

import prosper.common.prosper_cli as p_cli


from vincent import _version

HERE = path.abspath(path.dirname(__file__))
PROGNAME = 'GetNews'

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

    def main(self):
        """launcher logic"""
        self.logger.info('hello world')

def run_main():
    """entry point for launching app"""
    GetNewsCLI.run()

if __name__ == '__main__':
    run_main()
