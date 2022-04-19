from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SlowElement(object):
    def __init__(self, driver, value, by):
        self.driver = driver
        self.value = value
        self.by = by
        self.locator = (self.by, self.value)

        self.web_element = None
        self.find()

    # helps us find the web element
    def find(self):
        element = WebDriverWait(self.driver, 120). \
            until(EC.presence_of_element_located(self.locator))
        self.web_element = element
        return None

    def click(self):
        element = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(self.locator))
        element.click()
        return None

    def send_keys(self, keys):
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.locator))
        element.send_keys(keys)
        return None

    def get_attribute(self, argument):
        return self.web_element.get_attribute(argument)

    @property
    def text(self):
        text = self.web_element.text
        return text