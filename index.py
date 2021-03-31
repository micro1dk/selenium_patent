from automation import *

from classes.pyautogui_class import PyautoGUI
from classes.selenium_class import Browser

browser = Browser()
admin_login.main(browser.driver) # 관리자 페이지 로그인
admin_get_files.main(browser.driver) # 상세페이지에서 자료모으기 