import pytest
from fixture.application import Application
from data.user import User


fixture = None


@pytest.fixture
def app(request):
    global fixture
    browser = request.config.getoption("--browser")
    base_url = request.config.getoption("--baseUrl")
    if fixture is None:
        fixture = Application(browser=browser, base_url=base_url)
    elif not fixture.is_valid():
        fixture = Application(browser=browser, base_url=base_url)

    fixture.session.ensure_login(User.ADMIN)

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
    parser.addoption("--baseUrl", action="store", default="http://localhost/addressbook/")
