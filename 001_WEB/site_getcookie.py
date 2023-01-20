from lib.get_cookie import Get_Cookie as Getcookie
import json
from datetime import datetime
import os
from pathlib import Path


COOKIE_ROOT_DIR = 'cookie'
COOKIE_SITE_LIST_DIR = 'site_list'
COOKIE_DIR = 'cookie_list'
COOKIE_EXPIRATION_MINUTE = 60*6

def old_file_delete(site_name:str , id:str) -> None:
    cookie_file = Cookie_file(site_name=site_name, id=id)
    try:
        old_file = os.path.getctime(cookie_file)
        now = datetime.now().timestamp()
        timedelta = datetime.utcfromtimestamp(now-old_file).minute
        if timedelta > COOKIE_EXPIRATION_MINUTE:
            os.remove(cookie_file)
            
            return 1
        return 0
    except FileNotFoundError:
        return 2


def Get_Cookie(**kwargs)->None:
    site_name, login_url, id, pwd, tagid, tagpwd, button_xpath=kwargs.values()
    
    GetCookie = Getcookie()
    GetCookie.login(login_url=login_url, id=id,
     password=pwd, tag_id=tagid,
      tag_pwd=tagpwd, login_button_xpath=button_xpath)
    Cookie = GetCookie.get_cookie()
    
    cookie_file = Cookie_file(site_name=site_name, id=id)
    with open(cookie_file, 'w') as f:
        json.dump(Cookie, f)

def Cookie_file(site_name:str , id:str)->str:
    cookie_file = os.path.join(COOKIE_ROOT_DIR,COOKIE_DIR,site_name+'_'+id+'.json') 
    return cookie_file

def Execute():
    path = Path(os.path.join(COOKIE_ROOT_DIR,COOKIE_SITE_LIST_DIR))
    
    file_list = os.listdir(path)
    file_list.remove('default.json')
    

    for file in file_list:
        file_path =os.path.join(path, file)
      
        with open(file_path, 'r') as f:
            site = json.load(f)
            if old_file_delete(site_name=site['site_name'], id=site['id']) != 0:
                Get_Cookie(**site)

if __name__ == '__main__':
    Execute()
