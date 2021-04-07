import os
import sys
import time
import shutil
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from paths import *

from classes.pyautogui_class import PyautoGUI
from classes.selenium_class import Browser

class PATENT_PAGE(Browser, PyautoGUI):
  def __init__(self, driver):
    self.driver = driver
    self.IMAGE_PATH = f'{IMAGE_PATH}\\patent'
    self.spage = 1

  def movement(self, filename):
    for d in os.listdir(f'{DOWNLOAD_PATH}'):
      if d.endswith('.pdf'):
        shutil.move(f'{DOWNLOAD_PATH}\\{d}', f'{DOWNLOAD_PATH}\\{filename}\\{d}')
  
  def login_patent(self):
    try:
      # self.visit('www.naver.com')
      # self.driver.execute_script('window.open("about:blank", "_blank");')
      # self.switch_windows(2)
      self.visit('https://www.patent.go.kr/smart/LoginForm.do')
      # self.switch_windows(2)

      self.wait_element_clickable('xpath', '//*[@id="container"]/div/div[3]/div[1]/a', 10)
      self.click('xpath', '//*[@id="container"]/div/div[3]/div[1]/a')
      browser_success, m = self.wait_image_visible(f'{self.IMAGE_PATH}\\patent_browser.PNG', 0.3, 2.1)
      print(browser_success, '??')
      if browser_success:
        self.click_image(
          [f'{self.IMAGE_PATH}\\patent_harddisk_1.PNG',f'{self.IMAGE_PATH}\\patent_harddisk_2.PNG', f'{self.IMAGE_PATH}\\patent_harddisk_3.PNG', f'{self.IMAGE_PATH}\\patent_harddisk_4.PNG'],
          'patent_harddisk.png가 없음 하드디스크 버튼', 0.5, 3, True
        ); time.sleep(0.5)
        self.press_key(['enter'])

      self.click_image(
        [f'{self.IMAGE_PATH}\\patent_login_1_1.PNG', f'{self.IMAGE_PATH}\\patent_login_1_2.PNG'],
        '공인인증서 구공호 버튼 없음', 0.5, 3, True
      )

      self.press_key(['tab', 'tab']); time.sleep(0.3)
      self.write_key('akzmdlsvh2015!!'); time.sleep(0.3)
      self.press_key(['enter']); time.sleep(1.3)

      self.wait_element_visible('xpath', '//*[@id="gnb"]/ul/li[1]/a', 10)
      self.click('xpath', '//*[@id="gnb"]/ul/li[1]/a')
      self.click('xpath', '//*[@id="gnb"]/ul/li[1]/ul/li[3]')
      
      self.select_element('xpath', '//*[@id="recordCountPerPage"]', '20')
      self.press_key(['tab', 'enter'])
      
      # self.visit_folder()
    except Exception as e:
      print('에러발생: ', e)

  def visit_folder(self):
    # 폴더방문
    try:
      if not os.path.isdir(FOLDER_DIR):
        raise Exception('오늘날짜의 폴더가 생성되어있지 않음')
      
      for f in os.listdir(FOLDER_DIR):
        if f == 'temp': continue
        if len(os.listdir(f'{FOLDER_DIR}\\{f}')) == 0:
          print(f'{f}는 빈 폴더')
          continue
        
        pdfs, bibs = 0, 0
        for d in os.listdir(f'{FOLDER_DIR}\\{f}'):
          if d != 'warrant.pdf' and d.startswith('1-'): pdfs += 1
          if d.endswith('.BIB'): bibs += 1

        if pdfs != bibs:
          print('pdfs, bib 개수 매치 안됨')
          continue

        self.script_patent(f'{FOLDER_DIR}\\{f}', f)  
        print(f, '끝')
    except Exception as e:
      print('폴더 방문 중 에러발생', e)

  def script_patent(self, today_dir, markinfo_acc_no):
    txt_file = open(f'{today_dir}\\_codes.txt')

    complete_list = []
    while True:
      line = txt_file.readline()
      if not line: break
      complete_list.append(line.split('\n')[0])
    txt_file.close()

    for complete in complete_list:
      accept_no, application_no, classify_no = complete.split(',')
      print('page_search _before')
      self.page_search(accept_no, application_no, classify_no, markinfo_acc_no)
      print('complete!!')

  def page_search(self, accept_no, application_no, classify_no, markinfo_acc_no):
    try:

    
      page, btn_cnt, cnt = 1, 1, 0
      total_page = int(self.driver.find_element_by_xpath('//*[@id="form"]/div[2]/p/span[1]/em').text) // 20 + 1
      flag = False

      while True:
        tbody = self.driver.find_element_by_xpath('//*[@id="SearchSbmtHistoryList"]/tbody')
        number_tr = len(tbody.find_elements_by_tag_name('tr'))
        for i in range(1, number_tr + 1):
          print(f'{page}페이지 {i}번째 진행중, {cnt}, {total_page}')
          accept_text = self.driver.find_element_by_xpath(f'//*[@id="SearchSbmtHistoryList"]/tbody/tr[{i}]/td[2]').text
          if accept_text == accept_no:
            print(accept_text, 'accept_text')
            # 접수번호와 일치하면 먼저 분류 비교 후 출원번호 비교 후 pdf 저장
            classify_td = self.driver.find_element_by_xpath(f'//*[@id="SearchSbmtHistoryList"]/tbody/tr[{i}]').text
            state_td = self.driver.find_element_by_xpath(f'//*[@id="SearchSbmtHistoryList"]/tbody/tr[{i}]/td[7]').text
            if classify_no not in classify_td:
              print('분류번호 일치하지 않음', classify_no, classify_td)
              return

            if state_td != '접수완료':
              print('접수완료 상태가 아님')
              return
            if self.exist_element('xpath', f'//*[@id="SearchSbmtHistoryList"]/tbody/tr[{i}]/td[5]/a[1]'):
              self.click('xpath', f'//*[@id="SearchSbmtHistoryList"]/tbody/tr[{i}]/td[5]/a[1]')
              self.wait_new_window(self.spage + 1, 0.5, 4)
              self.switch_windows(self.spage + 1)
              self.wait_element_visible('xpath', '//*[@id="noprint"]/h3', 10)
              application_td = self.driver.find_element_by_xpath('/html/body/div/div/div[2]/table[2]/tbody/tr[3]/td[2]').text
              if application_no in application_td:
                self.hot_key('ctrl', 'p')
                time.sleep(1.5)
                self.press_key(['enter'])
                self.wait_image_visible([f'{IMAGE_PATH}\\adminpage\\adminpage_save_start.PNG', f'{IMAGE_PATH}\\adminpage\\adminpage_save_start.PNG'], 0.3, 3)
                self.pyper_copy(f'{DOWNLOAD_PATH}\\temp\\2-{classify_no}.pdf')
                self.hot_key('alt', 'n')
                self.hot_key('ctrl', 'v')
                self.press_key(['enter'])
                self.wait_download(f'{markinfo_acc_no}\\2-{classify_no}.pdf')
                self.driver.close()
                self.switch_windows(1)

              # success = self.exist_element('xpath', '//*[@id="back-to-top"]')
              success = self.wait_element_presence('xpath', '//*[@id="back-to-top"]', 0.5)
              print(success, '..?????')
              if success:
                self.click('xpath', '//*[@id="back-to-top"]', 0.5)
                time.sleep(0.5)
              # print(len(self.driver.window_handles), '개수')
              print('refresh')
              self.driver.refresh()
              print('refresh_ok')
              self.wait_element_visible('xpath', '//*[@id="searchBtn_Bef"]/a[1]')
              print('wait_//*[@id="searchBtn_Bef"]/_ok')
              self.click('xpath', '//*[@id="searchBtn_Bef"]/a[1]')
              self.click('xpath', '//*[@id="form"]/div[2]/div/a')
              flag = True
              return

        if btn_cnt == 10:
          if total_page > 10:
            self.click('xpath', '//*[@id="form"]/div[4]/p/a[12]')
            # wait_invisible_by_xpath('//*[@id="nppfs-loading-modal"]')
            btn_cnt = 0
        else:
          if page < total_page:
            if self.exist_element('xpath', '//*[@id="form"]/div[4]/p/a[12]'):
              self.click('xpath', f'//*[@id="form"]/div[4]/p/a[{btn_cnt + 2}]')
            else:
              if self.exist_element('xpath', f'//*[@id="form"]/div[4]/p/a[{btn_cnt}]'):
                self.click('xpath', f'//*[@id="form"]/div[4]/p/a[{btn_cnt}]')
              # wait_invisible_by_xpath('//*[@id="nppfs-loading-modal"]')

        cnt += 1
        if cnt >= total_page:
          break
        btn_cnt += 1
        page += 1
      if not flag:
        print('일치하는 접수번호가 없음')
        return
        # slack
    except Exception as e:
      print('페이지하나 에러: ', e)

