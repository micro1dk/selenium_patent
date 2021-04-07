import os
import sys
import time
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from classes.pyautogui_class import PyautoGUI
from classes.selenium_class import Browser

from paths import *

def user_login():
  try:
    user_setting(
      driver=driver,
      path=COOKIE_PATH,
      url='https://markinfo.co.kr/front/nanmin/phtml/list.php?code=doc&link_page=reply',
      username='mycampground001@gmail.com',
      password='2964391a@'
    )
  except Exception as e:
    print(f'로그인 과정에서 에러\n{e}')

def visit_folder():
  try:
    if not os.path.isdir(FOLDER_DIR):
      raise Exception('오늘날짜의 폴더가 생성이 되지 않았음')
    
    for f in os.listdir(FOLDER_DIR):
      if f == 'temp': continue
      if len(os.listdir(f'{FOLDER_DIR}\\{f}')) == 0: 
        print(f'{f}는 비었음') # slack api
        continue

      pdfs_1, pdfs_2 = 0, 0
      for d in os.listdir(f'{FOLDER_DIR}\\{f}'):
        if d.startswith('1-'): pdfs_1 += 1 
        elif d.startswith('2-'): pdfs_2 += 1

      if pdfs_1 != pdfs_2:
        print('1-.pdf, 2-.pdf 개수 매치가 안됨')
        continue

      script(f'{FOLDER_DIR}\\{f}', f) # 스크립트 실행
  except Exception as e:
    print(f'visit_folder 에러{e}')
    pass

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
  page = 1
  pagination = driver.find_element_by_xpath('//*[@id="form"]/div[4]/div/div/ul')
  pagination_elem = pagination.find_elements_by_tag_name('li')
  page_count = len(pagination_elem) - 4
  
  i = 3
  while True:
    if i > 3:
      driver.find_element_by_xpath(f'//*[@id="form"]/div[4]/div/div/ul/li[{i}]/a').click()
  
    # 폴더 순회 -> number 검색 -> 관리자페이지 리스트 순회
    tbody = driver.find_element_by_xpath('//*[@id="table-view"]/tbody')
    number_tr = len(tbody.find_elements_by_tag_name('tr'))

    for j in range(1, number_tr + 1):
      if driver.find_element_by_xpath(f'//*[@id="table-view"]/tbody/tr[{j}]').get_attribute('class') != 'template':
        continue
      title_elem = driver.find_element_by_xpath(f'//*[@id="table-view"]/tbody/tr[{j}]/td[5]') # 요기안에 제목 들어있음
      reply_elem = driver.find_element_by_xpath(f'//*[@id="table-view"]/tbody/tr[{j}]/td[6]') # 회신사항
      state_elem = driver.find_element_by_xpath(f'//*[@id="table-view"]/tbody/tr[{j}]/td[7]') # 회신사항
      print(markinfo_acc_no, title_elem.text)
      if '최종제출동의' == reply_elem.text and '처리대기' in state_elem.text and markinfo_acc_no in title_elem.text:
        driver.find_element_by_xpath(f'//*[@id="table-view"]/tbody/tr[{j}]/td[5]/div[3]/span/a').click()
        driver.switch_to.window(driver.window_handles[1])
        detail_page(accept_no, application_no, classify_no, markinfo_acc_no)

        time.sleep(10)
        print('ok')
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        if i > 3:
          driver.find_element_by_xpath('//*[@id="form"]/div[4]/div/div/ul/li[1]/a').click()
        return

    if i == 12:
      success, attr = check_attribute(driver, f'//*[@id="form"]/div[4]/div/div/ul/li[{i + 1}]/a', 'disabled')
      if success:
        if attr != 'disabled':
          driver.find_element_by_xpath(f'//*[@id="form"]/div[4]/div/div/ul/li[{i + 1}]/a').click()
          pagination = driver.find_element_by_xpath('//*[@id="form"]/div[4]/div/div/ul')
          pagination_elem = pagination.find_elements_by_tag_name('li')
          page_count = len(pagination_elem) - 4
          i = 3
          continue
    if i == page_count + 2: break
    i += 1

def detail_page(accept_no, application_no, classify_no, markinfo_acc_no):
  try:
    # bib_btns = driver.find_elements_by_class_name('bib_btn')
    bib_classifies = driver.find_elements_by_class_name('classify_bib')
    number_inputs = driver.find_elements_by_class_name('application_number')
    edit_btns = driver.find_elements_by_class_name('application_edit')
    for i in range(len(bib_classifies)):
      print(bib_classifies[i].text, classify_no, application_no)
      if bib_classifies[i].get_attribute('value') == classify_no:
        print('okkkk')
        number_inputs[i].send_keys(application_no)
        time.sleep(1)
        pyautogui.write(application_no)
        # edit_btns[i].click()

    # time.sleep(10)
    # if not success_download:
      # raise Exception('bib 다운로드 실패함')
  except Exception as e:
    raise Exception(f'출원번호 입력 과정에서 에러\n{e}')



def script_adminpage_upload():
  # 리스트와 파일을 순회하며 파일업로드

  # 테스트
  user_login()
  # 매니저 전체 선택
  driver.find_element_by_xpath('//*[@id="selected_manager_name"]').click()
  ul_select = driver.find_element_by_xpath('//*[@id="form"]/div[1]/div[1]/div/div[4]/div/ul')
  li_select = ul_select.find_elements_by_tag_name('li')
  li_select[len(li_select) - 1].click()
  driver.find_element_by_xpath('//*[@id="search"]').click()


  try:
    if not os.path.isdir(FOLDER_DIR):
      raise Exception('오늘날짜의 폴더가 생성이 되지 않았음')

    """
    리스트를 순회하고, accept_no에 들어있으면 업무상태를 처리완료로 변경
    (한번만)링크타고 들어가서 업로드하기
    """
    # searching(2)
    visit_folder()
    # print(accept_no_list, '마지막')
    
  except Exception as e:
    print(e)