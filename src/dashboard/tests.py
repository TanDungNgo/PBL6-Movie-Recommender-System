from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from django.conf import settings
from django.contrib.staticfiles.testing import LiveServerTestCase
CHROMEDRIVER_PATH = settings.BASE_DIR / 'chromedriver.exe'
class MovieCreateTest(LiveServerTestCase):
    def test_create_movie_success(self):
        # Đường dẫn đến ChromeDriver
        
        # Đường dẫn đến ChromeDriver
        chromedriver_path = CHROMEDRIVER_PATH

        # Khởi tạo driver Chrome với tùy chọn Service
        chrome_service = webdriver.chrome.service.Service(chromedriver_path)
        driver = webdriver.Chrome(service=chrome_service)
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
        poster_path_input = driver.find_element('name', 'poster_path')
        submit_button = driver.find_element('id', 'submit_button')

        time.sleep(2)
        title_input.send_keys('Sailor Moon ')
        time.sleep(2)
        overview_input.send_keys('Beautiful female guardian Sailor Moon: Eternal – Movie version is an anime film released in 2021 including 2 parts based on the Dream arc in the manga Sailor Moon by author Naoko Takeuchi.')
        time.sleep(2)
        release_date_input.send_keys('10/25/2023')
        time.sleep(2)
        poster_path_input.send_keys('https://imaginaire.com/en/images/SAILOR-MOON-FABRIC-POSTER-SAILOR-MOON-29-5-X-42__0699858777174-Z.JPG')
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
        chromedriver_path = CHROMEDRIVER_PATH

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
        poster_path_input = driver.find_element('name', 'poster_path')
        submit_button = driver.find_element('id', 'submit_button')

        time.sleep(2)
        title_input.send_keys('')
        time.sleep(2)
        overview_input.send_keys('Beautiful female guardian Sailor Moon: Eternal – Movie version is an anime film released in 2021 including 2 parts based on the Dream arc in the manga Sailor Moon by author Naoko Takeuchi.')
        time.sleep(2)
        release_date_input.send_keys('10/25/2023')
        time.sleep(2) 
        poster_path_input.send_keys('https://imaginaire.com/en/images/SAILOR-MOON-FABRIC-POSTER-SAILOR-MOON-29-5-X-42__0699858777174-Z.JPG')
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
        chromedriver_path = CHROMEDRIVER_PATH

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
        poster_path_input = driver.find_element('name', 'poster_path')

        submit_button = driver.find_element('id', 'submit_button')

        time.sleep(2)
        title_input.send_keys('Avatar')
        time.sleep(2)
        overview_input.send_keys('')
        time.sleep(2)
        release_date_input.send_keys('10/25/2023')
        time.sleep(2)
        poster_path_input.send_keys('https://upload.wikimedia.org/wikipedia/vi/b/b0/Avatar-Teaser-Poster.jpg')

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
        chromedriver_path = CHROMEDRIVER_PATH

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
        poster_path_input = driver.find_element('name', 'poster_path')

        submit_button = driver.find_element('id', 'submit_button')

        time.sleep(2)
        title_input.send_keys('Avatar')
        time.sleep(2)
        overview_input.send_keys('A paraplegic Marine dispatched to the moon Pandora on a unique mission becomes torn between following his orders and protecting the world he feels is his home.')
        time.sleep(2)
        release_date_input.send_keys('')
        time.sleep(2)
        poster_path_input.send_keys('https://upload.wikimedia.org/wikipedia/vi/b/b0/Avatar-Teaser-Poster.jpg')

        time.sleep(2)


        submit_button.click()

        error_message_locator = (By.XPATH, "//div[@class='jq-toast-wrap top-right']//div[@class='jq-toast-single jq-has-icon jq-icon-error']")
        error_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(error_message_locator))

        # Assert that the error message contains the expected text
        expected_error_text = "Release Date is required."
        assert expected_error_text in error_message.text

        time.sleep(2)
        driver.quit()

    def test_create_movie_empty_poster_path(self):
        chromedriver_path = CHROMEDRIVER_PATH

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
        poster_path_input = driver.find_element('name', 'poster_path')

        submit_button = driver.find_element('id', 'submit_button')

        time.sleep(2)
        title_input.send_keys('Avatar')
        time.sleep(2)
        overview_input.send_keys('A paraplegic Marine dispatched to the moon Pandora on a unique mission becomes torn between following his orders and protecting the world he feels is his home.')
        time.sleep(2)
        release_date_input.send_keys('10/25/2023')
        time.sleep(2)
        poster_path_input.send_keys('')

        time.sleep(2)

        submit_button.click()

        error_message_locator = (By.XPATH, "//div[@class='jq-toast-wrap top-right']//div[@class='jq-toast-single jq-has-icon jq-icon-error']")
        error_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(error_message_locator))

        # Assert that the error message contains the expected text
        expected_error_text = "Poster path is required."
        assert expected_error_text in error_message.text

        time.sleep(2)
        driver.quit()

    def test_create_movie_wrong_format_release_date(self):
        chromedriver_path = CHROMEDRIVER_PATH

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
        poster_path_input = driver.find_element('name', 'poster_path')

        submit_button = driver.find_element('id', 'submit_button')

        time.sleep(2)
        title_input.send_keys('Avatar')
        time.sleep(2)
        overview_input.send_keys('A paraplegic Marine dispatched to the moon Pandora on a unique mission becomes torn between following his orders and protecting the world he feels is his home.')
        time.sleep(2)
        release_date_input.send_keys('23/20/2023')
        time.sleep(2)
        poster_path_input.send_keys('https://upload.wikimedia.org/wikipedia/vi/b/b0/Avatar-Teaser-Poster.jpg')

        time.sleep(2)


        submit_button.click()

        error_message_locator = (By.XPATH, "//div[@class='jq-toast-wrap top-right']//div[@class='jq-toast-single jq-has-icon jq-icon-error']")
        error_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(error_message_locator))

        # Assert that the error message contains the expected text
        expected_error_text = "Invalid date format. Please use MM/DD/YYYY format."
        assert expected_error_text in error_message.text
        

        time.sleep(2)
        driver.quit()


