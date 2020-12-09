from datetime import datetime

from selenium import webdriver


def get_driver(browser, url):
    driver = None
    if browser == 'chrome':
        driver = webdriver.Chrome(executable_path='resources/chromedriver.exe')
    elif browser == 'firefox':
        driver = webdriver.Firefox(executable_path='resources/geckodriver.exe')
    elif browser == 'edge':
        driver = webdriver.Edge(executable_path='resources/msedgedriver.exe')
    driver.get(url)
    driver.implicitly_wait(10)
    driver.maximize_window()
    return driver


def take_screenshot(driver, name):
    now = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    driver.get_screenshot_as_file('screenshots/1200_700_%s_%s.png' % (name, now))
    # driver.set_window_size(900, 768)
    # driver.implicitly_wait(10)
    # driver.get_screenshot_as_file('screenshots/1024_768_%s_%s.png' % (name, now))
    # driver.set_window_size(200, 800)
    # driver.implicitly_wait(10)
    # driver.get_screenshot_as_file('screenshots/320_568_%s_%s.png' % (name, now))
