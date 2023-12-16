import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import confidential

class TestGetDeepLUsage():
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_getDeepLUsage(self):
        # Enter email and password before extracting values
        self.driver.get("https://www.deepl.com/ja/translator")
        time.sleep(3)
        self.driver.find_element(By.CSS_SELECTOR, ".LoginButton-module--loginButton--d2RRu").click()
        time.sleep(1)
        self.driver.find_element(By.NAME, "email").send_keys(confidential.email)  # Replace with your actual email address
        self.driver.find_element(By.NAME, "password").send_keys(confidential.deepl_pass)  # Replace with your actual password
        # Submit the login form
        self.driver.find_element(By.CSS_SELECTOR, ".variant_contained--P6Etj").click()
        time.sleep(7)
        self.driver.get("https://www.deepl.com/ja/account/usage")
        time.sleep(5)
        # Retrieve the API usage value
        usage_element = self.driver.find_element(By.CSS_SELECTOR, ".barChartBox-module--mainValue--wtxcr")
        usage_value = usage_element.text.strip()  # Remove any leading or trailing whitespace

        # Close the browser window
        self.driver.quit()

        return usage_value

# Call the test method and print the usage value
def How_to_use():
    pass
    test = TestGetDeepLUsage()
    test.setup_method(None)
    usage = test.test_getDeepLUsage()
    test.teardown_method(None)
    print("Usage is :" + usage)
