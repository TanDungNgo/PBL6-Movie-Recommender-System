from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from django.contrib.staticfiles.testing import LiveServerTestCase

class MovieCreateTest(LiveServerTestCase):
    def test_create_movie_success(self):
        # Đường dẫn đến ChromeDriver
        chromedriver_path = 'D:/Download/chromedriver-win64 (2)/chromedriver-win64/chromedriver.exe'

        # Khởi tạo driver Chrome với tùy chọn Service
        chrome_service = webdriver.chrome.service.Service(chromedriver_path)
        driver = webdriver.Chrome(service=chrome_service)
        # Navigate to the login page (if login is required)
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
        
        
        driver.get('http://127.0.0.1:8000/dashboard/create/')

        # Find and interact with the form elements to create a new movie
        title_input = driver.find_element('name', 'title')
        overview_input = driver.find_element('name', 'overview')
        release_date_input = driver.find_element('name', 'release_date')
        image_input = driver.find_element('name', 'image')
        submit_button = driver.find_element('id', 'submit_button')

        time.sleep(2)
        title_input.send_keys('Sailor Moon')
        time.sleep(2)
        overview_input.send_keys('Beautiful female guardian Sailor Moon: Eternal – Movie version is an anime film released in 2021 including 2 parts based on the Dream arc in the manga Sailor Moon by author Naoko Takeuchi.')
        time.sleep(2)
        release_date_input.send_keys('10/25/2023')
        time.sleep(2)
        image_input.send_keys('D:/Đồ Án 6 (repo Trang)/PBL6-Movie-Recommender-System/src/static/movies/img/07.jpg')
        time.sleep(2)
        submit_button.click()

        self.assertEqual(driver.current_url, 'http://127.0.0.1:8000/dashboard/movie_list/', 'Create successful!')
        success_message_locator = (By.XPATH, "//div[@class='jq-toast-wrap top-right']//div[@class='jq-toast-single jq-has-icon jq-icon-success']")
        success_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(success_message_locator))
        expected_success_text = "Create successful!"
        # assert expected_success_text in success_message.text
        
        # Close the browser
        driver.quit()

    def test_create_movie_empty_title(self):
        # Đường dẫn đến ChromeDriver
        chromedriver_path = 'D:/Download/chromedriver-win64 (2)/chromedriver-win64/chromedriver.exe'

        # Khởi tạo driver Chrome với tùy chọn Service
        chrome_service = webdriver.chrome.service.Service(chromedriver_path)
        driver = webdriver.Chrome(service=chrome_service)
        # Navigate to the login page (if login is required)
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
        time.sleep(2)
        driver.get('http://127.0.0.1:8000/dashboard/create/')

        # Find and interact with the form elements to create a new movie
        title_input = driver.find_element('name', 'title')
        overview_input = driver.find_element('name', 'overview')
        release_date_input = driver.find_element('name', 'release_date')
        image_input = driver.find_element('name', 'image')
        submit_button = driver.find_element('id', 'submit_button')

        time.sleep(2)
        title_input.send_keys('')
        time.sleep(2)
        overview_input.send_keys('Beautiful female guardian Sailor Moon: Eternal – Movie version is an anime film released in 2021 including 2 parts based on the Dream arc in the manga Sailor Moon by author Naoko Takeuchi.')
        time.sleep(2)
        release_date_input.send_keys('10/25/2023')
        time.sleep(2) 
        image_input.send_keys('D:/Đồ Án 6 (repo Trang)/PBL6-Movie-Recommender-System/src/static/movies/img/07.jpg')
        time.sleep(2)

        submit_button.click()

        error_message_locator = (By.XPATH, "//div[@class='jq-toast-wrap top-right']//div[@class='jq-toast-single jq-has-icon jq-icon-error']")
        error_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(error_message_locator))

        # Assert that the error message contains the expected text
        expected_error_text = "Title is required."
        assert expected_error_text in error_message.text

        time.sleep(2)
        driver.quit()
    def test_create_movie_empty_overview(self):
        # Đường dẫn đến ChromeDriver
        chromedriver_path = 'D:/Download/chromedriver-win64 (2)/chromedriver-win64/chromedriver.exe'

        # Khởi tạo driver Chrome với tùy chọn Service
        chrome_service = webdriver.chrome.service.Service(chromedriver_path)
        driver = webdriver.Chrome(service=chrome_service)
        # Navigate to the login page (if login is required)
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
        time.sleep(2)
        driver.get('http://127.0.0.1:8000/dashboard/create/')

        # Find and interact with the form elements to create a new movie
        title_input = driver.find_element('name', 'title')
        overview_input = driver.find_element('name', 'overview')
        release_date_input = driver.find_element('name', 'release_date')
        image_input = driver.find_element('name', 'image')

        submit_button = driver.find_element('id', 'submit_button')

        time.sleep(2)
        title_input.send_keys('Avatar')
        time.sleep(2)
        overview_input.send_keys('')
        time.sleep(2)
        release_date_input.send_keys('10/25/2023')
        time.sleep(2)
        image_input.send_keys('D:/Đồ Án 6 (repo Trang)/PBL6-Movie-Recommender-System/src/static/movies/img/07.jpg')

        time.sleep(2)


        submit_button.click()

        error_message_locator = (By.XPATH, "//div[@class='jq-toast-wrap top-right']//div[@class='jq-toast-single jq-has-icon jq-icon-error']")
        error_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(error_message_locator))

        # Assert that the error message contains the expected text
        expected_error_text = "Overview is required."
        assert expected_error_text in error_message.text

        time.sleep(2)
        driver.quit()
    
    def test_create_movie_empty_release_date(self):
        # Đường dẫn đến ChromeDriver
        chromedriver_path = 'D:/Download/chromedriver-win64 (2)/chromedriver-win64/chromedriver.exe'

        # Khởi tạo driver Chrome với tùy chọn Service
        chrome_service = webdriver.chrome.service.Service(chromedriver_path)
        driver = webdriver.Chrome(service=chrome_service)
        # Navigate to the login page (if login is required)
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
        time.sleep(2)
        driver.get('http://127.0.0.1:8000/dashboard/create/')

        # Find and interact with the form elements to create a new movie
        title_input = driver.find_element('name', 'title')
        overview_input = driver.find_element('name', 'overview')
        release_date_input = driver.find_element('name', 'release_date')
        image_input = driver.find_element('name', 'image')

        submit_button = driver.find_element('id', 'submit_button')

        time.sleep(2)
        title_input.send_keys('Avatar')
        time.sleep(2)
        overview_input.send_keys('A paraplegic Marine dispatched to the moon Pandora on a unique mission becomes torn between following his orders and protecting the world he feels is his home.')
        time.sleep(2)
        release_date_input.send_keys('')
        time.sleep(2)
        image_input.send_keys('D:/Đồ Án 6 (repo Trang)/PBL6-Movie-Recommender-System/src/static/movies/img/07.jpg')

        time.sleep(2)


        submit_button.click()

        error_message_locator = (By.XPATH, "//div[@class='jq-toast-wrap top-right']//div[@class='jq-toast-single jq-has-icon jq-icon-error']")
        error_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(error_message_locator))

        # Assert that the error message contains the expected text
        expected_error_text = "Release Date is required."
        assert expected_error_text in error_message.text

        time.sleep(2)
        driver.quit()

    def test_create_movie_wrong_format_release_date(self):
        # Đường dẫn đến ChromeDriver
        chromedriver_path = 'D:/Download/chromedriver-win64 (2)/chromedriver-win64/chromedriver.exe'

        # Khởi tạo driver Chrome với tùy chọn Service
        chrome_service = webdriver.chrome.service.Service(chromedriver_path)
        driver = webdriver.Chrome(service=chrome_service)
        # Navigate to the login page (if login is required)
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
        time.sleep(2)
        driver.get('http://127.0.0.1:8000/dashboard/create/')

        # Find and interact with the form elements to create a new movie
        title_input = driver.find_element('name', 'title')
        overview_input = driver.find_element('name', 'overview')
        release_date_input = driver.find_element('name', 'release_date')
        image_input = driver.find_element('name', 'image')

        submit_button = driver.find_element('id', 'submit_button')

        time.sleep(2)
        title_input.send_keys('Avatar')
        time.sleep(2)
        overview_input.send_keys('A paraplegic Marine dispatched to the moon Pandora on a unique mission becomes torn between following his orders and protecting the world he feels is his home.')
        time.sleep(2)
        release_date_input.send_keys('23/20/2023')
        time.sleep(2)
        image_input.send_keys('D:/Đồ Án 6 (repo Trang)/PBL6-Movie-Recommender-System/src/static/movies/img/07.jpg')

        time.sleep(2)


        submit_button.click()

        error_message_locator = (By.XPATH, "//div[@class='jq-toast-wrap top-right']//div[@class='jq-toast-single jq-has-icon jq-icon-error']")
        error_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(error_message_locator))

        # Assert that the error message contains the expected text
        expected_error_text = "Invalid date format. Please use MM/DD/YYYY format."
        assert expected_error_text in error_message.text
        

        time.sleep(2)
        driver.quit()