class MovieDeleteTest(LiveServerTestCase):
    def test_delete_movie_success(self):
        # Đường dẫn đến ChromeDriver
        chromedriver_path = CHROMEDRIVER_PATH

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
        
        
        driver.get('http://127.0.0.1:8000/dashboard/movie_list/')

        # Đợi cho trang danh sách phim được tải (bạn có thể điều chỉnh thời gian chờ)
        time.sleep(2)

        delete_buttons = driver.find_elements(By.CLASS_NAME, 'delete-movie')
        if delete_buttons:
            delete_buttons[0].click()  # Click the first delete button
            time.sleep(4)  # Wait for the SweetAlert dialog to appear

            # Confirm the deletion in the SweetAlert dialog
            confirm_button = driver.find_element(By.XPATH, "//button[contains(@class, 'swal2-confirm')]")
            confirm_button.click()  # Click 'Yes' to confirm deletion

            # [Add logic to verify successful deletion here...]

        else:
            print("No delete button found")
        
        self.assertEqual(driver.current_url, 'http://127.0.0.1:8000/dashboard/movie_list/', 'Movie deleted successfully!')
        success_message_locator = (By.XPATH, "//div[@class='jq-toast-wrap top-right']//div[@class='jq-toast-single jq-has-icon jq-icon-success']")
        success_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(success_message_locator))
        expected_success_text = "Movie deleted successfully!"
        assert expected_success_text in success_message.text

        # Wait for the page to load (you may need to adjust the sleep duration)
        time.sleep(4)

        driver.quit()
from selenium.common.exceptions import NoSuchElementException, TimeoutException
class MovieDeleteTest(LiveServerTestCase):
    def test_delete_movie_faild(self):
        # Đường dẫn đến ChromeDriver
        chromedriver_path = CHROMEDRIVER_PATH

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
        
        
        driver.get('http://127.0.0.1:8000/dashboard/movie_list/')

        # Đợi cho trang danh sách phim được tải (bạn có thể điều chỉnh thời gian chờ)
        time.sleep(2)

        delete_buttons = driver.find_elements(By.CLASS_NAME, 'delete-movie')
        if delete_buttons:
            delete_buttons[0].click()  # Click the first delete button
            time.sleep(2)  # Wait for the SweetAlert dialog to appear

            # Locate the 'No' button in the SweetAlert dialog
            no_button = driver.find_element(By.XPATH, "//button[contains(@class, 'swal2-cancel')]")
            no_button.click()  # Click 'No' to cancel deletion

            # [Add logic to verify that the movie was not deleted here...]

        else:
            print("No delete button found")

        # Verify that the current URL is still the movie list page, indicating no redirection occurred
        self.assertEqual(driver.current_url, 'http://127.0.0.1:8000/dashboard/movie_list/', 'Still on movie list page after canceling deletion')

        # Optionally, verify that the success message for deletion did NOT appear
        try:
            success_message_locator = (By.XPATH, "//div[@class='jq-toast-wrap top-right']//div[@class='jq-toast-single jq-has-icon jq-icon-success']")
            success_message = WebDriverWait(driver, 4).until(EC.visibility_of_element_located(success_message_locator))
            assert False, "Deletion success message appeared when it shouldn't have"
        except TimeoutException:
            # If the success message did not appear, this is the expected behavior
            pass
        # Wait for the page to load (you may need to adjust the sleep duration)
        time.sleep(4)

        driver.quit()

