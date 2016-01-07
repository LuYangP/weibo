from http.cookiejar import CookieJar, Cookie
from selenium import webdriver
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.support.ui import WebDriverWait
import config
import os
import pickle
import urllib.parse

def login(username, password):
    def dict_2_cookiejar(d):
        cj = CookieJar()

        for c in d:
            ck = Cookie(name=c['name'], value=urllib.parse.unquote(c['value']), domain=c['domain'], \
                    path=c['path'], \
                    secure=c['secure'], rest={'HttpOnly': c['httponly']}, \
                    version =0,    port=None,port_specified=False, \
                    domain_specified=False,domain_initial_dot=False, \
                    path_specified=True,   expires=None,   discard=True, \
                    comment=None, comment_url=None, rfc2109=False)
            cj.set_cookie(ck)

        return cj

    if os.path.exists('cookies'):
        return dict_2_cookiejar(pickle.load(open('cookies', 'rb')))

    driver = webdriver.PhantomJS(executable_path=config.PHANTOM_JS_PATH)

    driver.get('http://login.sina.com.cn')
    user = driver.find_element_by_xpath('//input[@id="username"]')
    user.send_keys(username)
    pw = driver.find_element_by_xpath('//input[@id="password"]')
    pw.send_keys(password)
    old_page = driver.find_element_by_tag_name('html')
    driver.find_element_by_xpath('//input[@class="smb_btn"]').click()
    WebDriverWait(driver, 10).until(staleness_of(old_page))

    #TODO change the login url from login.sina.com.cn to weibo.com
    old_page = driver.find_element_by_tag_name('html')
    driver.get('http://weibo.com')
    WebDriverWait(driver, 10).until(staleness_of(old_page))

    with open('cookies', 'wb') as f:
        pickle.dump(driver.get_cookies(), f)
    
    return dict_2_cookiejar(driver.get_cookies())
