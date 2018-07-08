"""test GetNews cli"""

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
