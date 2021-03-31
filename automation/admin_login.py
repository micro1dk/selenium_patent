import os
import sys
import time
import json
import pickle
import shutil
import getpass
from datetime import datetime, timedelta, date
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from classes.pyautogui_class import PyautoGUI
from classes.selenium_class import Browser

from paths import *

class Login(PyautoGUI):
  def __init__(self, driver):
    # super().__init__()
    self.driver = driver
  
  def connect_URL(driver, url):
    try:
      driver.get(url)
      return True
    except Exception as e:
      return False

  def cookie_setting(self, path):
    try:
      cookies = pickle.load(open(path, 'rb'))
      self.driver.get('https://markinfo.co.kr/markinfo')
      for cookie in cookies:
        self.driver.add_cookie(cookie)
      return True
    except Exception as e:
      return False
  
  def user_setting(self, path, url, username, password):
    if self.cookie_setting(path): # 쿠키 있으면 통과
      print('있음')
      if not self.connect_URL(url):
        # print('연결안됨')
        # self.login(path, username, password)
        self.driver.get(url)
      else:
        print('연결됨')
        success, alert = self.exist_alert()
        if success:
          self.accept_alert(alert)
          self.login(path, username, password)
          self.driver.get(url)
        # else:
    else: # 쿠키 없으면 로그인
      print('업음')
      self.login(path, username, password)
      self.driver.get(url)
  
  def save_cookies(self, path):
    cookies = self.driver.get_cookies()
    pickle.dump(cookies, open(path, 'wb'))

  def login(self, path, username, password):
    self.driver.get('https://markinfo.co.kr/front/nanmin/phtml/login.php')
    self.driver.find_element_by_xpath('//*[@id="id"]').send_keys(username)
    self.driver.find_element_by_xpath('//*[@id="pwd"]').send_keys(password)
    self.driver.find_element_by_xpath('//*[@id="loginFrm"]/fieldset/p/button').click()
    self.save_cookies(path)
  
  

  def user_login(self):
    """
    로그인 메인 메서드
    """
    try:
      self.user_setting(
        path=COOKIE_PATH,
        url='https://markinfo.co.kr/front/nanmin/phtml/list.php?code=doc&link_page=reply',
        username='mycampground001@gmail.com',
        password='2964391a@'
      )
    except Exception as e:
      print(f'로그인 과정에서 에러\n{e}')


def main(driver):
  Admin_login = Login(driver)
  Admin_login.user_login()