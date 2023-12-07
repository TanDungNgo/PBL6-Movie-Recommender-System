from selenium import webdriver
from django.test import LiveServerTestCase

from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from django.conf import settings

CHROMEDRIVER_PATH = settings.BASE_DIR / 'chromedriver.exe'
class LoginFormTest(LiveServerTestCase):
    def test_login_success(self):
        # Đường dẫn đến ChromeDriver
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
        time.sleep(2)
        email_input.send_keys('trang@gmail.com')
        time.sleep(2)
        password_input.send_keys('123456789')
        time.sleep(2)
        

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
        self.assertEqual(driver.current_url, 'http://127.0.0.1:8000/dashboard/', 'Login succeessfully')
        success_message_locator = (By.XPATH, "//div[@class='jq-toast-wrap top-right']//div[@class='jq-toast-single jq-has-icon jq-icon-success']")
        success_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(success_message_locator))
        expected_success_text = "Login successfully."
        assert expected_success_text in success_message.text

        # Wait for the page to load (you may need to adjust the sleep duration)
        time.sleep(4)

        # Close the browser
        driver.quit()

    def test_invalid_email(self):
        # Đường dẫn đến ChromeDriver
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
        time.sleep(2)
        email_input.send_keys('huyentrang@gmail.com')
        time.sleep(2)
        password_input.send_keys('123456789')
        time.sleep(2)
        

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

        # Submit the form
        submit_button.click()

        # Wait for any error message or indication of unsuccessful login
        error_message_locator = (By.XPATH, "//div[@class='jq-toast-wrap top-right']//div[@class='jq-toast-single jq-has-icon jq-icon-error']")
        error_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(error_message_locator))

        # Assert that the error message contains the expected text
        expected_error_text = "Email or password is incorrect."
        assert expected_error_text in error_message.text

        # Optionally, you can assert that the URL, title, or other elements indicate a failed login
        time.sleep(4)
        # Close the browser
        driver.quit()
    def test_invalid_password(self):
        # Đường dẫn đến ChromeDriver
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
        time.sleep(2)
        email_input.send_keys('trang@gmail.com')
        time.sleep(2)
        password_input.send_keys('123456')
        time.sleep(2)
        

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

        # Submit the form
        submit_button.click()

        # Wait for any error message or indication of unsuccessful login
        error_message_locator = (By.XPATH, "//div[@class='jq-toast-wrap top-right']//div[@class='jq-toast-single jq-has-icon jq-icon-error']")
        error_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(error_message_locator))

        # Assert that the error message contains the expected text
        expected_error_text = "Email or password is incorrect."
        assert expected_error_text in error_message.text

        # Optionally, you can assert that the URL, title, or other elements indicate a failed login
        time.sleep(4)
        # Close the browser
        driver.quit()
    
    def test_invalid_email_password(self):
        # Đường dẫn đến ChromeDriver
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
        time.sleep(2)
        email_input.send_keys('huyentrang@gmail.com')
        time.sleep(2)
        password_input.send_keys('123456')
        time.sleep(2)
        

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

        # Submit the form
        submit_button.click()

        # Wait for any error message or indication of unsuccessful login
        error_message_locator = (By.XPATH, "//div[@class='jq-toast-wrap top-right']//div[@class='jq-toast-single jq-has-icon jq-icon-error']")
        error_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(error_message_locator))

        # Assert that the error message contains the expected text
        expected_error_text = "Email or password is incorrect."
        assert expected_error_text in error_message.text

        # Optionally, you can assert that the URL, title, or other elements indicate a failed login
        time.sleep(4)
        # Close the browser
        driver.quit()

    def test_empty_email(self):
       # Đường dẫn đến ChromeDriver
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
        time.sleep(2)
        email_input.send_keys('')
        time.sleep(2)
        password_input.send_keys('123456789')
        time.sleep(2)
        

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

        # Submit the form
        submit_button.click()

        # Wait for any error message or indication of unsuccessful login
        error_message_locator = (By.XPATH, "//div[@class='jq-toast-wrap top-right']//div[@class='jq-toast-single jq-has-icon jq-icon-error']")
        error_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(error_message_locator))

        # Assert that the error message contains the expected text
        expected_error_text = "Please enter both email and password."
        assert expected_error_text in error_message.text

        # Optionally, you can assert that the URL, title, or other elements indicate a failed login
        time.sleep(4)
        # Close the browser
        driver.quit()

    def test_empty_password(self):
        # Đường dẫn đến ChromeDriver
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
        time.sleep(2)
        email_input.send_keys('trang@gmail.com')
        time.sleep(2)
        password_input.send_keys('')
        time.sleep(2)
        

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

        # Submit the form
        submit_button.click()

        # Wait for any error message or indication of unsuccessful login
        error_message_locator = (By.XPATH, "//div[@class='jq-toast-wrap top-right']//div[@class='jq-toast-single jq-has-icon jq-icon-error']")
        error_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(error_message_locator))

        # Assert that the error message contains the expected text
        expected_error_text = "Please enter both email and password."
        assert expected_error_text in error_message.text

        # Optionally, you can assert that the URL, title, or other elements indicate a failed login
        time.sleep(4)
        # Close the browser
        driver.quit()
    
    def test_empty_email_password(self):
        # Đường dẫn đến ChromeDriver
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
        time.sleep(2)
        email_input.send_keys('')
        time.sleep(2)
        password_input.send_keys('')
        time.sleep(2)
        

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

        # Submit the form
        submit_button.click()

        # Wait for any error message or indication of unsuccessful login
        error_message_locator = (By.XPATH, "//div[@class='jq-toast-wrap top-right']//div[@class='jq-toast-single jq-has-icon jq-icon-error']")
        error_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(error_message_locator))

        # Assert that the error message contains the expected text
        expected_error_text = "Please enter both email and password."
        assert expected_error_text in error_message.text

        # Optionally, you can assert that the URL, title, or other elements indicate a failed login
        time.sleep(4)
        # Close the browser
        driver.quit()

