import os
import sys
import time
import pickle
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from paths import *
from classes.selenium_class import Browser
from classes.pyautogui_class import PyautoGUI
from classes.slack import Slack

class Login(Browser):
    def __init__(self, driver):
        # super().__init__()
        self.driver = driver

    def connect_URL(self, url):
        try:
            self.visit(url)
            return True
        except Exception as e:
            return False
    
    def cookie_setting(self, path):
        try:
            cookies = pickle.load(open(path, 'rb'))
            self.visit('https://markinfo.co.kr/markinfo')
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            return True
        except Exception as e:
            return False

    def user_setting(self, path, url, username, password):
        if self.cookie_setting(path):  # 쿠키 있으면 통과
            if not self.connect_URL(url):
                self.login(path, username, password)
                self.visit(url)
            else:
                success, alert = self.exist_alert()
                if success:
                    self.accept_alert(alert)
                    self.login(path, username, password)
                    self.visit(url)
        else:  # 쿠키 없으면 로그인
            self.login(path, username, password)
            self.visit(url)

    def save_cookies(self, path):
        cookies = self.driver.get_cookies()
        pickle.dump(cookies, open(path, 'wb'))

    def login(self, path, username, password):
        # self.visit('https://markinfo.co.kr/front/nanmin/phtml/login.php')
        self.driver.find_element_by_xpath('//*[@id="id"]').send_keys(username)
        self.driver.find_element_by_xpath('//*[@id="pwd"]').send_keys(password)
        self.driver.find_element_by_xpath(
            '//*[@id="loginFrm"]/fieldset/p/button').click()
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
            raise Exception(e)

def main(driver):
    try:
        Slack.chat('서식상세', '=====================< 마크인포 관리자페이지 로그인 >=====================')
        Slack.chat('서식', '관리자페이지 로그인중')
        Admin_login = Login(driver)
        Admin_login.user_login()
        Slack.chat('서식', '관리자페이지 로그인 완료')
    except Exception as e:
        Slack.chat('서식', f'마크인포 관리자페이지 로그인 과정에서 에러')
        raise Exception(e)