def main(driver):
  patent_page = PATENT_PAGE(driver)
  patent_page.login_patent()
  patent_page.visit_folder()

# def script(today_dir, markinfo_acc_no):
#   txt_file = open(f'{today_dir}\\numbers.txt')
  
#   complete_list = []
#   while True:
#     line = txt_file.readline()
#     if not line: break
#     complete_list.append(line.split('\n')[0])
#   txt_file.close()
  
#   for complete in complete_list:
#     accept_no, application_no, classify_no = complete.split(',')
#     page_search(accept_no, application_no, classify_no, markinfo_acc_no)
    

# def page_search(accept_no, application_no, classify_no, markinfo_acc_no):
#   page, btn_cnt, cnt = 1, 1, 0
#   total_page = int(driver.find_element_by_xpath('//*[@id="form"]/div[2]/p/span[1]/em').text) // 20 + 1
#   flag = False
#   while True:

#     tbody = driver.find_element_by_xpath('//*[@id="SearchSbmtHistoryList"]/tbody')
#     number_tr = len(tbody.find_elements_by_tag_name('tr'))
#     for i in range(1, number_tr + 1):
#       print(f'{page}페이지 {i}번째 진행중, {cnt}, {total_page}')
#       accept_text = driver.find_element_by_xpath(f'//*[@id="SearchSbmtHistoryList"]/tbody/tr[{i}]/td[2]').text
#       print(accept_text)
#       if accept_text == accept_no:
#         # 접수번호와 일치하면 먼저 분류 비교 후 출원번호 비교 후 pdf 저장
#         classify_td = driver.find_element_by_xpath(f'//*[@id="SearchSbmtHistoryList"]/tbody/tr[{i}]').text
#         state_td = driver.find_element_by_xpath(f'//*[@id="SearchSbmtHistoryList"]/tbody/tr[{i}]/td[7]').text
#         if classify_no not in classify_td:
#           print('분류번호 일치하지 않음', classify_no, classify_td)
#           return

