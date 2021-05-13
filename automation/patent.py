import os
import re
import sys
import time
import shutil
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from paths import *
from classes.selenium_class import Browser
from classes.pyautogui_class import PyautoGUI
from classes.slack import Slack

class Patent(Browser, PyautoGUI):
    def __init__(self, driver):
        self.driver = driver
        self.IMAGE_PATH = f'{IMAGE_PATH}\\patent'
        self.spage = 1
        self.success = 0
        self.fail = 0
        self.folder_fail = 0

    def movement(self, filename):
        for d in os.listdir(f'{DOWNLOAD_PATH}'):
            if d.endswith('.pdf'):
                shutil.move(f'{DOWNLOAD_PATH}\\{d}',
                            f'{DOWNLOAD_PATH}\\{filename}\\{d}')
    
    def login_patent(self):
        try:
            # self.visit('www.naver.com')
            # self.driver.execute_script('window.open("about:blank", "_blank");')
            # self.switch_windows(2)
            Slack.chat('서식', '특허로 로그인')
            self.visit('https://www.patent.go.kr/smart/LoginForm.do')
            # self.switch_windows(2)

            self.wait_element_clickable(
                'xpath', '//*[@id="container"]/div/div[3]/div[1]/a', 10)
            self.click('xpath', '//*[@id="container"]/div/div[3]/div[1]/a')
            browser_success, m = self.wait_image_visible(
                f'{self.IMAGE_PATH}\\patent_browser.PNG', 0.3, 2.1)
            if browser_success:
                self.click_image(
                    [f'{self.IMAGE_PATH}\\patent_harddisk_1.PNG', f'{self.IMAGE_PATH}\\patent_harddisk_2.PNG',
                        f'{self.IMAGE_PATH}\\patent_harddisk_3.PNG', f'{self.IMAGE_PATH}\\patent_harddisk_4.PNG'],
                    'patent_harddisk.png가 없음 하드디스크 버튼', 0.5, 3, True
                )
                time.sleep(0.5)
                self.press_key(['enter'])

            self.click_image(
                [f'{self.IMAGE_PATH}\\patent_login_1_1.PNG',
                    f'{self.IMAGE_PATH}\\patent_login_1_2.PNG', f'{self.IMAGE_PATH}\\patent_login_1_3.PNG'],
                '공인인증서 구공호 버튼 없음', 0.5, 3, True
            )

            self.press_key(['tab', 'tab'])
            time.sleep(0.3)
            self.write_key('akzmdlsvh2015!!')
            time.sleep(0.3)
            self.press_key(['enter'])
            time.sleep(1.3)

            self.wait_element_visible('xpath', '//*[@id="gnb"]/ul/li[1]/a', 10)
            self.click('xpath', '//*[@id="gnb"]/ul/li[1]/a')
            self.click('xpath', '//*[@id="gnb"]/ul/li[1]/ul/li[3]')

            self.select_element('xpath', '//*[@id="recordCountPerPage"]', '20')
            self.press_key(['tab', 'enter'])
        except Exception as e:
            Slack.chat('서식상세', '특허청 로그인에러')
            print('특허로 로그인 에러발생: ', e)

    def visit_folder(self):
        # 폴더방문
        try:
            if not os.path.isdir(FOLDER_DIR):
                raise Exception('오늘날짜의 폴더가 생성되어있지 않음')

            for f in os.listdir(FOLDER_DIR):
                if f == 'temp':
                    continue

                Slack.chat('서식상세', f'3. {f} 폴더 진행 (특허로)')
                if len(os.listdir(f'{FOLDER_DIR}\\{f}')) == 0:
                    Slack.chat('서식상세', f'└        {f}는 빈 폴더')
                    self.folder_fail += 1
                    continue

                pdfs, bibs = 0, 0
                for d in os.listdir(f'{FOLDER_DIR}\\{f}'):
                    if d != 'warrant.pdf' and d.startswith('1-'):
                        pdfs += 1
                    if d.endswith('.BIB'):
                        bibs += 1

                if pdfs != bibs:
                    Slack.chat('서식상세', f'└        pdfs, bib 개수 매치가 안됨')
                    self.folder_fail += 1
                    continue
                
                self.script_patent(f'{FOLDER_DIR}\\{f}', f, pdfs)
        except Exception as e:
            Slack.chat('서식상세', '-------------------')
            print(f'폴더 방문 중 에러발생\n{e}')
            raise Exception(e)

    def script_patent(self, today_dir, markinfo_acc_no, length):
        txt_file = open(f'{today_dir}\\_codes.txt', 'r', encoding='utf-8')
        text_list = txt_file.readlines()
        
        # 반드시 2줄 이상이어야함
        if len(text_list) <= 1:
            Slack.chat('서식상세', f'└        _codes.txt file 에러! : {text_list}')
            return
        

        complete_list = [t.strip('\n') for t in text_list[1:]]
        applicant_name = text_list[0].strip('\n')

        if len(complete_list) != length:
            Slack.chat('서식상세', f'└        _codes.txt file 에러! : pdf 개수는 {length}개인데, 출원번호 발급된 개수는 {len(complete_list)}')
            return

        for complete in complete_list:
            accept_no, application_no, classify_no = complete.split(',')
            Slack.chat('서식상세', f'{accept_no}, {application_no}, {classify_no}류 탐색 시작')
            self.page_search(accept_no, application_no,
                             classify_no, markinfo_acc_no, applicant_name)
            print('complete!!')
    
    def page_search(self, accept_no, application_no, classify_no, markinfo_acc_no, applicant_name):
        try:
            page, btn_cnt, cnt = 1, 1, 0
            total_page = int(self.driver.find_element_by_xpath(
                '//*[@id="form"]/div[2]/p/span[1]/em').text) // 20 + 1
            flag = False

            while True:
                tbody = self.driver.find_element_by_xpath(
                    '//*[@id="SearchSbmtHistoryList"]/tbody')
                number_tr = len(tbody.find_elements_by_tag_name('tr'))
                for i in range(1, number_tr + 1):
                    print(f'{page}페이지 {i}번째 진행중, {cnt}, {total_page}')
                    accept_text = self.driver.find_element_by_xpath(
                        f'//*[@id="SearchSbmtHistoryList"]/tbody/tr[{i}]/td[2]').text
                    if accept_text == accept_no:
                        print(accept_text, 'accept_text')
                        # 접수번호와 일치하면 먼저 분류 비교 후 출원번호 비교 후 pdf 저장
                        classify_td = self.driver.find_element_by_xpath(
                            f'//*[@id="SearchSbmtHistoryList"]/tbody/tr[{i}]').text
                        state_td = self.driver.find_element_by_xpath(
                            f'//*[@id="SearchSbmtHistoryList"]/tbody/tr[{i}]/td[7]').text
                        if classify_no not in classify_td:
                            Slack.chat('서식상세', f'　└        분류번호 일치하지 않음 {classify_no} != {classify_td}')
                            # print('분류번호 일치하지 않음', classify_no, classify_td)
                            return

                        if state_td != '접수완료':
                            Slack.chat('서식상세', f'　└        접수완료 상태가 아님')
                            # print('접수완료 상태가 아님')
                            return
                        if self.exist_element('xpath', f'//*[@id="SearchSbmtHistoryList"]/tbody/tr[{i}]/td[5]/a[1]'):
                            self.click(
                                'xpath', f'//*[@id="SearchSbmtHistoryList"]/tbody/tr[{i}]/td[5]/a[1]')
                            self.wait_new_window(self.spage + 1, 0.5, 4)
                            self.switch_windows(self.spage + 1)
                            self.wait_element_visible(
                                'xpath', '//*[@id="noprint"]/h3', 10)
                            
                            # 출원인 이름이 다른경우 어떤 기록을 남길것을 요청
                            applicant_name_td = self.driver.find_element_by_xpath('/html/body/div/div/div[2]/table[2]/tbody/tr[4]/td[2]').text
                            reg_name = '(.*)\(\d'
                            match = re.search(reg_name, applicant_name_td)
                            if match:
                                applicant_name_patent = match.group(1)
                                print(applicant_name_patent, '특허청 기록된 이름')
                                if applicant_name != applicant_name_patent:
                                    Slack.chat('서식비고', f'{markinfo_acc_no} {classify_no}류 \n마크인포상세페이지 출원인 이름: {applicant_name}\n특허청 출원인 이름: {applicant_name_patent}')
                            else:
                                print('reg not matched')
                                Slack.chat('서식비고', f'{markinfo_acc_no} {classify_no}류 \n특허청 출원인 이름: {applicant_name_td} 확인바람.')
                            
                            application_td = self.driver.find_element_by_xpath(
                                '/html/body/div/div/div[2]/table[2]/tbody/tr[3]/td[2]').text
                            if application_no in application_td:
                                Slack.chat('서식상세', f'└        2-{classify_no}.pdf 저장')
                                self.hot_key('ctrl', 'p')
                                time.sleep(1.5)
                                self.press_key(['enter'])
                                self.wait_image_visible(
                                    [f'{IMAGE_PATH}\\adminpage\\adminpage_save_start.PNG', f'{IMAGE_PATH}\\adminpage\\adminpage_save_start.PNG'], 0.3, 3)
                                self.pyper_copy(
                                    f'{DOWNLOAD_PATH}\\temp\\2-{classify_no}.pdf')
                                self.hot_key('alt', 'n')
                                self.hot_key('ctrl', 'v'); time.sleep(0.3)

                                self.press_key(['enter'])
                                # self.click_image(f'{self.IMAGE_PATH}\\pdf_save_btn.PNG', '저장버튼없음', 0.5, 10, True)

                                self.wait_download(
                                    f'{markinfo_acc_no}\\2-{classify_no}.pdf')
                                self.driver.close()
                                self.switch_windows(1)
                                # raise Exception('테스트 에러')

                            success = self.wait_element_presence(
                                'xpath', '//*[@id="back-to-top"]', 0.5)
                            if success:
                                self.click(
                                    'xpath', '//*[@id="back-to-top"]', 0.5)
                                time.sleep(0.5)
 
                            self.driver.refresh()
                            self.wait_element_visible(
                                'xpath', '//*[@id="searchBtn_Bef"]/a[1]')
                            self.click(
                                'xpath', '//*[@id="searchBtn_Bef"]/a[1]')
                            self.click('xpath', '//*[@id="form"]/div[2]/div/a')
                            flag = True
                            self.success += 1
                            return

                if btn_cnt == 10:
                    if total_page > 10:
                        self.click('xpath', '//*[@id="form"]/div[4]/p/a[12]')
                        # wait_invisible_by_xpath('//*[@id="nppfs-loading-modal"]')
                        btn_cnt = 0
                else:
                    if page < total_page:
                        if self.exist_element('xpath', '//*[@id="form"]/div[4]/p/a[12]'):
                            self.click(
                                'xpath', f'//*[@id="form"]/div[4]/p/a[{btn_cnt + 2}]')
                        else:
                            if self.exist_element('xpath', f'//*[@id="form"]/div[4]/p/a[{btn_cnt}]'):
                                self.click(
                                    'xpath', f'//*[@id="form"]/div[4]/p/a[{btn_cnt}]')
                            # wait_invisible_by_xpath('//*[@id="nppfs-loading-modal"]')

                cnt += 1
                if cnt >= total_page:
                    break
                btn_cnt += 1
                page += 1
            if not flag:
                Slack.chat('서식상세', f'└        일치하는 접수번호가 없음..')
                self.fail += 1
                return
                # slack
        except Exception as e:
            self.fail += 1
            Slack.chat('서식상세', f'페이지하나 에러\n{e}')
            self.switch_windows(1)
            self.driver.refresh()
            s = self.wait_element_visible('xpath', '//*[@id="searchBtn_Bef"]/a[1]')
            print('s는', s)
            if s:
                self.click('xpath', '//*[@id="searchBtn_Bef"]/a[1]')
            print('페이지하나 에러: ', e)

def main(driver):
    try:
        Slack.chat('서식상세', '=====================< 특허로 시작 >=====================')
        Slack.chat('서식', '특허로 작업 시작 (2-분류번호.pdf 저장)')
        patent_page = Patent(driver)
        patent_page.login_patent()
        patent_page.visit_folder()
        total = patent_page.success + patent_page.fail
        Slack.chat('서식', 
            f'''
                특허로 완료, 합: {total} , 성공: {patent_page.success} , 실패: {patent_page.fail} , 폴더방문실패: {patent_page.folder_fail}
            '''
        )
    except Exception as e:
        Slack.chat('서식', '특허로 에러')
        raise Exception(e)