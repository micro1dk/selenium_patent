import time
import os
from automation import *

from classes.selenium_class import Browser

browser = Browser()

admin_login.main(browser.driver)

browser.visit('https://markinfo.co.kr/front/nanmin/phtml/list.php?code=doc&link_page=application')
browser.click('xpath', '//*[@id="in_charge_statistics"]/table/tbody/tr[2]/td[3]/a[1]')

browser.click('xpath', '//*[@id="table-view"]/tbody/tr[5]/td[4]/span[2]/a')

browser.wait_new_window(2, 0.1)
browser.switch_windows(2)

browser.click('xpath', '//*[@id="btn_add_file_77793"]')
browser.type_keys('xpath', '//*[@id="input_imgs_77793"]', f'{os.getcwd()}/Files/20210511/20210322_0047/1-30.pdf')
time.sleep(1)
browser.click('xpath', '//*[@id="upload_zone_77793"]/button')
time.sleep(1)


alert = browser.wait_alert()
browser.accept_alert(alert)

f = open('test1.html', 'w', encoding='utf-8')
f.write(browser.driver.page_source)

time.sleep(0.21)


f = open('test2.html', 'w', encoding='utf-8')
f.write(browser.driver.page_source)

time.sleep(0.21)

browser.click('xpath', '/html/body/div[8]/div[7]/button[2]')

# browser.driver.refresh()

browser.click('xpath', '/html/body/div[2]/div/div[3]/div/div[2]/div[2]/ul[1]/li[2]/a')

# time.sleep(1)

# browser.driver.close()

# browser.switch_windows(1)
# browser.click('xpath', '//*[@id="table-view"]/tbody/tr[6]/td[4]/span[2]/a')
