import os
import sys
import time
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from paths import *
from classes.selenium_class import Browser
from classes.pyautogui_class import PyautoGUI
from classes.slack import Slack

class UploadFiles(Browser, PyautoGUI):
    def __init__(self, driver):
        self.driver = driver
        self.success = 0
        self.fail = 0
    
    def open_codes(self, f):
        try:
            txt_file = open(f'{FOLDER_DIR}\\{f}\\_codes.txt')
            complete_list = []
            while True:
                line = txt_file.readline()
                if not line:
                    break
                complete_list.append(line.split('\n')[0])
            txt_file.close()
            return complete_list
        except Exception as e:
            return []
        
    
    def visit_folder(self):
        """
        폴더하나하나 순회
        """
        try:
            # 매니저 전체 선택
            self.driver.find_element_by_xpath(
                '//*[@id="selected_manager_name"]').click()
            ul_select = self.driver.find_element_by_xpath(
                '//*[@id="form"]/div[1]/div[1]/div/div[4]/div/ul')
            li_select = ul_select.find_elements_by_tag_name('li')
            li_select[len(li_select) - 1].click()
            # self.driver.find_element_by_xpath('//*[@id="search"]').click()
            # 위까지 테스트
            if not os.path.isdir(FOLDER_DIR):
                raise Exception('오늘날짜의 폴더가 생성이 되지 않았음')

            for f in os.listdir(FOLDER_DIR):
                if f == 'temp':
                    continue
                if len(os.listdir(f'{FOLDER_DIR}\\{f}')) == 0:
                    Slack.chat('서식상세', f'└        {f}는 빈 폴더')
                    # print(f'{f}는 비었음')  # slack api
                    continue

                pdfs_1, pdfs_2 = 0, 0
                for d in os.listdir(f'{FOLDER_DIR}\\{f}'):
                    if d.startswith('1-'):
                        pdfs_1 += 1
                    elif d.startswith('2-'):
                        pdfs_2 += 1

                if pdfs_1 != pdfs_2:
                    Slack.chat('서식상세', f'└        1-.pdf, 2-.pdf 개수 매치가 안됨')
                    # print('1-.pdf, 2-.pdf 개수 매치가 안됨')
                    continue

                complete_list = self.open_codes(f)
                if not complete_list:
                    continue

                for complete in complete_list:
                    accept_no, application_no, classify_no = complete.split(',')
                    # print('page_search _before')
                    Slack.chat('서식상세', f'admin 페이지 {f} {classify_no}류 시작')
                    # 한줄마다 페이지 전체를 순회하여 검색
                    self.page_search(accept_no, application_no, classify_no, f)
                    print('complete!')
        except Exception as e:
            print(f'visit_folder 에러{e}')
            pass

    def page_search(self, accept_no, application_no, classify_no, markinfo_acc_no):
        print(f'{accept_no}, {application_no}, {classify_no}, {markinfo_acc_no}를 탐색한다.')
        self.driver.find_element_by_xpath('//*[@id="search"]').click()
        time.sleep(3)
        page = 1
        pagination = self.driver.find_element_by_xpath(
            '//*[@id="form"]/div[4]/div/div/ul')
        pagination_elem = pagination.find_elements_by_tag_name('li')
        page_count = len(pagination_elem) - 4

        i = 3
        while True:
            if i > 3:
                self.driver.find_element_by_xpath(
                    f'//*[@id="form"]/div[4]/div/div/ul/li[{i}]/a').click()

            # 폴더 순회 -> number 검색 -> 관리자페이지 리스트 순회
            tbody = self.driver.find_element_by_xpath('//*[@id="table-view"]/tbody')
            number_tr = len(tbody.find_elements_by_tag_name('tr'))

            for j in range(1, number_tr + 1):
                if self.driver.find_element_by_xpath(f'//*[@id="table-view"]/tbody/tr[{j}]').get_attribute('class') != 'template':
                    continue
                title_elem = self.driver.find_element_by_xpath(
                    f'//*[@id="table-view"]/tbody/tr[{j}]/td[5]')  # 요기안에 제목 들어있음
                reply_elem = self.driver.find_element_by_xpath(
                    f'//*[@id="table-view"]/tbody/tr[{j}]/td[6]')  # 회신사항
                state_elem = self.driver.find_element_by_xpath(
                    f'//*[@id="table-view"]/tbody/tr[{j}]/td[7]')  # 회신사항

                # print(markinfo_acc_no, title_elem.text)
                if '최종제출동의' == reply_elem.text and '처리대기' in state_elem.text and markinfo_acc_no in title_elem.text and f'{classify_no}류' in title_elem.text:
                    # print('발견!!!=====================')
                    time.sleep(2)
                    self.driver.find_element_by_xpath(f'//*[@id="table-view"]/tbody/tr[{j}]/td[5]/div[3]/span/a').click()
                    self.driver.switch_to.window(self.driver.window_handles[1])
                    success = self.detail_page(accept_no, application_no, classify_no, markinfo_acc_no)

                    time.sleep(10)
                    # print('ok 상세페이지 업로드 성공?', success)
                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[0])

                    # if success:
                    #   self.click('xpath', f'//*[@id="table-view"]/tbody/tr[{j}]/td[7]/div/div/a') # 처리대기 클릭
                    # self.click('xpath', f'//*[@id="table-view"]/tbody/tr[{j}]/td[7]/div/div/ul/li[4]/a') # 처리완료 클릭

                    # 처리대기 클릭
                    Slack.chat('서식상세', f'└        상태값 처리완료로')
                    self.click(
                        'xpath', f'//*[@id="table-view"]/tbody/tr[{j}]/td[7]/div/div/a')
                    time.sleep(3)
                    if i > 3:
                        self.driver.find_element_by_xpath(
                            '//*[@id="form"]/div[4]/div/div/ul/li[1]/a').click()
                    return

            if i == 12:
                success, attr = self.check_attribute(
                    f'//*[@id="form"]/div[4]/div/div/ul/li[{i + 1}]/a', 'disabled')
                if success:
                    if attr != 'disabled':
                        self.driver.find_element_by_xpath(
                            f'//*[@id="form"]/div[4]/div/div/ul/li[{i + 1}]/a').click()
                        pagination = self.driver.find_element_by_xpath(
                            '//*[@id="form"]/div[4]/div/div/ul')
                        pagination_elem = pagination.find_elements_by_tag_name(
                            'li')
                        page_count = len(pagination_elem) - 4
                        i = 3
                        continue
            if i == page_count + 2:
                break
            i += 1
        # self.driver.find_element_by_xpath('//*[@id="search"]').click()
    
    def detail_page(self, accept_no, application_no, classify_no, markinfo_acc_no):
        try:
            bib_classifies = self.driver.find_elements_by_class_name(
                'classify_bib')
            number_inputs = self.driver.find_elements_by_class_name(
                'application_number')
            edit_btns = self.driver.find_elements_by_class_name(
                'application_edit')
            submit_btns = self.driver.find_elements_by_class_name(
                'btn_add_file')
            inputs = self.driver.find_elements_by_class_name('input_imgs')

            for i in range(len(bib_classifies)):
                """
                분류번호가 맞는 것
                """
                # print(bib_classifies[i].text, classify_no, application_no)
                if bib_classifies[i].get_attribute('value') == classify_no:
                    Slack.chat('서식상세', f'└        {classify_no}류에 출원번호는 {application_no}')
                    # print('okkkk')
                    number_inputs[i].send_keys(application_no)
                    time.sleep(1)
                    self.write_key(application_no)
                    Slack.chat('서식상세', f'└         1-{classify_no}.pdf, 2-{classify_no}.pdf 업로드')
                    # edit_btns[i].click()
                    # submit_btns[i].click()
                    # inputs[i].send_keys(
                    #     f'{FOLDER_DIR}\\{accept_no}\\1-{classify_no}.pdf\n{FOLDER_DIR}\\{accept_no}\\2-{classify_no}.pdf')
                    # 확인 필요

            # time.sleep(10)
            # if not success_download:
                # raise Exception('bib 다운로드 실패함')
            return True
        except Exception as e:
            print(f'출원번호 입력 과정에서 에러\n{e}')
            return False

    def script_adminpage_upload(self):
        # 리스트와 파일을 순회하며 파일업로드

        # 테스트
        # user_login()
        # 매니저 전체 선택
        # self.driver.find_element_by_xpath('//*[@id="selected_manager_name"]').click()
        # ul_select = self.driver.find_element_by_xpath('//*[@id="form"]/div[1]/div[1]/div/div[4]/div/ul')
        # li_select = ul_select.find_elements_by_tag_name('li')
        # li_select[len(li_select) - 1].click()
        # self.driver.find_element_by_xpath('//*[@id="search"]').click()

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


def main(driver):
    try:
        Slack.chat('서식상세', '=====================< 파일 업로드 시작 >=====================')
        upload_files = UploadFiles(driver)
        upload_files.visit_folder()
        total = upload_files.success + upload_files.fail
        Slack.chat('서식', 
            f'''
                업로드 완료, 합: {total}, 성공: {upload_files.success}, 실패: {upload_files.fail}
            '''
        )
        
        # upload_files.script_adminpage_upload()
    except Exception as e:
        Slack.chat('서식', f'마크인포 관리자페이지 탐색중 에러')
        raise Exception(e)