class SignupFormTest(LiveServerTestCase):
    # def test_signup_success(self):
    #     # Đường dẫn đến ChromeDriver
    #     chromedriver_path = CHROMEDRIVER_PATH

    #     # Khởi tạo driver Chrome với tùy chọn Service
    #     chrome_service = webdriver.chrome.service.Service(chromedriver_path)
    #     driver = webdriver.Chrome(service=chrome_service)
    #     # Navigate to the login page
    #     driver.get('http://127.0.0.1:8000/accounts/register/')

    #     # Find the email, password, and submit elements
    #     username_input = driver.find_element('name', 'username')
    #     email_input = driver.find_element('name', 'email')
    #     password_input = driver.find_element('name', 'password')
    #     submit_button = driver.find_element('id', 'submit')


    #     # Perform actions on the form
    #     time.sleep(2)
    #     username_input.send_keys('thaotran')
    #     time.sleep(2)
    #     email_input.send_keys('thao@gmail.com')
    #     time.sleep(2)
    #     password_input.send_keys('123456789')
    #     time.sleep(2)

    #     csrf_input = WebDriverWait(driver, 10).until(
    #         EC.presence_of_element_located((By.CSS_SELECTOR, 
    #                                         'input[name="csrfmiddlewaretoken"]')))
    #     if csrf_input:
    #         csrf_token = csrf_input.get_attribute('value')
    #         # Add the CSRF token to the headers
    #         headers = {'X-CSRFToken': csrf_token}
    #         # Set the CSRF token in the cookie for future requests
    #         driver.add_cookie({'name': 'csrftoken', 'value': csrf_token, 'path': '/'})
    #     else:
    #         print("CSRF token not found")

    #     # Submit the form with the CSRF token in the headers
    #     submit_button.click()

    #     self.assertEqual(driver.current_url, 'http://127.0.0.1:8000/accounts/login/', 'Signup successfully.')
    #     success_message_locator = (By.XPATH, "//div[@class='jq-toast-wrap top-right']//div[@class='jq-toast-single jq-has-icon jq-icon-success']")
    #     success_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(success_message_locator))
    #     time.sleep(4)

    #     # Close the browser
    #     driver.quit()
    
    # def test_empty_username(self):
    #     # Đường dẫn đến ChromeDriver
    #     chromedriver_path = CHROMEDRIVER_PATH

    #     # Khởi tạo driver Chrome với tùy chọn Service
    #     chrome_service = webdriver.chrome.service.Service(chromedriver_path)
    #     driver = webdriver.Chrome(service=chrome_service)
    #     # Navigate to the login page
    #     driver.get('http://127.0.0.1:8000/accounts/register/')

    #     # Find the email, password, and submit elements
    #     username_input = driver.find_element('name', 'username')
    #     email_input = driver.find_element('name', 'email')
    #     password_input = driver.find_element('name', 'password')
    #     submit_button = driver.find_element('id', 'submit')

    #     # Perform actions on the form
    #     time.sleep(2)
    #     username_input.send_keys('')
    #     time.sleep(2)
    #     email_input.send_keys('thao@gmail.com')
    #     time.sleep(2)
    #     password_input.send_keys('123456789')
    #     time.sleep(2)
        

    #     csrf_input = WebDriverWait(driver, 10).until(
    #         EC.presence_of_element_located((By.CSS_SELECTOR, 
    #                                         'input[name="csrfmiddlewaretoken"]')))
    #     if csrf_input:
    #         csrf_token = csrf_input.get_attribute('value')
    #         # Add the CSRF token to the headers
    #         headers = {'X-CSRFToken': csrf_token}
    #         # Set the CSRF token in the cookie for future requests
    #         driver.add_cookie({'name': 'csrftoken', 'value': csrf_token, 'path': '/'})
    #     else:
    #         print("CSRF token not found")

    #     # Submit the form
    #     submit_button.click()

    #     # Wait for any error message or indication of unsuccessful login
    #     error_message_locator = (By.XPATH, "//div[@class='jq-toast-wrap top-right']//div[@class='jq-toast-single jq-has-icon jq-icon-error']")
    #     error_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(error_message_locator))

    #     # Assert that the error message contains the expected text
    #     expected_error_text = "Username is required."
    #     assert expected_error_text in error_message.text

    #     # Optionally, you can assert that the URL, title, or other elements indicate a failed login
    #     time.sleep(4)
    #     # Close the browser
    #     driver.quit()

    # def test_empty_email(self):
    #     # Đường dẫn đến ChromeDriver
    #     chromedriver_path = CHROMEDRIVER_PATH

    #     # Khởi tạo driver Chrome với tùy chọn Service
    #     chrome_service = webdriver.chrome.service.Service(chromedriver_path)
    #     driver = webdriver.Chrome(service=chrome_service)
    #     # Navigate to the login page
    #     driver.get('http://127.0.0.1:8000/accounts/register/')

    #     # Find the email, password, and submit elements
    #     username_input = driver.find_element('name', 'username')
    #     email_input = driver.find_element('name', 'email')
    #     password_input = driver.find_element('name', 'password')
    #     submit_button = driver.find_element('id', 'submit')

    #     # Perform actions on the form
    #     time.sleep(2)
    #     username_input.send_keys('thaotran')
    #     time.sleep(2)
    #     email_input.send_keys('')
    #     time.sleep(2)
    #     password_input.send_keys('123456789')
    #     time.sleep(2)
        

    #     csrf_input = WebDriverWait(driver, 10).until(
    #         EC.presence_of_element_located((By.CSS_SELECTOR, 
    #                                         'input[name="csrfmiddlewaretoken"]')))
    #     if csrf_input:
    #         csrf_token = csrf_input.get_attribute('value')
    #         # Add the CSRF token to the headers
    #         headers = {'X-CSRFToken': csrf_token}
    #         # Set the CSRF token in the cookie for future requests
    #         driver.add_cookie({'name': 'csrftoken', 'value': csrf_token, 'path': '/'})
    #     else:
    #         print("CSRF token not found")

    #     # Submit the form
    #     submit_button.click()

    #     # Wait for any error message or indication of unsuccessful login
    #     error_message_locator = (By.XPATH, "//div[@class='jq-toast-wrap top-right']//div[@class='jq-toast-single jq-has-icon jq-icon-error']")
    #     error_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(error_message_locator))

    #     # Assert that the error message contains the expected text
    #     expected_error_text = "Email is required."
    #     assert expected_error_text in error_message.text

    #     # Optionally, you can assert that the URL, title, or other elements indicate a failed login
    #     time.sleep(4)
    #     # Close the browser
    #     driver.quit()

    # def test_empty_password(self):
    #     # Đường dẫn đến ChromeDriver
    #     chromedriver_path = CHROMEDRIVER_PATH

    #     # Khởi tạo driver Chrome với tùy chọn Service
    #     chrome_service = webdriver.chrome.service.Service(chromedriver_path)
    #     driver = webdriver.Chrome(service=chrome_service)
    #     # Navigate to the login page
    #     driver.get('http://127.0.0.1:8000/accounts/register/')

    #     # Find the email, password, and submit elements
    #     username_input = driver.find_element('name', 'username')
    #     email_input = driver.find_element('name', 'email')
    #     password_input = driver.find_element('name', 'password')
    #     submit_button = driver.find_element('id', 'submit')

    #     # Perform actions on the form
    #     time.sleep(2)
    #     username_input.send_keys('thaotran')
    #     time.sleep(2)
    #     email_input.send_keys('thao@gmail.com')
    #     time.sleep(2)
    #     password_input.send_keys('')
    #     time.sleep(2)
        

    #     csrf_input = WebDriverWait(driver, 10).until(
    #         EC.presence_of_element_located((By.CSS_SELECTOR, 
    #                                         'input[name="csrfmiddlewaretoken"]')))
    #     if csrf_input:
    #         csrf_token = csrf_input.get_attribute('value')
    #         # Add the CSRF token to the headers
    #         headers = {'X-CSRFToken': csrf_token}
    #         # Set the CSRF token in the cookie for future requests
    #         driver.add_cookie({'name': 'csrftoken', 'value': csrf_token, 'path': '/'})
    #     else:
    #         print("CSRF token not found")

    #     # Submit the form
    #     submit_button.click()

    #     # Wait for any error message or indication of unsuccessful login
    #     error_message_locator = (By.XPATH, "//div[@class='jq-toast-wrap top-right']//div[@class='jq-toast-single jq-has-icon jq-icon-error']")
    #     error_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(error_message_locator))

    #     # Assert that the error message contains the expected text
    #     expected_error_text = "Password is required."
    #     assert expected_error_text in error_message.text

    #     # Optionally, you can assert that the URL, title, or other elements indicate a failed login
    #     time.sleep(4)
    #     # Close the browser
    #     driver.quit()

    def test_already_exists_username(self):
        # Đường dẫn đến ChromeDriver
        chromedriver_path = CHROMEDRIVER_PATH

        # Khởi tạo driver Chrome với tùy chọn Service
        chrome_service = webdriver.chrome.service.Service(chromedriver_path)
        driver = webdriver.Chrome(service=chrome_service)
        # Navigate to the login page
        driver.get('http://127.0.0.1:8000/accounts/register/')

        # Find the email, password, and submit elements
        username_input = driver.find_element('name', 'username')
        email_input = driver.find_element('name', 'email')
        password_input = driver.find_element('name', 'password')
        submit_button = driver.find_element('id', 'submit')

        # Perform actions on the form
        time.sleep(2)
        username_input.send_keys('huyentrang')
        time.sleep(2)
        email_input.send_keys('thao@gmail.com')
        time.sleep(2)
        password_input.send_keys('123456789')
        time.sleep(2)
        

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

        # Submit the form
        submit_button.click()

        # Wait for any error message or indication of unsuccessful login
        error_message_locator = (By.XPATH, "//div[@class='jq-toast-wrap top-right']//div[@class='jq-toast-single jq-has-icon jq-icon-error']")
        error_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(error_message_locator))

        # Assert that the error message contains the expected text
        expected_error_text = "Username already exists."
        assert expected_error_text in error_message.text

        # Optionally, you can assert that the URL, title, or other elements indicate a failed login
        time.sleep(4)
        # Close the browser
        driver.quit()
    def test_already_exists_email(self):
        # Đường dẫn đến ChromeDriver
        chromedriver_path = CHROMEDRIVER_PATH

        # Khởi tạo driver Chrome với tùy chọn Service
        chrome_service = webdriver.chrome.service.Service(chromedriver_path)
        driver = webdriver.Chrome(service=chrome_service)
        # Navigate to the login page
        driver.get('http://127.0.0.1:8000/accounts/register/')

        # Find the email, password, and submit elements
        username_input = driver.find_element('name', 'username')
        email_input = driver.find_element('name', 'email')
        password_input = driver.find_element('name', 'password')
        submit_button = driver.find_element('id', 'submit')

        # Perform actions on the form
        time.sleep(2)
        username_input.send_keys('thaotran')
        time.sleep(2)
        email_input.send_keys('trang@gmail.com')
        time.sleep(2)
        password_input.send_keys('123456789')
        time.sleep(2)
        

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

        # Submit the form
        submit_button.click()

        # Wait for any error message or indication of unsuccessful login
        error_message_locator = (By.XPATH, "//div[@class='jq-toast-wrap top-right']//div[@class='jq-toast-single jq-has-icon jq-icon-error']")
        error_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(error_message_locator))

        # Assert that the error message contains the expected text
        expected_error_text = "Email already exists."
        assert expected_error_text in error_message.text

        # Optionally, you can assert that the URL, title, or other elements indicate a failed login
        time.sleep(4)
        # Close the browser
        driver.quit()

