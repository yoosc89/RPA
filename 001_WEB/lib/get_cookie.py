from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By

CHROME_DIR = '/Users/yuseungcheol/Desktop/project/test/chromedriver'
COOKIE_FILE = 'cookie.json'
COOKIE_EXPIRATION_MINUTE = 60*6


class Get_Cookie:
    def __init__(self) -> None:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(CHROME_DIR, options=options)

    def login(self, login_url: str, 
    id: str, password: str, tag_id: str, 
    tag_pwd: str, login_button_xpath: str) -> None:
        self.driver.get(login_url)
        self.driver.implicitly_wait(5)
        self.driver.find_element(By.ID, tag_id).send_keys(id)
        self.driver.find_element(By.ID, tag_pwd).send_keys(password)
        self.driver.find_element(
            By.XPATH, login_button_xpath).click()
        self.driver.implicitly_wait(5)

    def get_cookie(self)-> dict:
        _cookie = self.driver.get_cookies()
        cookie_dict = {}
        for cookie in _cookie:
            cookie_dict[cookie['name']] = cookie['value']
        return cookie_dict

class Crawlling_Selenium:
    def __init__(self) -> None:
        options = webdriver.ChromeOptions()
        #options.add_argument('--headless')
        #options.add_argument('--disable-gpu')

        self.driver = webdriver.Chrome(CHROME_DIR, options=options)
    
    
    def cookie_login(self, cookie_dict:dict, login_url:str)->None:
        self.driver.delete_all_cookies()
        self.driver.get(url=login_url)
        for name, value in cookie_dict.items():
            self.driver.add_cookie({'name':name,'value':value})
        self.driver.refresh()
        
    def web_page_load(self, url:str)->None:
        self.driver.get(url=url)
        

    def button_clicked(self, xpath:str)->None:
        self.driver.find_element(By.XPATH, xpath).click()
        

    def text_field(self, By:By, by_value:str, text:str):
        self.driver.find_element(By, by_value).send_keys(text)
    
    def Crawlling(self, By:By, by_value:str)->list:
        data = self.driver.find_elements(By,by_value)
        return data
        
