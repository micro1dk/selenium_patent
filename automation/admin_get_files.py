import os
import sys
import time
import shutil
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import requests

from paths import *
from classes.selenium_class import Browser
from classes.pyautogui_class import PyautoGUI
from classes.slack import Slack

class GetFiles(Browser, PyautoGUI):
    def __init__(self, driver):
        # super().__init__()
        self.driver = driver
        self.success = 0
        self.fail = 0
        self.pass_list = []
        self.applicant_name = ''
    
    def searching(self):
        try:
            # 매니저 전체 선택
            print(len(self.driver.window_handles))
            self.driver.find_element_by_xpath(
                '//*[@id="selected_manager_name"]').click()
            ul_select = self.driver.find_element_by_xpath(
                '//*[@id="form"]/div[1]/div[1]/div/div[4]/div/ul')
            li_select = ul_select.find_elements_by_tag_name('li')
            li_select[len(li_select) - 1].click() # 전체는 -1 
            # li_select[1].click() # 전체는 -1 
            self.driver.find_element_by_xpath('//*[@id="search"]').click()

            # paginate
            pagination = self.driver.find_element_by_xpath(
                '//*[@id="form"]/div[4]/div/div/ul')
            pagination_elem = pagination.find_elements_by_tag_name('li')
            page_count = len(pagination_elem) - 4

            # 페이지 이동
            complete_list = []
            wait_list = []
            remove_list = []
            for mode in range(1, 3):
                i = 3
                print(wait_list)
                # 끝나면 초기화
                if mode == 2:
                    self.driver.find_element_by_xpath('//*[@id="search"]').click()

                while True:
                    if i > 3:
                        self.driver.find_element_by_xpath(
                            f'//*[@id="form"]/div[4]/div/div/ul/li[{i}]/a').click()  # 페이지 이동

                    # 시작하기
                    tbody = self.driver.find_element_by_xpath(
                        '//*[@id="table-view"]/tbody')
                    tr_list     = tbody.find_elements_by_class_name('template')                    
                    for tr in tr_list:
                        state_1 = tr.find_element_by_xpath('td[6]').text
                        state_2 = tr.find_element_by_xpath('td[7]/div/div/a').text
                        state_3 = tr.find_element_by_xpath('td[3]/div/div[3]').text
                        number = tr.find_element_by_xpath('td[5]/div[1]').text
                        link = tr.find_element_by_xpath('td[5]/div[3]/span/a')
   
                        if state_3 != '(금일 4시 이전)':
                            continue

                        if mode == 1: 
                            if state_1 == '최종제출동의':
                                if number not in remove_list:
                                    if number not in wait_list:
                                        wait_list.append(number)
                        
                            elif state_1 == '[무료]수정요청': 
                                if number in wait_list:
                                    wait_list.remove(number)
                                    if number not in remove_list:
                                        remove_list.append(number)
                                else:
                                    if number not in remove_list:
                                        remove_list.append(number)

                        elif mode == 2:
                            if number in wait_list and number not in complete_list:
                                complete_list.append(number)
                                Slack.chat('서식상세', f'1. {number} {link.text} 진행중...')
                                link.click()
                                self.wait_new_window(2, 0.3, 2.1)
                                self.switch_windows(2)
                                success, err = self.detail_page()  # 상세페이지에서 자료 다운
                                self.switch_windows(1)

                                if success:
                                    self.success += 1
                                else:
                                    self.fail += 1

                    if i == 12: # 다음버튼인듯
                        success, attr = self.check_attribute(
                            self.driver, f'//*[@id="form"]/div[4]/div/div/ul/li[{i + 1}]/a', 'disabled')
                        if success:
                            if attr != 'disabled':
                                self.driver.find_element_by_xpath(
                                    f'//*[@id="form"]/div[4]/div/div/ul/li[{i + 1}]/a').click()
                                pagination = self.driver.find_element_by_xpath(
                                    '//*[@id="form"]/div[5]/div/div/ul')
                                pagination_elem = pagination.find_elements_by_tag_name(
                                    'li')
                                page_count = len(pagination_elem) - 4
                                i = 3
                                continue
                    if i == page_count + 2:
                        break
                    i += 1

        except Exception as e:
            print(f'매니저 전체 클릭 후 검색에서 에러\n{e}')
            raise Exception(e)

    def download_bib(self):
        try:
            self.click('xpath', '/html/body/div[2]/div/div[3]/div/div[2]/div[2]/ul[1]/li[4]/a'); time.sleep(0.2)
            # bib_btns = self.driver.find_elements_by_class_name('bib_btn')
            # bib_classifies = self.driver.find_elements_by_class_name(
            #     'classify_bib')
            
            table_container = self.driver.find_element_by_xpath('//*[@id="tab-4"]/div[2]')
            table_list = table_container.find_elements_by_tag_name('table')

            success_download = False
            for i in range(1, len(table_list) - 1):
                table = table_list[i]
                classify = table.find_element_by_class_name('classify_bib').get_attribute('value')
                # classify = bib_classifies[i].get_attribute('value')
                if classify + '류' not in self.pass_list:
                    btn = table.find_element_by_class_name('bib_btn')
                    Slack.chat('서식상세', f'　└        BIB_{classify}.BIB 다운로드')
                    btn.click()
                    success_download = self.wait_download(f'BIB_{classify}.BIB')
                    time.sleep(1.3)
                    break
            if not success_download:
                raise Exception('bib 다운로드 실패함')
        except Exception as e:
            Slack.chat('서식상세', f'　└        bib 다운에러: {e}')
            raise Exception(f'bib 다운로드 과정에서 에러\n{e}')
    
    def download_image(self):
        try:
            self.driver.find_element_by_xpath( # 인명정보 클릭
                '/html/body/div[2]/div/div[3]/div/div[2]/div[2]/ul[1]/li[1]/a').click()
            tbody = self.driver.find_element_by_xpath(
                '//*[@id="tab-1"]/div/table/tbody')
            tr_list = tbody.find_elements_by_tag_name('tr')
            temp = ''
            for i in range(len(tr_list)):
                if i % 2 == 0:  # 짝수에서 분류코드
                    classify = tr_list[i].find_element_by_xpath(
                        'td[3]/div[1]').text
                    temp = classify
                    state = tr_list[i].find_element_by_xpath(
                        'td[5]/div[2]/span[1]').text
                    if state != '컨펌요청':
                        self.pass_list.append(classify)
                else:  # 홀수에서 이미지 썸네일
                    if temp not in self.pass_list:
                        src = tr_list[i].find_element_by_tag_name(
                            'img').get_attribute('src')
                        if src == 'https://markinfo.co.kr/common/images/no_image_file.png':
                            raise Exception('상표 이미지 업로드 바람')
                        Slack.chat('서식상세', f'　└        logo_{classify}.jpg 다운로드')
                        res = requests.get(src)
                        img = open(
                            f'{DOWNLOAD_PATH}\\logo_{classify[:-1]}.jpg', 'wb')
                        img.write(res.content)
                        img.close()
        except Exception as e:
            raise Exception(f'상표 이미지 다운로드 과정에서 에러\n{e}')


    def movement(self, filename):
        time.sleep(1)
        if not os.path.isdir(f'{DOWNLOAD_PATH}\\{filename}'):
            os.mkdir(f'{DOWNLOAD_PATH}\\{filename}')

        for d in os.listdir(f'{DOWNLOAD_PATH}'):
            if d.endswith('.BIB') or d.endswith('.jpg') or d.endswith('.pdf'):
                shutil.move(f'{DOWNLOAD_PATH}\\{d}',
                            f'{DOWNLOAD_PATH}\\{filename}\\{d}')

    def download_pdf(self):
        try:
            self.wait_element_clickable(
                'xpath', '/html/body/div[2]/div/div[3]/div/div[2]/div[2]/ul[1]/li[2]/a', 10)
            self.driver.find_element_by_xpath(
                '/html/body/div[2]/div/div[3]/div/div[2]/div[2]/ul[1]/li[2]/a').click()
            # 출원인 이름 먼저 저장
            self.applicant_name = self.driver.find_element_by_xpath('//*[@id="tab-2"]/div/table[1]/tbody/tr[2]/td[1]').text

            sign_text = self.driver.find_element_by_xpath(
                '//*[@id="tab-2"]/div/table[1]/tbody/tr[4]/td[1]/div/button[1]').text
            self.app_num = self.driver.find_element_by_xpath(
                '/html/body/div[2]/div/div[4]/div/div[1]/div/div[2]/div[2]').text
            if sign_text == '만들기':
                self.driver.find_element_by_xpath(
                    '//*[@id="tab-2"]/div/table[1]/tbody/tr[4]/td[1]/div/button[1]').click()
                time.sleep(1)
                self.driver.switch_to.window(
                    self.driver.window_handles[1])  # 새로운창으로 이동
                success_wait_new_window = self.wait_new_window(3, 0.3, 3)

                if not success_wait_new_window:
                    raise Exception('인감만들기창이 뜨지 않아')
                self.driver.switch_to.window(
                    self.driver.window_handles[2])  # 인감만들기창으로 이동
                self.wait_element_visible(
                    'xpath', '//*[@id="form"]/div[1]/div[2]/button', 7)
                self.driver.find_element_by_xpath(
                    '//*[@id="form"]/div[1]/div[2]/button').click()

                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[1])
                url = 'https://markinfo.co.kr/common/make/seal/download_file.php?d=../../secure/member/image/markinfo@naver.com/&f=stamp.jpg'
                file_src = f'{DOWNLOAD_PATH}\\stamp.jpg'
                res = requests.get(url, stream=True)
                with open(file_src, 'wb') as out_file:
                    shutil.copyfileobj(res.raw, out_file)

                # 이미지를 다운 받은 후 업로드 해야함
                self.driver.find_element_by_xpath(
                    '//*[@id="tab-2"]/div/table[1]/tbody/tr[4]/td[1]/div/button[2]').click()
                self.wait_new_window(3, 0.3, 3)
                self.driver.switch_to.window(
                    self.driver.window_handles[2])  # 인감 업로드 창으로 이동
                self.wait_element_visible(
                    'xpath', '//*[@id="form"]/div/input', 7)
                self.driver.find_element_by_xpath(
                    '//*[@id="form"]/div/input').send_keys(f'{DOWNLOAD_PATH}\\stamp.jpg')
                self.driver.find_element_by_xpath(
                    '//*[@id="upload_file_seal"]').click()
                success, alert = self.exist_alert()
                if success:
                    self.accept_alert(alert)
                time.sleep(1)
                self.driver.switch_to.window(
                    self.driver.window_handles[1])  # 인감 업로드 창으로 이동

            self.driver.find_element_by_xpath(
                '/html/body/div[2]/div/div[3]/div/div[2]/div[1]/table/tbody/tr[1]/td[1]/div[3]/button[4]').click()
            success, alert = self.exist_alert()
            if success:
                self.accept_alert(alert)  # 알러트 뜨면 안된 것
                raise Exception(f'인감 업로드가 안되었음')

            self.wait_new_window(3, 0.3, 3)
            self.driver.switch_to.window(
                self.driver.window_handles[2])  # 위임장 창으로 이동
            Slack.chat('서식상세', f'　└        warrant.pdf 위임장 다운로드')
            s, elmnt = self.wait_image_visible(
                f'{CURRENT_PATH}\\images\\adminpage\\adminpage_pdf_down.PNG', 0.5, 4)
            if not s:
                raise Exception(f'위임장 화면 에러')
    
            self.driver.execute_script('window.print();')
            time.sleep(1)
            self.press_key(['enter'])
            self.wait_image_visible(
                f'{CURRENT_PATH}\\images\\adminpage\\adminpage_save_start.PNG', 0.5, 4)
            self.pyper_copy(f'{DOWNLOAD_PATH}\\temp\\warrant.pdf')
            self.hot_key('alt', 'n')
            self.hot_key('ctrl', 'v')
            self.press_key(['enter'])
            self.wait_download('warrant.pdf', 0.5, 15)

            if 'stamp.jpg' in os.listdir(DOWNLOAD_PATH):
                os.remove(f'{DOWNLOAD_PATH}\\stamp.jpg')  # 인감이미지 삭제
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[1])
        except Exception as e:
            print('위임장 에러', e)
            raise Exception(f'위임장 다운과정에서 에러\n{e}')

    def detail_page(self, url=''):
        try:
            # 폴더 생성
            if not os.path.isdir(DOWNLOAD_PATH):
                os.mkdir(DOWNLOAD_PATH)
                os.mkdir(f'{DOWNLOAD_PATH}\\temp')

            t = 0
            while not os.path.isdir(f'{DOWNLOAD_PATH}\\temp'):
                if t >= 10:
                    raise Exception('temp 폴더생성이 안됨')
                time.sleep(0.65)
                t += 0.65

            self.wait_element_visible('xpath', '//*[@id="tab-4"]/div[2]', 10)
            table_container = self.driver.find_element_by_xpath(
                '//*[@id="tab-4"]/div[2]')
            tables = table_container.find_elements_by_tag_name('table')

            Slack.chat('서식상세', '　└        분류검증')
            temp_list = []
            table_container = self.driver.find_element_by_xpath('//*[@id="tab-4"]/div[2]')
            table_list = table_container.find_elements_by_tag_name('table')
            for i in range(1, len(table_list) - 1):
                table = table_list[i]
                classify = table.find_element_by_class_name('classify_bib').get_attribute('value')
                if classify not in temp_list:
                    temp_list.append(classify)
                else:
                    return False, ''
            # 위 까지 분류검증

            # if len(tables) == 3:
            # 이미지 다운로드
            self.download_image()

            # 다운로드 시작
            self.download_bib()  # 다운로드 완료를 기다려야 할듯..


            # 인감확인하고 위임장 다운받기
            self.download_pdf()

             # 주문번호 폴더로 옮기기
            self.movement(self.app_num)

            if not os.path.isfile(f'{DOWNLOAD_PATH}\\{self.app_num}\\_codes.txt'):
                # 출원인 txt 파일에 저장하기
                f = open(f'{DOWNLOAD_PATH}\\{self.app_num}\\_codes.txt', 'a', encoding='utf-8')
                f.write(f'{self.applicant_name}\n')
                f.close()

            # 드라이버 종료
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])

            return True, ''

        except Exception as e:
            print(f'상세페이지 에러\n{e}')
            self.close_window_except_first()
            for d in os.listdir(f'{DOWNLOAD_PATH}'):
                if d.endswith('.BIB') or d.endswith('.jpg') or d.endswith('.pdf'):
                    os.remove(f'{DOWNLOAD_PATH}\\{d}')
            Slack.chat('서식상세', f'　└        에러발생: {e}')
            # if len(self.driver.window_handles[0]) > 1:
            #     self.driver.close()
            #     self.driver.switch_to.window(self.driver.window_handles[0])
            return False, e


def main(driver):
    try:
        Slack.chat('서식', '파일/폴더 저장 시작')
        get_files = GetFiles(driver)
        get_files.searching()
        total = get_files.success + get_files.fail
        Slack.chat('서식', 
            f'''
                폴더 + 파일 생성완료, 합: {total} , 성공: {get_files.success} , 실패: {get_files.fail}
            '''
        )
    except Exception as e:
        Slack.chat('서식', f'마크인포 관리자페이지 탐색중 에러')
        raise Exception(e)