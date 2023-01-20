from lib.get_cookie import Get_Cookie, Crawlling_Selenium
import json
from time import sleep
import os
from datetime import datetime


LOGIN_URL = 'https://signinssl.gmarket.co.kr/login/login?url=https://www.gmarket.co.kr/'
COOKIE_FILE = 'gmarket.json'
COOKIE_EXPIRATION_MINUTE = 60*6

def GetCookie():
    id = ''
    pwd = ''
    tagid = 'id'
    tagpwd= 'pwd'
    xpath = '/html/body/div[2]/div/div/form/div[3]/div[1]/div[2]/div[1]/div[3]/button'

    GetCookie = Get_Cookie()
    GetCookie.login(login_url=LOGIN_URL, id=id, password=pwd, tag_id=tagid, tag_pwd=tagpwd, login_button_xpath=xpath)
    Cookie = GetCookie.get_cookie()
    
    with open('gmarket.json', 'w') as f:
        json.dump(Cookie, f)

    return Cookie

def webpage(url, cookie):
    xpath='//*[@id="orderList"]/tr[1]/td[3]/div/ul/li/span/a'
    Get_Cookie = Crawlling_Selenium()
    Get_Cookie.cookie_login(cookie_dict=cookie, login_url=LOGIN_URL)
    Get_Cookie.web_page_load(url=url)
    Get_Cookie.button_clicked(xpath=xpath)
   

if __name__ == '__main__':
    url = 'https://myg.gmarket.co.kr'
    Cookie= GetCookie()
    with open(COOKIE_FILE, 'r') as f:
        Cookie= json.load(f)
    webpage(cookie=Cookie,url=url)
    