class UpdateProfileTest(LiveServerTestCase):
    def test_update_success(self):
        # Đường dẫn đến ChromeDriver

        chromedriver_path = 'D:/Download/chromedriver-win64 (2)/chromedriver-win64/chromedriver.exe'

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
        time.sleep(2)
        email_input.send_keys('trang@gmail.com')
        time.sleep(2)
        password_input.send_keys('123456789')
        time.sleep(2)
        

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
        self.assertEqual(driver.current_url, 'http://127.0.0.1:8000/dashboard/', 'Login succeessfully')
        success_message_locator = (By.XPATH, "//div[@class='jq-toast-wrap top-right']//div[@class='jq-toast-single jq-has-icon jq-icon-success']")
        success_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(success_message_locator))
        expected_success_text = "Login successfully."
        assert expected_success_text in success_message.text

        # Wait for the page to load (you may need to adjust the sleep duration)
        time.sleep(4)

        driver.get('http://127.0.0.1:8000/accounts/profile/')

        # Find the email, password, and submit elements
        username_input = driver.find_element('name', 'username')
        email_input = driver.find_element('name', 'email')
        first_name_input = driver.find_element('name', 'first_name')
        last_name_input = driver.find_element('name', 'last_name')
        submit_button = driver.find_element('id', 'update-profile-button')

        # Perform actions on the form
        time.sleep(2)
        username_input.clear()  # Clear the existing username
        time.sleep(2)
        username_input.send_keys('huyentrangle')

        time.sleep(2)
        email_input.clear()
        time.sleep(2)
        email_input.send_keys('trangle@gmail.com')
        time.sleep(2)
        first_name_input.clear()
        time.sleep(2)
        first_name_input.send_keys('Thi Huyen Trang')
        time.sleep(2)
        last_name_input.clear()
        time.sleep(2)
        last_name_input.send_keys('Le')
        time.sleep(2)
        

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
        self.assertEqual(driver.current_url, 'http://127.0.0.1:8000/accounts/profile/', 'Successfully updated')
        success_message_locator = (By.XPATH, "//div[@class='jq-toast-wrap top-right']//div[@class='jq-toast-single jq-has-icon jq-icon-success']")
        success_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(success_message_locator))
        expected_success_text = "Successfully updated"
        assert expected_success_text in success_message.text

        # Wait for the page to load (you may need to adjust the sleep duration)
        time.sleep(4)
        # Close the browser
        driver.quit()

    def test_update_invalid_username(self):
        # Đường dẫn đến ChromeDriver
        chromedriver_path = 'D:/Download/chromedriver-win64 (2)/chromedriver-win64/chromedriver.exe'

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
        time.sleep(2)
        email_input.send_keys('trang@gmail.com')
        time.sleep(2)
        password_input.send_keys('123456789')
        time.sleep(2)
        

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
        self.assertEqual(driver.current_url, 'http://127.0.0.1:8000/dashboard/', 'Login succeessfully')
        success_message_locator = (By.XPATH, "//div[@class='jq-toast-wrap top-right']//div[@class='jq-toast-single jq-has-icon jq-icon-success']")
        success_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(success_message_locator))
        expected_success_text = "Login successfully."
        assert expected_success_text in success_message.text

        # Wait for the page to load (you may need to adjust the sleep duration)
        time.sleep(4)

        driver.get('http://127.0.0.1:8000/accounts/profile/')

        # Find the email, password, and submit elements
        username_input = driver.find_element('name', 'username')
        email_input = driver.find_element('name', 'email')
        first_name_input = driver.find_element('name', 'first_name')
        last_name_input = driver.find_element('name', 'last_name')
        submit_button = driver.find_element('id', 'update-profile-button')

        # Perform actions on the form
        time.sleep(2)
        username_input.clear()  # Clear the existing username
        time.sleep(2)
        username_input.send_keys('ductran')

        time.sleep(2)
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

        # Wait for any error message or indication of unsuccessful login
        error_message_locator = (By.XPATH, "//div[@class='jq-toast-wrap top-right']//div[@class='jq-toast-single jq-has-icon jq-icon-error']")
        error_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(error_message_locator))

        # Assert that the error message contains the expected text
        expected_error_text = "Username already exists. Please choose a different one."
        assert expected_error_text in error_message.text

        # Wait for the page to load (you may need to adjust the sleep duration)
        time.sleep(4)
        # Close the browser
        driver.quit()

    def test_update_invalid_email(self):
        # Đường dẫn đến ChromeDriver
        chromedriver_path = 'D:/Download/chromedriver-win64 (2)/chromedriver-win64/chromedriver.exe'

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
        time.sleep(2)
        email_input.send_keys('trang@gmail.com')
        time.sleep(2)
        password_input.send_keys('123456789')
        time.sleep(2)
        

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
        self.assertEqual(driver.current_url, 'http://127.0.0.1:8000/dashboard/', 'Login succeessfully')
        success_message_locator = (By.XPATH, "//div[@class='jq-toast-wrap top-right']//div[@class='jq-toast-single jq-has-icon jq-icon-success']")
        success_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(success_message_locator))
        expected_success_text = "Login successfully."
        assert expected_success_text in success_message.text

        # Wait for the page to load (you may need to adjust the sleep duration)
        time.sleep(4)

        driver.get('http://127.0.0.1:8000/accounts/profile/')

        # Find the email, password, and submit elements
        username_input = driver.find_element('name', 'username')
        email_input = driver.find_element('name', 'email')
        first_name_input = driver.find_element('name', 'first_name')
        last_name_input = driver.find_element('name', 'last_name')
        submit_button = driver.find_element('id', 'update-profile-button')

        # Perform actions on the form
        time.sleep(2)
        email_input.clear()  # Clear the existing username
        time.sleep(2)
        email_input.send_keys('duc@gmail.com')

        time.sleep(2)
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

        # Wait for any error message or indication of unsuccessful login
        error_message_locator = (By.XPATH, "//div[@class='jq-toast-wrap top-right']//div[@class='jq-toast-single jq-has-icon jq-icon-error']")
        error_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(error_message_locator))

        # Assert that the error message contains the expected text
        expected_error_text = "Email already exists. Please use a different one."
        assert expected_error_text in error_message.text

        # Wait for the page to load (you may need to adjust the sleep duration)
        time.sleep(4)
        # Close the browser
        driver.quit()

