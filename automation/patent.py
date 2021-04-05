from pyautogui_module import *
from seleste_module import * 

def movement(filename): 
  for d in os.listdir(f'{DOWNLOAD_PATH}'):
    if d.endswith('.pdf'):
      shutil.move(f'{DOWNLOAD_PATH}\\{d}', f'{DOWNLOAD_PATH}\\{filename}\\{d}')


def script_patent():
  driver.get('https://www.naver.com')
  driver.execute_script('window.open("about:blank", "_blank");')

  driver.switch_to.window(driver.window_handles[1])
  driver.get('https://www.daum.net')
  driver.execute_script('window.open("about:blank", "_blank");')

  driver.switch_to.window(driver.window_handles[2])
  driver.get('https://www.patent.go.kr/smart/LoginForm.do')

  # wait_clickable(driver, By.XPATH, '//*[@id="container"]/div/div[3]/div[1]/a')
  wait_clickable(driver, By.XPATH, '//*[@id="container"]/div/div[3]/div[1]/a')
  driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div[1]/a').click()
  browser_success, m = wait_element_visible(f'{CURRENT_PATH}\\search\\patent_browser.PNG', 0.3, 1.2)
  
  if browser_success:
    click_element(
      [f'{CURRENT_PATH}\\search\\patent_harddisk_1.PNG',f'{CURRENT_PATH}\\search\\patent_harddisk_2.PNG', f'{CURRENT_PATH}\\search\\patent_harddisk_3.PNG', f'{CURRENT_PATH}\\search\\patent_harddisk_4.PNG'],
      'wait element visible 에러: patent_harddisk.PNG와 일치하는 이미지가 없음 (하드디스크 검색)'
    )
    time.sleep(0.5)
    pyautogui.press(['enter'])

  click_element(
    [f'{CURRENT_PATH}\\search\\patent_login_1_1.PNG', f'{CURRENT_PATH}\\search\\patent_login_1_2.PNG'],
    'wait element visible 에러: patent_login_1_1.PNG와 일치하는 이미지가 없음 (공인인증서 구공호)'
  )
  pyautogui.press(['tab', 'tab'])
  pyautogui.write('akzmdlsvh2015!!')
  pyautogui.press(['enter'])
  
  time.sleep(1)
  wait_visible(driver, By.XPATH, '//*[@id="gnb"]/ul/li[1]/a')
  driver.find_element_by_xpath('//*[@id="gnb"]/ul/li[1]/a').click()
  driver.find_element_by_xpath('//*[@id="gnb"]/ul/li[1]/ul/li[3]').click()

  select = Select(driver.find_element_by_xpath('//*[@id="recordCountPerPage"]'))
  select.select_by_value('20')
  pyautogui.press(['tab', 'enter'])

  # 테스트
  visit_folder()
  
def visit_folder():
  try:
    if not os.path.isdir(FOLDER_DIR):
      raise Exception('오늘날짜의 폴더가 생성이 되지 않았음')
    
    for f in os.listdir(FOLDER_DIR):
      if f == 'temp': continue
      if len(os.listdir(f'{FOLDER_DIR}\\{f}')) == 0: 
        print(f'{f}는 비었음') # slack api
        continue

      pdfs, bibs = 0, 0
      for d in os.listdir(f'{FOLDER_DIR}\\{f}'):
        if d != 'warrant.pdf' and d.startswith('1-'): pdfs += 1
        if d.endswith('.BIB'): bibs += 1

      if pdfs != bibs:
        print('pdfs, bib 개수 매치가 안됨')
        continue
    
      script(f'{FOLDER_DIR}\\{f}', f)
  except Exception as e:
    print(f'visit_folder 에러{e}')

  
def script(today_dir, markinfo_acc_no):
  txt_file = open(f'{today_dir}\\numbers.txt')
  
  complete_list = []
  while True:
    line = txt_file.readline()
    if not line: break
    complete_list.append(line.split('\n')[0])
  txt_file.close()
  
  for complete in complete_list:
    accept_no, application_no, classify_no = complete.split(',')
    page_search(accept_no, application_no, classify_no, markinfo_acc_no)
    

