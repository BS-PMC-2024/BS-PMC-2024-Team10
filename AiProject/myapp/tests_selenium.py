from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import unittest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MyAppIntegrationTests(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()






    def logout(self):
        driver = self.driver
        driver.find_element(By.LINK_TEXT, "Logout").click()
        time.sleep(2)  # Wait for logout to complete

    def tearDown(self):
        self.driver.quit()

if _name_ == "_main_":
    unittest.main()