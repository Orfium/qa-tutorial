from selenium.webdriver.common.by import By


COMPANIES_LOCATORS = {
    "WCM": (By.XPATH, "//div[contains(text(),'WCM')]"),
    "WMG": (By.XPATH, "//div[contains(text(),'WMG')]"),
    "SATV": (By.XPATH, "//div[contains(text(),'SATV')]"),
    "GMR": (By.XPATH, "//div[contains(text(),'GMR')]"),
    "EMI": (By.XPATH, "//div[contains(text(),'EMI')]"),
    "SME": (By.XPATH, "//div[contains(text(),'SME')]"),
    "KOBALT": (By.XPATH, "//div[contains(text(),'KOBALT')]")
}

COMPANIES_NAMES = list(COMPANIES_LOCATORS.keys())