def page_search(accept_no, application_no, classify_no, markinfo_acc_no):
  page, btn_cnt, cnt = 1, 1, 0
  total_page = int(driver.find_element_by_xpath('//*[@id="form"]/div[2]/p/span[1]/em').text) // 20 + 1
  flag = False
  while True:

    tbody = driver.find_element_by_xpath('//*[@id="SearchSbmtHistoryList"]/tbody')
    number_tr = len(tbody.find_elements_by_tag_name('tr'))
    for i in range(1, number_tr + 1):
      print(f'{page}페이지 {i}번째 진행중, {cnt}, {total_page}')
      accept_text = driver.find_element_by_xpath(f'//*[@id="SearchSbmtHistoryList"]/tbody/tr[{i}]/td[2]').text
      print(accept_text)
      if accept_text == accept_no:
        # 접수번호와 일치하면 먼저 분류 비교 후 출원번호 비교 후 pdf 저장
        classify_td = driver.find_element_by_xpath(f'//*[@id="SearchSbmtHistoryList"]/tbody/tr[{i}]').text
        state_td = driver.find_element_by_xpath(f'//*[@id="SearchSbmtHistoryList"]/tbody/tr[{i}]/td[7]').text
        if classify_no not in classify_td:
          print('분류번호 일치하지 않음', classify_no, classify_td)
          return

        if state_td != '접수완료':
          print('접수완료 상태가 아님')
          return
        
        if exist_element_by_xpath(driver, f'//*[@id="SearchSbmtHistoryList"]/tbody/tr[{i}]/td[5]/a[1]'):
          link = driver.find_element_by_xpath(f'//*[@id="SearchSbmtHistoryList"]/tbody/tr[{i}]/td[5]/a[1]').click()
          wait_new_window(driver, 4)
          driver.switch_to.window(driver.window_handles[3])
          wait_visible(driver, By.XPATH, '//*[@id="noprint"]/h3')
          application_td = driver.find_element_by_xpath('/html/body/div/div/div[2]/table[2]/tbody/tr[3]/td[2]').text
          if application_no in application_td:
            # driver.execute_script('window.print();')
            pyautogui.hotkey('ctrl', 'p')
            time.sleep(1)
            pyautogui.press(['enter'])
            wait_element_visible(f'{CURRENT_PATH}\\search\\adminpage_save_start.PNG')
            pyperclip.copy(f'{DOWNLOAD_PATH}\\temp\\2-{classify_no}.pdf')
            pyautogui.hotkey('alt', 'n')
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.press(['enter'])
            wait_download(f'{markinfo_acc_no}\\2-{classify_no}.pdf')
            driver.close()
            driver.switch_to.window(driver.window_handles[2])
        
        success = exist_element_by_xpath(driver, '//*[@id="back-to-top"]')
        if success:
          driver.find_element_by_xpath('//*[@id="back-to-top"]').click()
          time.sleep(0.5)
        # print(len(driver.window_handles), '개수')
        # driver.refresh()
        # wait_visible(driver, By.XPATH, '//*[@id="searchBtn_Bef"]/a[1]')
        driver.find_element_by_xpath('//*[@id="searchBtn_Bef"]/a[1]').click()

        # driver.find_element_by_xpath('//*[@id="form"]/div[2]/div/a').click()

        flag = True
        return

    if btn_cnt == 10:
      if total_page > 10:
        driver.find_element_by_xpath('//*[@id="form"]/div[4]/p/a[12]').click()
        # wait_invisible_by_xpath('//*[@id="nppfs-loading-modal"]')
        btn_cnt = 0
    else:
      if page < total_page:
        if exist_element_by_xpath(driver, '//*[@id="form"]/div[4]/p/a[12]'):
          driver.find_element_by_xpath(f'//*[@id="form"]/div[4]/p/a[{btn_cnt + 2}]').click()
        else:
          if exist_element_by_xpath(driver, f'//*[@id="form"]/div[4]/p/a[{btn_cnt}]'):
            driver.find_element_by_xpath(f'//*[@id="form"]/div[4]/p/a[{btn_cnt}]').click()
    # wait_invisible_by_xpath('//*[@id="nppfs-loading-modal"]')
    
    cnt += 1
    if cnt >= total_page:
      break
    btn_cnt += 1
    page += 1
  if not flag:
    print('일치하는 접수번호가 없음')
    # slack