import time
from automation import *

from classes.pyautogui_class import PyautoGUI
from classes.selenium_class import Browser
from classes.slack import Slack

def main():
    try:
        print('??')
        browser = Browser()
        admin_login.main(browser.driver) # 관리자 페이지 로그인
        # admin_get_files.main(browser.driver) # 상세페이지에서 자료모으기
        # time.sleep(3)
        keaps.main()
        patent.main(browser.driver)
        admin_upload_files.main(browser.driver)

        # test.main(browser.driver)
    except Exception as e:
        print('본체에러', e)
        Slack.chat('서식상세', f'에러 종료\n{e}')

main()