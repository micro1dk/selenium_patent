import os
import sys
import time
import shutil
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from paths import *
from classes.selenium_class import Browser
from classes.pyautogui_class import PyautoGUI

class Test(Browser):
    def __init__(self, driver):
        self.driver = driver
    
    def script(self):
        self.visit('https://markinfo.co.kr/front/nanmin/phtml/view.php?code=doc&link_page=patent_info2&accept_number=20210413_0013')
        if self.exist_element('xpath', '/html/body/div[2]/div/div[3]/div/div[2]/div[1]/table/tbody/tr[3]/td[2]/div[4]'):
            elmnt = self.driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/div/div[2]/div[1]/table/tbody/tr[3]/td[2]/div[4]')
            if elmnt.text == '출원완료보고':
                elmnt.click()
                self.wait_new_window(2, 0.5)
                self.switch_windows(2)
                self.click('xpath', '/html/body/div[1]/div[2]/div[1]/div/button[1]')
                alert = self.wait_alert()
                self.accept_alert(alert)
                time.sleep(0.5)
                alert = self.wait_alert()
                self.accept_alert(alert)
                # self.driver.close()
                self.switch_windows(1)
        else:
            print('없다는데')

def main(driver):
    test = Test(driver)
    test.script()
    time.sleep(50)