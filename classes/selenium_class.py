import os
import sys
import time
import json

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from paths import CHROMEDRIVER_PATH ,DOWNLOAD_PATH, WINDOW_SIZE # 다운로드 경로를 불러옴

chrome_options = Options()
# chrome_options.add_argument( '--headless' )     # 크롬창이 열리지 않음
chrome_options.add_argument( '--no-sandbox' )   # GUI를 사용할 수 없는 환경에서 설정, linux, docker 등
chrome_options.add_argument( '--disable-gpu' )  # GUI를 사용할 수 없는 환경에서 설정, linux, docker 등
chrome_options.add_argument(f'--window-size={ WINDOW_SIZE }')
chrome_options.add_argument('Content-Type=application/json; charset=utf-8')
chrome_options.add_experimental_option("prefs", {
  "download.default_directory": f'{DOWNLOAD_PATH}\\temp',
  "download.prompt_for_download": False,
  "download.directory_upgrade": True,
  "safebrowsing.enabled": True,
  "printing.print_preview_sticky_settings.appState": json.dumps({
    "recentDestinations": [{
      "id": "Save as PDF",
      "origin": "local",
      "account": "",
    }],
    "selectedDestinationId": "Save as PDF",
    "version": 2
  })
})

class Browser:
  def __init__(self):
    self.driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)

  def visit(self, url):
    self.driver.get(url)
  
  def str_to_by(self, string):
    if string == 'xpath':
      return By.XPATH
    elif string == 'id':
      return By.ID
    elif string == 'class':
      return By.CLASS_NAME
    elif string == 'tag':
      return By.TAG_NAME

  def click(self, by, selector, timeout=7):
    self.wait_element_visible(self.str_to_by(by), selector, timeout)
    if by == By.XPATH:
      self.driver.find_element(self.str_to_by(by), selector).click()

  def type_keys(self, by, selector, string):
    self.driver.find_element(self.str_to_by(by), selector).send_keys(string)

  ### alert 함수
  def wait_alert(self):
    t = 0
    while True:
      success, elem = self.exist_alert()
      if success:
        return elem
      time.sleep(0.3)
      t += 0.3
      if t >= 3:
        raise Exception('알러트없음')
      
  def exist_alert(self):
    try:
      alert = self.driver.switch_to.alert
      return True, alert
    except Exception as e:
      return False, None

  def accept_alert(self, alert):
    alert.accept()

  ### 로딩함수
  def wait_element_visible(self, by, selector, timeout=7):
    WebDriverWait(self.driver, timeout).until(
      EC.visibility_of_element_located((by, selector))
    )
  def wait_element_presence(self, by, selector, timeout=7):
    WebDriverWait(self.driver, timeout).until(
      EC.presence_of_element_located((by, selector))
    )
  def wait_element_inivisible(self, by, selector, timeout=7):
    WebDriverWait(self.driver, timeout).until(
      EC.invisibility_of_element_located((by, selector))
    )
  def wait_new_window(self, length, delay, timeout=7):
    t = 0
    while True:
      if len(self.driver.window_handles) >= length:
        return True
      time.sleep(delay)
      t += delay
      if t >= timeout:
        return False
  def wait_element_clickable(self, by, selector, timeout=7):
    WebDriverWait(self.driver, timeout).until(
      EC.element_to_be_clickable((by, selector))
    )
  
  ### 스위치 함수
  def switch_windows(self, n):
    self.driver.switch_to.window(self.driver.window_handles[n - 1])

  def select_element(self, by, selector, value):
    """
    셀렉트 박스에서 어떤 값을 선택
    """
    select = Select(self.driver.find_element(self.str_to_by(by), selector))
    select.select_by_value(value)

  def exist_element(self, by, selector):
    try:
      t = self.driver.find_element(self.str_to_by(by), selector)
      del t
      return True
    except:
      return False