class MovieEditTest(LiveServerTestCase):
    def test_edit_movie_success(self):
        chromedriver_path = CHROMEDRIVER_PATH

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

        # Wait for the page to load (you may need to adjust the sleep duration)
        time.sleep(4)

        driver.get('http://127.0.0.1:8000/dashboard/movie_list/')

        time.sleep(2)

        edit_button = driver.find_elements('name', 'edit_btn')
        if edit_button:
            edit_button[1].click()  # Click the first delete button
            time.sleep(2)  # Wait for the SweetAlert dialog to appear
        else:
            print("No edit button found")

        # Find and interact with the form elements to create a new movie
        title_input = driver.find_element('name', 'title')
        overview_input = driver.find_element('name', 'overview')
        release_date_input = driver.find_element('name', 'release_date')
        poster_path_input = driver.find_element('name', 'poster_path')
        submit_button = driver.find_element('id', 'submit_button')

        time.sleep(2)
        poster_path_input.clear()
        time.sleep(2)
        poster_path_input.send_keys('https://m.media-amazon.com/images/I/61R-TCEvkBS._AC_UF894,1000_QL80_.jpg')
        time.sleep(2)

        driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        time.sleep(2)

        submit_button.click()

        self.assertEqual(driver.current_url, 'http://127.0.0.1:8000/dashboard/movie_list/', 'Update successful!')
        success_message_locator = (By.XPATH, "//div[@class='jq-toast-wrap top-right']//div[@class='jq-toast-single jq-has-icon jq-icon-success']")
        success_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(success_message_locator))
        expected_success_text = "Update successful!"
        assert expected_success_text in success_message.text
        
        time.sleep(4)
        driver.quit()

    def test_edit_movie_empty_title(self):
        chromedriver_path = CHROMEDRIVER_PATH

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

        # Wait for the page to load (you may need to adjust the sleep duration)
        time.sleep(4)
        
        driver.get('http://127.0.0.1:8000/dashboard/movie_list/')

        time.sleep(2)

        edit_button = driver.find_elements('name', 'edit_btn')
        if edit_button:
            edit_button[1].click()  # Click the first delete button
            time.sleep(2)  # Wait for the SweetAlert dialog to appear
        else:
            print("No edit button found")


        # Find and interact with the form elements to create a new movie
        title_input = driver.find_element('name', 'title')
        overview_input = driver.find_element('name', 'overview')
        release_date_input = driver.find_element('name', 'release_date')
        poster_path_input = driver.find_element('name', 'poster_path')
        submit_button = driver.find_element('id', 'submit_button')

        time.sleep(2)
        title_input.clear()
        time.sleep(2)
        
        driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        time.sleep(2)

        submit_button.click()

        error_message_locator = (By.XPATH, "//div[@class='jq-toast-wrap top-right']//div[@class='jq-toast-single jq-has-icon jq-icon-error']")
        error_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(error_message_locator))

        # Assert that the error message contains the expected text
        expected_error_text = "Title is required."
        assert expected_error_text in error_message.text

        time.sleep(4)
        driver.quit()

    def test_edit_movie_empty_overview(self):
        chromedriver_path = CHROMEDRIVER_PATH

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

        # Wait for the page to load (you may need to adjust the sleep duration)
        time.sleep(4)
        
        driver.get('http://127.0.0.1:8000/dashboard/movie_list/')

        time.sleep(2)

        edit_button = driver.find_elements('name', 'edit_btn')
        if edit_button:
            edit_button[1].click()  # Click the first delete button
            time.sleep(2)  # Wait for the SweetAlert dialog to appear
        else:
            print("No edit button found")


        # Find and interact with the form elements to create a new movie
        title_input = driver.find_element('name', 'title')
        overview_input = driver.find_element('name', 'overview')
        release_date_input = driver.find_element('name', 'release_date')
        poster_path_input = driver.find_element('name', 'poster_path')
        submit_button = driver.find_element('id', 'submit_button')

        time.sleep(2)
        overview_input.clear()
        time.sleep(2)

        driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        time.sleep(2)

        submit_button.click()

        error_message_locator = (By.XPATH, "//div[@class='jq-toast-wrap top-right']//div[@class='jq-toast-single jq-has-icon jq-icon-error']")
        error_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(error_message_locator))

        # Assert that the error message contains the expected text
        expected_error_text = "Overview is required."
        assert expected_error_text in error_message.text

        time.sleep(4)
        driver.quit()
    
    def test_edit_movie_empty_release_date(self):
        chromedriver_path = CHROMEDRIVER_PATH

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

        # Wait for the page to load (you may need to adjust the sleep duration)
        time.sleep(4)
        
        driver.get('http://127.0.0.1:8000/dashboard/movie_list/')

        time.sleep(2)

        edit_button = driver.find_elements('name', 'edit_btn')
        if edit_button:
            edit_button[1].click()  # Click the first delete button
            time.sleep(2)  # Wait for the SweetAlert dialog to appear
        else:
            print("No edit button found")


        # Find and interact with the form elements to create a new movie
        title_input = driver.find_element('name', 'title')
        overview_input = driver.find_element('name', 'overview')
        release_date_input = driver.find_element('name', 'release_date')
        poster_path_input = driver.find_element('name', 'poster_path')
        submit_button = driver.find_element('id', 'submit_button')

        time.sleep(2)
        release_date_input.clear()
        time.sleep(2)

        driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        time.sleep(2)

        submit_button.click()

        error_message_locator = (By.XPATH, "//div[@class='jq-toast-wrap top-right']//div[@class='jq-toast-single jq-has-icon jq-icon-error']")
        error_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(error_message_locator))

        # Assert that the error message contains the expected text
        expected_error_text = "Release Date is required."
        assert expected_error_text in error_message.text

        time.sleep(4)
        driver.quit()

    def test_edit_movie_empty_poster_path(self):
        chromedriver_path = CHROMEDRIVER_PATH

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

        # Wait for the page to load (you may need to adjust the sleep duration)
        time.sleep(4)
        
        driver.get('http://127.0.0.1:8000/dashboard/movie_list/')

        time.sleep(2)

        edit_button = driver.find_elements('name', 'edit_btn')
        if edit_button:
            edit_button[1].click()  # Click the first delete button
            time.sleep(2)  # Wait for the SweetAlert dialog to appear
        else:
            print("No edit button found")

        # Find and interact with the form elements to create a new movie
        title_input = driver.find_element('name', 'title')
        overview_input = driver.find_element('name', 'overview')
        release_date_input = driver.find_element('name', 'release_date')
        poster_path_input = driver.find_element('name', 'poster_path')
        submit_button = driver.find_element('id', 'submit_button')

        time.sleep(2)
        poster_path_input.clear()
        time.sleep(2)

        driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        time.sleep(2)

        submit_button.click()

        error_message_locator = (By.XPATH, "//div[@class='jq-toast-wrap top-right']//div[@class='jq-toast-single jq-has-icon jq-icon-error']")
        error_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(error_message_locator))

        # Assert that the error message contains the expected text
        expected_error_text = "Poster path is required."
        assert expected_error_text in error_message.text

        time.sleep(4)
        driver.quit()

    def test_edit_movie_wrong_format_release_date(self):
        chromedriver_path = CHROMEDRIVER_PATH

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

        # Wait for the page to load (you may need to adjust the sleep duration)
        time.sleep(4)
        
        driver.get('http://127.0.0.1:8000/dashboard/movie_list/')

        time.sleep(2)

        edit_button = driver.find_elements('name', 'edit_btn')
        if edit_button:
            edit_button[1].click()  # Click the first delete button
            time.sleep(2)  # Wait for the SweetAlert dialog to appear
        else:
            print("No edit button found")


        # Find and interact with the form elements to create a new movie
        title_input = driver.find_element('name', 'title')
        overview_input = driver.find_element('name', 'overview')
        release_date_input = driver.find_element('name', 'release_date')
        poster_path_input = driver.find_element('name', 'poster_path')
        submit_button = driver.find_element('id', 'submit_button')

        time.sleep(2)
        release_date_input.clear()
        time.sleep(2)
        release_date_input.send_keys('23/20/2023')
        time.sleep(2)

        driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        time.sleep(2)

        submit_button.click()

        error_message_locator = (By.XPATH, "//div[@class='jq-toast-wrap top-right']//div[@class='jq-toast-single jq-has-icon jq-icon-error']")
        error_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(error_message_locator))

        # Assert that the error message contains the expected text
        expected_error_text = "Invalid date format. Please use MM/DD/YYYY format."
        assert expected_error_text in error_message.text

        time.sleep(4)
        driver.quit()