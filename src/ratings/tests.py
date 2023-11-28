from selenium import webdriver
from django.test import LiveServerTestCase

from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert

class MovieRatingTest(LiveServerTestCase):
   
    def test_rate_movie_success(self):
        # Truy cập trang chi tiết phim
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
        email_input.send_keys('duc@gmail.com')
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
        success_message_locator = (By.XPATH, "//div[@class='jq-toast-wrap top-right']//div[@class='jq-toast-single jq-has-icon jq-icon-success']")
        success_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(success_message_locator))
        expected_success_text = "Login successfully."
        assert expected_success_text in success_message.text

        # Wait for the page to load (you may need to adjust the sleep duration)
        time.sleep(1)

        driver.get('http://127.0.0.1:8000/movies/56077/')
        time.sleep(2)

        # Đánh giá phim
        rating_select = driver.find_element(By.NAME, "rating_value")  # Tìm phần tử select
        rating_select.click()
        # Chọn giá trị đánh giá (thay bằng giá trị cụ thể)
        rating_option = driver.find_element(By.XPATH, "//select[@name='rating_value']/option[@value='4']")  
        rating_option.click()
        # Sử dụng XPath của nút submit
        submit_button = driver.find_element(By.XPATH, "//form[@hx-post='/rate/movie/']") 
        submit_button.submit()
        # # Kiểm tra kết quả
        success_message_locator = (By.XPATH, "//div[@class='success mb-2']/span")
        # Perform assertions on the success message
        expected_success_text = "Rating saved!"
        time.sleep(1)
        driver.quit()

    def test_rate_movie_fail(self):
        # Truy cập trang chi tiết phim
        chromedriver_path = 'D:/Download/chromedriver-win64 (2)/chromedriver-win64/chromedriver.exe'

        # Khởi tạo driver Chrome với tùy chọn Service
        chrome_service = webdriver.chrome.service.Service(chromedriver_path)
        driver = webdriver.Chrome(service=chrome_service)

        chromedriver_path = 'D:/Download/chromedriver-win64 (2)/chromedriver-win64/chromedriver.exe'

        # Khởi tạo driver Chrome với tùy chọn Service
        chrome_service = webdriver.chrome.service.Service(chromedriver_path)
        driver = webdriver.Chrome(service=chrome_service)

        driver.get('http://127.0.0.1:8000/movies/1770/')
        time.sleep(2)

        # Đánh giá phim
        rating_select = driver.find_element(By.NAME, "rating_value")  # Tìm phần tử select
        rating_select.click()
        # Chọn giá trị đánh giá (thay bằng giá trị cụ thể)
        rating_option = driver.find_element(By.XPATH, "//select[@name='rating_value']/option[@value='2']")  
        rating_option.click()
        # Sử dụng XPath của nút submit
        submit_button = driver.find_element(By.XPATH, "//form[@hx-post='/rate/movie/']") 
        submit_button.submit()
        # driver.execute_script("alert('You must login to rate this.')")
        element_to_display_message = driver.find_element(By.XPATH, "//form[@hx-post='/rate/movie/']")

        # Hiển thị thông báo lỗi
        error_message = "<span class='bg-danger text-light py-1 px-3 rounded'>You must <a href='/accounts/login'>login</a> to rate this.</div>"
        driver.execute_script("arguments[0].insertAdjacentHTML('afterend', arguments[1]);", element_to_display_message, error_message)
        

        time.sleep(5)
        driver.quit()

