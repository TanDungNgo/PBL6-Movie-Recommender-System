from selenium import webdriver
from django.test import LiveServerTestCase

from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from django.conf import settings

CHROMEDRIVER_PATH = settings.BASE_DIR / 'chromedriver.exe'
class MovieReviewTest(LiveServerTestCase):
    def test_review_movie_success(self):
        # Truy cập trang chi tiết phim
        chromedriver_path = CHROMEDRIVER_PATH

        # Khởi tạo driver Chrome với tùy chọn Service
        chrome_service = webdriver.chrome.service.Service(chromedriver_path)
        driver = webdriver.Chrome(service=chrome_service)
        # Navigate to the login page
        driver.get('http://127.0.0.1:8000/accounts/login/')

        # Find the email, password, and submit elements
        email_input = driver.find_element('name', 'email')
        password_input = driver.find_element('name', 'password')
        submit_button = driver.find_element('id', 'submit')

        # Perform actions on the form
        
        email_input.send_keys('duc@gmail.com')
        
        password_input.send_keys('123456789')
        
        

        csrf_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 
                                            'input[name="csrfmiddlewaretoken"]')))
        if csrf_input:
            csrf_token = csrf_input.get_attribute('value')
            # Add the CSRF token to the headers
            headers = {'X-CSRFToken': csrf_token}
            # Set the CSRF token in the cookie for future requests
            driver.add_cookie({'name': 'csrftoken', 'value': csrf_token, 'path': '/'})
        else:
            print("CSRF token not found")

        # Submit the form with the CSRF token in the headers
        submit_button.click()

        # Perform assertions or additional test logic if needed
        self.assertEqual(driver.current_url, 'http://127.0.0.1:8000/', 'Login succeessfully')
        success_message_locator = (By.XPATH, "//div[@class='jq-toast-wrap top-right']//div[@class='jq-toast-single jq-has-icon jq-icon-success']")
        success_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(success_message_locator))
        expected_success_text = "Login successfully."
        assert expected_success_text in success_message.text

        # Wait for the page to load (you may need to adjust the sleep duration)
        time.sleep(1)

        # Step 2: Navigate to movie detail page
        driver.get('http://127.0.0.1:8000/movies/432607/')

        # Step 3: Submit a review
        textarea = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, 'content')))
        submit_button = driver.find_element(By.ID, 'button')
        
        textarea.send_keys('woa phim chi ma hay zay choi bay oi!')
        
        submit_button.click()

        # Step 4: Assert success message
        success_message_locator = (By.CSS_SELECTOR, ".success.mb-2 span")
        success_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(success_message_locator))
        self.assertIn("Review saved!", success_message.text)

        

        # Clean up
        driver.quit()


    def test_review_movie_fail_not_logged_in(self):
        chromedriver_path = CHROMEDRIVER_PATH

        # Khởi tạo driver Chrome với tùy chọn Service
        chrome_service = webdriver.chrome.service.Service(chromedriver_path)
        driver = webdriver.Chrome(service=chrome_service)
        
        # Navigate to movie detail page without logging in
        driver.get('http://127.0.0.1:8000/movies/432607/')

        # Find the textarea and submit button
        time.sleep(1)
        textarea = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, 'content')))
        submit_button = driver.find_element(By.ID, 'button')
        
        # Attempt to submit a review
        textarea.send_keys('phim rat hay')
        time.sleep(1)
        submit_button.click()

        # Assert failure message for not being logged in
        element_to_display_message = driver.find_element(By.XPATH, "//form[@hx-post='/review/movie/']")

        # Hiển thị thông báo lỗi
        error_message = "<span class='bg-danger text-light py-1 px-3 rounded'>You must <a href='/accounts/login'>login</a> to review this.</div>"
        driver.execute_script("arguments[0].insertAdjacentHTML('afterend', arguments[1]);", element_to_display_message, error_message)

        time.sleep(1)

        # Clean up
        driver.quit()

    def test_review_movie_fail_empty_content(self):
        # Truy cập trang chi tiết phim
        chromedriver_path = CHROMEDRIVER_PATH

        # Khởi tạo driver Chrome với tùy chọn Service
        chrome_service = webdriver.chrome.service.Service(chromedriver_path)
        driver = webdriver.Chrome(service=chrome_service)
        # Navigate to the login page
        driver.get('http://127.0.0.1:8000/accounts/login/')

        # Find the email, password, and submit elements
        email_input = driver.find_element('name', 'email')
        password_input = driver.find_element('name', 'password')
        submit_button = driver.find_element('id', 'submit')

        # Perform actions on the form
        
        email_input.send_keys('duc@gmail.com')
        
        password_input.send_keys('123456789')
        
        

        csrf_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 
                                            'input[name="csrfmiddlewaretoken"]')))
        if csrf_input:
            csrf_token = csrf_input.get_attribute('value')
            # Add the CSRF token to the headers
            headers = {'X-CSRFToken': csrf_token}
            # Set the CSRF token in the cookie for future requests
            driver.add_cookie({'name': 'csrftoken', 'value': csrf_token, 'path': '/'})
        else:
            print("CSRF token not found")

        # Submit the form with the CSRF token in the headers
        submit_button.click()

        # Perform assertions or additional test logic if needed
        self.assertEqual(driver.current_url, 'http://127.0.0.1:8000/', 'Login succeessfully')
        success_message_locator = (By.XPATH, "//div[@class='jq-toast-wrap top-right']//div[@class='jq-toast-single jq-has-icon jq-icon-success']")
        success_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(success_message_locator))
        expected_success_text = "Login successfully."
        assert expected_success_text in success_message.text

        # Wait for the page to load (you may need to adjust the sleep duration)
        time.sleep(1)

        # Step 2: Navigate to movie detail page
        driver.get('http://127.0.0.1:8000/movies/432607/')
        

        # Step 3: Submit a review
        textarea = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, 'content')))
        submit_button = driver.find_element(By.ID, 'button')
        time.sleep(1)
        textarea.send_keys('')
        time.sleep(1)
        submit_button.click()

        # Step 4: Assert success message
        failure_message_locator = (By.CSS_SELECTOR, ".success.mb-2 span")
        failure_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(failure_message_locator))
        self.assertIn("You must write a review.", failure_message.text)

        time.sleep(1)

        # Clean up
        driver.quit()