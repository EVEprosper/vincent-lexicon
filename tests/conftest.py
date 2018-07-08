"""pytest helpers"""
import pytest

import prosper.common.prosper_config as p_config

def pytest_addoption(parser):
    """add cli args to pytest"""
    parser.addoption(
        '--secret-cfg',
        action='store',
        default='',
        help='secret template for credentials'
    )
    parser.addini('app_cfg', 'path to app.cfg for project')

@pytest.fixture
def auth_config(request):
    """combine --secret-cfg with app.cfg and render a ProsperConfig object"""
    return p_config.render_secret(
        request.config.getoption('--secret-cfg'),
        request.config.getini('app_cfg'),
    )

@pytest.fixture
def config(request):
    """render a ProsperConfig object for testing"""
    return p_config.ProsperConfig(request.config.getini('app_cfg'))
