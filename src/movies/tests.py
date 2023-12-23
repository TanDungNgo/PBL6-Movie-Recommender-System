import time
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from django.conf import settings
from movies.models import Movie

# Create your tests here.
CHROMEDRIVER_PATH = settings.BASE_DIR / 'chromedriver.exe'
class MovieFindTest(LiveServerTestCase):
    def test_find_with_title(self):
        chromedriver_path = CHROMEDRIVER_PATH
        
        chrome_service = webdriver.chrome.service.Service(chromedriver_path)
        driver = webdriver.Chrome(service=chrome_service)
        # Navigate to the login page
        driver.get('http://127.0.0.1:8000/')

        search_input = driver.find_element('name', 'search')
        search_button = driver.find_element('id', 'searchButton')

        # Perform actions on the form
        search_value = 'dragonball'
        
        search_input.send_keys(search_value)
        

        # Submit the form
        search_button.click()

        self.assertEqual(driver.current_url, 'http://127.0.0.1:8000/movies/find/?search=' + search_value)
        response = self.client.get('/movies/find/?search=' + search_value)
        self.assertEqual(response.status_code, 200)
        self.assertIn('object_list', response.context)

        for movie in response.context['object_list']:
            self.assertIsInstance(movie, Movie)
        
        assert 'Find' in driver.title
        time.sleep(1)
        driver.quit()

    def test_find_with_genre(self):
        chromedriver_path = CHROMEDRIVER_PATH
        
        chrome_service = webdriver.chrome.service.Service(chromedriver_path)
        driver = webdriver.Chrome(service=chrome_service)
        # Navigate to the login page
        driver.get('http://127.0.0.1:8000/')

        search_input = driver.find_element('name', 'search')
        search_button = driver.find_element('id', 'searchButton')

        # Perform actions on the form
        search_value = 'drama'
        
        search_input.send_keys(search_value)
        

        # Submit the form
        search_button.click()

        self.assertEqual(driver.current_url, 'http://127.0.0.1:8000/movies/find/?search=' + search_value)
        assert 'Find' in driver.title
        message = 'Search results for: "' + search_value + '"'
        print(message)
        # assert message in driver.page_source

        time.sleep(1)
        driver.quit()

    def test_find_with_movie_dont_exist(self):
        chromedriver_path = CHROMEDRIVER_PATH
        
        chrome_service = webdriver.chrome.service.Service(chromedriver_path)
        driver = webdriver.Chrome(service=chrome_service)
        # Navigate to the login page
        driver.get('http://127.0.0.1:8000/')

        search_input = driver.find_element('name', 'search')
        search_button = driver.find_element('id', 'searchButton')

        # Perform actions on the form
        search_value = 'phuong'
        
        search_input.send_keys(search_value)
        
        # Submit the form
        search_button.click()

        self.assertEqual(driver.current_url, 'http://127.0.0.1:8000/movies/find/?search=' + search_value)
        assert 'Find' in driver.title
        message = 'No results found for"' + search_value + '"'
        print(message)
        # assert message in driver.page_source
        time.sleep(1)
        driver.quit()

    def test_empty_input(self):
        chromedriver_path = CHROMEDRIVER_PATH
        
        chrome_service = webdriver.chrome.service.Service(chromedriver_path)
        driver = webdriver.Chrome(service=chrome_service)
        # Navigate to the login page
        driver.get('http://127.0.0.1:8000/')

        search_input = driver.find_element('name', 'search')
        search_button = driver.find_element('id', 'searchButton')

        # Perform actions on the form
        search_value = ''
        
        search_input.send_keys(search_value)
        

        # Submit the form
        search_button.click()
        self.assertEqual(driver.current_url, 'http://127.0.0.1:8000/movies/find/?search=' + search_value)
        assert 'Find' in driver.title
        assert 'Search by typing a word or phrase in the search box at the top of this page.' in driver.page_source
        time.sleep(1)
        driver.quit()