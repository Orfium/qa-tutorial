import time

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


class Driver:

    def __init__(self, driver):
        self.driver = driver

    def loadUrl(self, url):
        self.driver.get(url)

    def quitDriver(self):
        self.driver.quit()

    def closeTab(self):
        self.driver.close()

    def refreshPage(self):
        self.driver.refresh()

    def findElement(self, *locator):
        return self.driver.find_element(*locator)

    def findElements(self, *locator):
        return self.driver.find_elements(*locator)

    def isDisplayed(self, *locator):
        return self.driver.find_element(*locator).is_displayed()

    def isSelected(self, *locator):
        return self.driver.find_element(*locator).is_selected()

    def isEnabled(self, *locator):
        return self.driver.find_element(*locator).is_enabled()

    def clickOn(self, *locator):
        self.driver.find_element(*locator).click()

    def sendKeys(self, value, *locator):
        self.driver.find_element(*locator).send_keys(value)

    def clearField(self, *locator):
        self.driver.find_element(*locator).clear()

    def getCurrentUrl(self):
        return self.driver.current_url

    def getElementText(self, *locator):
        return self.driver.find_element(*locator).text

    def getElementAttribute(self, attribute_name, *locator):
        return self.driver.find_element(*locator).get_attribute(attribute_name)

    def getTextFieldInput(self, *locator):
        return self.driver.find_element(*locator).get_attribute('value')

    def getPageTitle(self):
        return self.driver.title

    def hoverOverElement(self, element):
        return ActionChains(self.driver).move_to_element(element).perform()

    def waitUntilClickable(self, locator, time_in_secs):
        """
        Waits until the element at 'locator' is clickable.
        :param locator:
        :param time_in_secs:
        :return: The element itself
        """
        wait = WebDriverWait(self.driver, time_in_secs)
        return wait.until(EC.element_to_be_clickable(locator))

    def waitUntilElementVisible(self, locator, time_in_secs):
        wait = WebDriverWait(self.driver, time_in_secs)
        return wait.until(EC.visibility_of_element_located(locator))

    def waitUntilElementText(self, locator, text, time_in_secs):
        """
        Wait until the element at 'locator' shows the 'text'
        :param locator:
        :param text:
        :param time_in_secs:
        :return: Boolean
        """
        wait = WebDriverWait(self.driver, time_in_secs)
        return wait.until(EC.text_to_be_present_in_element(locator, text))

    def waitUntilElementPresent(self, locator, time_in_secs):
        wait = WebDriverWait(self.driver, time_in_secs)
        return wait.until(EC.presence_of_element_located(locator))

    def waitUntilUrlContains(self, partial_url, time_in_secs):
        """
        Wait until the driver current url contains a 'partial_url'
        :param partial_url:
        :param time_in_secs:
        :return: Boolean
        """
        wait = WebDriverWait(self.driver, time_in_secs)
        return wait.until(EC.url_contains(partial_url))

    def waitUntilUrlMatches(self, url, time_in_secs):
        """
        Wait until the driver current url matches a 'url'
        :param url: string
        :param time_in_secs:
        :return: Boolean
        """
        wait = WebDriverWait(self.driver, time_in_secs)
        return wait.until(EC.url_matches(url))

    def elementIsFound(self, *locator):
        try:
            self.findElement(*locator)
            return True
        except NoSuchElementException:
            return False

    # Here you can write a login function and use it in every test setup
        # def login(self):
        #     self.driver.find_element_by_id("username").send_keys(VALID_USERNAME)
        #     self.driver.find_element_by_id("password").send_keys(VALID_PASSWORD)
        #     self.driver.find_element_by_xpath("//button[@class='css-kxkgtp eollt5m0']").click()
        #
