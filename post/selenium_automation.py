from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


__author__ = 'Tarun'

default_timeout = 45

class count_zero_or_invisible(object):

    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        try:
            elems = driver.find_elements(*self.locator)
            if len(elems) == 0:
                return True
            else:
                for elem in elems:
                    if elem.is_displayed():
                        return False
                return True
        except StaleElementReferenceException:
            return False


class count_non_zero_and_visible(object):

    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        try:
            elems = driver.find_elements(*self.locator)
            if not elems or len(elems) == 0:
                return False
            else:
                for elem in elems:
                    if elem.is_displayed():
                        return elems
                return False
        except StaleElementReferenceException:
            return False


class count_non_zero_and_clickable(object):

    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        try:
            elems = driver.find_elements(*self.locator)
            if not elems or len(elems) == 0:
                return False
            else:
                for elem in elems:
                    if elem.is_displayed() and elem.is_enabled():
                        return elems
                return False
        except StaleElementReferenceException:
            return False


def get_context():
    global driver
    return driver 

def goto(url):
    get_context().get(url)

def get_identifier( identifier):
    locator = "css"
    locatorValue = ""
    if isinstance(identifier, dict):
        if not 'locator' in identifier:
            raise ValueError("The identifier has no specified locator - {}".format(identifier))
        identifier = identifier['locator']

    map_locator_to_by = {
           "id": By.ID,
           "class": By.CLASS_NAME,
           "css": By.CSS_SELECTOR,
           "xpath": By.XPATH,
           "linktext":By.LINK_TEXT,
           "text": By.LINK_TEXT,
           "partialtext":By.PARTIAL_LINK_TEXT,
           "partiallinktext":By.PARTIAL_LINK_TEXT,
           "name": By.NAME,
           "tag": By.TAG_NAME,
           "tagname":By.TAG_NAME
         }

    if isinstance(identifier, str) or isinstance(identifier, unicode):
        identify = identifier.split('=', 1)
        if len(identify) == 1:
            locatorValue = identify[0]
        else:
            locator = identify[0]
            locatorValue = identify[1]

    if not locator.lower() in map_locator_to_by:
        locator = "css"
        locatorValue = identifier

    return (map_locator_to_by[locator],locatorValue)


def click( identifier, context=None, timeout = -1):
    find(identifier, context, timeout, EC.element_to_be_clickable).click()

def set(identifier, text, context=None, timeout = -1):
    elem = find(identifier, context, timeout)
    elem.clear()
    elem.send_keys(text)

def finds( identifier, context=None, timeout=-1, condition=None):
    """
        @return: Returns the web element found by identifier
        @rtype: selenium.webdriver.remote.webelement.WebElement
    """
    if timeout == -1:
        timeout = default_timeout

    if isinstance(identifier, WebElement):
        return identifier

    if context is None:
        context = driver

    locator = get_identifier(identifier)

    if condition is None:
        condition = count_non_zero_and_visible(locator)
    else:
        condition = condition(locator)

    wdw = WebDriverWait(driver, timeout)

    try:
        elems = wdw.until(condition)
        return elems if isinstance(elems, list) else []

    except TimeoutException:
        return []

def wait_any(identifiers, **kwargs):
    timeout = kwargs.get('timeout', default_timeout)
    if 'timeout' in kwargs:
        del kwargs['timeout']

    time_start = time.time()

    while True:
        for identifier in identifiers:
            try:
                find(identifier, timeout=0, **kwargs)
                return True
            except Exception as ex:
                pass
        if time.time() - time_start > timeout:
            return False
    return False


def find(identifier, context=None, timeout=-1, condition=EC.presence_of_element_located):
    """
        @return: Returns the web element found by identifier
        @rtype: selenium.webdriver.remote.webelement.WebElement
    """
    if timeout == -1:
        timeout = default_timeout

    if isinstance(identifier, WebElement):
        return identifier

    if context is None:
        context = driver

    locator = get_identifier(identifier)
    wdw = WebDriverWait(driver=context, timeout=timeout)
    try:
        element = wdw.until(condition(locator))
    except Exception as ex:
        element = context.find_element(*locator)
        return element
        raise
    return element

def refresh_page():
    get_context().refresh()
    
def init_driver(param_driver):
    """
        @type driver: RemoteWebDriver
    """
    global driver
    driver = param_driver
    driver.implicitly_wait(0)

def get_driver():
    """
        @rtype: selenium.webdriver.remote.WebDriver
    """
    global driver
    return driver

def quit_driver():
    global driver
    if driver:
        driver.quit()
        driver = None

def execute_script(text,args=None):
    global driver
    if args is None:
        args = []
    return driver.execute_script(text,args)
    
    
def take_screen_shot(path):
    global driver
    driver.save_screenshot(path)

def get_page_source():
    global driver
    return driver.page_source
    