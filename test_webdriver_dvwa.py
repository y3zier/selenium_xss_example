from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import unittest
from ddt import ddt, data


@ddt
class WebdtiverDvwaTest(unittest.TestCase):
    list_of_payloads = []

    @classmethod
    def setUpClass(cls):
        with open('payloads.txt') as f: cls.list_of_payloads = [line.rstrip('\n') for line in f]

    def setUp(self):
        self.driver = webdriver.Firefox()

    def tearDown(self):
        self.driver.close()

    @data(list_of_payloads)
    def test_xss_alert(self, value):
        # logowanie
        self.driver.get('http://localhost/login.php')
        self.driver.find_element_by_name('username').send_keys('admin')
        self.driver.find_element_by_name('password').send_keys('password')
        self.driver.find_element_by_name('Login').click()

        self._wait_for_element_to_be_displayed(By.XPATH, "//a[contains(., 'XSS (Stored')]", 5).click()

        # zmiana atrybutu - dugosc pola name jest ustalana po stronie klienta

        name_box = self._wait_for_element_to_be_displayed(By.NAME, 'txtName', 5)
        self.driver.execute_script("arguments[0].setAttribute('maxlength','50')", name_box)
        name_box.send_keys(value)
        self.driver.find_element_by_name('mtxMessage').send_keys(value)
        self.driver.find_element_by_name('btnSign').click()
        self.assertTrue(self._is_alert_present(self.driver, 1))

    def _is_alert_present(self, driver, time_to_wait):
        try:
            WebDriverWait(driver, time_to_wait).until(EC.alert_is_present(), 'alert is not present')

            alert = driver.switch_to_alert()
            alert.accept()
            return True
        except TimeoutException:
            return False

    def _wait_for_element_to_be_displayed(self, by, locator, timeout):
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.visibility_of_element_located((by, locator)))