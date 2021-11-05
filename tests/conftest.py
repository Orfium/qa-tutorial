import pytest
from selenium import webdriver

from misc_data.project_urls import BASE_URL
from webdriver import browser_options
from utilities import post_test_reports_to_slack, send_test_report_to_email, google_chat_post


@pytest.fixture()
def driver_setup(request):
    url = request.config.getoption("--url")
    browser = request.config.getoption("--browser")
    if browser.lower() == "firefox":
        driver = webdriver.Firefox(executable_path=browser_options.GECKODRIVER_EXECUTABLE_PATH,
                                   options=browser_options.ffox_options)
    elif browser.lower() == "chrome":
        driver = webdriver.Chrome(executable_path=browser_options.CHROMEDRIVER_EXECUTABLE_PATH,
                                  options=browser_options.chrome_options_global)
    else:
        print("Not valid browser")
    driver.implicitly_wait(10)

    try:
        driver.get(BASE_URL[url.lower()])
    except KeyError:
        print("Not valid url")
        driver.close()

    if request.cls is not None:
        request.cls.driver = driver

    yield driver
    driver.quit()


def pytest_addoption(parser):
    parser.addoption("--browser",
                     default="chrome",
                     help="Choose browser: firefox, chrome")

    parser.addoption("--url",
                     default="staging",
                     help="Choose URL ot perform the test: staging, live")

    parser.addoption("-S", "--slack_report",
                     dest="slack_report",
                     action="store_true",
                     help="Select this flag to post test report to slack channel #qatestreports")

    parser.addoption("-G", "--google_chat_report",
                     dest="google_chat_report",
                     action="store_true",
                     help="Select this flag to post test report to google chat channel #qa_test_reports")

    parser.addoption("-E", "--send_email_to",
                     action="store",
                     help="Select this flag to send the test report to an email. "
                          "Separate multiple email receipients with comma within a string")

    parser.addoption("--ci",
                     action="store_true",
                     help="Select this flag to run the webdriver with ci configured options (headless etc)")


def pytest_sessionfinish(session, exitstatus):
    """executes after whole test run finishes."""
    slack = session.config.getoption("-S")
    if slack is True:
        post_test_reports_to_slack.post_reports_to_slack(exitstatus)

    google_chat = session.config.getoption("-G")
    if google_chat:
        google_chat_post.post_reports_to_google_chat(exitstatus)

    email = session.config.getoption("-E")
    if email is not None and exitstatus != 0:
        send_test_report_to_email.send_test_report_to_email(email)


def pytest_sessionstart(session):
    if session.config.getoption('--ci'):
        # Chrome Options
        browser_options.chrome_options_global.add_argument('--headless')
        browser_options.chrome_options_global.add_argument("--window-size=1440,900")
        # Firefox Options
        browser_options.ffox_options.add_argument('--headless')
        browser_options.ffox_options.add_argument("--window-size=1440,900")
        # CI/Jenkins server executable path
        browser_options.CHROMEDRIVER_EXECUTABLE_PATH = "/usr/local/bin/chromedriver"









