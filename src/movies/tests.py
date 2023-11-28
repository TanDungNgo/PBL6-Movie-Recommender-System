import time
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Create your tests here.
class MovieFindTest(LiveServerTestCase):
    def test_find_with_title(self):
        chromedriver_path = 'E:/PBL6/PBL6-Movie-Recommender-System/src/chromedriver.exe'
        
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
        
        driver.get('http://127.0.0.1:8000')

        time.sleep(2)

        search_input = driver.find_element('name', 'search')
        search_button = driver.find_element('id', 'searchButton')

        # Perform actions on the form
        time.sleep(2)
        search_input.send_keys('Terkel in Trouble')
        time.sleep(2)

        # Submit the form
        search_button.click()

        title_url = driver.find_elements('id', 'title')
        title_url[0].click()

        time.sleep(5)
        driver.quit()
    def test_find_with_genre(self):
        chromedriver_path = 'E:/PBL6/PBL6-Movie-Recommender-System/src/chromedriver.exe'
        
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
        
        driver.get('http://127.0.0.1:8000')

        time.sleep(2)

        search_input = driver.find_element('name', 'search')
        search_button = driver.find_element('id', 'searchButton')

        # Perform actions on the form
        time.sleep(2)
        search_input.send_keys('drama')
        time.sleep(2)

        # Submit the form
        search_button.click()

        title_url = driver.find_elements('id', 'title')
        title_url[1].click()

        time.sleep(5)
        driver.quit()

    def test_find_with_movie_dont_exist(self):
        chromedriver_path = 'E:/PBL6/PBL6-Movie-Recommender-System/src/chromedriver.exe'
        
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
        
        driver.get('http://127.0.0.1:8000')

        time.sleep(2)

        search_input = driver.find_element('name', 'search')
        search_button = driver.find_element('id', 'searchButton')

        # Perform actions on the form
        time.sleep(2)
        search_input.send_keys('Phuong')
        time.sleep(2)

        # Submit the form
        search_button.click()

        time.sleep(5)
        driver.quit()
