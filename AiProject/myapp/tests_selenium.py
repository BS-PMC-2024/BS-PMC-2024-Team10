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

    def create_user_and_login(self, username, password, is_student=True):
        driver = self.driver

        if is_student:
            driver.get("http://localhost:8000/student_register/")
        else:
            driver.get("http://localhost:8000/practitioner_register/")

        driver.find_element(By.NAME, "first_name").send_keys("John")
        driver.find_element(By.NAME, "last_name").send_keys("Doe")
        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "email").send_keys(f"{username}@example.com")
        driver.find_element(By.NAME, "password1").send_keys(password)
        driver.find_element(By.NAME, "password2").send_keys(password)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        self.login(username, password)

    def test_register_student_and_login(self):
        self.create_user_and_login("studenttest1", "mmllmkmm", is_student=True)
        self.assertIn("student_dashboard", self.driver.current_url)



    def test_register_practitioner_and_add_recording(self):
        self.create_user_and_login("practitionertest3", "mmllmkmm", is_student=False)

        self.driver.get("http://localhost:8000/practitioner_dashboard/add_recording/")

        self.driver.find_element(By.NAME, "title").send_keys("Test Recording")
        self.driver.find_element(By.NAME, "description").send_keys("This is a test recording.")
        
        file_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "confession"))
        )
        file_input.send_keys("C:\\Users\\User\\Desktop\\93907ff065615ceadd3da6646eaa821ef969c9a3.mp4")

        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()



    def test_add_study_material(self):
        self.create_user_and_login("practitionertest3", "mmllmkmm", is_student=False)

        self.driver.get("http://localhost:8000/add_study_material/")

        self.driver.find_element(By.NAME, "title").send_keys("Study Material")
        self.driver.find_element(By.NAME, "description").send_keys("This is a study material.")
        
        file_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "file"))
        )
        file_input.send_keys("C:\\Users\\User\\Desktop\\SCE\\cv_2023\\Ali Afawi - CV1.pdf")
        
        # Submit the form
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()





    def login(self, username, password):
        driver = self.driver
        driver.get("http://localhost:8000/")
        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # Wait for the login process to complete
        time.sleep(2)


    def test_add_exam(self):
        self.create_user_and_login("practitionertest3", "mmllmkmm", is_student=False)

        self.driver.get("http://localhost:8000/practitioner_dashboard/newTest/")

        self.driver.find_element(By.NAME, "title").send_keys("Add exam")
        self.driver.find_element(By.NAME, "description").send_keys("This is a new exam.")
        
        file_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "file"))
        )
        file_input.send_keys("C:\\Users\\User\\Desktop\\SCE\\cv_2023\\Ali Afawi - CV1.pdf")
        
        # Submit the form
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()


        

    def test_student_do_exam(self):
        # Step 1: Log in as the student
        self.create_user_and_login("studenttest7", "mmllmkmm", is_student=True)

        # Step 2: Navigate to the exams page
        self.driver.get("http://localhost:8000/student_dashboard/exams/")

        # Step 3: Wait for assignment cards to be present
        try:
            assignment_cards = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".assignment-card"))
            )
        except Exception as e:
            self.fail(f"Failed to locate assignment cards. Error: {e}")

        if not assignment_cards:
            self.fail("No exams found on the exams page.")

        # Step 4: Upload the submission file
        try:
            upload_form = assignment_cards[0].find_element(By.CSS_SELECTOR, "form")
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of(upload_form)
            )
            file_input = upload_form.find_element(By.NAME, "file")
            file_input.send_keys("C:\\Users\\User\\Desktop\\SCE\\cv_2023\\Ali Afawi - CV1.pdf")
            upload_form.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

            # Step 5: Wait for submission confirmation
            self.driver.get("http://localhost:8000/student_dashboard/exams/")

            assignment_cards = self.driver.find_elements(By.CSS_SELECTOR, ".assignment-card")
            
            confirmation_text = WebDriverWait(assignment_cards[0], 10).until(
                EC.visibility_of_element_located((By.XPATH, "//*[contains(text(),'You have already submitted a solution.')]"))
            )
            self.assertTrue(confirmation_text.is_displayed())
        except Exception as e:
            self.fail(f"Failed to upload the exam submission. Error: {e}")


    def logout(self):
        driver = self.driver
        driver.find_element(By.LINK_TEXT, "Logout").click()
        time.sleep(2)  # Wait for logout to complete

    def tearDown(self):
        self.driver.quit()

if _name_ == "_main_":
    unittest.main()