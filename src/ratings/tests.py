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
class MovieRatingTest(LiveServerTestCase):
   
    def test_rate_movie_success(self):
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

        section = driver.find_element('id', 'trend')

        
        driver.execute_script("arguments[0].scrollIntoView(true);", section)


        driver.get('http://127.0.0.1:8000/movies/271404/')
        

        # Đánh giá phim
        message = driver.find_element('name', 'card')
        time.sleep(1)
        driver.execute_script("arguments[0].scrollIntoView(true);", message)
        time.sleep(1)
        rating_select = driver.find_element(By.NAME, "rating_value")  # Tìm phần tử select
        rating_select.click()
        # Chọn giá trị đánh giá (thay bằng giá trị cụ thể)
        rating_option = driver.find_element(By.XPATH, "//select[@name='rating_value']/option[@value='4']")  
        rating_option.click()
        # Sử dụng XPath của nút submit
        submit_button = driver.find_element(By.XPATH, "//form[@hx-post='/rate/movie/']") 
        submit_button.click()
        
        
        

        
        # # Kiểm tra kết quả
        success_message_locator = (By.CSS_SELECTOR, ".success.mb-2 span")
        success_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(success_message_locator))
        self.assertIn("Rating saved!", success_message.text)

        time.sleep(1)


    def test_rate_movie_fail(self):
        chromedriver_path = CHROMEDRIVER_PATH

        # Khởi tạo driver Chrome với tùy chọn Service
        chrome_service = webdriver.chrome.service.Service(chromedriver_path)
        driver = webdriver.Chrome(service=chrome_service)
        driver.get('http://127.0.0.1:8000/')
        section = driver.find_element('id', 'trend')

        
        driver.execute_script("arguments[0].scrollIntoView(true);", section)

        driver.get('http://127.0.0.1:8000/movies/271404/')
        

        # Đánh giá phim
        message = driver.find_element('name', 'card')
        time.sleep(1)
        driver.execute_script("arguments[0].scrollIntoView(true);", message)
        time.sleep(1)
        rating_select = driver.find_element(By.NAME, "rating_value")  # Tìm phần tử select
        rating_select.click()
        # Chọn giá trị đánh giá (thay bằng giá trị cụ thể)
        rating_option = driver.find_element(By.XPATH, "//select[@name='rating_value']/option[@value='2']")  
        rating_option.click()
        # Sử dụng XPath của nút submit
        submit_button = driver.find_element(By.XPATH, "//form[@hx-post='/rate/movie/']") 
        submit_button.click()
        # driver.execute_script("alert('You must login to rate this.')")
        element_to_display_message = driver.find_element(By.XPATH, "//form[@hx-post='/rate/movie/']")

        # Hiển thị thông báo lỗi
        error_message = "<span class='bg-danger text-light py-1 px-3 rounded'>You must <a href='/accounts/login'>login</a> to rate this.</div>"
        driver.execute_script("arguments[0].insertAdjacentHTML('afterend', arguments[1]);", element_to_display_message, error_message)
        

        time.sleep(1)
        driver.quit()