class ChangePasswordTest(LiveServerTestCase):
    def test_change_success(self):
        chromedriver_path = CHROMEDRIVER_PATH
        
        chrome_service = webdriver.chrome.service.Service(chromedriver_path)
        driver = webdriver.Chrome(service=chrome_service)
        # Navigate to the login page
        driver.get('http://127.0.0.1:8000/accounts/login/')

        email_input = driver.find_element('name', 'email')
        password_input = driver.find_element('name', 'password')
        submit_button = driver.find_element('id', 'submit')

        # Perform actions on the form
        time.sleep(2)
        email_input.send_keys('phuong@gmail.com')
        time.sleep(2)
        password_input.send_keys('123456789')
        time.sleep(2)
        

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
        self.assertEqual(driver.current_url, 'http://127.0.0.1:8000/dashboard/', 'Login succeessfully')
        success_message_locator = (By.XPATH, "//div[@class='jq-toast-wrap top-right']//div[@class='jq-toast-single jq-has-icon jq-icon-success']")
        success_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(success_message_locator))
        expected_success_text = "Login successfully."
        assert expected_success_text in success_message.text

        time.sleep(4)

        driver.get('http://127.0.0.1:8000/accounts/profile/')

        old_password_input = driver.find_element('name', 'old_password')
        new_password_input = driver.find_element('name', 'new_password')
        confirm_password_input = driver.find_element('name', 'confirm_password')
        change = driver.find_element('id', 'change_password_btn')
        form = driver.find_element('id', 'form_change_password')

        time.sleep(2)
        driver.execute_script("arguments[0].scrollIntoView(true);", form)

        # Perform actions on the form
        time.sleep(2)
        old_password_input.send_keys('123456789')
        time.sleep(2)
        new_password_input.send_keys('12345678')
        time.sleep(2)
        confirm_password_input.send_keys('12345678')
        time.sleep(2)

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

        # Submit the form
        change.click()

        success_message_locator = (By.XPATH, "//div[@class='jq-toast-wrap top-right']//div[@class='jq-toast-single jq-has-icon jq-icon-success']")
        success_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(success_message_locator))

        # Assert that the success message contains the expected text
        expected_success_text = "Successfully changed."
        assert expected_success_text in success_message.text

        time.sleep(3)
        driver.quit()

    def test_invalid_old_password(self):
        chromedriver_path = CHROMEDRIVER_PATH

        chrome_service = webdriver.chrome.service.Service(chromedriver_path)
        driver = webdriver.Chrome(service=chrome_service)
        # Navigate to the login page
        driver.get('http://127.0.0.1:8000/accounts/login/')

        email_input = driver.find_element('name', 'email')
        password_input = driver.find_element('name', 'password')
        submit_button = driver.find_element('id', 'submit')

        # Perform actions on the form
        time.sleep(2)
        email_input.send_keys('phuong@gmail.com')
        time.sleep(2)
        password_input.send_keys('12345678')
        time.sleep(2)
        

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
        self.assertEqual(driver.current_url, 'http://127.0.0.1:8000/dashboard/', 'Login succeessfully')
        success_message_locator = (By.XPATH, "//div[@class='jq-toast-wrap top-right']//div[@class='jq-toast-single jq-has-icon jq-icon-success']")
        success_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(success_message_locator))
        expected_success_text = "Login successfully."
        assert expected_success_text in success_message.text

        time.sleep(4)

        driver.get('http://127.0.0.1:8000/accounts/profile/')

        old_password_input = driver.find_element('name', 'old_password')
        new_password_input = driver.find_element('name', 'new_password')
        confirm_password_input = driver.find_element('name', 'confirm_password')
        change_button = driver.find_element('id', 'change_password_btn')
        form = driver.find_element('id', 'form_change_password')

        time.sleep(2)
        driver.execute_script("arguments[0].scrollIntoView(true);", form)

        # Perform actions on the form
        time.sleep(2)
        old_password_input.send_keys('phuong123')
        time.sleep(2)
        new_password_input.send_keys('123456789')
        time.sleep(2)
        confirm_password_input.send_keys('123456789')
        time.sleep(2)
        
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

        # Submit the form
        change_button.click()

        error_message_locator = (By.XPATH, "//div[@class='jq-toast-wrap top-right']//div[@class='jq-toast-single jq-has-icon jq-icon-error']")
        error_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(error_message_locator))

        # Assert that the error message contains the expected text
        expected_error_text = "Old password is incorrect."
        assert expected_error_text in error_message.text

        time.sleep(4)
        driver.quit()

    def test_invalid_new_password(self):
        chromedriver_path = CHROMEDRIVER_PATH

        chrome_service = webdriver.chrome.service.Service(chromedriver_path)
        driver = webdriver.Chrome(service=chrome_service)
        # Navigate to the login page
        driver.get('http://127.0.0.1:8000/accounts/login/')

        # Find the email, password, and submit elements
        email_input = driver.find_element('name', 'email')
        password_input = driver.find_element('name', 'password')
        submit_button = driver.find_element('id', 'submit')

        # Perform actions on the form
        time.sleep(2)
        email_input.send_keys('phuong@gmail.com')
        time.sleep(2)
        password_input.send_keys('12345678')
        time.sleep(2)
        

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
        self.assertEqual(driver.current_url, 'http://127.0.0.1:8000/dashboard/', 'Login succeessfully')
        success_message_locator = (By.XPATH, "//div[@class='jq-toast-wrap top-right']//div[@class='jq-toast-single jq-has-icon jq-icon-success']")
        success_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(success_message_locator))
        expected_success_text = "Login successfully."
        assert expected_success_text in success_message.text

        time.sleep(4)

        driver.get('http://127.0.0.1:8000/accounts/profile/')

        old_password_input = driver.find_element('name', 'old_password')
        new_password_input = driver.find_element('name', 'new_password')
        confirm_password_input = driver.find_element('name', 'confirm_password')
        change_button = driver.find_element('id', 'change_password_btn')
        form = driver.find_element('id', 'form_change_password')

        time.sleep(2)
        driver.execute_script("arguments[0].scrollIntoView(true);", form)

        # Perform actions on the form
        time.sleep(2)
        old_password_input.send_keys('12345678')
        time.sleep(2)
        new_password_input.send_keys('phuong123')
        time.sleep(2)
        confirm_password_input.send_keys('phuong1234')
        time.sleep(2)

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
        change_button.click()

        error_message_locator = (By.XPATH, "//div[@class='jq-toast-wrap top-right']//div[@class='jq-toast-single jq-has-icon jq-icon-error']")
        error_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(error_message_locator))

        # Assert that the error message contains the expected text
        expected_error_text = "New password and confirm password do not match."
        assert expected_error_text in error_message.text

        time.sleep(4)
        driver.quit()