from selenium import webdriver
from django.test import LiveServerTestCase

from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class LoginFormTest(LiveServerTestCase):
    def test_login_success(self):
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
        self.assertEqual(driver.current_url, 'http://127.0.0.1:8000/', 'Login succeessfully')
        assert "Home" in driver.title
        assert 'DPT Movie' in driver.page_source

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