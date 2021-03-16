import pytest
import json
import os.path
from fixture.application import Application


fixture = None
config = None


@pytest.fixture
def app(request):
    global fixture
    global config
    browser = request.config.getoption("--browser")
    if config is None:
        conf_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), request.config.getoption("--config"))
        with open(conf_file_path) as config_file:
            config = json.load(config_file)
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, base_url=config["baseUrl"])

    fixture.session.ensure_login(name=config["login"], pwd=config["password"])

    return fixture


@pytest.fixture(scope="session", autouse=True)
def stop(request):
    global fixture

    def finalizer():
        fixture.session.ensure_logout()
        fixture.destroy()

    request.addfinalizer(finalizer)
    return fixture


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="firefox")
    parser.addoption("--config", action="store", default="config.json")
