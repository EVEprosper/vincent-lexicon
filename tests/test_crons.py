"""test GetNews cli"""
import copy
import os

import helpers
from plumbum import local
import pytest

import vincent_crons
from vincent._version import __version__
class TestGetNews:
    """validates GetNews cron"""
    cli = local['GetNews']
    dummy_app = vincent_crons.GetNews.GetNewsCLI(__file__)

    def test_help(self):
        """validate -h works"""
        result = self.cli('-h')

        result = self.cli('--version')
        assert result.strip() == f'{vincent_crons.GetNews.PROGNAME} {__version__}'

    def test_ticker_csv(self):
        """validate --ticker-csv behavior"""
        app = copy.deepcopy(self.dummy_app)
        app.ticker_csv(os.path.join(helpers.ROOT, 'vincent', 'data', 'stock_list.csv'))

        assert len(app.ticker_list.split(',')) == 102  #WTF?