#         if state_td != '접수완료':
#           print('접수완료 상태가 아님')
#           return
        
#         if exist_element_by_xpath(driver, f'//*[@id="SearchSbmtHistoryList"]/tbody/tr[{i}]/td[5]/a[1]'):
#           link = driver.find_element_by_xpath(f'//*[@id="SearchSbmtHistoryList"]/tbody/tr[{i}]/td[5]/a[1]').click()
#           wait_new_window(driver, 4)
#           driver.switch_to.window(driver.window_handles[3])
#           wait_visible(driver, 'xpath', '//*[@id="noprint"]/h3')
#           application_td = driver.find_element_by_xpath('/html/body/div/div/div[2]/table[2]/tbody/tr[3]/td[2]').text
#           if application_no in application_td:
#             # driver.execute_script('window.print();')
#             self.hot_key('ctrl', 'p')
#             time.sleep(1)
#             self.press_key(['enter'])
#             wait_element_visible(f'{CURRENT_PATH}\\search\\adminpage_save_start.PNG')
#             self.pyper_copy(f'{DOWNLOAD_PATH}\\temp\\2-{classify_no}.pdf')
#             self.hot_key('alt', 'n')
#             self.hot_key('ctrl', 'v')
#             self.press_key(['enter'])
#             wait_download(f'{markinfo_acc_no}\\2-{classify_no}.pdf')
#             driver.close()
#             driver.switch_to.window(driver.window_handles[2])
        
#         success = exist_element_by_xpath(driver, '//*[@id="back-to-top"]')
#         if success:
#           driver.find_element_by_xpath('//*[@id="back-to-top"]').click()
#           time.sleep(0.5)
#         # print(len(driver.window_handles), '개수')
#         # driver.refresh()
#         # wait_visible(driver, 'xpath', '//*[@id="searchBtn_Bef"]/a[1]')
#         driver.find_element_by_xpath('//*[@id="searchBtn_Bef"]/a[1]').click()

#         # driver.find_element_by_xpath('//*[@id="form"]/div[2]/div/a').click()

#         flag = True
#         return

#     if btn_cnt == 10:
#       if total_page > 10:
#         driver.find_element_by_xpath('//*[@id="form"]/div[4]/p/a[12]').click()
#         # wait_invisible_by_xpath('//*[@id="nppfs-loading-modal"]')
#         btn_cnt = 0
#     else:
#       if page < total_page:
#         if exist_element_by_xpath(driver, '//*[@id="form"]/div[4]/p/a[12]'):
#           driver.find_element_by_xpath(f'//*[@id="form"]/div[4]/p/a[{btn_cnt + 2}]').click()
#         else:
#           if exist_element_by_xpath(driver, f'//*[@id="form"]/div[4]/p/a[{btn_cnt}]'):
#             driver.find_element_by_xpath(f'//*[@id="form"]/div[4]/p/a[{btn_cnt}]').click()
#     # wait_invisible_by_xpath('//*[@id="nppfs-loading-modal"]')
    
#     cnt += 1
#     if cnt >= total_page:
#       break
#     btn_cnt += 1
#     page += 1
#   if not flag:
#     print('일치하는 접수번호가 없음')
#     # slack