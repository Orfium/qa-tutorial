import pathlib

from selenium import webdriver


DOWNLOAD_FOLDER = pathlib.Path(__file__).parent / 'browser_download_folder'
CHROMEDRIVER_EXECUTABLE_PATH = pathlib.Path(__file__).parent.parent / 'drivers_binaries' / 'chromedriver'
GECKODRIVER_EXECUTABLE_PATH = pathlib.Path(__file__).parent.parent / 'drivers_binaries' / 'geckodriver'


# Chrome Options ================================
prefs = {'download.default_directory': str(DOWNLOAD_FOLDER)}
chrome_options_global = webdriver.ChromeOptions()
chrome_options_global.add_experimental_option('prefs', prefs)
chrome_options_global.add_argument('--start-maximized')

# Firefox Options ===============================
mime_types = ['text/plain',
              'application/vnd.ms-excel',
              'text/csv',
              'application/csv',
              'text/comma-separated-values',
              'application/download',
              'application/octet-stream',
              'binary/octet-stream',
              'application/binary',
              'application/x-unknown'
              ]

ffox_options = webdriver.FirefoxOptions()
ffox_options.set_preference("browser.download.folderList", 2)
ffox_options.set_preference("browser.download.manager.showWhenStarting", False)
ffox_options.set_preference("browser.download.dir", str(DOWNLOAD_FOLDER))
ffox_options.set_preference("browser.helperApps.neverAsk.saveToDisk", ",".join(mime_types))
ffox_options.add_argument('--start-maximized')




